"""Prépare deux archives de test indépendantes, sans publication ni installation."""
import argparse
import hashlib
from pathlib import Path
import zipfile
from maintenance.translation_audit import dump

ROOT = Path(__file__).resolve().parents[1]


def build(output):
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
    result = []
    for name, entries in [('IRR_Assistant_FR_0.2.1_TEST1.zip', fr), ('IRR_Assistant_AZERTY_0.2.0_TEST1.zip', az)]:
        # Liste explicite : aucune sauvegarde ou donnée personnelle n’est distribuée.
        data = {target: path.read_bytes() for path, target in entries.items()}
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
    print(build(parser.parse_args().output))
