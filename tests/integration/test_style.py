# Tests d'intégration - AMÉLIORATION : mise en forme CSS (pas de bug associé)
import pytest


def test_stylesheet_is_served(client):
    # Le fichier static/style.css doit être servi par Flask
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert "text/css" in response.content_type


@pytest.mark.parametrize(
    "url", ["/", "/pointsBoard", "/book/Spring%20Festival/Simply%20Lift"]
)
def test_pages_link_the_stylesheet(client, url):
    # Chaque page doit charger la feuille de style
    response = client.get(url)
    assert b"static/style.css" in response.data


def test_welcome_page_links_the_stylesheet(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"static/style.css" in response.data


def test_success_message_has_success_class(client):
    # Le message de confirmation doit pouvoir être stylé en "succès"
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "1"},
    )
    assert b'class="flash success"' in response.data


def test_error_message_has_error_class(client):
    # Un message d'erreur doit pouvoir être stylé en "erreur"
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "abc"},
    )
    assert b'class="flash error"' in response.data
