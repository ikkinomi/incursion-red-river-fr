"""Lecture seule des bibliothèques Steam et du build installé, sans réseau."""
import os
from pathlib import Path
import re


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
        if manifest.is_file():
            match = re.search(r'"installdir"\s+"([^"]+)"', manifest.read_text(encoding='utf-8-sig'))
            if match and Path(match[1]).name == match[1]:
                game = library / 'steamapps/common' / match[1]
                if (game / 'Test_C/Content/Paks').is_dir():
                    found.append(game)
    return list(dict.fromkeys(p.resolve() for p in found))


def compatibility(expected, game=None):
    games = detect_games() if game is None else [Path(game)]
    if len(games) != 1:
        return {'state': 'unknown', 'build': None, 'expected': expected,
                'message': 'Build non vérifié : aucune installation unique détectée. Aucun fichier modifié.'}
    build = game_build(games[0])
    state = 'validated' if build == expected else 'unknown' if build is None else 'changed'
    message = ('Build Steam ' + str(build or 'inconnu') + ' — ' +
               ('build validé.' if state == 'validated' else 'compatibilité à revérifier ; build validé : ' + expected + '.'))
    return {'state': state, 'build': build, 'expected': expected, 'message': message}
