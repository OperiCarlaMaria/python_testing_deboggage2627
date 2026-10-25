# Tests unitaires - BUG n°12 : le message de confirmation indique le nombre de places
from server import confirmationMessage


def test_confirmation_message_contains_number_of_places():
    # Le secrétaire doit voir combien de places il vient d'acheter
    competition = {"name": "Spring Festival"}
    message = confirmationMessage(3, competition)
    assert "3 place(s)" in message


def test_confirmation_message_contains_competition_name():
    competition = {"name": "Spring Festival"}
    message = confirmationMessage(3, competition)
    assert "Spring Festival" in message


def test_confirmation_message_keeps_original_start():
    # On garde le début historique du message pour la compatibilité
    competition = {"name": "Spring Festival"}
    assert confirmationMessage(1, competition).startswith("Great-booking complete!")