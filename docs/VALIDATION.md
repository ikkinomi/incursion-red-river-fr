# Audit du patch français pour Incursion Red River 1.4.0.2

Comparaison du build Steam **26596277** avec **26487830** et le patch français **0.1.6**. L’annonce officielle décrit le hotfix 1.4.0.2. [Notes de mise à jour Steam](https://steamcommunity.com/app/2116120/allnews/)

| Périmètre | Résultat |
| --- | --- |
| Archives du jeu | 26 archives indexées, couvrant 99 812 chemins distincts |
| Fichiers ciblés | 957 fichiers d’interface, de données, de carte ou de langue inspectés. 687 identiques, 21 modifiés et 1 nouveau. Pour 248 fichiers déjà présents dans l’ancienne version, seule la copie actuelle était disponible. |
| Ressource officielle anglaise | 6 746 entrées. 76 ajouts, 3 textes modifiés et aucune clé supprimée. |
| Nouveautés traduites | 56 textes de réglages IA, le message de piratage, une réplique de mission, les descriptions du Rattler et du MCX, la description de la pince et les nouveaux libellés d’interface. Les unités et noms de modèle appropriés sont conservés. |
| Inventaire | Deux textes « Provisions » trouvés en dehors de la ressource officielle ont été traduits par « Vivres ». |
| Audio et commandes | Les textes de volume des voix et les raccourcis rapides figuraient déjà dans la traduction. |
| Avertissement au démarrage | Formulation française reprise avec conservation de la variable qui affiche la liste des mods. |
| Cartes | 86 entrées de la 0.1.6 retrouvées dans les fichiers principaux de Quarry, Delta, Outskirts et Bunker. Les textes de carte détectés n’ont pas changé. |

## Adaptation des fichiers traduits

Sept composants ont été repris depuis la version actuelle du jeu. Il s’agit de l’inventaire, de la boîte de réception, de l’aperçu des missions et des quatre missions `0008x5`, `0020`, `0021` et `0022`. Au total, 91 champs de texte ont été réappliqués. Les données hors traduction des fichiers reconstruits ont été conservées et vérifiées octet par octet. L’ancien fichier de traduction du contrat de sabotage du brouilleur ADLER de Bunker a été retiré du patch, car son équivalent n’existe plus dans les archives actuelles.

## Contrôles et limites

Le patch compilé a été réextrait pour contrôler ses 539 fichiers. Les 6 834 entrées ont été relues depuis la ressource compilée et comparées à la table française. Les empreintes des sources de la 1.4.0.2 et des entrées ajoutées correspondent aux textes du jeu. Le CSV `Nouveaux_textes_FR.csv` contient les modifications de cette version.

La comparaison couvre les ressources de langue et les fichiers ciblés ci-dessus. Des textes peuvent aussi venir du code natif, d’images, d’éléments de carte distincts ou de services en ligne. Le joueur a confirmé le lancement et l’affichage en français sur la 0.1.7. La progression de chaque mission n’a pas été testée individuellement.

## Avertissement au démarrage

Le jeu détecte `pakchunk99-French_P.pak` comme un mod et peut afficher « Mods are installed » en anglais. La fenêtre signale les mods installés et rappelle que des mods conçus pour une version précédente peuvent provoquer un plantage. Si le jeu se lance normalement, fermez la fenêtre pour continuer. Le message peut revenir après une mise à jour du jeu ou un changement de mod.
