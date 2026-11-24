"""Offline AZERTY preset editor for Incursion Red River 1.4.0.4 / UE 5.6.

Python 3.9+, standard library only. No network, injection, background service or game launch.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import uuid

if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.steam import compatibility

PROFILE_CLASS = '/Script/EnhancedInput.EnhancedPlayerMappableKeyProfile'
PROFILE_ID = 'InputUserSettings.Profiles.Default'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def fstring(value):
    raw = value.encode('ascii') + b'\0'
    return struct.pack('<i', len(raw)) + raw

class Reader:
    def __init__(self, data, offset):
        self.data, self.pos = data, offset
    def take(self, length):
        if not 0 <= length <= len(self.data) - self.pos:
            raise ValueError('Truncated profile; no change made.')
        result = self.data[self.pos:self.pos + length]
        self.pos += length
        return result
    def integer(self):
        return struct.unpack('<i', self.take(4))[0]
    def string(self):
        length = self.integer()
        if length == 0:
            return ''
        if not 1 <= abs(length) <= 4096:
            raise ValueError('Unsupported string size.')
        width = 2 if length < 0 else 1
        raw = self.take(abs(length) * width)
        if raw[-width:] != bytes(width):
            raise ValueError('Invalid profile string.')
        return raw[:-width].decode('utf-16-le' if length < 0 else 'utf-8')

def parse(data):
    if not 32 <= len(data) <= 1024 * 1024 or data[:4] != b'GVAS':
        raise ValueError('Unsupported save file.')
    if struct.unpack_from('<i', data, 4)[0] != 3 or struct.unpack_from('<HH', data, 16) != (5, 6):
        raise ValueError('Unsupported engine version; expected Unreal Engine 5.6.')
    marker = fstring(PROFILE_CLASS)
    if data.count(marker) != 1 or not data.endswith(fstring('ObjectEnd')):
        raise ValueError('Unsupported Enhanced Input profile.')
    start = data.index(marker)
    if start < 4 or struct.unpack_from('<i', data, start - 4)[0] != 1:
        raise ValueError('Only one saved default key profile is supported.')
    reader = Reader(data, start + len(marker))
    if not reader.string().startswith('EnhancedPlayerMappableKeyProfile_'):
        raise ValueError('Unsupported profile class.')
    count_offset = reader.pos
    count = reader.integer()
    if not 0 <= count <= 256:
        raise ValueError('Invalid mapping count.')
    rows = []
    for _ in range(count):
        begin = reader.pos
        name = reader.string()
        key_start = reader.pos
        key = reader.string()
        key_end = reader.pos
        device_class, device_id = reader.string(), reader.string()
        metadata = reader.take(6)
        rows.append({'name': name, 'key': key,
                     'keyboard': device_class == device_id == 'None' and metadata == bytes(6),
                     'raw': data[begin:reader.pos], 'before_key': data[begin:key_start],
                     'after_key': data[key_end:reader.pos]})
    suffix_offset = reader.pos
    if reader.string() != PROFILE_ID:
        raise ValueError('Only the default key profile is supported.')
    return data[:count_offset], rows, data[suffix_offset:]

def encode(prefix, rows, suffix):
    return prefix + struct.pack('<i', len(rows)) + b''.join(row['raw'] for row in rows) + suffix

def apply_preset(data, bindings):
    prefix, rows, suffix = parse(data)
    if encode(prefix, rows, suffix) != data:
        raise ValueError('Profile round-trip failed.')
    requested = {row['action']: row['key'] for row in bindings}
    if len(requested) != len(bindings) or len(set(requested.values())) != len(bindings):
        raise ValueError('Invalid preset: duplicate action or key.')
    conflicts = [row['name'] + ' = ' + row['key'] for row in rows
                 if row['keyboard'] and row['name'] not in requested and row['key'] in requested.values()]
    if conflicts:
        raise ValueError('Custom binding conflict(s): ' + '; '.join(conflicts) +
                         '. Resolve these in the game first. No file was changed.')
    for name, key in requested.items():
        matches = [row for row in rows if row['keyboard'] and row['name'] == name]
        if len(matches) > 1:
            raise ValueError('Duplicate keyboard mapping: ' + name)
        if matches:
            row = matches[0]
            if row['key'] != key:
                row['raw'] = row['before_key'] + fstring(key) + row['after_key']
                row['key'] = key
        else:
            rows.append({'name': name, 'key': key, 'keyboard': True,
                         'raw': fstring(name) + fstring(key) + fstring('None') + fstring('None') + bytes(6)})
    result = encode(prefix, rows, suffix)
    vp, verified, vs = parse(result)
    if vp != prefix or vs != suffix or encode(vp, verified, vs) != result:
        raise ValueError('Generated profile validation failed.')
    for name, key in requested.items():
        if sum(row['keyboard'] and row['name'] == name and row['key'] == key for row in verified) != 1:
            raise ValueError('Generated mapping validation failed: ' + name)
    return result

def assert_game_closed():
    if os.name != 'nt':
        raise ValueError('Installation and restoration support Windows only.')
    for process in ['Test_C.exe', 'Test_C-Win64-Shipping.exe']:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ' + process, '/FO', 'CSV', '/NH'],
                                capture_output=True, check=True)
        text = result.stdout.decode(errors='replace')
        if any(row and row[0].casefold() == process.casefold() for row in csv.reader(io.StringIO(text))):
            raise ValueError('Close Incursion Red River before changing the controls.')

def replace_profile(path, before, after):
    assert_game_closed()
    if path.read_bytes() != before:
        raise ValueError('The profile changed. No file was replaced.')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), prefix=path.name + '.', suffix='.azerty-tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(after)
            stream.flush()
            os.fsync(stream.fileno())
        assert_game_closed()
        if path.read_bytes() != before:
            raise ValueError('The profile changed. No file was replaced.')
        os.replace(str(temporary), str(path))
        if path.read_bytes() != after:
            raise OSError('Profile verification failed. Use the original backup.')
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()

def save_backup(directory, path, before, after, version):
    directory.mkdir(parents=True, exist_ok=True)
    name = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex
    backup = directory / (name + '.sav')
    backup.write_bytes(before)
    if backup.read_bytes() != before:
        raise OSError('Backup verification failed.')
    record = {'profile': str(path.resolve()), 'backup': backup.name, 'before_sha256': digest(before),
              'after_sha256': digest(after), 'preset_version': version}
    (directory / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return backup


def load_preset():
    path = Path(sys.executable).with_name('preset.json') if getattr(sys, 'frozen', False) else Path(__file__).with_name('preset.json')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def select_preset(mode='all', preset=None):
    if mode not in ('all', 'movement', 'equipment'):
        raise ValueError('Mode AZERTY inconnu.')
    preset = dict(preset or load_preset())
    preset['bindings'] = [b for b in preset['bindings'] if mode == 'all' or
                          b['action'].startswith('IA_Equip') == (mode == 'equipment')]
    if not preset['bindings']:
        raise ValueError('Ce mode ne contient aucune affectation.')
    preset['mode'] = mode
    return preset


def diagnose(data, preset=None, mode='all'):
    """Diagnostic local ; les affectations absentes du .sav sont des valeurs implicites."""
    preset = select_preset(mode, preset)
    _, rows, _ = parse(data)
    requested = {b['action']: b['key'] for b in preset['bindings']}
    bindings = []
    for binding in preset['bindings']:
        matches = [r for r in rows if r['keyboard'] and r['name'] == binding['action']]
        current = [r['key'] for r in matches]
        state = ('duplicate' if len(matches) > 1 else 'implicit' if not matches
                 else 'ok' if current[0] == binding['key'] else 'different')
        bindings.append(dict(binding, current=current, state=state))
    conflicts = [{'action': r['name'], 'key': r['key']} for r in rows
                 if r['keyboard'] and r['name'] not in requested and r['key'] in requested.values()]
    preserved = [{'action': r['name'], 'key': r['key'], 'keyboard': r['keyboard']} for r in rows
                 if not r['keyboard'] or r['name'] not in requested]
    duplicates = [b['action'] for b in bindings if b['state'] == 'duplicate']
    result = {'schema': 1, 'mode': mode, 'preset_version': preset['version'], 'target_game_version': preset['game_version'],
              'target_steam_build': preset['steam_build'], 'profile_sha256': digest(data),
              'all_bindings_applied': all(b['state'] == 'ok' for b in bindings),
              'can_install': not conflicts and not duplicates, 'bindings': bindings,
              'conflicts': conflicts, 'preserved': preserved,
              'limits': 'Le .sav ne contient que les personnalisations : les nouvelles actions et touches par défaut du jeu ne peuvent pas être déduites de ce fichier. Le build du jeu n’est pas vérifié par ce diagnostic.'}
    return result


def format_diagnosis(report):
    states = {'ok': 'OK', 'implicit': 'non enregistrée (valeur du jeu)',
              'different': 'différente du préréglage', 'duplicate': 'doublon : installation refusée'}
    lines = ['Profil AZERTY : ' + ('déjà appliqué' if report['all_bindings_applied'] else 'à installer ou à réappliquer'), '']
    for b in report['bindings']:
        lines.append(f"{b.get('label', b['action'])} : {', '.join(b['current']) or 'implicite'} → {b['keycap']} [{states[b['state']]}]")
    lines += ['', 'Autres commandes conservées :']
    lines += [f"  {r['action']} = {r['key']}" + ('' if r['keyboard'] else ' (manette/autre entrée)') for r in report['preserved']]
    if report['conflicts']:
        lines += ['', 'CONFLITS :'] + [f"  {r['action']} utilise déjà {r['key']}" for r in report['conflicts']]
    lines += ['', report['limits']]
    return '\n'.join(lines)


def install(path, backups, mode='all'):
    path, backups = Path(path).resolve(), Path(backups)
    before = path.read_bytes()
    preset = select_preset(mode)
    after = apply_preset(before, preset['bindings'])
    if after == before:
        return 'Le profil AZERTY est déjà appliqué. Aucun fichier modifié.'
    assert_game_closed()
    backup = save_backup(backups, path, before, after, preset['version'])
    replace_profile(path, before, after)
    return 'AZERTY installé. Sauvegarde des commandes précédentes : ' + str(backup)


def restore(path, backups):
    path, backups = Path(path).resolve(), Path(backups)
    before = path.read_bytes()
    assert_game_closed()
    for file in sorted(backups.glob('*.json'), reverse=True):
        record = json.loads(file.read_text(encoding='utf-8-sig'))
        if record['profile'].casefold() != str(path).casefold() or record['after_sha256'] != digest(before):
            continue
        if Path(record['backup']).name != record['backup']:
            raise ValueError('Invalid backup path.')
        original = (backups / record['backup']).read_bytes()
        if digest(original) != record['before_sha256']:
            raise ValueError('Backup checksum mismatch.')
        replace_profile(path, before, original)
        return 'Commandes précédentes restaurées. Le jeu n’a pas été lancé.'
    raise ValueError('Aucune sauvegarde correspondante. Le jeu a peut-être réécrit le profil. Les sauvegardes restent disponibles ; conservez votre fichier actuel avant une restauration manuelle.')

def main(argv=None):
    local = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'Test_C'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preview', 'diagnose', 'install', 'restore'], nargs='?', default='preview')
    parser.add_argument('--profile', type=Path, default=local / 'Saved/SaveGames/EnhancedInputUserSettings.sav')
    parser.add_argument('--backups', type=Path, default=local / 'AZERTY-Backups')
    parser.add_argument('--mode', choices=['all', 'movement', 'equipment'], default='all', help='Les deux groupes, déplacements/actions, ou rangée d’équipement.')
    parser.add_argument('--game', type=Path, help='Installation Steam pour le contrôle du build.')
    parser.add_argument('--json', type=Path, help='Exporter le diagnostic local (peut contenir des touches personnalisées).')
    args = parser.parse_args(argv)
    path = args.profile.resolve()
    if not path.is_file():
        raise ValueError('No input profile found. Launch the game once, save a key binding, close it, then retry.')
    if args.action == 'restore':
        print(restore(path, args.backups))
    elif args.action == 'install':
        print(install(path, args.backups, args.mode))
    else:
        report = diagnose(path.read_bytes(), mode=args.mode)
        report['compatibility'] = compatibility(load_preset()['steam_build'], args.game)
        print(format_diagnosis(report))
        print(report['compatibility']['message'])
        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if not report['can_install']:
            return 1
    return 0

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
        sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, struct.error, subprocess.SubprocessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
