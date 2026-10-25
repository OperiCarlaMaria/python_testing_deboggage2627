# Tests fonctionnels - parcours complets d'un secrétaire de club
# Ils couvrent l'ensemble des bugs n°1 à n°11 bout en bout


def test_full_booking_journey_happy_path(client):
    # 1. Le secrétaire se connecte avec un email valide (bug n°1)
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"Welcome, john@simplylift.co" in response.data
    assert b"Points available: 13" in response.data

    # 2. Il ouvre la page de réservation d'une compétition
    response = client.get("/book/Spring%20Festival/Simply%20Lift")
    assert b"Places available: 25" in response.data

    # 3. Il réserve 3 places (bugs n°2, 3, 4, 5)
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 10" in response.data
    assert b"Number of Places: 22" in response.data

    # 4. Le tableau public affiche le nouveau total (bug n°11)
    response = client.get("/pointsBoard")
    assert b"<td>10</td>" in response.data

    # 5. Il se déconnecte et revient à l'accueil
    response = client.get("/logout", follow_redirects=True)
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_journey_unknown_email_then_correct_email(client):
    # Sad path : mauvais email (bug n°1), puis le secrétaire corrige
    response = client.post("/showSummary", data={"email": "faux@exemple.com"})
    assert b"not found" in response.data
    assert b"Welcome, " not in response.data

    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert b"Welcome, admin@irontemple.com" in response.data
    assert b"Points available: 4" in response.data


def test_journey_not_enough_points_then_valid_booking(client):
    # Sad path : Iron Temple (4 points) demande trop de places (bug n°3)
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "5"},
    )
    assert b"Not enough points" in response.data
    assert b"Points available: 4" in response.data

    # Puis une saisie invalide (bug n°8)
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "abc"},
    )
    assert b"valid number of places" in response.data

    # Puis une réservation correcte avec tous ses points
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "4"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 0" in response.data

    # Plus aucun point : une nouvelle réservation est refusée
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "1"},
    )
    assert b"Not enough points" in response.data


def test_journey_competition_becomes_full_for_other_clubs(client):
    # She Lifts réserve 12 places sur Fall Classic (13 places), bug n°4
    client.post(
        "/purchasePlaces",
        data={"club": "She Lifts", "competition": "Fall Classic", "places": "12"},
    )
    # Simply Lift prend la dernière place : la compétition est complète
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Fall Classic", "places": "1"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Number of Places: 0" in response.data

    # Iron Temple se connecte : plus de lien de réservation (bug n°5)
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert b"book/Fall%20Classic" not in response.data

    # Et une réservation forcée est refusée avec un message clair
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Fall Classic", "places": "1"},
    )
    assert b"This competition is full." in response.data


def test_journey_visitor_sees_points_board_without_login(client):
    # Un visiteur non connecté consulte le tableau (bug n°11)
    response = client.get("/pointsBoard")
    assert response.status_code == 200
    assert b"Clubs points board" in response.data

    # Il n'a pas accès à la réservation d'un club inexistant (bug n°7)
    response = client.get("/book/Spring%20Festival/Club%20Fantome")
    assert response.status_code == 404