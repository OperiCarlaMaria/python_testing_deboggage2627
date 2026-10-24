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
    
    
## test bug 4 restriction réservation de places
def test_validate_purchase_rejects_more_than_12_places():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    error = validatePurchase(club, competition, 13)
    assert error == "You cannot book more than 12 places per competition."


def test_validate_purchase_accepts_exactly_12_places():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25"}
    assert validatePurchase(club, competition, 12) is None


def test_validate_purchase_rejects_when_total_with_previous_bookings_exceeds_12():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25", "booked": {"Test Club": 8}}
    error = validatePurchase(club, competition, 5)
    assert error == "You cannot book more than 12 places per competition."


def test_validate_purchase_accepts_when_total_with_previous_bookings_reaches_12():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25", "booked": {"Test Club": 8}}
    assert validatePurchase(club, competition, 4) is None
    
    
## bug 5 test reserver plus de place qu'il n'en reste 
def test_validate_purchase_rejects_more_places_than_available():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "3"}
    error = validatePurchase(club, competition, 5)
    assert error == "Not enough places available in this competition."


def test_validate_purchase_accepts_places_equal_to_available():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "5"}
    assert validatePurchase(club, competition, 5) is None


def test_validate_purchase_rejects_when_competition_is_full():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "0"}
    error = validatePurchase(club, competition, 1)
    assert error == "This competition is full."
    
## bug 6 test date passée
def test_validate_purchase_rejects_past_competition():
    club = {"name": "Test Club", "points": "20"}
    competition = {"name": "Test Comp", "numberOfPlaces": "25", "date": "2020-01-01 10:00:00"}
    error = validatePurchase(club, competition, 2)
    assert error == "This competition is already over."