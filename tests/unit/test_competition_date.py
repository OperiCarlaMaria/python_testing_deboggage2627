from server import isCompetitionPast


def test_competition_in_the_past_is_past():
    assert isCompetitionPast({"name": "X", "date": "2020-01-01 10:00:00"}) is True


def test_competition_in_the_future_is_not_past():
    assert isCompetitionPast({"name": "X", "date": "2099-01-01 10:00:00"}) is False


def test_competition_without_date_is_not_past():
    assert isCompetitionPast({"name": "X"}) is False
