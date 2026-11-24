"""Construit deux exécutables autonomes ; aucun accès au jeu ou aux sauvegardes."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name, entry in [('INSTALLER-FR', 'installation/frozen_entry.py'), ('AZERTY', 'azerty/frozen_entry.py')]:
        command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onefile', '--windowed', '--noupx',
                   '--name', name, '--distpath', str(output), '--workpath', str(output / 'build' / name),
                   '--specpath', str(output / 'specs'), '--paths', str(ROOT), '--paths', str(ROOT / 'azerty')]
        if name == 'INSTALLER-FR':
            command += ['--add-data', str(ROOT / 'installation/manifest.json') + ';installation', '--hidden-import', 'installation.interface']
        command += [str(ROOT / entry)]
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
