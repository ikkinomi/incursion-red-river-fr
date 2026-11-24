"""Point d’entrée de l’assistant Windows autonome ; données externes vérifiées."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
from installation import fr_manager as manager


def main():
    if '--self-check' in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument('--self-check', action='store_true')
        parser.add_argument('--report', type=Path, required=True)
        args = parser.parse_args()
        manifest = manager.json_read(Path(manager.__file__).with_name('manifest.json'))
        source, pak = manager.defaults()
        actual = {p.name: manager.digest(p.read_bytes()) for p in source.glob('*.json') if not p.name.startswith('_')}
        assert actual == manifest['json_files'], 'Empreintes JSON incorrectes'
        assert manager.digest(pak.read_bytes()) == manifest['market_sha256'], 'Empreinte marché incorrecte'
        audit = manager.audit(source, manager.json_read(manager.ROOT / 'docs/REGLES-TRADUCTION.json'))
        assert not audit['errors'], 'Traduction invalide'
        with tempfile.TemporaryDirectory(prefix='fr-check-', dir=args.report.parent) as folder:
            base = Path(folder)
            game = base / 'steamapps/common/PROJECT QUARANTINE'
            (game / 'Test_C/Content/Paks').mkdir(parents=True)
            (base / 'steamapps/appmanifest_2116120.acf').write_text('"buildid" "' + manifest['steam_build'] + '"\n"installdir" "PROJECT QUARANTINE"', encoding='utf-8')
            target = base / 'Translations'
            plan = manager.plan_install(source, target, game, True)
            transaction = manager.apply_plan(plan, base / 'Backups')
            assert manager.check_update(source, target, game)['market_validated']
            assert manager.plan_install(source, target, game, True)['operations'] == []
            manager.restore(transaction)
            assert not list((target / 'fr').glob('*.json'))
            assert not (game / 'Test_C/Content/Paks' / manager.PAK).exists()
        args.report.write_text(json.dumps({'frozen': bool(getattr(sys, 'frozen', False)), 'version': manifest['translation_version'], 'files': len(actual), 'errors': 0, 'install_restore_on_copy': True}), encoding='utf-8')
    else:
        manager.main()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        from tkinter import messagebox
        messagebox.showerror('Assistant FR interrompu', str(error))
        sys.exit(1)
