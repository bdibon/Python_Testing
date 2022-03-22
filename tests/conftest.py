import pytest

from repository.club import ClubRepository
from repository.competition import CompetitionRepository
from server import create_app


@pytest.fixture()
def club_list():
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


@pytest.fixture()
def club_repo(club_list):
    club_repo = ClubRepository(club_list)
    return club_repo


@pytest.fixture()
def competition_list():
    return [
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


@pytest.fixture()
def competition_repo(competition_list):
    competition_repo = CompetitionRepository(competition_list)
    return competition_repo


@pytest.fixture()
def client(club_repo, competition_repo):
    app = create_app(club_repo, competition_repo)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
