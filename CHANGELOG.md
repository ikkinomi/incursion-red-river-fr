# En préparation — assistants TEST 1, 24 novembre 2026

- Contrôle réutilisable des traductions et comparaison avec le modèle anglais / une référence antérieure ; règles du glossaire exécutées automatiquement, rapport de longueurs et brouillon des textes à adapter.
- 28 propositions de libellés courts, pour 52 entrées, conservées hors des traductions actives en attendant le contrôle visuel.
- Assistant FR avec détection des bibliothèques Steam, aperçu, complément du marché facultatif soumis au build validé, sauvegarde et restauration contrôlée.
- Interface AZERTY et diagnostic des 13 affectations, conflits et autres commandes conservées. Les touches restent identiques à la 0.1.0.
- Essais automatiques et copies locales : voir les validations TEST1. L’affichage des fenêtres reste à confirmer sur le bureau du joueur ; aucune nouvelle publication à ce stade.

---

# Traduction française 0.2.1 bêta

Pour Incursion Red River 1.4.0.4 / build Steam 26761568.

- 240 entrées corrigées : Stock/Crosse selon le contexte, noms AK Star, Longbow, Paraclete Origin et Team Wendy, contrats FANG, terminal et descriptions d’équipement.
- 368 valeurs de la table du marché synchronisées, chemins composés compris ; les dix fichiers des widgets testés restent identiques.
- Glossaire et règles de conservation des noms ajoutés. Contrôles des 6 894 entrées : aucune erreur de structure, variable, balise ou identité ; 667 occurrences de noms protégés vérifiées.
- Installation et essai par le joueur : bon fonctionnement rapporté. Cela ne constitue pas un test exhaustif de tous les objets, missions ou transactions.

**Mettre à jour les deux composants**, jeu fermé : `fr/` dans `%LOCALAPPDATA%/Test_C/Saved/Translations`, puis le nouveau `pakchunk98-FrenchMarketTest_P.pak` dans `Test_C/Content/Paks` du jeu. Le nom du .pak est identique, son contenu a changé. Garder l’ancien pakchunk99 désactivé. Désactiver le complément du marché après une mise à jour du jeu jusqu’à nouvelle validation.

