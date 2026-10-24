import pytest


def book(client, club, competition, places):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": places},
    )


@pytest.mark.parametrize("places", ["", "0", "-3", "abc", "2.5"])
def test_purchase_rejected_for_invalid_places(client, places):
    response = book(client, "Simply Lift", "Spring Festival", places)
    assert response.status_code == 200
    assert b"valid number of places" in response.data
    assert b"Great-booking complete!" not in response.data
    assert b"Points available: 13" in response.data
    assert b"Number of Places: 25" in response.data


def test_purchase_rejected_when_places_field_is_missing(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival"},
    )
    assert response.status_code == 200
    assert b"valid number of places" in response.data


def test_purchase_with_unknown_club_shows_error(client):
    response = book(client, "Club Fantome", "Spring Festival", "2")
    assert response.status_code == 404
    assert b"Something went wrong" in response.data


def test_purchase_with_unknown_competition_shows_error(client):
    response = book(client, "Simply Lift", "Competition Fantome", "2")
    assert response.status_code == 404
    assert b"Something went wrong" in response.data
    assert b"Points available: 13" in response.data


def test_booking_page_with_unknown_club_shows_error(client):
    response = client.get("/book/Spring%20Festival/Club%20Fantome")
    assert response.status_code == 404
    assert b"Something went wrong" in response.data


def test_booking_page_with_unknown_competition_shows_error(client):
    response = client.get("/book/Competition%20Fantome/Simply%20Lift")
    assert response.status_code == 404
    assert b"Something went wrong" in response.data