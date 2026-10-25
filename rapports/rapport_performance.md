# Rapport de performance

## Objectif
Vérifier les exigences de la phase 2 des spécifications fonctionnelles :
- récupérer une liste de compétitions en **moins de 5 secondes** ;
- mettre à jour le total de points en **moins de 2 secondes**.

Le nombre d'utilisateurs par défaut des tests de performance est de **6**.

## Outils et méthode
- **Locust 2.47.0**, scénario dans `tests/performance/locustfile.py`.
- 6 utilisateurs simulés (secrétaires de clubs), lancés en même temps, pendant 30 secondes.
- Pause de 1 à 3 secondes entre deux actions de chaque utilisateur.
- Trois actions mesurées : connexion avec affichage de la liste des compétitions,
  consultation du tableau public des points, réservation de places.
- Une requête est comptée comme un échec si le code HTTP n'est pas 200
  ou si elle dépasse le seuil des spécifications.
- Des tests pytest (`tests/integration/test_response_time.py`) vérifient aussi
  ces seuils à chaque exécution de la suite de tests.

Commande utilisée :

    locust -f tests/performance/locustfile.py --headless -u 6 -r 6 -t 30s \
      --host http://127.0.0.1:5000 --html tests/performance/rapport_locust.html

## Résultats

| Action | Requêtes | Échecs | Moyenne | Médiane | 95 % | Maximum | Limite |
|---|---|---|---|---|---|---|---|
| Liste des compétitions (connexion) | 46 | 0 | 15 ms | 5 ms | 65 ms | 156 ms | 5 000 ms |
| Mise à jour des points (réservation) | 33 | 0 | 14 ms | 5 ms | 86 ms | 138 ms | 2 000 ms |
| Tableau public des points | 9 | 0 | 5 ms | 4 ms | 10 ms | 10 ms | 5 000 ms |
| Total | 88 | 0 | 13 ms | 5 ms | 73 ms | 156 ms | |

Débit moyen : environ 3 requêtes par seconde. Le détail complet est dans
`tests/performance/rapport_locust.html`.

## Conclusion
Les deux exigences sont respectées avec une très grande marge :
- la liste des compétitions s'affiche en 156 ms au maximum (limite : 5 s) ;
- la mise à jour des points prend 138 ms au maximum (limite : 2 s) ;
- aucune requête n'a échoué.

## Limites de ce test
- Le test est exécuté en local avec le serveur de développement Flask, sur une
  machine personnelle : les résultats dépendent de cette machine.
- Les données sont stockées en mémoire (fichiers JSON), avec seulement 3 clubs
  et 2 compétitions.
- Les clubs n'ont que 29 points au total : une partie des réservations a été
  refusée par l'application une fois les points épuisés. Ces refus sont
  rapides et sont inclus dans les mesures, mais ils ne modifient pas les points.
- Pour un nouveau test avec des points neufs, il faut redémarrer le serveur.