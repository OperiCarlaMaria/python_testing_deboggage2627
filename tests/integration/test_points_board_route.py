# Tests d'intégration - BUG n°11 : page publique du tableau des points


def test_points_board_is_public_without_login(client):
    # Aucune connexion nécessaire pour voir la page
    response = client.get("/pointsBoard")
    assert response.status_code == 200
    assert b"<td>Simply Lift</td>" in response.data
    assert b"<td>13</td>" in response.data
    assert b"<td>Iron Temple</td>" in response.data
    assert b"<td>4</td>" in response.data


def test_points_board_does_not_show_emails(client):
    response = client.get("/pointsBoard")
    assert b"john@simplylift.co" not in response.data
    assert b"admin@irontemple.com" not in response.data


def test_points_board_is_read_only(client):
    # La page n'accepte que la lecture (GET) : un POST est refusé
    response = client.post("/pointsBoard", data={"points": "999"})
    assert response.status_code == 405


def test_points_board_shows_updated_points_after_booking(client):
    client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    response = client.get("/pointsBoard")
    assert b"<td>10</td>" in response.data


def test_login_page_has_link_to_points_board(client):
    response = client.get("/")
    assert b'href="/pointsBoard"' in response.data


def test_welcome_page_has_link_to_points_board(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b'href="/pointsBoard"' in response.data