from repository.club import ClubRepository


def test_init(club_list):
    club_repo = ClubRepository(club_list)

    assert len(club_repo.clubs) == len(club_list)
    for club_index, club in enumerate(club_repo.clubs):
        assert club.name == club_list[club_index]["name"]
        assert club.email == club_list[club_index]["email"]
        assert club.points == int(club_list[club_index]["points"])


def test_get_club_by_name(club_list):
    club_repo = ClubRepository(club_list)

    club = club_repo.get_club_by_name("Simply Lift")
    assert club.name == "Simply Lift"


def test_get_club_by_email(club_list):
    club_repo = ClubRepository(club_list)

    club = club_repo.get_club_by_email("john@simplylift.co")
    assert club.email == "john@simplylift.co"
