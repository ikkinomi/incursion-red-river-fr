"""Installation FR avec aperçu, sauvegardes et restauration contrôlée. Aucun lancement du jeu."""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from maintenance.translation_audit import audit

PAK = 'pakchunk98-FrenchMarketTest_P.pak'
OLD_PAK = 'pakchunk99-French_P.pak'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def local_base():
    return Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'Test_C'


def assert_game_closed():
    if os.name != 'nt':
        raise ValueError('Installation et restauration disponibles sous Windows uniquement.')
    for process in ('Test_C.exe', 'Test_C-Win64-Shipping.exe'):
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ' + process, '/FO', 'CSV', '/NH'], capture_output=True, check=True)
        if any(row and row[0].casefold() == process.casefold() for row in csv.reader(io.StringIO(result.stdout.decode(errors='replace')))):
            raise ValueError('Fermez Incursion Red River avant de modifier la traduction.')


def assert_plain_path(path):
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and getattr(part.stat(follow_symlinks=False), 'st_file_attributes', 0) & 0x400):
            raise ValueError('Lien ou jonction non pris en charge : ' + str(part))
    return path


def game_build(game):
    game = Path(game)
    if not (game / 'Test_C/Content/Paks').is_dir():
        raise ValueError('Choisissez le dossier PROJECT QUARANTINE contenant Test_C/Content/Paks.')
    manifest = game.parent.parent / 'appmanifest_2116120.acf'
    if not manifest.is_file():
        return None
    text = manifest.read_text(encoding='utf-8-sig')
    build = re.search(r'"buildid"\s+"(\d+)"', text)
    install = re.search(r'"installdir"\s+"([^"]+)"', text)
    if not install or install[1].casefold() != game.name.casefold():
        return None
    return build[1] if build else None


def detect_games():
    """Lit la configuration Steam locale, sans accès réseau ni lancement de Steam."""
    roots = {Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')) / 'Steam'}
    if os.name == 'nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam') as key:
                roots.add(Path(winreg.QueryValueEx(key, 'SteamPath')[0]))
        except OSError:
            pass
    libraries = set(roots)
    for root in roots:
        config = root / 'steamapps/libraryfolders.vdf'
        if config.is_file():
            libraries.update(Path(p.replace('\\\\', '\\')) for p in re.findall(r'"path"\s+"([^"]+)"', config.read_text(encoding='utf-8-sig')))
    found = []
    for library in sorted(libraries):
        manifest = library / 'steamapps/appmanifest_2116120.acf'
        if not manifest.is_file():
            continue
        match = re.search(r'"installdir"\s+"([^"]+)"', manifest.read_text(encoding='utf-8-sig'))
        if match and Path(match[1]).name == match[1]:
            game = library / 'steamapps/common' / match[1]
            if (game / 'Test_C/Content/Paks').is_dir():
                found.append(game)
    return found


def defaults():
    source = ROOT / 'fr' if (ROOT / 'fr').is_dir() else ROOT / 'translations/fr'
    pak = ROOT / 'Test_C/Content/Paks' / PAK
    if not pak.is_file():
        pak = ROOT / 'patch/Test_C/Content/Paks' / PAK
    return source, pak


