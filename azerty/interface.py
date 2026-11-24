"""Interface locale AZERTY, Python + Tkinter. Aucun lancement du jeu."""
import argparse
import os
from pathlib import Path
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except ImportError:
    raise SystemExit('Tkinter est indisponible. Installez Python avec Tcl/Tk, ou utilisez azerty.py en ligne de commande.')
import azerty


def main(argv=None):
    local = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'Test_C'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, default=local / 'Saved/SaveGames/EnhancedInputUserSettings.sav')
    parser.add_argument('--backups', type=Path, default=local / 'AZERTY-Backups')
    args = parser.parse_args(argv)
    root = tk.Tk()
    root.title('Incursion Red River — Assistant AZERTY 0.2.0 bêta')
    root.geometry('960x690')
    root.minsize(760, 580)
    frame = ttk.Frame(root, padding=18)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='Vos commandes en AZERTY', font=('Segoe UI', 19, 'bold')).pack(anchor='w')
    ttk.Label(frame, text='Gardez Windows en français pour jouer et écrire au terminal. Fermez le jeu avant toute modification.').pack(anchor='w', pady=(5, 15))
    profile = tk.StringVar(value=str(args.profile))
    line = ttk.Frame(frame)
    line.pack(fill='x')
    ttk.Entry(line, textvariable=profile).pack(side='left', fill='x', expand=True)
    def choose():
        selected = filedialog.askopenfilename(title='Choisir EnhancedInputUserSettings.sav', filetypes=[('Profil de commandes', '*.sav')])
        if selected:
            profile.set(selected)
            verify()
    ttk.Button(line, text='Parcourir…', command=choose).pack(side='left', padx=(8, 0))
    status = tk.StringVar(value='Cliquez sur Vérifier pour lire les commandes actuelles.')
    ttk.Label(frame, textvariable=status, wraplength=900).pack(anchor='w', pady=12)
    text = tk.Text(frame, wrap='word', font=('Consolas', 10), padx=12, pady=10)
    text.pack(fill='both', expand=True)
    def show(value):
        text.config(state='normal')
        text.delete('1.0', 'end')
        text.insert('1.0', value)
        text.config(state='disabled')
    def verify():
        try:
            report = azerty.diagnose(Path(profile.get()).read_bytes())
            show(azerty.format_diagnosis(report))
            status.set('Profil déjà configuré.' if report['all_bindings_applied'] else 'Installation possible après vérification des touches.' if report['can_install'] else 'Conflit ou doublon : consultez le détail ci-dessous.')
            install_button.config(state='normal' if report['can_install'] and not report['all_bindings_applied'] else 'disabled')
            return report
        except Exception as error:
            show(str(error))
            status.set('Vérification impossible. Aucun fichier modifié.')
            install_button.config(state='disabled')
            return None
    def change(action):
        if action == 'install':
            report = verify()
            if report is None or not report['can_install']:
                return
            prompt = 'Appliquer les 13 touches affichées ? Les autres commandes seront conservées et une sauvegarde sera créée.'
        else:
            prompt = 'Restaurer les commandes précédentes ? La restauration exige une sauvegarde correspondant exactement au profil actuel.'
        if not messagebox.askyesno('Confirmer', prompt, parent=root):
            return
        try:
            result = getattr(azerty, action)(Path(profile.get()), args.backups)
            verify()
            status.set(result)
        except Exception as error:
            messagebox.showerror('Opération interrompue', str(error), parent=root)
            verify()
    buttons = ttk.Frame(frame)
    buttons.pack(fill='x', pady=(14, 8))
    ttk.Button(buttons, text='Vérifier les touches', command=verify).pack(side='left')
    install_button = ttk.Button(buttons, text='Installer', state='disabled', command=lambda: change('install'))
    install_button.pack(side='left', padx=8)
    ttk.Button(buttons, text='Restaurer', command=lambda: change('restore')).pack(side='left')
    ttk.Button(buttons, text='Fermer', command=root.destroy).pack(side='right')
    ttk.Label(frame, text='Sauvegardes : ' + str(args.backups), wraplength=900).pack(anchor='w')
    root.mainloop()


if __name__ == '__main__':
    main()
