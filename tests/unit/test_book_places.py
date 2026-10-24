from server import bookPlaces


def test_book_places_deducts_points_from_club():
    club = {"name": "Test Club", "points": "13"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    bookPlaces(club, competition, 3)
    assert club["points"] == 10


def test_book_places_deducts_places_from_competition():
    club = {"name": "Test Club", "points": "13"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    bookPlaces(club, competition, 3)
    assert competition["numberOfPlaces"] == 22