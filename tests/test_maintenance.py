import importlib.util
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from maintenance import translation_audit as audit
from installation import fr_manager as installer
spec = importlib.util.spec_from_file_location('azerty_core', ROOT / 'azerty/azerty.py')
azerty = importlib.util.module_from_spec(spec)
spec.loader.exec_module(azerty)
RULES = json.loads((ROOT / 'docs/REGLES-TRADUCTION.json').read_text(encoding='utf-8'))


def row(key='a', source='Hello {Name}', text='Bonjour {Name}', ns=''):
    return dict(ns=ns, key=key, source=source, text=text)


def catalogue(path, rows):
    path.mkdir(parents=True, exist_ok=True)
    audit.dump(path / 'fr_001.json', {'texts': rows})


def profile(bindings):
    # Fixture synthétique : aucune sauvegarde personnelle dans le dépôt.
    header = bytearray(32)
    header[:4] = b'GVAS'
    struct.pack_into('<i', header, 4, 3)
    struct.pack_into('<HH', header, 16, 5, 6)
    prefix = bytes(header) + struct.pack('<i', 1) + azerty.fstring(azerty.PROFILE_CLASS) + azerty.fstring('EnhancedPlayerMappableKeyProfile_Test')
    rows = [{'raw': azerty.fstring(action) + azerty.fstring(key) + azerty.fstring('None') * 2 + bytes(6)} for action, key in bindings]
    return azerty.encode(prefix, rows, azerty.fstring(azerty.PROFILE_ID) + azerty.fstring('ObjectEnd'))


