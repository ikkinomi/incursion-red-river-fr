# Complément du marché — 0.2.0 bêta

Date : **23 novembre 2026**. Jeu **1.4.0.4**, build Steam **26761568**.

## Contenu

- 36 fichiers JSON, 6 894 entrées : 6 798 textes du modèle du jeu et 96 entrées supplémentaires. Leur contenu reprend la 0.1.9.
- Complément du marché : cinq widgets, six conversions d’affichage modifiées et une table de 5 277 entrées, incluant des noms conservés et des chemins composés. Ce chiffre ne signifie pas 5 277 nouvelles phrases traduites.
- Le binaire est identique à celui installé et essayé sous le nom TEST1. Son empreinte SHA-256 est fournie dans les contrôles.

## Contrôles des fichiers

Les fonctions modifiées sont relues et comparées à leur représentation attendue. Les tailles de bytecode, les sauts, les contextes et les points d’entrée sont contrôlés. Les autres exports sont conservés octet pour octet. Les 12 fichiers du .pak ont été vérifiés après empaquetage. Un contrôle sur les expressions réellement compilées couvre 31 722 cas avec un modèle des appels natifs, dont libellés inconnus et langues différentes du français. Ce modèle ne remplace pas l’exécution dans Unreal.

## Premier essai en jeu

Vérifiés : démarrage, chargement de la base, catégories françaises, feuilles d’objets dans la sous-catégorie des capots de culasse, filtre retournant le bon objet AK Izhmash, fiche et chemin de catégorie, recherche de compatibilité et retrait de ce filtre. Aucun incident lié aux widgets modifiés ni erreur fatale/de sérialisation n’a été relevé dans le journal pendant ce contrôle. Les 36 fichiers JSON installés sont restés inchangés et le rapport du jeu indique 6 798/6 798 textes utilisés, plus 96 hors modèle, sans erreur de formatage.

Le joueur confirme que cela semble bien fonctionner et indique qu’il refera un test approfondi plus tard. Il s’agit d’une validation initiale, pas d’une garantie d’absence de bug sur tous les écrans ou toutes les configurations.

## Encore à tester ou à relire

- Achats/ventes et panier ; marché noir ; saisie dans la recherche ; changement de langue ; ensemble des objets et des écrans.
- Formulations héritées de la traduction existante, dont certains noms d’objets maladroits ou conservés en anglais.
- Libellés longs dans des filtres à largeur fixe : une coupure a été observée sur un nom long.
- En-têtes d’inventaire, certains titres des commandes, Joinability et RANDOM : non corrigés par ce complément du marché.

## Compatibilité et retrait

Le complément remplace des ressources d’interface liées à ce build. Le désactiver avant de jouer sur un nouveau build et refaire les contrôles après une mise à jour. Le renommer en `.pak.disabled` suffit à le retirer ; la traduction JSON reste indépendante. Aucun ancien patch n’est réactivé.
