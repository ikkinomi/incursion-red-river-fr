# Audit de la traduction 0.1.9 bêta

Jeu installé : **Incursion Red River 1.4.0.4**, build Steam **26761568**. Audit du 22 novembre 2026.

## Étendue et résultat

L’ensemble des fichiers installés et des 6 798 textes du modèle anglais courant a été comparé. Le build installé n’a pas changé depuis la 0.1.8. Les 25 textes manquants du rapport sont des outils d’édition ou des états internes, désormais couverts ; ce ne sont pas 25 nouveautés de gameplay.

Cette révision contient 6 894 entrées : les 6 798 du modèle et les 96 entrées supplémentaires déjà présentes. Les contrôles portent sur les identifiants et sources inchangés, doublons, variables, balises, sauts de ligne, espaces aux extrémités, noms de fichiers, noms de cartes, noms propres balisés et mots russes/vietnamiens. Ils passent sans erreur. Le détail chiffré est dans VALIDATION.json.

La relecture sémantique cible les signalements, les documents du terminal, les messages radio récurrents, plusieurs briefings et les anomalies repérées par le scan. Elle ne constitue pas une certification que chaque longue description est désormais parfaite. Les variantes répétées ont été corrigées ensemble.

## Corrections notables

- PROJECT EMBER : conservation du titre et traduction fidèle du message de test, qui vérifie la condition HasItem. Le contenu de test existe déjà dans l’anglais du jeu ; aucun texte narratif n’a été inventé.
- Relecture des documents et messages du terminal : habilitations, commandes, téléchargement, fermeture de session et aperçus de documents.
- « Film Case » : « Boîte de pellicule » ; « Cornflakes » : « Flocons de maïs » ; « Check Magazine » : « Vérifier le chargeur ».
- « Laser Range Finder » : « Télémètre laser » ; nom compact du dispositif : « TactiNav (GCPS) ».
- Messages radio tronqués ou calqués : phrases de validation, départ vers l’extraction, ordres de mission et confirmations de frappe.
- Noms de cartes Quarry, Delta, Outskirts et Bunker conservés ; restauration des noms de personnages et des passages russes/vietnamiens altérés.
- Discord, NVIDIA Reflex, Boost et Incursion Red River restent des appellations d’origine.

## Pourquoi certains textes des captures restent en anglais

Ces limites ont été vérifiées dans les ressources de la version installée, extraites en lecture seule. Les fichiers de traduction ne peuvent remplacer que les textes dotés d’une identité de localisation. Ajouter un faux identifiant JSON ou une traduction d’une autre occurrence identique ne modifie pas un texte invariant ou construit à partir d’un nom interne.

| Zone | Constat dans les ressources actuelles | Conséquence |
| --- | --- | --- |
| En-têtes inventaire | W_InventoryHeadline convertit Headline avec Conv_NameToText ; W_InventorySection fait de même avec SectionName | GEAR, INVENTORY, TACTICAL RIG, BACKPACK et certains autres titres échappent aux JSON |
| Emplacements d’équipement | W_EquipToContainer convertit Headline avec Conv_NameToText | HEADGEAR, Plate Carrier, Tactical Rig, backpack, Device restent concernés |
| Catégories du marché | W_VendorCategoryFilter convertit CallFunc_Array_Get_Item avec Conv_StringToText | Ammunition, Attachments, Dust Cover, Gas Tube et autres libellés dynamiques ne passent pas par les entrées localisées homonymes |
| Titres de commandes | WB_KeybindsSettings contient des noms de sections transmis à W_InventorySection | EQUIPMENT INPUT, COMBAT INPUT et autres titres peuvent rester en anglais malgré leurs traductions existantes |
| Salon | WBP_KronosLobby contient « Joinability: » comme texte invariant sans identité ; la valeur de session est convertie depuis une FString | « Joinability » et « RANDOM » ne sont pas corrigeables avec les seuls JSON |

Pour résoudre ces cas à la source, les développeurs doivent exposer des FText localisables dans leur modèle. L’autre possibilité est un mod binaire spécifique à chaque build. Aucun ancien .pak ni remplacement de Blueprint n’est inclus ou réactivé dans cette révision.

## Validation en jeu encore nécessaire

Cette révision n’a pas été chargée dans le jeu pendant cet audit. Le rapport _Report.txt existant se rapporte à la 0.1.8. Au prochain lancement, vérifier le nouveau rapport, le terminal, les commandes, les missions et les sous-titres. Un rapport sans erreur de formatage ne prouve pas que tous les textes visibles passent par la localisation.
