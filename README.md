# Incursion Red River — Traduction française

Traduction communautaire pour **Incursion Red River 1.4.0.4**, build Steam **26761568**.

**Version 0.1.9 bêta.** Audit et corrections du 22 novembre 2026. Les contrôles statiques des fichiers sont réussis ; la validation en jeu de cette révision reste à effectuer. Le test en partie précédemment confirmé concernait la 0.1.8.

[Télécharger la 0.1.9 bêta](https://github.com/ikkinomi/incursion-red-river-fr/releases/download/v0.1.9-beta/Incursion_Red_River_FR_1.4.0.4_v0.1.9-beta.zip) · [Voir la publication](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.1.9-beta)

## Migration depuis la 0.1.7 et les versions précédentes

**Fermez le jeu et désactivez l’ancien patch avant d’installer la 0.1.9.**

1. Dans Steam, ouvrez **Incursion Red River → Propriétés → Fichiers installés → Parcourir**.
2. Ouvrez `Test_C/Content/Paks`.
3. Renommez uniquement `pakchunk99-French_P.pak` en `pakchunk99-French_P.pak.disabled`, ou déplacez ce fichier dans un dossier de sauvegarde hors du jeu.
4. Installez ensuite le dossier `fr` selon les étapes ci-dessous.

L’ancien patch remplaçait des composants du jeu prévus pour une version antérieure. La 0.1.9 utilise le système de langues communautaires intégré au jeu depuis les derniers hotfixes.

## Installation de la 0.1.9

1. Lancez le jeu une fois pour qu’il crée son dossier de traductions, puis fermez-le.
2. Téléchargez et extrayez le ZIP ci-dessus.
3. Appuyez sur **Windows + R**, saisissez `%LOCALAPPDATA%\Test_C\Saved\Translations`, puis validez.
4. Copiez le dossier **`fr`** de l’archive dans ce dossier. Le résultat doit être `Translations/fr/fr_001.json`, avec les autres fichiers JSON à côté.
5. Lancez le jeu et choisissez **Français** dans **Paramètres → Langue**. L’ancien choix **English / Français (patch)** concernait les versions précédentes.

Lors d’une prochaine mise à jour de la traduction, jeu fermé, remplacez les fichiers de votre dossier `fr` avec ceux de la nouvelle archive.

## Nouveautés et validation

- 6 894 entrées : les 6 798 textes du modèle courant et 96 entrées supplémentaires.
- 1 092 entrées modifiées ou ajoutées, dont 78 changements limités aux espaces et sauts de ligne.
- Corrections du terminal, des messages radio récurrents, de plusieurs briefings et de libellés mal traduits.
- Noms du jeu, des cartes, des personnages et des marques préservés, notamment Discord et NVIDIA Reflex / Boost.
- Les 25 textes internes auparavant manquants sont couverts ; ils ne correspondent pas à 25 nouveautés de gameplay.
- Contrôles des identifiants, sources, doublons, variables, balises, sauts de ligne et noms propres réussis.

**Limites connues :** les en-têtes d’inventaire, certaines catégories dynamiques du marché, des titres de commandes, « Joinability » et « RANDOM » sont construits hors du système de localisation. Les JSON seuls ne peuvent pas les corriger. Aucun ancien .pak n’est réactivé.

Cette bêta n’a pas encore été testée en jeu. Le rapport sans erreur de la 0.1.8 ne vaut pas validation de la 0.1.9. La relecture sémantique est ciblée ; chaque longue description, chaque mission et chaque écran n’ont pas été validés individuellement. [Audit détaillé et diagnostic des textes bloqués](docs/AUDIT-0.1.9.md).

## Si le jeu plante au démarrage

Vérifiez d’abord que l’ancien `pakchunk99-French_P.pak` est désactivé. Un essai sur le PC de test a également révélé une erreur DirectX `DXGI_ERROR_INVALID_CALL` en plein écran à 3440 × 1440. Un démarrage en mode fenêtré a permis d’atteindre le menu. Ce résultat concerne la configuration testée et ne constitue pas une correction universelle de tous les plantages.

Si Steam signale des fichiers corrompus, utilisez **Propriétés → Fichiers installés → Vérifier l’intégrité des fichiers du jeu**.

## Désactivation et diagnostic de la traduction

Choisissez une autre langue dans les paramètres. Pour retirer la traduction, jeu fermé, déplacez le dossier `fr` hors de `Translations`.

Le jeu écrit `_Report.txt` et `_Todo_*.json` dans le dossier de langue. Ces fichiers indiquent les textes chargés, manquants ou à adapter après une mise à jour. Les fichiers commençant par `_` sont des rapports générés par le jeu.

## Signaler une correction

Indiquez la version du jeu, le texte concerné et, si possible, une capture. [Signaler un problème](https://github.com/ikkinomi/incursion-red-river-fr/issues)

Les fichiers éditables actuels se trouvent dans [`translations/fr`](translations/fr). Conservez `ns`, `key`, `source`, les variables et les balises. Modifiez le champ `text`, puis changez de langue et revenez au français pour recharger les traductions. Les anciens CSV restent disponibles comme références historiques.

[Validation](docs/VALIDATION.md) · [Historique](CHANGELOG.md) · [Crédits](CREDITS.md)

Projet communautaire non officiel.
