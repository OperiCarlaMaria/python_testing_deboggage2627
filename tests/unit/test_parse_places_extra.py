# Tests unitaires - BUG n°8 : cas supplémentaires sur la saisie du nombre de places
import pytest

from server import parsePlaces


@pytest.mark.parametrize("raw, expected", [
    ("1", 1),
    ("2", 2),
    ("12", 12),
    ("13", 13),  # pas de plafond ici : la limite de 12 est gérée par validatePurchase
    ("100", 100),
    ("  7  ", 7),
    ("007", 7),
    ("+5", 5),
    (3, 3),
])
def test_parse_places_accepts_valid_values(raw, expected):
    assert parsePlaces(raw) == expected


@pytest.mark.parametrize("raw", [
    "-1", "-100", " ", "1e3", "1,5", "3 places", "0x10",
    "0.0", "1.0", "one", "--1", 0, -3, [],
])
def test_parse_places_rejects_invalid_values(raw):
    assert parsePlaces(raw) is None
