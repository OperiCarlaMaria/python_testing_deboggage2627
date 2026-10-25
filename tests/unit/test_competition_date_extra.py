# Tests unitaires - BUG n°6 : cas supplémentaires sur la date des compétitions
from datetime import datetime, timedelta

import pytest

from server import DATE_FORMAT, isCompetitionPast


@pytest.mark.parametrize("date", [
    "2000-01-01 00:00:00",
    "2020-03-27 10:00:00",
    "2020-10-22 13:30:00",
    "2024-12-31 23:59:59",
    "1999-12-31 23:59:59",
])
def test_past_dates_are_past(date):
    assert isCompetitionPast({"name": "X", "date": date}) is True


@pytest.mark.parametrize("date", [
    "2099-01-01 10:00:00",
    "2100-12-31 23:59:59",
    "3000-01-01 00:00:00",
])
def test_future_dates_are_not_past(date):
    assert isCompetitionPast({"name": "X", "date": date}) is False


@pytest.mark.parametrize("competition", [
    {"name": "X", "date": ""},
    {"name": "X", "date": None},
])
def test_empty_date_is_not_past(competition):
    assert isCompetitionPast(competition) is False


@pytest.mark.parametrize("date", ["27/03/2020", "not a date", "2020-03-27"])
def test_invalid_date_format_raises_value_error(date):
    with pytest.raises(ValueError):
        isCompetitionPast({"name": "X", "date": date})


def test_competition_started_seconds_ago_is_past():
    date = (datetime.now() - timedelta(seconds=5)).strftime(DATE_FORMAT)
    assert isCompetitionPast({"name": "X", "date": date}) is True


def test_competition_starting_in_minutes_is_not_past():
    date = (datetime.now() + timedelta(minutes=5)).strftime(DATE_FORMAT)
    assert isCompetitionPast({"name": "X", "date": date}) is False
