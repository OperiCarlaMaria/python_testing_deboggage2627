def test_login_with_known_email_shows_welcome_page(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_login_with_unknown_email_shows_error_instead_of_crashing(client):
    response = client.post("/showSummary", data={"email": "inconnu@nulle-part.com"})
    assert response.status_code == 200
    assert b"not found" in response.data
