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