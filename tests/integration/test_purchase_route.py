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
    
## bug 5 test reserver plus de place qu'il n'en reste 
def book(client, club, competition, places):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


def test_purchase_rejected_when_more_places_than_available(client):
    book(client, "She Lifts", "Fall Classic", "12")
    response = book(client, "Simply Lift", "Fall Classic", "2")
    assert b"Not enough places available" in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 13" in response.data
    assert b"Number of Places: 1" in response.data


def test_purchase_accepted_when_places_equal_available(client):
    book(client, "She Lifts", "Fall Classic", "12")
    response = book(client, "Simply Lift", "Fall Classic", "1")
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 12" in response.data
    assert b"Number of Places: 0" in response.data


def test_purchase_rejected_when_competition_is_full(client):
    book(client, "She Lifts", "Fall Classic", "12")
    book(client, "Simply Lift", "Fall Classic", "1")
    response = book(client, "Iron Temple", "Fall Classic", "1")
    assert b"This competition is full." in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 4" in response.data
    
    
## bug 6 test date passée
def test_purchase_rejected_for_past_competition(client):
    response = book(client, "Simply Lift", "Past Competition", "2")
    assert b"This competition is already over." in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 13" in response.data
    assert b"Number of Places: 7" in response.data