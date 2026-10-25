# Tests unitaires - BUG n°2 et n°4 : réservation et mémorisation par club
import pytest

from server import bookPlaces, getPlacesBooked


@pytest.mark.parametrize("points, places, n, expected_points, expected_places", [
    (13, 25, 1, 12, 24),
    (13, 25, 12, 1, 13),
    (4, 4, 4, 0, 0),
    (12, 13, 12, 0, 1),
    ("13", "25", 3, 10, 22),  # nombres stockés en chaînes
])
def test_book_places_updates_points_and_places(
        points, places, n, expected_points, expected_places):
    club = {"name": "Test Club", "points": points}
    competition = {"name": "Test Comp", "numberOfPlaces": places}
    bookPlaces(club, competition, n)
    assert club["points"] == expected_points
    assert competition["numberOfPlaces"] == expected_places


def test_book_places_does_not_touch_other_club():
    club_a = {"name": "Club A", "points": 10}
    club_b = {"name": "Club B", "points": 10}
    competition = {"name": "Test Comp", "numberOfPlaces": 25}
    bookPlaces(club_a, competition, 3)
    assert club_b["points"] == 10
    assert competition["booked"] == {"Club A": 3}


def test_book_places_tracks_each_club_separately():
    club_a = {"name": "Club A", "points": 10}
    club_b = {"name": "Club B", "points": 10}
    competition = {"name": "Test Comp", "numberOfPlaces": 25}
    bookPlaces(club_a, competition, 2)
    bookPlaces(club_b, competition, 3)
    assert competition["booked"] == {"Club A": 2, "Club B": 3}


def test_book_places_creates_booked_entry_when_absent():
    club = {"name": "Test Club", "points": 10}
    competition = {"name": "Test Comp", "numberOfPlaces": 25}
    assert "booked" not in competition
    bookPlaces(club, competition, 4)
    assert competition["booked"] == {"Test Club": 4}


@pytest.mark.parametrize("competition, expected", [
    ({"name": "C"}, 0),
    ({"name": "C", "booked": {}}, 0),
    ({"name": "C", "booked": {"Other Club": 5}}, 0),
    ({"name": "C", "booked": {"Test Club": 7}}, 7),
])
def test_get_places_booked(competition, expected):
    assert getPlacesBooked({"name": "Test Club"}, competition) == expected
