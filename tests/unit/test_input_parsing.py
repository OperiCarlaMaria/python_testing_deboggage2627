import pytest

from server import getClubByName, getCompetitionByName, parsePlaces


def test_parse_places_returns_int_for_valid_number():
    assert parsePlaces("3") == 3


def test_parse_places_ignores_surrounding_spaces():
    assert parsePlaces(" 3 ") == 3


@pytest.mark.parametrize("raw", ["", None, "abc", "0", "-2", "2.5"])
def test_parse_places_returns_none_for_invalid_value(raw):
    assert parsePlaces(raw) is None


def test_get_club_by_name_returns_club_when_it_exists():
    assert getClubByName("Simply Lift")["email"] == "john@simplylift.co"


def test_get_club_by_name_returns_none_when_unknown():
    assert getClubByName("Club Fantome") is None


def test_get_competition_by_name_returns_competition_when_it_exists():
    assert getCompetitionByName("Spring Festival")["name"] == "Spring Festival"


def test_get_competition_by_name_returns_none_when_unknown():
    assert getCompetitionByName("Competition Fantome") is None
