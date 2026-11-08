# Incursion Red River — Traduction française

Patch français non officiel pour **Incursion Red River 1.4.0.1** (build Steam **26487830**).

**Version : 0.1.1 bêta.** Le chargement du patch a été vérifié dans le journal du jeu. Les menus et les missions ont été testés et validés visuellement par le joueur le 8 novembre 2026. La correction des catégories du marchand a également été validée par le joueur. Une validation complète de toutes les situations de jeu reste à faire.

[Télécharger la version bêta](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.1.1-beta)

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

## Correction des catégories du marchand

Cette version traduit les catégories et sous-catégories du marchand : Munitions, Canon, Poignée avant, Conteneurs, etc. Une table de libellés dédiée est ajoutée, car ces noms étaient générés directement à partir des identifiants internes. Ces identifiants et le fonctionnement des filtres sont conservés.

L’onglet « Sécuriser le marché » devient « Marché officiel ».

## Contenu

- 6 670 entrées traitées, représentant 4 345 textes distincts.
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

Les traductions éditables sont dans [`translations/fr.csv`](translations/fr.csv), avec les noms de catégories dans [`translations/categories-fr.json`](translations/categories-fr.json). Conservez les identifiants de la colonne `key` et les variables comme `{count}` ou `{x}`, les balises comme `<Red>...</>`, les noms de fichiers et les commandes à saisir. Une modification du CSV nécessite une recompilation du patch pour apparaître en jeu.

Voir aussi les [contrôles effectués](docs/VALIDATION.md), les [notes de version](RELEASE_NOTES.md) et les [crédits](CREDITS.md).

Projet communautaire non officiel, sans affiliation avec les développeurs du jeu.
