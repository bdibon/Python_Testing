import pytest

from models import Club, Competition
from repository.club import ClubRepository
from repository.competition import CompetitionRepository
from server import create_app


COMPETITION_LIST = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    },
    {
        "name": "Winter Classic",
        "date": "2022-10-22 13:30:00",
        "numberOfPlaces": "19",
    },
]


CLUB_LIST = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4",
    },
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]


@pytest.fixture()
def competition():
    return COMPETITION_LIST[2]


@pytest.fixture()
def competition_instance(competition):
    competition_instance = Competition(
        competition["name"],
        competition["date"],
        competition["numberOfPlaces"],
    )
    return competition_instance


@pytest.fixture()
def club_instance():
    club_dict = CLUB_LIST[0]
    club_name = club_dict["name"]
    club_email = club_dict["email"]
    club_points = club_dict["points"]
    club = Club(club_name, club_email, club_points)
    return club


@pytest.fixture()
def club_list():
    return CLUB_LIST


@pytest.fixture()
def club_repo(club_list):
    club_repo = ClubRepository(club_list)
    return club_repo


@pytest.fixture()
def competition_list():
    return COMPETITION_LIST


@pytest.fixture()
def competition_repo(competition_list):
    competition_repo = CompetitionRepository(competition_list)
    return competition_repo


@pytest.fixture()
def app(club_repo, competition_repo):
    app = create_app(club_repo, competition_repo)
    app.config["TESTING"] = True

    return app


@pytest.fixture()
def client(app):

    with app.test_client() as client:
        yield client
