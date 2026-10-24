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