# Tests unitaires - BUG n°3, 4, 5 et 6 : valeurs limites de validatePurchase
import pytest

from server import validatePurchase

MSG_FULL = "This competition is full."
MSG_PLACES = "Not enough places available in this competition."
MSG_POINTS = "Not enough points to book that many places."
MSG_LIMIT = "You cannot book more than 12 places per competition."
MSG_PAST = "This competition is already over."


def make_case(points, available, already=0, date=None):
    # Fabrique un club et une compétition fictifs pour un test
    club = {"name": "Test Club", "points": points}
    competition = {"name": "Test Comp", "numberOfPlaces": available}
    if already:
        competition["booked"] = {"Test Club": already}
    if date:
        competition["date"] = date
    return club, competition


@pytest.mark.parametrize("points, available, already, requested", [
    (1, 1, 0, 1),     # dernier point et dernière place
    (12, 12, 0, 12),  # tout juste 12 places, points et places égaux
    (13, 25, 0, 12),  # maximum autorisé
    (20, 25, 11, 1),  # 11 déjà réservées + 1 = 12 pile
    (5, 5, 0, 5),
    (12, 13, 0, 12),
    (4, 25, 0, 4),
])
def test_validate_purchase_accepts_valid_requests(points, available, already, requested):
    club, competition = make_case(points, available, already)
    assert validatePurchase(club, competition, requested) is None


@pytest.mark.parametrize("points, available, already, requested, message", [
    # BUG n°5 : compétition complète
    (20, 0, 0, 1, MSG_FULL),
    (20, 0, 0, 5, MSG_FULL),
    # BUG n°5 : plus de places demandées que disponibles
    (20, 3, 0, 4, MSG_PLACES),
    (20, 1, 0, 2, MSG_PLACES),
    (20, 12, 0, 13, MSG_PLACES),
    # BUG n°3 : pas assez de points
    (3, 25, 0, 4, MSG_POINTS),
    (0, 25, 0, 1, MSG_POINTS),
    (4, 25, 0, 5, MSG_POINTS),
    (11, 25, 0, 12, MSG_POINTS),
    # BUG n°4 : plus de 12 places (seul ou en cumulé)
    (20, 25, 0, 13, MSG_LIMIT),
    (20, 25, 12, 1, MSG_LIMIT),
    (20, 25, 8, 5, MSG_LIMIT),
    (20, 25, 11, 2, MSG_LIMIT),
    # Priorité des messages quand plusieurs règles sont violées
    (0, 0, 0, 1, MSG_FULL),
    (1, 3, 0, 5, MSG_PLACES),
    (5, 25, 0, 13, MSG_POINTS),
])
def test_validate_purchase_rejects_with_expected_message(
        points, available, already, requested, message):
    club, competition = make_case(points, available, already)
    assert validatePurchase(club, competition, requested) == message


def test_validate_purchase_reports_past_competition_first():
    # BUG n°6 : la date passée est vérifiée avant tout le reste
    club, competition = make_case(20, 0, date="2020-01-01 10:00:00")
    assert validatePurchase(club, competition, 1) == MSG_PAST


def test_validate_purchase_handles_numbers_stored_as_strings():
    club, competition = make_case("4", "25")
    assert validatePurchase(club, competition, 4) is None
