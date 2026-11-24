"""Point d’entrée de l’assistant AZERTY autonome, sans lancement du jeu."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import azerty
import interface


if __name__ == '__main__':
    try:
        if '--self-check' in sys.argv:
            parser = argparse.ArgumentParser()
            parser.add_argument('--self-check', action='store_true')
            parser.add_argument('--report', type=Path, required=True)
            parser.add_argument('--profile', type=Path)
            args = parser.parse_args()
            preset = azerty.load_preset()
            counts = {mode: len(azerty.select_preset(mode, preset)['bindings']) for mode in ('all', 'movement', 'equipment')}
            assert counts == {'all': 13, 'movement': 4, 'equipment': 9}
            checked = False
            if args.profile:
                original = args.profile.read_bytes()
                for mode in counts:
                    with tempfile.TemporaryDirectory(prefix='az-check-', dir=args.report.parent) as folder:
                        path = Path(folder) / 'input.sav'
                        path.write_bytes(original)
                        expected = azerty.apply_preset(original, azerty.select_preset(mode)['bindings'])
                        azerty.install(path, Path(folder) / 'Backups', mode)
                        assert path.read_bytes() == expected
                        if expected != original:
                            azerty.restore(path, Path(folder) / 'Backups')
                        assert path.read_bytes() == original
                checked = True
            args.report.write_text(json.dumps({'frozen': bool(getattr(sys, 'frozen', False)), 'version': preset['version'], 'groups': counts, 'install_restore_on_copies': checked}), encoding='utf-8')
        else:
            interface.main()
    except Exception as error:
        from tkinter import messagebox
        messagebox.showerror('Assistant AZERTY interrompu', str(error))
        sys.exit(1)
