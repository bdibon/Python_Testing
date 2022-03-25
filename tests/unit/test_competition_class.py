import pytest
from datetime import datetime, timedelta

from models import Competition, ClubException, CompetitionException
from models.club import PLACE_POINTS_COST


def test_init(competition):
    competition_instance = Competition(
        competition["name"],
        competition["date"],
        competition["numberOfPlaces"],
    )

    assert competition_instance.name == competition["name"]
    # NOTE: This mean we might need to add specific logic in our serialization step. # noqa E501
    assert competition_instance.date.isoformat(sep=" ") == competition["date"]
    assert competition_instance.numberOfPlaces == int(
        competition["numberOfPlaces"]
    )


def test_book_places_club_is_debited(get_club_instance, competition_instance):
    club_instance = get_club_instance()
    club_original_points = club_instance.points
    competition_instance.book_places(club_instance, 2)

    assert club_instance.points == club_original_points - 2 * PLACE_POINTS_COST


def test_book_places_club_cannot_spend_more_than_they_own(
    get_club_instance, competition_instance
):
    club_instance = get_club_instance()
    club_instance._points = 4

    with pytest.raises(ClubException):
        competition_instance.book_places(club_instance, 5)


def test_a_club_cannot_book_places_for_a_past_competition(get_club_instance):
    club_instance = get_club_instance()
    past = datetime.today() - timedelta(days=50)
    competition_instance = Competition(
        "Super Compét", past.isoformat(sep=" "), 42
    )

    with pytest.raises(CompetitionException):
        competition_instance.book_places(club_instance, 1)
