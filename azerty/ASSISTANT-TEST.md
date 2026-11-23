# Assistant AZERTY 0.2.0 — TEST 1

Cette version ajoute une interface et un diagnostic au préréglage AZERTY déjà essayé en jeu. Les **13 touches sont identiques à la 0.1.0**. J’ai vérifié la fenêtre, le diagnostic, l’installation et la restauration sur une copie du profil. Les 13 touches restent celles déjà validées en jeu ; un nouvel essai en partie reste à faire.

## Installation et vérification

1. Installer une version maintenue de Python 3 avec Tkinter depuis [python.org](https://www.python.org/downloads/windows/), Python 3.11 ou plus récent conseillé.
2. Extraire tous les fichiers du ZIP dans un même dossier.
3. Ouvrir `AZERTY.cmd`, choisir **0 — Interface graphique**, puis **Vérifier les touches**.
4. Lire les touches actuelles, celles proposées, les commandes conservées et les conflits éventuels.
5. Fermer le jeu avant de cliquer sur **Installer**. Confirmer l’application des 13 touches ; une sauvegarde des commandes précédentes est créée.

Gardez Windows en français : Z/Q/S/D pour les déplacements, A/E pour se pencher, W pour les accessoires. Les raccourcis d’équipement utilisent **& é " ' ( - è _ ç sans Maj**. S/D/E restent les valeurs du jeu ou vos personnalisations. La saisie dans le terminal reste gérée par la disposition Windows.

**Restaurer** remet les commandes précédant l’installation de cet outil. L’outil exige une sauvegarde dont l’empreinte correspond au fichier actuel. Si le jeu a réécrit le profil, une restauration automatique peut être refusée pour conserver les personnalisations.

Fichier modifié : `%LOCALAPPDATA%/Test_C/Saved/SaveGames/EnhancedInputUserSettings.sav`. Sauvegardes : `%LOCALAPPDATA%/Test_C/AZERTY-Backups`.

## Après une mise à jour

Relancer **Vérifier les touches**. Le diagnostic indique les affectations réinitialisées, différentes ou absentes du fichier. Une affectation absente est une valeur implicite du jeu, pas la preuve qu’une touche ne fonctionne pas.

Ce fichier de préférences contient seulement les personnalisations. Il ne permet pas de découvrir toutes les nouvelles commandes, les valeurs par défaut ou la version installée du jeu. Le diagnostic précise cette limite. Le format UE 5.6 / profil unique reste exigé ; un format différent provoque un refus.

Commandes facultatives :

```text
py -3 azerty.py diagnose
py -3 azerty.py diagnose --json diagnostic-local.json
py -3 azerty.py install
py -3 azerty.py restore
```

`--profile` et `--backups` permettent de viser des copies de test. Le diagnostic exporté contient vos touches personnalisées : relisez-le avant de le partager. Aucun fichier .sav personnel n’est fourni.

[Guide Steam AZERTY](https://steamcommunity.com/sharedfiles/filedetails/?id=3844936408) · [Signaler un problème](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=azerty.md) · [Guide FR](https://steamcommunity.com/sharedfiles/filedetails/?id=3835740541)
