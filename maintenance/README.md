# Suivre les traductions après une mise à jour

Ces outils travaillent hors jeu, avec Python 3.11 ou plus récent conseillé. Ils ne lancent pas Incursion Red River. Le glossaire de référence reste dans `docs/GLOSSAIRE.md` et ses règles dans `docs/REGLES-TRADUCTION.json`.

## Contrôle habituel

Depuis la racine du dépôt :

```text
py -3 maintenance/translation_audit.py --market translations/market-display-fr.json --baseline maintenance/baseline-0.2.1.json --output work/audit
```

Le rapport vérifie les identités ns/key, les doublons, les textes vides, variables, balises, retours à la ligne, espaces de bord, noms de fichiers, commandes entre accents graves, appellations protégées et chemins du marché. Les divergences de glossaire sont des avertissements à relire, car le contexte prime.

Le contrôle de longueur est une **heuristique**. Un texte français plus long n’est pas forcément coupé ; un texte non signalé n’est pas forcément adapté au widget. `textes-a-verifier.json` est une liste de contrôle à l’écran. Les propositions courtes relues sont dans `LIBELLES-COURTS.md` et `libelles-courts-proposes.json` ; elles ne sont pas appliquées automatiquement.

## Comparer avec les textes du jeu

Après un lancement normal du jeu mis à jour, puis sa fermeture :

```text
py -3 maintenance/translation_audit.py --english "%LOCALAPPDATA%/Test_C/Saved/Translations/_English" --baseline maintenance/baseline-0.2.1.json --market translations/market-display-fr.json --output work/audit-maj
```

`_English` est réécrit par le jeu et reflète son dernier lancement. L’outil ne peut pas découvrir de nouveaux textes dans des archives du jeu qu’il n’extrait pas. Comparer son résultat au build Steam avant de conclure qu’une mise à jour est couverte.

Le dossier de résultat contient :

- `audit.json` : détails, nouveaux textes, sources anglaises modifiées, textes retirés et modifications françaises depuis la référence.
- `RAPPORT.md` : résumé et premières longueurs à vérifier.
- `snapshot.json` : empreintes par identité pour la prochaine comparaison.
- `a-traduire.json` : brouillon avec les nouvelles sources et les anciennes traductions lorsqu’elles existent. **Relire et valider avant de l’intégrer dans fr**.
- `textes-a-verifier.json` : tous les candidats pour le contrôle visuel.

Pour examiner aussi les `_Todo_*.json` du jeu, donner son dossier `fr` à `--translations`. Les fichiers commençant par `_` ne sont jamais traités comme des traductions actives.

Conserver l’ancienne référence avant de remplacer `--baseline` par le dernier `snapshot.json` validé. L’audit ne met jamais cette référence à jour tout seul.

Codes de sortie : 0 sans erreur bloquante, 1 pour les erreurs détectées, 2 pour une erreur d’accès ou d’arguments. Les avertissements seuls ne font pas échouer le contrôle.

## Vérifications du projet

```text
py -3 -m unittest discover -s tests -v
```

Les essais d’écriture utilisent uniquement des dossiers temporaires et des profils synthétiques. Les contrôles de processus sont simulés dans cette suite pour éprouver les refus ; les essais locaux supplémentaires utilisent des copies du profil validé en jeu.

Le workflow GitHub `controle.yml` est préparé pour exécuter ces contrôles à chaque push ou pull request et conserver le rapport. Son exécution sur GitHub reste à vérifier après publication. Les actions suivent leurs documentations officielles : [checkout](https://github.com/actions/checkout), [setup-python](https://github.com/actions/setup-python), [upload-artifact](https://github.com/actions/upload-artifact).