class AuditTests(unittest.TestCase):
    def test_format_and_names_are_errors_but_glossary_is_advice(self):
        rows = {('', 'a'): dict(row(source='Discord {User}', text='Discorde {Utilisateur}'), file='fr.json')}
        errors, _, _, _ = audit.checks(rows, RULES)
        self.assertEqual({e['code'] for e in errors}, {'format_tokens', 'protected_name'})
        rows = {('', 'a'): dict(row(source='Sight', text='Viseur'), file='fr.json')}
        self.assertEqual(audit.checks(rows, RULES)[0], [])
        self.assertEqual(audit.checks(rows, RULES)[1][0]['code'], 'glossary_review')

    def test_context_and_named_models(self):
        rows = {('', k): dict(row(k, s, t), file='fr.json') for k, s, t in [
            ('3FB5E6334103C8519F640493F70A5671', 'Stock', 'Stock'), ('b', 'Stock', 'Crosse'),
            ('c', 'A bunker', 'Un bunker'), ('d', 'AK Star magazine', 'Chargeur AK Star')]}
        errors, warnings, _, _ = audit.checks(rows, RULES)
        self.assertEqual(errors + warnings, [])

    def test_update_detects_new_changed_removed_and_stale_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            fr, en = base / 'fr', base / 'en'
            catalogue(fr, [row(), row('removed')])
            catalogue(en, [row(), row('removed')])
            first = audit.audit(fr, RULES, en)
            audit.dump(base / 'snapshot.json', first['snapshot'])
            catalogue(en, [row(source='Hello {Name}!'), row('new', 'New button', '')])
            report = audit.audit(fr, RULES, en, base / 'snapshot.json')
            self.assertEqual({r['code'] for r in report['english_changes']}, {'source_changed', 'new', 'removed'})
            self.assertEqual({r['code'] for r in report['errors']}, {'missing_translation', 'stale_source'})
            audit.write_report(report, base / 'report')
            pending = json.loads((base / 'report/a-traduire.json').read_text(encoding='utf-8'))['texts']
            self.assertEqual(len(pending), 2)
            self.assertEqual(next(r for r in pending if r['key'] == 'a')['source'], 'Hello {Name}!')

    def test_ignores_generated_files_and_reports_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            catalogue(base, [row(), row()])
            (base / '_Report.json').write_text('invalid', encoding='utf-8')
            _, issues, count = audit.load_catalogue(base)
            self.assertEqual(count, 1)
            self.assertEqual(issues[0]['code'], 'duplicate_identity')

    def test_market_paths_are_checked_without_changing_them(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            catalogue(base / 'fr', [row()])
            audit.dump(base / 'market.json', {'Stock': 'Crosse', 'Attachments': 'Accessoires', 'Attachments > Stock': 'bad'})
            result = audit.audit(base / 'fr', RULES, market=base / 'market.json')
            self.assertEqual(result['errors'][0]['code'], 'market_path')

    def test_changed_translation_and_namespace_are_tracked(self):
        original = {('', 'a'): dict(row(), file='a.json')}
        previous = audit.snapshot(original)['translations']
        changed = {('', 'a'): dict(row(text='Salut {Name}'), file='b.json')}
        self.assertEqual(audit.changes(changed, previous)[0]['code'], 'text_changed')
        changed = {('other', 'a'): dict(row(ns='other'), file='b.json')}
        self.assertEqual({r['code'] for r in audit.changes(changed, previous)}, {'new', 'removed'})

    def test_uppercase_map_names_are_protected(self):
        rows = {('', 'map'): dict(row(source='OUTSKIRTS', text='PÉRIPHÉRIE'), file='a.json')}
        self.assertEqual(audit.checks(rows, RULES)[0][0]['code'], 'protected_name')


class AzertyTests(unittest.TestCase):
    def test_diagnostic_reports_reset_keys_and_conflicts(self):
        data = profile([('IA_Movement_W', 'W'), ('IA_Inventory', 'Z')])
        report = azerty.diagnose(data)
        self.assertFalse(report['can_install'])
        self.assertEqual(report['bindings'][0]['state'], 'different')
        self.assertTrue(any(b['state'] == 'implicit' for b in report['bindings']))
        self.assertEqual(report['conflicts'], [{'action': 'IA_Inventory', 'key': 'Z'}])

    def test_diagnose_is_read_only_and_preserves_unrelated_keys(self):
        data = profile([('IA_Crouch', 'C')])
        original = data
        installed = azerty.apply_preset(data, azerty.load_preset()['bindings'])
        self.assertEqual(data, original)
        report = azerty.diagnose(installed)
        self.assertTrue(report['all_bindings_applied'])
        self.assertEqual(report['preserved'], [{'action': 'IA_Crouch', 'key': 'C', 'keyboard': True}])
        self.assertEqual(azerty.apply_preset(installed, azerty.load_preset()['bindings']), installed)

    def test_duplicate_binding_is_not_installable(self):
        report = azerty.diagnose(profile([('IA_Movement_W', 'Z'), ('IA_Movement_W', 'F1')]))
        self.assertFalse(report['can_install'])
        self.assertEqual(report['bindings'][0]['state'], 'duplicate')

    def test_azerty_restore_rejects_changes_or_corrupt_backup(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(azerty, 'assert_game_closed'):
            base = Path(folder)
            path, backups = base / 'input.sav', base / 'backups'
            original = profile([('IA_Crouch', 'C')])
            path.write_bytes(original)
            azerty.install(path, backups)
            installed = path.read_bytes()
            path.write_bytes(installed + b'x')
            with self.assertRaises(ValueError):
                azerty.restore(path, backups)
            path.write_bytes(installed)
            next(backups.glob('*.sav')).write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                azerty.restore(path, backups)
            self.assertEqual(path.read_bytes(), installed)

    def test_running_game_guard_blocks_install(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(azerty, 'assert_game_closed', side_effect=ValueError('Close game')):
            base = Path(folder)
            path = base / 'input.sav'
            original = profile([])
            path.write_bytes(original)
            with self.assertRaisesRegex(ValueError, 'Close game'):
                azerty.install(path, base / 'backups')
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse((base / 'backups').exists())


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / 'source'
        catalogue(self.source, [row()])
        self.translations, self.backups = self.base / 'Translations', self.base / 'backups'
        self.game = self.base / 'steamapps/common/PROJECT QUARANTINE'
        (self.game / 'Test_C/Content/Paks').mkdir(parents=True)
        self.pak = self.base / 'market.pak'
        self.pak.write_bytes(b'test market')
        self.manifest = dict(schema=1, translation_version='test', steam_build='123',
                             json_files={'fr_001.json': installer.digest((self.source / 'fr_001.json').read_bytes())},
                             market_sha256=installer.digest(self.pak.read_bytes()))
        self.set_build('123')

    def set_build(self, build):
        (self.base / 'steamapps/appmanifest_2116120.acf').write_text('"buildid" "' + build + '"\n"installdir" "PROJECT QUARANTINE"', encoding='utf-8')

    def plan(self, market=False):
        return installer.plan_install(self.source, self.translations, self.game, market, self.manifest, self.pak)

    @patch.object(installer, 'assert_game_closed')
    def test_install_and_restore_keep_reports_and_other_files(self, _guard):
        target = self.translations / 'fr'
        catalogue(target, [row(text='Ancien {Name}')])
        (target / '_Report.txt').write_text('previous report', encoding='utf-8')
        (self.game / 'Test_C/Content/Paks/base.pak').write_bytes(b'game')
        old = target.joinpath('fr_001.json').read_bytes()
        transaction = installer.apply_plan(self.plan(True), self.backups)
        self.assertEqual((target / 'fr_001.json').read_bytes(), (self.source / 'fr_001.json').read_bytes())
        self.assertEqual(self.plan(True)['operations'], [])
        installer.restore(transaction)
        self.assertEqual((target / 'fr_001.json').read_bytes(), old)
        self.assertFalse((self.game / 'Test_C/Content/Paks' / installer.PAK).exists())
        self.assertEqual((target / '_Report.txt').read_text(), 'previous report')
        self.assertEqual((self.game / 'Test_C/Content/Paks/base.pak').read_bytes(), b'game')

    def test_market_refused_on_new_build_but_json_preview_allowed(self):
        self.set_build('456')
        with self.assertRaisesRegex(ValueError, 'build Steam'):
            self.plan(True)
        self.assertEqual(len(self.plan(False)['operations']), 1)

    def test_rejects_tampered_source(self):
        catalogue(self.source, [row(text='Changed {Name}')])
        with self.assertRaisesRegex(ValueError, 'manifeste'):
            self.plan()

    def test_unknown_active_translation_is_not_overwritten(self):
        target = self.translations / 'fr'
        catalogue(target, [row()])
        audit.dump(target / 'personal.json', {'texts': [row('x')]})
        with self.assertRaisesRegex(ValueError, 'supplémentaires'):
            self.plan()

    @patch.object(installer, 'assert_game_closed')
    def test_refuses_concurrent_change_before_any_write(self, _guard):
        plan = self.plan()
        path = plan['operations'][0]['path']
        path.parent.mkdir(parents=True)
        path.write_bytes(b'concurrent')
        with self.assertRaisesRegex(ValueError, 'changé'):
            installer.apply_plan(plan, self.backups)
        self.assertEqual(path.read_bytes(), b'concurrent')

    @patch.object(installer, 'assert_game_closed')
    def test_rollback_after_partial_failure(self, _guard):
        plan = self.plan(True)
        real = installer.atomic_set
        def fail_once(path, data):
            if path.name == installer.PAK and data == b'test market':
                raise OSError('simulated disk failure')
            return real(path, data)
        with patch.object(installer, 'atomic_set', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'disk failure'):
                installer.apply_plan(plan, self.backups)
        self.assertFalse((self.translations / 'fr/fr_001.json').exists())
        record = next(self.backups.glob('*/transaction.json'))
        self.assertEqual(json.loads(record.read_text())['state'], 'rolled_back')

    @patch.object(installer, 'assert_game_closed')
    def test_restore_refuses_modified_destination(self, _guard):
        transaction = installer.apply_plan(self.plan(), self.backups)
        path = self.translations / 'fr/fr_001.json'
        path.write_bytes(b'changed after install')
        with self.assertRaisesRegex(ValueError, 'modifié depuis'):
            installer.restore(transaction)
        self.assertEqual(path.read_bytes(), b'changed after install')

    @patch.object(installer, 'assert_game_closed')
    def test_legacy_pak_is_disabled_and_reversible(self, _guard):
        paks = self.game / 'Test_C/Content/Paks'
        old = paks / installer.OLD_PAK
        old.write_bytes(b'legacy')
        transaction = installer.apply_plan(self.plan(), self.backups)
        self.assertFalse(old.exists())
        self.assertEqual((paks / (installer.OLD_PAK + '.disabled')).read_bytes(), b'legacy')
        installer.restore(transaction)
        self.assertEqual(old.read_bytes(), b'legacy')

    @patch.object(installer, 'assert_game_closed')
    def test_backups_cannot_go_in_loaded_folder(self, _guard):
        with self.assertRaisesRegex(ValueError, 'sauvegardes hors'):
            installer.apply_plan(self.plan(), self.translations / 'backup')

    def test_real_process_guard_detects_running_game_output(self):
        with patch.object(installer.os, 'name', 'nt'), patch.object(installer.subprocess, 'run') as tasklist:
            tasklist.return_value.stdout = b'"Test_C.exe","123","Console","1","100 K"'
            with self.assertRaisesRegex(ValueError, 'Fermez'):
                installer.assert_game_closed()


if __name__ == '__main__':
    unittest.main(verbosity=2)
