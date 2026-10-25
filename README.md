# GÜDLFT - Application de réservation de compétitions

Version légère (POC) d'une plateforme de réservation pour des compétitions
locales et régionales. Les **secrétaires de clubs** utilisent les points de leur
club pour réserver des places pour leurs athlètes. Un tableau public, sans
connexion, affiche les points de tous les clubs, par souci de transparence.

Ce dépôt est notre version du projet : nous avons repris le code de départ, corrigé
les bugs de la phase 1, implémenté la phase 2, et ajouté les tests et les rapports.

## Règles métier
- Un point = une place réservée.
- Un club ne peut pas réserver plus de places que de points.
- Un club ne peut pas réserver plus de **12 places** par compétition (en cumulé).
- Une réservation ne peut pas dépasser les places disponibles.
- On ne peut pas réserver sur une compétition **déjà passée**.
- Seul un secrétaire connecté (email d'un club) peut réserver.
- Le tableau des points est public, en lecture seule, trié par nom de club.

## Technologies
- Python 3.x
- [Flask](https://flask.palletsprojects.com/) (framework web léger)
- Fichiers JSON à la place d'une base de données
- [pytest](https://docs.pytest.org/) (tests), [coverage](https://coverage.readthedocs.io/) (couverture),
  [Locust](https://locust.io/) (performance), [flake8](https://flake8.pycqa.org/) (style)

## Installation
```bash
git clone https://github.com/OperiCarlaMaria/python_testing_deboggage2627.git
cd python_testing_deboggage2627
python -m venv venv
```
Activer l'environnement virtuel :
- Windows (PowerShell) : `venv\Scripts\activate`
- Mac / Linux : `source venv/bin/activate`

Installer les dépendances :
```bash
pip install -r requirements.txt
```
Si l'installation de Flask échoue avec une version récente de Python, installez
des versions plus récentes (`pip install flask`) puis mettez à jour `requirements.txt`
avec `pip freeze > requirements.txt`.

## Lancer l'application
Windows (PowerShell) :
```powershell
$env:FLASK_APP = "server.py"
flask run
```
Mac / Linux :
```bash
export FLASK_APP=server.py
flask run
```
Puis ouvrir http://127.0.0.1:5000 dans le navigateur.

Pages principales :
- `/` : connexion par email
- `/showSummary` : tableau de bord du club (après connexion)
- `/book/<competition>/<club>` : page de réservation
- `/pointsBoard` : tableau public des points (sans connexion)

## Données
L'application lit deux fichiers JSON au démarrage (redémarrer le serveur après toute modification) :
- `clubs.json` : nom, email et points de chaque club. Les emails de ce fichier sont
  ceux acceptés pour la connexion.
- `competitions.json` : nom, date (`AAAA-MM-JJ HH:MM:SS`) et nombre de places.

Les points et les places sont des **nombres sans guillemets**. Les réservations
sont gardées en mémoire : elles sont perdues au redémarrage du serveur.

## Tests
Tous les tests sont dans le dossier `tests/`, séparés en trois catégories :
```
tests/
  unit/          tests unitaires (fonctions isolées)
  integration/   tests d'intégration (routes, templates, temps de réponse)
  functional/    tests fonctionnels (parcours complets d'un secrétaire)
  performance/   scénario Locust
  conftest.py    fixtures communes (client de test, données réinitialisées)
```
Lancer tous les tests :
```bash
python -m pytest -v
```
Lancer une catégorie : `python -m pytest tests/unit`

**Résultat actuel : 168 tests, 168 réussis.** Les tests couvrent les cas valides
(happy paths) et les cas refusés (sad paths).

### Couverture
```bash
coverage run -m pytest
coverage report -m
coverage html        # rapport détaillé dans htmlcov/index.html
```
Couverture actuelle de `server.py` : **100 %** (objectif : 60 % minimum).
La configuration est dans `.coveragerc`.

### Performance (Locust)
Les spécifications imposent moins de 5 secondes pour afficher la liste des
compétitions et moins de 2 secondes pour mettre à jour les points, avec 6 utilisateurs.

Dans un premier terminal, lancer le serveur (`flask run`). Dans un second :
```bash
locust -f tests/performance/locustfile.py --headless -u 6 -r 6 -t 30s --host http://127.0.0.1:5000 --html tests/performance/rapport_locust.html
```
Résultat : 88 requêtes, **0 échec**, temps maximum de 156 ms.

## Rapports
Les rapports demandés sont dans le dossier `rapports/` :
- `rapport_tests.md` : tests, couverture, bugs corrigés et tests associés
- `rapport_couverture.txt` : sortie brute de `coverage report -m`
- `rapport_performance.md` : résultats Locust
- `rapport_flake8.md` : rapport flake8 (voir aussi ci-dessous)

## Rapport flake8
Configuration dans `.flake8` : ligne maximale de 100 caractères.
```bash
flake8 --count
```
- Avant correction : **87 avertissements** (mise en forme : espaces, lignes vides, commentaires).
  Voir `rapports/flake8_avant.txt`.
- Après correction : **0 avertissement**. Voir `rapports/flake8_apres.txt`.

## Bugs corrigés
| N° | Problème | Branche |
|---|---|---|
| 1 | Crash avec un email inconnu | `bug/email-inconnu` |
| 2 | Points non déduits après réservation | `bug/points-non-deduits` |
| 3 | Réservation avec plus de points que disponibles | `bug/points-insuffisants` |
| 4 | Plus de 12 places par club et par compétition | `bug/limite-12-places` |
| 5 | Plus de places que disponibles / compétition complète | `bug/places-depassent-disponibles` |
| 6 | Réservation sur une compétition passée | `bug/competition-passee` |
| 7 et 8 | Crash avec un club ou une compétition inconnus, saisie invalide | `bug/saisie-invalide` |
| 9 et 10 | Nombres en chaînes dans les JSON, HTML cassé | `amelioration/nettoyage-html-et-types` |
| 11 | Tableau public des points (phase 2) | `feature/tableau-points-public` |
| 12 | Message de confirmation sans le nombre de places | `bug/message-confirmation` |

Les autres branches : `amelioration/style-css`, `amelioration/tests-fonctionnels`,
`amelioration/tests-performance`, `amelioration/couverture-tests`,
`amelioration/conformite-flake8`, `amelioration/tests-unitaires-supplementaires`
et `amelioration/readme`.

## Conventions de travail
- `main` est la branche de référence : elle contient du code qui fonctionne et dont
  tous les tests passent.
- Une branche par bug, fonctionnalité ou amélioration, nommée
  `<bug|feature|amelioration>/nom-descriptif`, puis une Pull Request vers `main`.
- Les tests sont écrits avant le correctif (TDD) : un test qui échoue, puis le correctif.
- La branche **`QA`** est créée depuis `main` pour la relecture et n'est **jamais fusionnée**.
- Les commentaires dans le code sont en français et indiquent le numéro du bug corrigé.

## Ressources
- Spécifications fonctionnelles : `Spécifications fonctionnelles.pdf`
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation coverage](https://coverage.readthedocs.io/)
- [Documentation Locust](https://docs.locust.io/)