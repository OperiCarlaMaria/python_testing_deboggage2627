from server import getClubByEmail


def test_get_club_by_email_returns_club_when_email_exists():
    club = getClubByEmail("john@simplylift.co")
    assert club is not None
    assert club["name"] == "Simply Lift"


def test_get_club_by_email_returns_none_when_email_unknown():
    assert getClubByEmail("inconnu@nulle-part.com") is None


def test_get_club_by_email_returns_none_when_email_empty():
    assert getClubByEmail("") is None