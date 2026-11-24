"""Prépare deux archives indépendantes, sans publication ni installation."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import zipfile
from maintenance.translation_audit import dump

ROOT = Path(__file__).resolve().parents[1]


def packaged_readme(text, directory=''):
    def link(match):
        label, target = match.groups()
        if target.startswith(('https://', 'http://', '#')):
            return match[0]
        path = posixpath.normpath(posixpath.join(directory, target))
        return '[' + label + '](https://github.com/ikkinomi/incursion-red-river-fr/blob/main/' + path + ')'
    return re.sub(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', link, text)


def build(output, release=False):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    fr = {ROOT / 'INSTALLER-FR.cmd': 'INSTALLER-FR.cmd',
          ROOT / 'installation/README.md': 'LISEZ-MOI.md',
          ROOT / 'maintenance/translation_audit.py': 'maintenance/translation_audit.py',
          ROOT / 'docs/REGLES-TRADUCTION.json': 'docs/REGLES-TRADUCTION.json'}
    for name in ('fr_manager.py', 'interface.py', 'manifest.json', 'README.md', 'VALIDATION-TEST1.json'):
        fr[ROOT / 'installation' / name] = 'installation/' + name
    for path in (ROOT / 'translations/fr').glob('*.json'):
        if not path.name.startswith('_'):
            fr[path] = 'fr/' + path.name
    fr[ROOT / 'patch/Test_C/Content/Paks/pakchunk98-FrenchMarketTest_P.pak'] = 'Test_C/Content/Paks/pakchunk98-FrenchMarketTest_P.pak'
    az = {ROOT / 'azerty' / name: name for name in ('azerty.py', 'interface.py', 'preset.json', 'AZERTY.cmd')}
    az[ROOT / 'azerty/ASSISTANT-TEST.md'] = 'LISEZ-MOI.md'
    az[ROOT / 'azerty/VALIDATION-TEST1.json'] = 'VALIDATION-TEST1.json'
    versions = (json.loads((ROOT / 'installation/manifest.json').read_text(encoding='utf-8'))['translation_version'],
                json.loads((ROOT / 'azerty/preset.json').read_text(encoding='utf-8'))['version'])
    if release:
        fr[ROOT / 'README.md'] = 'LISEZ-MOI.md'
        del fr[ROOT / 'installation/README.md']
        fr[ROOT / 'installation/README.md'] = 'installation/README.md'
        az.pop(ROOT / 'azerty/ASSISTANT-TEST.md')
        az[ROOT / 'azerty/README.md'] = 'LISEZ-MOI.md'
        for path in (ROOT / 'docs/images').glob('assistant-fr-*.jpg'):
            fr[path] = 'docs/images/' + path.name
        for path in (ROOT / 'docs/images').glob('assistant-azerty-*.jpg'):
            az[path] = 'images/' + path.name
    names = ([f'Incursion_Red_River_FR_1.4.0.4_v{versions[0]}.zip', f'Incursion_Red_River_AZERTY_1.4.0.4_v{versions[1]}.zip']
             if release else ['IRR_Assistant_FR_0.2.1_TEST1.zip', 'IRR_Assistant_AZERTY_0.2.0_TEST1.zip'])
    result = []
    for name, entries in zip(names, (fr, az)):
        # Liste explicite : aucune sauvegarde ou donnée personnelle n’est distribuée.
        data = {target: path.read_bytes() for path, target in entries.items()}
        if release:
            is_azerty = 'AZERTY' in name
            doc = packaged_readme(data['LISEZ-MOI.md'].decode('utf-8'), 'azerty' if is_azerty else '')
            if is_azerty:
                doc = doc.replace('../docs/images/', 'images/')
            data['LISEZ-MOI.md'] = doc.encode('utf-8')
        sums = ''.join(hashlib.sha256(value).hexdigest() + '  ' + target + '\n' for target, value in sorted(data.items()))
        data['SHA256SUMS.txt'] = sums.encode('utf-8')
        archive = output / name
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as stream:
            for target, value in sorted(data.items()):
                stream.writestr(target, value)
        with zipfile.ZipFile(archive) as stream:
            if stream.testzip() is not None or any(stream.read(target) != value for target, value in data.items()):
                raise ValueError('Archive non vérifiée : ' + name)
        checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
        archive.with_suffix('.zip.sha256').write_text(checksum + '  ' + name + '\n', encoding='utf-8')
        result.append({'name': name, 'sha256': checksum, 'files': len(data)})
    dump(output / 'archives.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()
    print(build(args.output, args.release))
