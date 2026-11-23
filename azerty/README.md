# Incursion Red River — Préréglage AZERTY 0.1.0 bêta

Ce complément permet de jouer avec ZQSD et les touches de la rangée française, tout en gardant Windows en français pour écrire dans le terminal de hack. Les déplacements, le terminal et les raccourcis d’équipement ont été essayés par le joueur, qui confirme leur fonctionnement.

**Pour Windows et un clavier AZERTY français classique. Vérifié sur Incursion Red River 1.4.0.4 / build 26761568.** Les dispositions belge ou française normalisée récente peuvent avoir une rangée différente.

Il fonctionne indépendamment de la traduction française. [Téléchargement AZERTY](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/azerty-v0.1.0-beta) · [Traduction française](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.2.1-beta) · [Signaler un bug](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=azerty.md)

## Guides Steam

[Guide de la traduction FR](https://steamcommunity.com/sharedfiles/filedetails/?id=3835740541) · [Guide du préréglage AZERTY](https://steamcommunity.com/sharedfiles/filedetails/?id=3844936408)

Les deux compléments sont indépendants et disposent chacun de leur téléchargement et de leur formulaire de signalement.

## Fonctionnement

L’outil fusionne 13 affectations avec le fichier personnel `EnhancedInputUserSettings.sav`, jeu fermé. Il ne remplace pas votre profil par celui d’un autre joueur. Il conserve les autres personnalisations, y compris les entrées manette ; les 13 actions du préréglage prennent les touches indiquées ci-dessous.

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

## Installation

1. Installer une version maintenue de **Python 3** pour Windows (Python 3.11 ou plus récent conseillé), depuis [python.org](https://www.python.org/downloads/windows/). Aucune bibliothèque supplémentaire n’est nécessaire.
2. Fermer Incursion Red River. Si aucun profil n’existe encore, lancer le jeu une fois, enregistrer une affectation dans les paramètres, puis le fermer.
3. Télécharger le ZIP **AZERTY**, puis extraire **tous** ses fichiers dans un dossier, en les gardant ensemble.
4. Ouvrir `AZERTY.cmd`. Choisir **1** pour l’aperçu, puis relancer et choisir **2** pour installer. Si une erreur apparaît, le texte explique le blocage.
5. Garder Windows en français, lancer le jeu et tester ZQSD, A/E, W, les neuf raccourcis, puis la saisie d’une commande habituelle au terminal.

Alternative depuis un terminal ouvert dans le dossier extrait : `py -3 azerty.py preview`, puis `py -3 azerty.py install`. Avec une installation sans lanceur py, utiliser `python` à sa place. Aucune exécution en administrateur ni modification de la politique PowerShell n’est demandée.

Le seul fichier modifié est `%LOCALAPPDATA%/Test_C/Saved/SaveGames/EnhancedInputUserSettings.sav`. Le jeu doit être fermé. Les sauvegardes des commandes sont stockées dans `%LOCALAPPDATA%/Test_C/AZERTY-Backups`, en dehors des sauvegardes Steam du jeu.

L’outil s’arrête si le format n’est pas pris en charge, si plusieurs profils sont détectés, si le jeu est ouvert ou si une autre action personnalisée utilise déjà une des touches réservées. Dans ce dernier cas, résoudre le conflit dans les paramètres du jeu, fermer le jeu et réessayer. Une installation répétée sur un profil déjà configuré n’ajoute pas de doublons.

## Retour arrière

Fermer le jeu, ouvrir `AZERTY.cmd` et choisir **3**, ou exécuter `py -3 azerty.py restore`. L’outil restaure la sauvegarde correspondant au profil installé et vérifie ses empreintes.

Si le jeu a réécrit le fichier ou si vous avez changé des commandes, la restauration automatique peut refuser pour éviter d’écraser vos modifications. Les sauvegardes restent disponibles : conserver une copie du profil actuel, puis copier la sauvegarde `.sav` voulue depuis AZERTY-Backups vers le dossier SaveGames, sous le nom **EnhancedInputUserSettings.sav**, jeu fermé. Le fichier JSON voisin indique les empreintes et le profil concerné.

Ce retour arrière remet les commandes qui précédaient l’installation de cet outil. Il ne supprime pas des personnalisations AZERTY que vous aviez déjà réalisées avant son utilisation.

## Limites et vérifications

Le profil a été testé en jeu sur une configuration. L’outil public reproduit octet pour octet le profil validé et a passé sept tests, dont installation/restauration sur copies, conservation d’autres commandes et de la manette, refus de conflits, fichiers tronqués et formats non pris en charge. Cela ne garantit pas toutes les configurations Windows.

Pas d’injecteur, de DLL, de macro, de programme résident ni de modification des archives ou de l’exécutable du jeu. Python ne sert qu’à lire et écrire les préférences, puis se ferme. Aucune certification par un fournisseur d’anticheat n’est revendiquée.

Pour un signalement, préciser la version du jeu, le message de l’outil, la disposition Windows et la touche physique concernée. **Ne pas joindre vos sauvegardes complètes.** [Formulaire direct de bug ou de correction](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=azerty.md)

Projet communautaire non officiel.
