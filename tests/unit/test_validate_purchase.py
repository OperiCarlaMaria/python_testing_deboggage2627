from server import validatePurchase


def test_validate_purchase_rejects_more_places_than_points():
    club = {"name": "Test Club", "points": "4"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    error = validatePurchase(club, competition, 5)
    assert error == "Not enough points to book that many places."


def test_validate_purchase_accepts_places_equal_to_points():
    club = {"name": "Test Club", "points": "4"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    assert validatePurchase(club, competition, 4) is None


def test_validate_purchase_accepts_fewer_places_than_points():
    club = {"name": "Test Club", "points": "4"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    assert validatePurchase(club, competition, 2) is None