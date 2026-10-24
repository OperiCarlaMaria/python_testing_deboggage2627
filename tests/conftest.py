import pytest ##test pour les emails

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
        
import copy ##test pour les points

import pytest

import server
from server import app


@pytest.fixture(autouse=True)
def reset_data():
    """Restore clubs and competitions after each test."""
    original_clubs = copy.deepcopy(server.clubs)
    original_competitions = copy.deepcopy(server.competitions)
    yield
    server.clubs[:] = original_clubs
    server.competitions[:] = original_competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client