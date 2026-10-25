# Tests d'intégration - BUG n°10 : HTML des templates


def test_welcome_page_has_no_invalid_br_tag(client):
    # Le template contenait </br> au lieu de <br />
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"</br>" not in response.data


def test_login_form_label_is_linked_to_email_input(client):
    # Le label pointait vers un champ dont l'id était vide
    response = client.get("/")
    assert b'for="email"' in response.data
    assert b'id="email"' in response.data


def test_welcome_page_still_shows_flash_messages_and_points(client):
    # Garde-fou : doit déjà passer, il nous protège pendant la réécriture
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "2"},
    )
    assert b"Great-booking complete!" in response.data
    assert b"Points available: 11" in response.data