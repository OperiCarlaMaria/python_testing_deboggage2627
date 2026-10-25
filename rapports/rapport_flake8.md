# Rapport flake8

## Outil et configuration
- **flake8** (vérification du style PEP 8), configuré dans `.flake8` :
  ligne maximale de **100 caractères** (au lieu de 79 par défaut), dossiers
  `venv` et `htmlcov` exclus.
- Commande : `flake8 --count`

## Avant correction
**87 avertissements** (voir `flake8_avant.txt`), uniquement de mise en forme :

| Code | Signification | Cause principale |
|---|---|---|
| W292 | pas de retour à la ligne final | presque tous les fichiers |
| W291 / W293 | espaces en fin de ligne ou sur ligne vide | `server.py`, tests |
| E302 / E303 / E305 | nombre de lignes vides incorrect | `server.py`, tests |
| E265 / E266 | commentaires mal formés (`###`) | `server.py`, tests |
| E231 / E261 / E262 | espaces manquants (code d'origine) | `server.py` |
| E116 | commentaire mal indenté | `server.py` |
| E501 | ligne trop longue | un test d'intégration |

Aucune erreur de logique (variable inutilisée, import manquant, etc.).

## Correction
Mise en forme automatique avec `autopep8`, puis correction manuelle de la
ligne trop longue. Aucun changement de comportement : les 93 tests passent
toujours et la couverture reste à 100 %.

## Après correction
**0 avertissement** (voir `flake8_apres.txt`).