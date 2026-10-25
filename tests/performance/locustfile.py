# Tests de performance Locust (phase 2 des specs)
# Simule des secrétaires de club qui se connectent, consultent le tableau
# des points et réservent des places.
from random import choice

from locust import HttpUser, between, events, task

# Seuils imposés par les specs, en millisecondes
MAX_LOAD_TIME_MS = 5000    # liste des compétitions : 5 secondes maximum
MAX_UPDATE_TIME_MS = 2000  # mise à jour des points : 2 secondes maximum

# Clubs de clubs.json : email -> nom
CLUBS = {
    "john@simplylift.co": "Simply Lift",
    "admin@irontemple.com": "Iron Temple",
    "kate@shelifts.co.uk": "She Lifts",
}
COMPETITIONS = ["Spring Festival", "Fall Classic"]


class SecretaryUser(HttpUser):
    # Pause de 1 à 3 secondes entre deux actions, comme un vrai utilisateur
    wait_time = between(1, 3)

    def on_start(self):
        # Chaque utilisateur simulé représente un club tiré au hasard
        self.email = choice(list(CLUBS))
        self.club = CLUBS[self.email]

    def _check(self, response, max_ms, label):
        # La requête est un échec si le code n'est pas 200
        # ou si elle dépasse le seuil des specs
        elapsed_ms = response.elapsed.total_seconds() * 1000
        if response.status_code != 200:
            response.failure(f"{label} : code HTTP {response.status_code}")
        elif elapsed_ms > max_ms:
            response.failure(f"{label} : {elapsed_ms:.0f} ms (max {max_ms} ms)")
        else:
            response.success()

    @task(3)
    def load_competitions(self):
        # Connexion + affichage de la liste des compétitions (max 5 s)
        with self.client.post(
            "/showSummary",
            data={"email": self.email},
            name="Liste des competitions (connexion)",
            catch_response=True,
        ) as response:
            self._check(response, MAX_LOAD_TIME_MS, "Liste des competitions")

    @task(1)
    def view_points_board(self):
        # Tableau public des points, sans connexion (max 5 s)
        with self.client.get(
            "/pointsBoard",
            name="Tableau public des points",
            catch_response=True,
        ) as response:
            self._check(response, MAX_LOAD_TIME_MS, "Tableau des points")

    @task(2)
    def book_places(self):
        # Réservation d'une place = mise à jour du total de points (max 2 s)
        with self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club,
                "competition": choice(COMPETITIONS),
                "places": "1",
            },
            name="Mise a jour des points (reservation)",
            catch_response=True,
        ) as response:
            self._check(response, MAX_UPDATE_TIME_MS, "Mise a jour des points")


@events.quitting.add_listener
def set_exit_code(environment, **kwargs):
    # Code de sortie 1 si au moins une requête a échoué ou dépassé un seuil
    if environment.stats.total.num_failures > 0:
        environment.process_exit_code = 1
