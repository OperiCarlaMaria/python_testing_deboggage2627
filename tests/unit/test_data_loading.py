# Tests unitaires - BUG n°9 : conversion des chaînes en entiers au chargement
import json

from server import loadClubs, loadCompetitions


def test_load_clubs_converts_points_to_int(tmp_path, monkeypatch):
    # création d'un faux clubs.json avec des points en chaîne ("7")
    data = {"clubs": [{"name": "A", "email": "a@a.com", "points": "7"}]}
    (tmp_path / "clubs.json").write_text(json.dumps(data))
    monkeypatch.chdir(tmp_path)
    clubs = loadClubs()
    assert clubs[0]["points"] == 7
    assert isinstance(clubs[0]["points"], int)


def test_load_competitions_converts_places_to_int(tmp_path, monkeypatch):
    # Même chose pour le nombre de places d'une compétition
    data = {"competitions": [{"name": "C", "date": "2099-01-01 10:00:00", "numberOfPlaces": "25"}]}
    (tmp_path / "competitions.json").write_text(json.dumps(data))
    monkeypatch.chdir(tmp_path)
    competitions = loadCompetitions()
    assert competitions[0]["numberOfPlaces"] == 25
    assert isinstance(competitions[0]["numberOfPlaces"], int)