def plan_install(source, translations, game=None, market=False, manifest=None, pak=None):
    manifest = manifest or json_read(Path(__file__).with_name('manifest.json'))
    source, translations = assert_plain_path(source), assert_plain_path(translations)
    target = translations / 'fr'
    if source.resolve() == target.resolve():
        raise ValueError('La source et le dossier installé doivent être différents.')
    report = audit(source, json_read(ROOT / 'docs/REGLES-TRADUCTION.json'))
    if report['errors']:
        raise ValueError('Traduction source invalide : ' + str(report['errors'][:2]))
    actual = {p.name: digest(p.read_bytes()) for p in source.glob('*.json') if not p.name.startswith('_')}
    if actual != manifest['json_files']:
        raise ValueError('Les fichiers de traduction ne correspondent pas au manifeste. Réextrayez l’archive complète.')
    for name in manifest['json_files']:
        if Path(name).name != name or not re.fullmatch(r'fr_[A-Za-z0-9_]+\.json', name):
            raise ValueError('Nom de fichier inattendu dans le manifeste.')
        assert_plain_path(source / name)
    operations, notices = [], []
    def put(path, after):
        path = assert_plain_path(path)
        before = path.read_bytes() if path.is_file() else None
        if before != after:
            operations.append({'path': path, 'before': before, 'after': after})
    # Un ancien fichier additionnel pourrait gagner un doublon ns/key : arrêt explicite.
    if target.is_dir():
        unknown = [p.name for p in target.glob('*.json') if not p.name.startswith('_') and p.name not in actual]
        if unknown:
            raise ValueError('Fichiers de traduction supplémentaires à sauvegarder hors de fr avant installation : ' + ', '.join(unknown))
    for name in actual:
        put(target / name, (source / name).read_bytes())
    build = None
    if game:
        game = assert_plain_path(game)
        build = game_build(game)
        paks = game / 'Test_C/Content/Paks'
        old = paks / OLD_PAK
        if old.is_file():
            old = assert_plain_path(old)
            disabled = assert_plain_path(paks / (OLD_PAK + '.disabled'))
            data = old.read_bytes()
            if disabled.exists() and disabled.read_bytes() != data:
                raise ValueError('Une sauvegarde différente de l’ancien pak existe déjà. Déplacez-la hors du jeu avant de réessayer.')
            put(disabled, data)
            operations.append({'path': old, 'before': data, 'after': None})
            notices.append('L’ancien pakchunk99 sera désactivé et sauvegardé.')
        if (paks / PAK).is_file() and build != manifest['steam_build'] and not market:
            notices.append('Complément du marché déjà présent sur un build non validé : désactivez-le avant de jouer.')
    if market:
        if not game or build != manifest['steam_build']:
            raise ValueError('Complément du marché refusé : build Steam absent ou différent du build validé ' + manifest['steam_build'] + '.')
        pak = assert_plain_path(pak or defaults()[1])
        data = pak.read_bytes()
        if digest(data) != manifest['market_sha256']:
            raise ValueError('Empreinte du complément du marché incorrecte.')
        put(game / 'Test_C/Content/Paks' / PAK, data)
    notices.append('Les rapports _Report et _Todo existants sont conservés ; ils décrivent le dernier lancement du jeu.')
    return {'operations': operations, 'notices': notices, 'game_build': build,
            'target': str(target), 'market': market, 'manifest_version': manifest['translation_version']}


def describe(plan):
    lines = ['Destination FR : ' + plan['target'], 'Build Steam détecté : ' + str(plan['game_build'] or 'inconnu'),
             'Complément du marché : ' + ('oui' if plan['market'] else 'non'), '']
    for op in plan['operations']:
        lines.append(('Retirer' if op['after'] is None else 'Remplacer' if op['before'] is not None else 'Créer') + ' : ' + str(op['path']))
    if not plan['operations']:
        lines.append('Les fichiers sélectionnés sont déjà installés à l’identique.')
    return '\n'.join(lines + [''] + plan['notices'])


def current(path):
    path = assert_plain_path(path)
    if path.exists() and not path.is_file():
        raise ValueError('Un dossier occupe un emplacement de fichier : ' + str(path))
    return path.read_bytes() if path.exists() else None


def atomic_set(path, data):
    path = assert_plain_path(path)
    if data is None:
        if path.exists():
            path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.fr-tmp', delete=False) as stream:
            temp = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        if path.read_bytes() != data:
            raise OSError('Vérification après copie impossible : ' + str(path))
    finally:
        if temp and temp.exists():
            temp.unlink()


