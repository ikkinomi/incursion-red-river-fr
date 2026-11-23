# Audit de la traduction française 0.2.1 bêta

23 novembre 2026. Cible : Incursion Red River 1.4.0.4, build Steam 26761568.

## Résultat

Les **6 894 entrées des 36 JSON** ont été contrôlées structurellement et comparées au modèle anglais courant : **6 798 entrées du modèle et 96 supplémentaires**. La relecture sémantique est ciblée ; elle ne signifie pas que chaque longue description a été relue intégralement.

La copie contient **240 entrées corrigées**, pour **230 sources distinctes**. La table du marché comporte **368 valeurs modifiées, chemins composés compris** : ce ne sont pas autant de nouvelles phrases indépendantes.

## Corrections concrètes

- En-tête des quantités du marché : Stock, au lieu de Crosse. Les catégories et objets de type crosse restent correctement traduits par Crosse.
- Indicateur de disponibilité : Stock : 2/10. Le message sur les objets échangeables parle désormais du stock du marchand.
- Noms conservés : AK Star, QBZ-97 Longbow, Paraclete Origin, Team Wendy, National Match, noms du jeu et des cartes, Discord, NVIDIA Reflex et Boost.
- Objectifs FANG : contrats à accomplir pendant un raid, objectifs d’extraction et de livraison reformulés. Le tutoriel distingue missions scénarisées et contrats.
- Caméra de casque, vitesse initiale, descriptions de gilets, casques, crosses et accessoires : correction de contresens et de phrases mêlant français et anglais.
- Ajout d’un glossaire et de règles de contexte, notamment pour Stock, Star, Boost et Bunker. Les commandes du terminal et les noms de fichiers sont préservés.

## Contrôles passés

Aucune erreur sur les identifiants, sources, doublons, variables, balises, sauts de ligne et espaces aux extrémités. 667 occurrences de noms protégés vérifiées, ainsi que les commandes du terminal placées entre accents graves.

Le complément du marché a été reconstruit hors jeu avec la nouvelle table. Ses **10 fichiers de widgets sont identiques à ceux du complément testé** ; seuls les deux fichiers de la table sont régénérés. Les 12 fichiers empaquetés ont été extraits et comparés. **31674 cas passent dans le modèle des appels natifs sur les expressions existantes** ; cela ne remplace pas une exécution dans Unreal.

## Ce qui reste ouvert

- Les alertes des heuristiques ciblées ont été traitées. Cela ne certifie pas une relecture humaine exhaustive.
- 399 entrées avec forte expansion de longueur sont listées dans TEXTES-LONGS-A-VERIFIER.json. Sans affichage en jeu, ce sont des risques potentiels, pas des débordements constatés.
- En-têtes d’inventaire et d’équipement, titres de sections des commandes, Joinability et RANDOM : ce complément ne corrige pas ces zones. Elles nécessiteraient un chantier d’interface séparé.
- Marché noir, panier, achats/ventes, recherche au clavier et tous les écrans restent à vérifier en jeu.

## Situation et suite

La relecture a été préparée hors jeu, puis installée à la demande du joueur. Il rapporte que la traduction fonctionne. Le problème de rangée numérique concernait le profil AZERTY séparé et a été corrigé avant son essai positif. Les contrôles techniques ne prouvent pas une couverture exhaustive en jeu.

Les achats/ventes, le marché noir, tous les écrans et la lisibilité complète restent à approfondir. Voir le README pour l’installation, les sauvegardes et le retour arrière.
