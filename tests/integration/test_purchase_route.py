def test_purchase_deducts_points_shown_on_summary(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 10" in response.data


def test_purchase_deducts_places_shown_on_summary(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    assert b"Number of Places: 22" in response.data
    
    
    
def test_purchase_rejected_when_not_enough_points(client): ## bug 3 point insuffisant et reservation allant au delà test
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "5"},
    )
    assert response.status_code == 200
    assert b"Not enough points" in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 4" in response.data
    assert b"Number of Places: 25" in response.data


def test_purchase_accepted_when_places_equal_points(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "4"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 0" in response.data
    
    
## test bug 4  réservation de places
def test_purchase_rejected_when_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "13"},
    )
    assert b"more than 12 places" in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 13" in response.data
    assert b"Number of Places: 25" in response.data


def test_purchase_accepted_when_exactly_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "12"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 1" in response.data
    assert b"Number of Places: 13" in response.data


def test_purchase_rejected_when_cumulative_bookings_exceed_12(client):
    client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "8"},
    )
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "5"},
    )
    assert b"more than 12 places" in response.data
    assert b"Points available: 5" in response.data
    assert b"Number of Places: 17" in response.data