Le préréglage AZERTY est un [téléchargement séparé](https://github.com/ikkinomi/incursion-red-river-fr/releases/tag/azerty-v0.1.0-beta), facultatif et indépendant. Il n’est pas inclus dans ce ZIP.

[Installation](https://github.com/ikkinomi/incursion-red-river-fr#installation-ou-mise-à-jour) · [Signaler un bug ou une erreur de traduction](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=correction.md)

---

# Mise à jour du patch majeure

**0.2.0 bêta — Incursion Red River 1.4.0.4 / Steam 26761568 — 23 novembre 2026**

- Nouveau complément pour les catégories du marché, les feuilles d’objets, les filtres et les chemins de catégories.
- Traduction JSON de la 0.1.9 incluse, avec les corrections du terminal, de messages radio et de briefings.
- Installation revue : dossier `fr` dans `%LOCALAPPDATA%\Test_C\Saved\Translations`, puis complément `pakchunk98-FrenchMarketTest_P.pak` dans `Test_C/Content/Paks` du jeu.
- L’ancien `pakchunk99-French_P.pak` doit rester désactivé.
- Retour à l’anglais prévu pour un libellé inconnu ; noms propres et identifiants fonctionnels conservés.

**Premier essai concluant, confirmé par le joueur. Test approfondi à venir.** Le démarrage, les catégories, un filtre d’objet, sa fiche et la recherche de compatibilité ont été contrôlés. Les achats/ventes, le panier, le marché noir, la saisie dans la recherche, le changement de langue et tous les objets ne sont pas encore validés en jeu. Quelques formulations et textes longs restent à revoir.

**Après une mise à jour du jeu, désactivez le complément du marché jusqu’à nouvelle vérification de compatibilité.** Le dossier de traduction JSON est indépendant.

[Installation complète](https://github.com/ikkinomi/incursion-red-river-fr#installation-ou-mise-à-jour) · [Signaler un bug ou une erreur de traduction](https://github.com/ikkinomi/incursion-red-river-fr/issues/new?template=correction.md)

---

# 0.1.9 bêta — révision du 22 novembre 2026

1092 entrées modifiées ou ajoutées, dont 78 changements limités aux espaces et sauts de ligne. Modèle courant entièrement couvert. Relecture ciblée du terminal, des messages radio, des briefings et des noms propres. Les libellés construits hors localisation restent détaillés dans AUDIT.md.

Contrôles statiques réussis ; validation en jeu de cette révision à effectuer.

Prévue pour Incursion Red River 1.4.0.4, build Steam 26761568. Installation par le dossier `fr` dans `%LOCALAPPDATA%/Test_C/Saved/Translations`, jeu fermé. L’ancien `pakchunk99-French_P.pak` doit rester désactivé.

Certains textes des captures restent en anglais parce qu’ils sont générés hors localisation : inventaire, catégories du marché, titres de commandes, Joinability et RANDOM. Voir l’audit dans l’archive et le dépôt. Cette publication ne prétend pas les corriger.

---

# Version 0.1.8 bêta — jeu 1.4.0.4

**Installation différente des versions précédentes.** Désactivez d’abord `Test_C/Content/Paks/pakchunk99-French_P.pak`, puis copiez le dossier `fr` dans `%LOCALAPPDATA%/Test_C/Saved/Translations`. Choisissez **Français** dans les paramètres du jeu.

La traduction utilise maintenant le format JSON intégré au jeu. Elle comprend 6 773 textes du modèle courant et 96 entrées supplémentaires. Le rapport de chargement indique 0 erreur de formatage et 0 fichier illisible. 50 entrées nouvelles ou modifiées ont été prises en charge. Le lancement, le menu français et un essai en partie ont été confirmés.

25 libellés d’outils ou identifiants internes restent en anglais. Chaque mission et chaque écran restent à vérifier individuellement. Les réglages graphiques du PC de test ont aussi été ajustés après une erreur DirectX de plein écran. La désactivation de l’ancien patch et ce changement ont été appliqués ensemble pour rétablir le lancement.

La procédure complète est dans le README de l’archive et du dépôt.

---

# Version 0.1.7 bêta — compatibilité avec le hotfix 1.4.0.2

Pour **Incursion Red River 1.4.0.2**, build Steam **26596277**.

- 79 entrées nouvelles ou modifiées prises en charge, dont les réglages IA, une réplique de mission, le message de piratage et plusieurs descriptions d’objets.
- Deux libellés d’inventaire « Provisions » traduits par « Vivres ».
- Sept composants de l’inventaire et des missions repris depuis la mise à jour du jeu. Les 86 entrées des quatre cartes ont été vérifiées et les corrections précédentes sont incluses.
- 6 834 entrées compilées et 539 fichiers du patch contrôlés. Le joueur a confirmé le lancement et l’affichage de la traduction avec cette version.

Jeu fermé, copiez le dossier `Test_C` de l’archive dans le dossier du jeu et remplacez l’ancien fichier `pakchunk99-French_P.pak`. Gardez **English** ou **Français (patch)** comme langue.

## Avertissement au démarrage

Le jeu détecte `pakchunk99-French_P.pak` comme un mod et peut afficher « Mods are installed » en anglais. La fenêtre signale les mods installés et rappelle que des mods conçus pour une version précédente peuvent provoquer un plantage. Si le jeu se lance normalement, fermez la fenêtre pour continuer. Le message peut revenir après une mise à jour du jeu ou un changement de mod.

---

# Version 0.1.6 bêta — nom Discord

Pour **Incursion Red River 1.4.0.1**, build Steam **26487830**.

- Le bouton **Discord** du menu principal conserve le nom du service, au lieu de « Discorde ».
- Correction dans la ressource principale et dans le composant du menu principal.
- Toutes les corrections précédentes sont incluses.

Les 6 756 traductions compilées et leurs empreintes sources ont été vérifiées. Le menu principal a été reconstruit puis relu. Cette correction reste à vérifier visuellement en jeu.

## Installation

**Fermez le jeu avant de remplacer le patch.** Copiez le dossier `Test_C` de l'archive dans le dossier du jeu et remplacez uniquement l'ancien `pakchunk99-French_P.pak`. Gardez **English / Français (patch)** comme langue.

Pour désactiver, jeu fermé, renommez ce fichier en `pakchunk99-French_P.pak.disabled`.

---

# Version 0.1.5 bêta — boîte de munitions vide

Pour **Incursion Red River 1.4.0.1**, build Steam **26487830**.

- Le nom de l'objet **Empty Ammo Can** devient **Boîte de munitions vide**, à la place de « Vider la boîte munitions » : il décrit un objet vide, pas une action.
- Correction dans la ressource principale et dans la table de noms d'objets utilisée par le marchand.
- Les corrections précédentes, dont l'option **Boost** de **Nvidia Reflex**, sont incluses.

Les 6 756 entrées compilées et leurs empreintes sources ont été vérifiées. La table de noms a été reconstruite puis relue. Cette correction reste à vérifier visuellement en jeu.

## Installation

**Fermez le jeu avant de remplacer le patch.** Copiez le dossier `Test_C` de l'archive dans le dossier du jeu et remplacez uniquement l'ancien `pakchunk99-French_P.pak`. Gardez **English / Français (patch)** comme langue. Cette archive comprend les corrections précédentes.

Pour désactiver, jeu fermé, renommez ce fichier en `pakchunk99-French_P.pak.disabled`.

---

# Version 0.1.4 bêta — option NVIDIA Reflex

Pour **Incursion Red River 1.4.0.1**, build Steam **26487830**.

- L'option **Boost** de **Nvidia Reflex** conserve son appellation d'origine. La traduction incorrecte « Coup de pouce » a été supprimée de la ressource de langue et du menu graphique.
- Les corrections de la 0.1.3 sont incluses.

Les 6 756 entrées compilées et leurs empreintes sources ont été vérifiées. Le composant du menu graphique a été reconstruit puis relu. Cette correction n'a pas encore été vérifiée visuellement en jeu ; elle est publiée en bêta à la demande du joueur.

## Installation

**Fermez le jeu avant de remplacer le patch.** Copiez le dossier `Test_C` de l'archive dans le dossier du jeu et remplacez uniquement l'ancien `pakchunk99-French_P.pak`. Gardez **English / Français (patch)** comme langue. Cette archive comprend les corrections précédentes.

Pour désactiver, jeu fermé, renommez ce fichier en `pakchunk99-French_P.pak.disabled`.

---

# Version 0.1.3 bêta — équipement et dialogues des cartes

Pour **Incursion Red River 1.4.0.1**, build Steam **26487830**.

- Correction des libellés des emplacements d'équipement : casque, porte-plaques, gilet tactique, armes, jumelles, sac à dos et appareil.
- 49 répliques radio supplémentaires traduites manuellement, dont les introductions des cartes.
- 86 entrées ajoutées : dialogues et noms de lieux de Quarry, Delta, Outskirts et Bunker.
- Introduction de Quarry « Quarry is a riverside district… » incluse.
- Libellé du TactiNav raccourci : « Données satellite : OFF » pour l'état non chargé existant. Le fonctionnement du satellite est conservé.
- Corrections précédentes et titre **Incursion Red River** conservés.

Les contrôles des fichiers compilés ont réussi. Cette version est publiée à la demande du joueur ; elle reste une bêta et toutes les situations de jeu n'ont pas fait l'objet d'une validation visuelle exhaustive.

## Installation

Jeu fermé, copiez le dossier `Test_C` de l'archive dans le dossier du jeu et remplacez uniquement l'ancien `pakchunk99-French_P.pak`. Gardez **English / Français (patch)** comme langue. L'archive regroupe les corrections précédentes : aucun cumul de versions n'est nécessaire.

Pour désactiver, fermez le jeu et renommez uniquement ce fichier en `pakchunk99-French_P.pak.disabled`.

---

# Version 0.1.2 bêta — inventaire, sous-titres et textes intégrés

Pour **Incursion Red River 1.4.0.1**, build Steam **26487830**.

- Nom du jeu conservé : **Incursion Red River**.
- Traduction des titres et des emplacements de l'inventaire en raid.
- Traduction de l'avertissement sur l'emplacement permanent du TactiNav.
- 25 répliques de voix off relues manuellement et intégrées aux données des missions.
- Reprise de 2 613 champs de texte intégrés aux interfaces et aux missions, dont dix composants du TactiNav.
- Fonctions non concernées conservées à l'identique.
- Correctif des catégories du marchand de la 0.1.1 conservé.

Les fichiers compilés et le contenu de l'archive ont passé les contrôles. Cette version est publiée à la demande du joueur ; elle reste une bêta et toutes les situations de jeu n'ont pas fait l'objet d'une validation visuelle exhaustive.

## Installation

Jeu fermé, copiez le dossier `Test_C` de l'archive dans le dossier du jeu et remplacez uniquement l'ancien `pakchunk99-French_P.pak`. Gardez **English / Français (patch)** comme langue. L'archive regroupe les corrections précédentes : aucun cumul de versions n'est nécessaire.

Pour désactiver, fermez le jeu et renommez uniquement ce fichier en `pakchunk99-French_P.pak.disabled`.

---

# Version 0.1.1 bêta — catégories du marchand

Cible : Incursion Red River 1.4.0.1, build Steam 26487830.

- Traduction des catégories du marchand, dont Munitions, Cartouches, Accessoires, Canon, Poignée avant, Conteneurs, Troc et Matériel médical.
- Les catégories étaient affichées depuis des identifiants internes et ne passaient pas par le fichier de langue principal. Le widget lit maintenant une table française dédiée, en conservant les identifiants d'origine.
- Correction de « Sécuriser le marché » en « Marché officiel » dans l'onglet concerné.
- Correction de plusieurs termes d'accessoires dans la ressource de langue.

Les contrôles de compilation et de structure ont réussi. La correction des catégories a été validée visuellement par le joueur.

Installation : jeu fermé, remplacez uniquement l'ancienne archive `pakchunk99-French_P.pak` par celle de cette version. Conservez English / Français (patch) comme langue. Les archives d'origine et les sauvegardes ne sont pas remplacées.

## Version 0.1.0 bêta

Première traduction française pour la version 1.4.0.1 : menus et missions validés en jeu. Certaines catégories du marchand restaient en anglais et sont corrigées dans la version 0.1.1.
