"""Fenêtre de l’installateur FR ; rien n’est écrit avant aperçu et confirmation."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from installation import fr_manager as manager


def launch(args):
    root = tk.Tk()
    root.title('Incursion Red River — Assistant traduction FR 0.2.2 bêta')
    root.geometry('980x750')
    root.minsize(780, 650)
    frame = ttk.Frame(root, padding=18)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='Installer la traduction française', font=('Segoe UI', 19, 'bold')).pack(anchor='w')
    ttk.Label(frame, text='Vérifiez les destinations, consultez l’aperçu, puis installez avec le jeu fermé.').pack(anchor='w', pady=(5, 12))
    games = manager.detect_games() if args.game is None else []
    game = tk.StringVar(value=str(args.game or (games[0] if len(games) == 1 else '')))
    target = tk.StringVar(value=str(args.translations))
    def field(label, variable):
        ttk.Label(frame, text=label).pack(anchor='w')
        line = ttk.Frame(frame)
        line.pack(fill='x', pady=(2, 10))
        ttk.Entry(line, textvariable=variable).pack(side='left', fill='x', expand=True)
        def choose():
            value = filedialog.askdirectory(title=label)
            if value:
                variable.set(value)
        ttk.Button(line, text='Parcourir…', command=choose).pack(side='left', padx=(8, 0))
    field('Dossier du jeu (PROJECT QUARANTINE)', game)
    field('Dossier Translations dans les données Windows', target)
    market = tk.BooleanVar(value=args.market)
    ttk.Checkbutton(frame, text='Ajouter le complément du marché (facultatif, build compatible exigé)', variable=market).pack(anchor='w')
    status = tk.StringVar(value='Aucun fichier modifié. Le complément du marché est facultatif.')
    ttk.Label(frame, textvariable=status, wraplength=920).pack(anchor='w', pady=10)
    text = tk.Text(frame, wrap='word', font=('Consolas', 10), padx=10, pady=8)
    text.pack(fill='both', expand=True)
    previewed = {'plan': None}
    def render(value):
        text.config(state='normal')
        text.delete('1.0', 'end')
        text.insert('1.0', value)
        text.config(state='disabled')
    def invalidate(*_):
        previewed['plan'] = None
        install_button.config(state='disabled')
        status.set('Destinations modifiées : relancez Vérifier avant l’installation.')
    def verify():
        try:
            plan = manager.plan_install(args.source, Path(target.get()), Path(game.get()) if game.get() else None, market.get())
            previewed['plan'] = plan
            render(manager.describe(plan))
            install_button.config(state='normal' if plan['operations'] else 'disabled')
            status.set(f"Aperçu : {len(plan['operations'])} fichier(s) à modifier. Sauvegarde avant toute copie.")
        except Exception as error:
            invalidate()
            render(str(error))
            status.set('Vérification interrompue. Aucun fichier modifié.')
    def install():
        plan = previewed['plan']
        if not plan:
            return
        if not messagebox.askyesno('Installer la traduction', 'Appliquer les changements de l’aperçu ? Une sauvegarde des fichiers précédents sera créée.', parent=root):
            return
        try:
            backup = manager.apply_plan(plan, args.backups)
            invalidate()
            status.set('Installation terminée. Sauvegarde : ' + str(backup))
        except Exception as error:
            messagebox.showerror('Installation interrompue', str(error), parent=root)
            invalidate()
    def restore():
        selected = filedialog.askdirectory(title='Choisir un dossier de transaction FR', initialdir=str(args.backups))
        if not selected:
            return
        if not messagebox.askyesno('Restaurer', 'Restaurer les fichiers précédents de cette transaction ? Les fichiers modifiés depuis son installation seront protégés.', parent=root):
            return
        try:
            recovery = manager.restore(Path(selected))
            invalidate()
            status.set('Restauration terminée. Sauvegarde de retour : ' + str(recovery))
        except Exception as error:
            messagebox.showerror('Restauration interrompue', str(error), parent=root)
    buttons = ttk.Frame(frame)
    buttons.pack(fill='x', pady=12)
    ttk.Button(buttons, text='Vérifier et afficher l’aperçu', command=verify).pack(side='left')
    install_button = ttk.Button(buttons, text='Installer', state='disabled', command=install)
    install_button.pack(side='left', padx=8)
    ttk.Button(buttons, text='Restaurer une sauvegarde', command=restore).pack(side='left')
    ttk.Button(buttons, text='Fermer', command=root.destroy).pack(side='right')
    ttk.Label(frame, text='Sauvegardes : ' + str(args.backups), wraplength=920).pack(anchor='w')
    for variable in (game, target, market):
        variable.trace_add('write', invalidate)
    root.mainloop()
