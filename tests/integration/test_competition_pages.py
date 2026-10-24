def test_booking_page_not_available_for_past_competition(client):
    response = client.get("/book/Past%20Competition/Simply%20Lift")
    assert response.status_code == 200
    assert b"This competition is already over." in response.data
    assert b"How many places?" not in response.data


def test_booking_page_available_for_future_competition(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")
    assert response.status_code == 200
    assert b"How many places?" in response.data


def test_welcome_page_hides_booking_link_for_past_competition(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"book/Past%20Competition" not in response.data


def test_welcome_page_shows_booking_link_for_future_competition(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"book/Spring%20Festival" in response.data