# Tests unitaires - BUG n°11 : tableau public des points
from server import bookPlaces, clubs, competitions, getClubsPoints


def test_get_clubs_points_returns_name_and_points_for_each_club():
    # Chaque club doit apparaître avec son nom et son total de points
    board = getClubsPoints()
    assert {"name": "Simply Lift", "points": 13} in board
    assert {"name": "Iron Temple", "points": 4} in board
    assert {"name": "She Lifts", "points": 12} in board


def test_get_clubs_points_does_not_expose_emails():
    # Le tableau est public : on n'expose jamais les emails des secrétaires
    for entry in getClubsPoints():
        assert "email" not in entry


def test_get_clubs_points_is_sorted_by_name():
    # Tri alphabétique : aucun club n'est mis en avant (favoritisme)
    names = [entry["name"] for entry in getClubsPoints()]
    assert names == ["Iron Temple", "She Lifts", "Simply Lift"]


def test_get_clubs_points_reflects_bookings():
    # Après une réservation, le tableau doit afficher le nouveau total
    bookPlaces(clubs[0], competitions[0], 3)
    board = getClubsPoints()
    assert {"name": "Simply Lift", "points": 10} in board
