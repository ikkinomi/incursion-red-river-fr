# Incursion Red River — Traduction française

Patch français non officiel pour **Incursion Red River 1.4.0.1** (build Steam **26487830**).

**Version : 0.1.6 bêta.** Le bouton **Discord** du menu principal conserve son nom d'origine. Les corrections précédentes sont incluses. Contrôles des fichiers compilés réussis ; affichage à confirmer en jeu.

[Télécharger la version bêta](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.1.6-beta)

## Installation

1. Fermez le jeu.
2. Téléchargez l'archive ZIP attachée à la version ci-dessus et extrayez-la.
3. Dans Steam : **Incursion Red River → Propriétés → Fichiers installés → Parcourir**.
4. Copiez le dossier `Test_C` de l'archive dans le dossier d'installation du jeu, généralement nommé `PROJECT QUARANTINE`.
5. Vérifiez la présence de ce seul fichier ajouté :

   ```text
   PROJECT QUARANTINE/
   └── Test_C/
       └── Content/
           └── Paks/
               └── pakchunk99-French_P.pak
   ```

6. Lancez le jeu. Gardez **English** ou **Français (patch)** dans le réglage de langue : le patch utilise l'emplacement anglais.

Aucun injecteur ni UE4SS n'est nécessaire. L'installation ajoute une archive de traduction séparée, sans remplacer les archives originales et sans modifier les sauvegardes.

## Désactivation

Jeu fermé, renommez `pakchunk99-French_P.pak` en `pakchunk99-French_P.pak.disabled`. Pour réactiver la traduction, remettez son nom d'origine.

Vous pouvez aussi retirer uniquement ce fichier du dossier `Paks`.

## Correction 0.1.6

Le bouton **Discord** du menu principal conserve le nom du service au lieu de « Discorde ».

## Correction 0.1.5

Le nom de l'objet **Empty Ammo Can** devient **Boîte de munitions vide**, dans la ressource principale et dans la table de noms d'objets.

## Correction 0.1.4

L'option **Boost** de **Nvidia Reflex** conserve son nom d'origine dans la ressource de langue et dans le menu graphique. Elle n'est plus affichée comme « Coup de pouce ».

## Corrections 0.1.3

- Libellés des emplacements d'équipement traduits dans leur composant d'affichage, avec conservation des identifiants et des noms de modèles.
- 49 répliques radio supplémentaires traduites manuellement, dont l'introduction de Quarry.
- 86 entrées ajoutées pour Quarry, Delta, Outskirts et Bunker, portant la ressource principale à 6 756 entrées.
- TactiNav : « Données satellite : OFF » pour l'état non chargé existant, sans modification de la logique du satellite.
- Correctifs précédents conservés et titre **Incursion Red River** inchangé.

## Corrections 0.1.2

- Le titre du jeu reste **Incursion Red River**.
- Titres et emplacements de l'inventaire en raid traduits.
- Avertissement sur l'emplacement permanent du TactiNav traduit à l'affichage.
- 25 répliques de voix off identifiées, relues manuellement et intégrées aux données des missions.
- Textes intégrés des interfaces et des missions repris, dont dix composants du TactiNav.
- Fonctions qui ne nécessitent aucun changement conservées à l'identique.
- Correctif des catégories du marchand de la 0.1.1 conservé.

Les fichiers reconstruits ont été relus pour contrôler leur contenu, les instructions modifiées et les traductions attendues. Cette version reste une bêta : le résultat de chaque sous-titre, écran ou situation doit encore être confirmé en jeu.

## Correction des catégories du marchand

Cette version traduit les catégories et sous-catégories du marchand : Munitions, Canon, Poignée avant, Conteneurs, etc. Une table de libellés dédiée est ajoutée, car ces noms étaient générés directement à partir des identifiants internes. Ces identifiants et le fonctionnement des filtres sont conservés.

L’onglet « Sécuriser le marché » devient « Marché officiel ».

## Contenu

- 6 756 entrées dans la ressource principale, dont 86 entrées supplémentaires issues des cartes.
- Traduction automatique locale comme base de travail.
- 1 383 textes distincts corrigés manuellement, principalement les menus, actions, soins, objectifs courts, tutoriels et réglages.
- Lexique contrôlé pour les composants d'armes.
- Variables, balises et noms de fichiers vérifiés après compilation.

Les noms de marques, modèles, identifiants et commandes à saisir dans les terminaux sont conservés quand nécessaire. Les voix ne sont pas doublées.

## Limites connues

C'est une première bêta. Les longs briefings et certaines descriptions n'ont pas tous été relus intégralement : des maladresses ou approximations peuvent subsister. Des textes codés en dur, contenus dans des images ou provenant d'autres ressources peuvent rester en anglais. Tous les écrans, toutes les résolutions et le multijoueur n'ont pas été validés.

La compatibilité est établie pour la version 1.4.0.1 citée ci-dessus. Après une mise à jour du jeu, de nouveaux textes ou des textes modifiés peuvent rester en anglais. Désactivez le patch si vous constatez un problème.

## Signaler une correction

Ouvrez une [issue](https://github.com/ikkinomi/incursion-red-river-fr/issues) en indiquant la version du jeu, l'écran concerné, le texte observé et la correction proposée. Une capture aide à repérer un texte coupé ou mal placé.

Les traductions éditables sont dans [`translations/fr.csv`](translations/fr.csv), avec les noms de catégories dans [`translations/categories-fr.json`](translations/categories-fr.json) et les répliques relues dans [`translations/subtitles-fr.json`](translations/subtitles-fr.json). Conservez les identifiants de la colonne `key` et les variables comme `{count}` ou `{x}`, les balises comme `<Red>...</>`, les noms de fichiers et les commandes à saisir. Les ajouts issus des cartes sont aussi disponibles dans [`translations/map-texts-fr.csv`](translations/map-texts-fr.csv). Une modification du CSV nécessite une recompilation du patch pour apparaître en jeu.

Voir aussi les [contrôles effectués](docs/VALIDATION.md), les [notes de version](RELEASE_NOTES.md) et les [crédits](CREDITS.md).

Projet communautaire non officiel, sans affiliation avec les développeurs du jeu.
