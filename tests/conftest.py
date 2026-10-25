import copy

import pytest

import server
from server import app


@pytest.fixture(autouse=True)
def reset_data():
    """Give tests stable data, and restore it after each test."""
    original_clubs = copy.deepcopy(server.clubs)
    original_competitions = copy.deepcopy(server.competitions)

    for competition in server.competitions:
        competition["date"] = "2099-01-01 10:00:00"
    server.competitions.append(
        {"name": "Past Competition", "date": "2020-01-01 10:00:00", "numberOfPlaces": "7"}
    )

    yield

    server.clubs[:] = original_clubs
    server.competitions[:] = original_competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
