# Tests d'intégration - PERFORMANCE (phase 2 des specs) : temps de réponse
import time

# Seuils imposés par les specs, en secondes
MAX_LOAD_SECONDS = 5    # récupérer la liste des compétitions
MAX_UPDATE_SECONDS = 2  # mettre à jour le total de points


def test_competitions_list_loads_in_less_than_5_seconds(client):
    start = time.perf_counter()
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < MAX_LOAD_SECONDS


def test_points_board_loads_in_less_than_5_seconds(client):
    start = time.perf_counter()
    response = client.get("/pointsBoard")
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < MAX_LOAD_SECONDS


def test_points_update_takes_less_than_2_seconds(client):
    start = time.perf_counter()
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "2"},
    )
    elapsed = time.perf_counter() - start
    # La réservation doit avoir réussi ET être rapide
    assert b"Great-booking complete!" in response.data
    assert elapsed < MAX_UPDATE_SECONDS