# Incursion Red River — Traduction française

Traduction communautaire pour **Incursion Red River 1.4.0.4**, build Steam **26761568**.

**Version 0.1.8 bêta.** Le démarrage et le menu français ont été vérifiés. Le joueur a également confirmé le fonctionnement lors de son essai en partie.

[Télécharger la 0.1.8 bêta](https://github.com/ikkinomi/incursion-red-river-fr/releases/download/v0.1.8-beta/Incursion_Red_River_FR_1.4.0.4_v0.1.8-beta.zip) · [Voir la publication](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/v0.1.8-beta)

## Migration depuis la 0.1.7 et les versions précédentes

**Fermez le jeu et désactivez l’ancien patch avant d’installer la 0.1.8.**

1. Dans Steam, ouvrez **Incursion Red River → Propriétés → Fichiers installés → Parcourir**.
2. Ouvrez `Test_C/Content/Paks`.
3. Renommez uniquement `pakchunk99-French_P.pak` en `pakchunk99-French_P.pak.disabled`, ou déplacez ce fichier dans un dossier de sauvegarde hors du jeu.
4. Installez ensuite le dossier `fr` selon les étapes ci-dessous.

L’ancien patch remplaçait des composants du jeu prévus pour une version antérieure. La 0.1.8 utilise le système de langues communautaires intégré au jeu depuis les derniers hotfixes.

## Installation de la 0.1.8

1. Lancez le jeu une fois pour qu’il crée son dossier de traductions, puis fermez-le.
2. Téléchargez et extrayez le ZIP ci-dessus.
3. Appuyez sur **Windows + R**, saisissez `%LOCALAPPDATA%\Test_C\Saved\Translations`, puis validez.
4. Copiez le dossier **`fr`** de l’archive dans ce dossier. Le résultat doit être `Translations/fr/fr_001.json`, avec les autres fichiers JSON à côté.
5. Lancez le jeu et choisissez **Français** dans **Paramètres → Langue**. L’ancien choix **English / Français (patch)** concernait les versions précédentes.

Lors d’une prochaine mise à jour de la traduction, jeu fermé, remplacez les fichiers de votre dossier `fr` avec ceux de la nouvelle archive.

## Nouveautés et validation

- Migration vers le format JSON pris en charge par le jeu.
- 6 773 textes du modèle courant chargés et 96 entrées supplémentaires acceptées par le moteur.
- 50 entrées nouvelles ou modifiées prises en charge, notamment les annonces de ressources, les invites des coffres et « Récupérer » les récompenses.
- Le rapport du jeu indique **0 erreur de formatage et 0 fichier illisible**.
- 25 libellés d’outils d’édition ou identifiants internes restent en anglais.

Les traductions des noms propres et les corrections précédentes, dont **Discord**, **NVIDIA Reflex / Boost** et **Boîte de munitions vide**, sont reprises lorsqu’elles correspondent aux sources actuelles. Des maladresses ou textes absents du modèle peuvent subsister. Chaque mission et chaque écran n’ont pas été testés individuellement.

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
