# Rapport de tests

Date : 25 octobre 2026

## Outils
- **pytest** pour l'exécution des tests (`python -m pytest -v`).
- **coverage** pour la couverture (`coverage run -m pytest`, puis `coverage report -m`),
  configuré dans `.coveragerc` avec la mesure des branches.
- **Locust** pour la performance (voir `rapport_performance.md`).

## Organisation
Les tests sont dans le dossier `tests/`, séparés en trois sous-dossiers
comme demandé par le guide de développement :
- `tests/unit/` : tests unitaires (fonctions isolées) ;
- `tests/integration/` : tests d'intégration (routes Flask, templates, temps de réponse) ;
- `tests/functional/` : tests fonctionnels (parcours complets d'un secrétaire).

`tests/conftest.py` fournit les fixtures communes : un client Flask de test,
des données stables (dates des compétitions fixées) et la remise à zéro des
données après chaque test.

## Résultats
**93 tests, 93 réussis, 0 échec.**

| Catégorie | Nombre de tests |
|---|---|
| Unitaires | 41 |
| Intégration | 47 |
| Fonctionnels | 5 |
| **Total** | **93** |

## Couverture
| Fichier | Instructions | Manquées | Branches | Couverture |
|---|---|---|---|---|
| server.py | 114 | 0 | 32 | **100 %** |

L'objectif du guide est de 60 % minimum : **il est dépassé**.
Le fichier mesuré est `server.py`, qui contient toute la logique de l'application.
Les tests eux-mêmes sont exclus de la mesure.

Une couverture de 100 % signifie que chaque ligne et chaque branche sont exécutées
par au moins un test. Elle ne prouve pas à elle seule que tous les cas sont bien
vérifiés : c'est pourquoi chaque règle a ses cas limites (valeur exacte, valeur
juste au-dessus, valeur invalide).

## Bugs corrigés et tests associés
| N° | Problème | Tests |
|---|---|---|
| 1 | Crash avec un email inconnu | unitaires + intégration + fonctionnels |
| 2 | Points non déduits après réservation | unitaires + intégration |
| 3 | Réservation avec plus de points que disponibles | unitaires + intégration + fonctionnels |
| 4 | Plus de 12 places par club et par compétition (y compris en cumulé) | unitaires + intégration |
| 5 | Plus de places que disponibles, compétition complète | unitaires + intégration + fonctionnels |
| 6 | Réservation sur une compétition passée | unitaires + intégration |
| 7 | Crash avec un club ou une compétition inconnus | unitaires + intégration + fonctionnels |
| 8 | Saisie invalide (vide, texte, 0, négatif, décimal) | unitaires + intégration + fonctionnels |
| 9 | Nombres stockés en chaînes dans les JSON | unitaires |
| 10 | HTML invalide dans les templates | intégration |
| 11 | Tableau public des points (phase 2) | unitaires + intégration + fonctionnels |
| 12 | Message de confirmation sans le nombre de places | unitaires + intégration |

Chaque règle est testée en **happy path** (cas valide, y compris les valeurs limites
exactes) et en **sad path** (cas refusé avec un message d'erreur clair).

## Méthode : TDD
Pour chaque bug, les tests ont été écrits en premier et lancés pour constater
l'échec, puis le code a été corrigé jusqu'à obtenir des tests verts. Chaque bug
a été traité dans sa propre branche (`bug/...`, `feature/...`, `amelioration/...`).

## Limites et points d'amélioration
- **Ratio de tests** : le guide recommande environ deux fois plus de tests unitaires
  que de tests d'intégration et fonctionnels. Nous en avons 41 pour 52, soit un ratio
  d'environ 0,8 pour 1 : l'objectif n'est pas encore atteint.
- Les données sont en mémoire (fichiers JSON) : les réservations ne sont pas
  sauvegardées après un redémarrage du serveur.
- Les tests de performance ont été réalisés en local avec le serveur de
  développement Flask.