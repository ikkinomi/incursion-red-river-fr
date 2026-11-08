# Validation de la bêta 0.1.1

Cible : Incursion Red River 1.4.0.1, build Steam 26487830.

## Catégories du marchand

Les noms des catégories étaient construits directement à partir des identifiants internes, sans passer par la ressource de langue. Le widget de la liste consulte désormais une table de noms français. Les identifiants du jeu et les filtres sont conservés.

- 1 010 entrées dans la table dédiée, incluant tous les niveaux des catégories déclarées dans les fichiers examinés.
- Le contrôle de couverture ne détecte aucun segment de catégorie manquant.
- Le fichier du widget a été recompilé puis relu : les fonctions, leurs tailles et les données inchangées ont été contrôlées.
- Les branchements du widget ont été ajustés à l'ajout de la référence à la table.
- La table de catégories relue après compilation correspond aux traductions attendues.
- Le joueur a validé visuellement la correction le 8 novembre 2026.

## Ressource principale et archive

- 6 670 entrées dans la ressource principale ; 25 corrections supplémentaires de libellés dans cette version.
- L'archive contient la ressource principale, le widget du marchand et la table de catégories, soit cinq fichiers internes.
- Le patch préparé pour la publication correspond au patch installé.
- La version 0.1.0 avait déjà été validée sur les menus et les missions.

Tous les écrans, toutes les résolutions, toutes les missions et le multijoueur n'ont pas été testés de façon exhaustive. Les journaux complets et les données personnelles du joueur ne sont pas publiés.

Résultats détaillés et empreinte du patch : [validation.json](validation.json).