def apply_plan(plan, backups):
    operations = plan['operations']
    if not operations:
        return None
    assert_game_closed()
    for op in operations:
        if current(op['path']) != op['before']:
            raise ValueError('Un fichier a changé depuis l’aperçu. Relancez Vérifier.')
    backups = assert_plain_path(backups)
    # Les sauvegardes ne doivent jamais se retrouver dans les dossiers lus par le jeu.
    protected = {Path(plan['target']).parent.resolve()}
    protected.update(op['path'].parent.resolve() for op in operations)
    if any(backups == p or p in backups.parents for p in protected):
        raise ValueError('Placez les sauvegardes hors des dossiers de traduction et de Paks.')
    transaction = backups / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex)
    transaction.mkdir(parents=True)
    records = []
    for index, op in enumerate(operations):
        saved = f'{index:03d}.bin' if op['before'] is not None else None
        if saved:
            (transaction / saved).write_bytes(op['before'])
            if (transaction / saved).read_bytes() != op['before']:
                raise OSError('Sauvegarde non vérifiée. Installation interrompue.')
        records.append({'path': str(op['path']), 'backup': saved,
                        'before_sha256': digest(op['before']) if op['before'] is not None else None,
                        'after_sha256': digest(op['after']) if op['after'] is not None else None})
    record = {'schema': 1, 'state': 'prepared', 'operations': records, 'version': plan['manifest_version']}
    def journal():
        atomic_set(transaction / 'transaction.json', (json.dumps(record, indent=2) + '\n').encode('utf-8'))
    journal()
    touched = []
    try:
        assert_game_closed()
        for op in operations:
            if current(op['path']) != op['before']:
                raise ValueError('Un fichier a changé pendant l’installation.')
            touched.append(op)
            atomic_set(op['path'], op['after'])
        record['state'] = 'installed'
        journal()
    except Exception:
        rollback_failed = []
        for op in reversed(touched):
            try:
                # Ne pas écraser une modification concurrente imprévue.
                if current(op['path']) not in (op['after'], op['before']):
                    raise OSError('Modification concurrente')
                atomic_set(op['path'], op['before'])
            except Exception:
                rollback_failed.append(str(op['path']))
        record['state'] = 'recovery_required' if rollback_failed else 'rolled_back'
        record['recovery_required'] = rollback_failed
        journal()
        raise
    return transaction


def restore(transaction):
    """Refuse d’écraser un fichier modifié depuis l’installation. Retour arrière sauvegardé."""
    transaction = assert_plain_path(transaction)
    record = json_read(transaction / 'transaction.json')
    if record.get('state') != 'installed':
        raise ValueError('Cette transaction ne correspond pas à une installation restaurable.')
    operations = []
    for item in record['operations']:
        path = assert_plain_path(item['path'])
        before = current(path)
        if (digest(before) if before is not None else None) != item['after_sha256']:
            raise ValueError('Fichier modifié depuis l’installation : restauration refusée pour conserver vos changements. ' + str(path))
        backup = item['backup']
        if backup is not None and Path(backup).name != backup:
            raise ValueError('Chemin de sauvegarde invalide.')
        after = assert_plain_path(transaction / backup).read_bytes() if backup else None
        if (digest(after) if after is not None else None) != item['before_sha256']:
            raise ValueError('Sauvegarde corrompue.')
        operations.append({'path': path, 'before': before, 'after': after})
    # Même mécanisme transactionnel : la restauration peut elle-même être annulée.
    plan = {'operations': operations, 'target': record['operations'][0]['path'], 'manifest_version': 'restore'}
    recovery = apply_plan(plan, transaction.parent)
    record['state'] = 'restored'
    atomic_set(transaction / 'transaction.json', (json.dumps(record, indent=2) + '\n').encode('utf-8'))
    return recovery


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preview', 'install', 'restore', 'gui'], nargs='?', default='gui')
    parser.add_argument('--translations', type=Path, default=local_base() / 'Saved/Translations')
    parser.add_argument('--source', type=Path, default=defaults()[0])
    parser.add_argument('--game', type=Path)
    parser.add_argument('--market', action='store_true')
    parser.add_argument('--backups', type=Path, default=local_base() / 'FR-Backups')
    parser.add_argument('--transaction', type=Path)
    args = parser.parse_args(argv)
    if args.action == 'gui':
        from installation.interface import launch
        launch(args)
    elif args.action == 'restore':
        if not args.transaction:
            raise ValueError('Indiquez --transaction avec le dossier de sauvegarde à restaurer.')
        print('Restauration terminée. Sauvegarde de retour : ' + str(restore(args.transaction)))
    else:
        games = detect_games() if args.game is None else []
        game = args.game or (games[0] if len(games) == 1 else None)
        plan = plan_install(args.source, args.translations, game, args.market)
        print(describe(plan))
        if args.action == 'install':
            print('Sauvegarde : ' + str(apply_plan(plan, args.backups)))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
        sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, ImportError, subprocess.SubprocessError) as error:
        print('ERREUR : ' + str(error), file=sys.stderr)
        sys.exit(1)
