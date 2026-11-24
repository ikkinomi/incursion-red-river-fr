# Incursion Red River — Préréglage AZERTY 0.3.0 bêta

La 0.3.0 ajoute un assistant Windows autonome, trois choix de touches et un contrôle local après mise à jour. Le choix complet conserve les 13 affectations de la 0.1.0 déjà testée en jeu. Les modes partiels ont été vérifiés sur copies ; ils restent à essayer en partie.

Ce complément permet de jouer avec ZQSD et les touches de la rangée française, tout en gardant Windows en français pour écrire dans le terminal de hack. J’ai testé les déplacements, la saisie au terminal et les raccourcis d’équipement : tout fonctionne bien sur ma configuration.

**Pour Windows et un clavier AZERTY français classique. Vérifié sur Incursion Red River 1.4.0.4 / build 26761568.** Les dispositions belge ou française normalisée récente peuvent avoir une rangée différente.

Il fonctionne indépendamment de la traduction française. [Téléchargement AZERTY](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/azerty-v0.3.0-beta) · [Traduction française](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.3.0-beta) · [Signaler un bug](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=azerty.md)

## Guides Steam

[Guide de la traduction FR](https://steamcommunity.com/sharedfiles/filedetails/?id=3835740541) · [Guide du préréglage AZERTY](https://steamcommunity.com/sharedfiles/filedetails/?id=3844936408)

Les deux compléments sont indépendants et disposent chacun de leur téléchargement et de leur formulaire de signalement.

## Fonctionnement

Selon le groupe choisi, l’outil fusionne 4, 9 ou 13 affectations avec le fichier personnel `EnhancedInputUserSettings.sav`, jeu fermé. Il ne remplace pas votre profil par celui d’un autre joueur. Il conserve les autres personnalisations, y compris les entrées manette ; seules les actions du groupe choisi prennent les touches indiquées ci-dessous.

Il n’agit pas sur les caractères saisis dans le terminal. **Gardez la disposition Windows en français.** Le nom interne du profil reste Default Profile ; aucun bouton AZERTY n’est ajouté au menu.

| Action | Touche |
|---|---|
| Avancer / gauche / reculer / droite | Z / Q / S / D |
| Se pencher à gauche / droite | A / E |
| Faire défiler les accessoires tactiques | W |
| Arme principale / secondaire / arme de poing | & / é / " |
| TactiNav / équipement spécial | ' / ( |
| Emplacements rapides 1 à 4 | - / è / _ / ç |

Les touches de la rangée du haut s’utilisent **sans Maj**. S, D et E restent les valeurs d’origine ; le préréglage ne les écrase pas si vous les aviez personnalisées. La touche C, la touche 0 et le pavé numérique ne sont pas modifiés.

## Méthode A — Assistant Windows, sans Python à installer

1. Fermez le jeu. Si le profil de commandes n’existe pas encore, lancez le jeu une fois, enregistrez une affectation, puis fermez-le.
2. Téléchargez le ZIP **AZERTY**, extrayez **tous** ses fichiers ensemble, puis ouvrez **AZERTY.exe**. Gardez `preset.json` à côté de l’exécutable.
3. Vérifiez le profil proposé pour votre compte Windows. **Parcourir…** permet d’en choisir un autre ou une copie.
4. Choisissez **Les deux groupes (13 touches)**, **Déplacements et actions (4)**, ou **Rangée d’équipement (9)**. Un choix partiel conserve les personnalisations de l’autre groupe.
5. Cliquez sur **Vérifier les touches**, lisez les changements, puis sur **Installer** et confirmez. Si les touches sélectionnées sont déjà correctes, Installer reste désactivé.
6. Gardez Windows en français, lancez le jeu vous-même et testez les commandes et la saisie dans le terminal.

Le groupe déplacements/actions applique Z, Q, A et W. S, D et E restent leurs valeurs actuelles : ils ne font pas partie des quatre modifications. Le groupe équipement applique uniquement les neuf touches de la rangée du haut, sans Maj.

Le seul fichier modifié est `%LOCALAPPDATA%/Test_C/Saved/SaveGames/EnhancedInputUserSettings.sav`. Une sauvegarde est créée avant modification dans `%LOCALAPPDATA%/Test_C/AZERTY-Backups`.

Le jeu doit être fermé. L’outil refuse un format non pris en charge, plusieurs profils, un doublon ou un conflit avec une autre commande personnalisée. Résolvez le conflit dans le jeu et fermez-le avant de réessayer. Une nouvelle application n’ajoute pas de doublons.

![Assistant AZERTY dans un dossier de démonstration](../docs/images/assistant-azerty-installation.jpg)

## Méthode B — Réglage manuel dans le jeu

Vous pouvez régler les commandes vous-même, sans lancer l’outil ni installer Python. Gardez Windows en français et reprenez le tableau des touches dans les paramètres des commandes du jeu. Déplacez d’abord une action qui occupe déjà une touche voulue.

**Je n’ai pas vérifié la capture de chaque caractère français dans le menu d’affectation.** Si une touche de la rangée française est refusée ou ne fonctionne pas en partie, utilisez le préréglage de l’outil : ses neuf raccourcis ont été essayés en jeu. Le fichier .sav est binaire ; ne l’ouvrez pas dans un éditeur de texte pour changer les touches.

## Variante Python et ligne de commande

Les scripts restent disponibles avec Python 3 et Tcl/Tk pour la fenêtre. Depuis le dossier extrait : `py -3 interface.py` pour l’interface, ou `py -3 azerty.py preview --mode all`, puis `py -3 azerty.py install --mode all`. Les choix de mode sont `all`, `movement` et `equipment`. Utilisez d’abord l’aperçu ; la commande install applique directement les changements. Ce mode nécessite Python et ne correspond pas au réglage manuel dans le jeu.

`py -3 azerty.py diagnose --mode all --json diagnostic-local.json` exporte les touches personnalisées. Relisez le rapport avant de le partager. Aucune sauvegarde personnelle n’est fournie dans le ZIP.

## Retour arrière

Fermer le jeu et utiliser le bouton **Restaurer** de l’interface, exécuter `py -3 azerty.py restore`. L’outil restaure la sauvegarde correspondant au profil installé et vérifie ses empreintes.

Si le jeu a réécrit le fichier ou si vous avez changé des commandes, la restauration automatique peut refuser pour éviter d’écraser vos modifications. Les sauvegardes restent disponibles : conserver une copie du profil actuel, puis copier la sauvegarde `.sav` voulue depuis AZERTY-Backups vers le dossier SaveGames, sous le nom **EnhancedInputUserSettings.sav**, jeu fermé. Le fichier JSON voisin indique les empreintes et le profil concerné.

Ce retour arrière remet les commandes qui précédaient l’installation de cet outil. Il ne supprime pas des personnalisations AZERTY que vous aviez déjà réalisées avant son utilisation.

## Limites et vérifications

J’ai testé ce profil en jeu sur ma configuration. L’outil public reproduit octet pour octet le profil validé et a passé sept tests, dont installation/restauration sur copies, conservation d’autres commandes et de la manette, refus de conflits, fichiers tronqués et formats non pris en charge. Cela ne garantit pas toutes les configurations Windows.

Pas d’injection de DLL, de macro ou de programme résident ni de modification des archives ou de l’exécutable du jeu. Python ne sert qu’à lire et écrire les préférences, puis se ferme. Aucune certification par un fournisseur d’anticheat n’est revendiquée.

Pour un signalement, préciser la version du jeu, le message de l’outil, la disposition Windows et la touche physique concernée. **Ne pas joindre vos sauvegardes complètes.** [Formulaire direct de bug ou de correction](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=azerty.md)

Projet communautaire non officiel.

## Après une mise à jour du jeu

Cliquez sur **Contrôler après une mise à jour** : le bouton relit le profil et compare le build Steam local au build vérifié. Il ne lance pas le jeu, ne télécharge rien et ne modifie aucune touche. Un nouveau build appelle une vérification supplémentaire, même si le fichier reste lisible. En cas de plusieurs installations, le build est indiqué non vérifié ; les commandes Python acceptent `--game` pour préciser le dossier.

Une action absente du .sav est une valeur implicite du jeu. Ce fichier ne permet pas de découvrir toutes les nouvelles commandes ni leurs valeurs par défaut. Le format et les conflits personnalisés restent contrôlés avant toute installation.

![Restauration AZERTY dans un dossier de démonstration](../docs/images/assistant-azerty-restauration.jpg)

Les captures montrent des copies de test. Aucun nom de compte Windows ou chemin personnel n’y est affiché.
