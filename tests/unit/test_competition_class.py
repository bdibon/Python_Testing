import pytest

from models import Competition, ClubException


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


def test_book_places_club_is_debited(club_instance, competition_instance):
    club_original_points = club_instance.points
    competition_instance.book_places(club_instance, 4)

    assert club_instance.points == club_original_points - 4


def test_book_places_club_cannot_spend_more_than_they_own(
    club_instance, competition_instance
):
    club_instance._points = 4

    with pytest.raises(ClubException):
        competition_instance.book_places(club_instance, 5)
