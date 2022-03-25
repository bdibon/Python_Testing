import pytest

from models import Club, ClubException
from models.club import PLACE_POINTS_COST


@pytest.fixture()
def club():
    return {
        "name": "Complex Lift",
        "email": "bill@complexlift.co",
        "points": "7",
    }


def test_init(club):
    club_name = club["name"]
    club_email = club["email"]
    club_points = club["points"]
    club_instance = Club(club_name, club_email, club_points)

    assert club_instance.name == club_name
    assert club_instance.email == club_email
    assert club_instance.points == int(club_points)


def test_has_enough_points(club):
    club_name = club["name"]
    club_email = club["email"]
    club_points = 8
    club_instance = Club(club_name, club_email, club_points)

    assert not club_instance.has_enough_points(9)
    assert club_instance.has_enough_points(8 // PLACE_POINTS_COST)


def test_buy_places(club):
    club_name = club["name"]
    club_email = club["email"]
    club_points = 8
    club_instance = Club(club_name, club_email, club_points)

    with pytest.raises(ClubException):
        club_instance.buy_places(9)

    club_instance.buy_places(1)
    assert club_instance.points == club_points - 1 * PLACE_POINTS_COST
