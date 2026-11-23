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

def main(argv=None):
    local = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'Test_C'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preview', 'install', 'restore'], nargs='?', default='preview')
    parser.add_argument('--profile', type=Path, default=local / 'Saved/SaveGames/EnhancedInputUserSettings.sav')
    parser.add_argument('--backups', type=Path, default=local / 'AZERTY-Backups')
    args = parser.parse_args(argv)
    path = args.profile.resolve()
    if not path.is_file():
        raise ValueError('No input profile found. Launch the game once, save a key binding, close it, then retry.')
    before = path.read_bytes()
    if args.action == 'restore':
        assert_game_closed()
        for file in sorted(args.backups.glob('*.json'), reverse=True):
            record = json.loads(file.read_text(encoding='utf-8'))
            if record['profile'].casefold() != str(path).casefold() or record['after_sha256'] != digest(before):
                continue
            if Path(record['backup']).name != record['backup']:
                raise ValueError('Invalid backup path.')
            original = (args.backups / record['backup']).read_bytes()
            if digest(original) != record['before_sha256']:
                raise ValueError('Backup checksum mismatch.')
            replace_profile(path, before, original)
            print('Previous controls restored. The game was not launched.')
            return
        raise ValueError('No matching backup. The game may have rewritten the profile. Backups remain available; save your current file before restoring one manually.')
    preset = json.loads(Path(__file__).with_name('preset.json').read_text(encoding='utf-8'))
    after = apply_preset(before, preset['bindings'])
    for row in preset['bindings']:
        # Escape keycaps so Windows consoles with a legacy code page can display the output.
        print(row['action'] + ' -> ' + row['key'])
    if before == after:
        print('The AZERTY preset is already applied. No file was changed.')
    elif args.action == 'preview':
        print('Preview only. Use install with the game closed to apply the preset.')
    else:
        assert_game_closed()
        backup = save_backup(args.backups, path, before, after, preset['version'])
        replace_profile(path, before, after)
        print('AZERTY installed. Original backup: ' + str(backup))
        print('Keep Windows in French. The game was not launched.')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, struct.error, subprocess.SubprocessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
