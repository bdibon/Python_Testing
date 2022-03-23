from bs4 import BeautifulSoup


def test_points_board_display_clubs_and_their_points(client, club_repo):
    html_doc = client.get("/displayPoints").data
    soup = BeautifulSoup(html_doc, "html.parser")
    table_rows = soup.table.tbody.find_all("tr")

    for tr in table_rows:
        td_name, td_points = tr.find_all("td")
        club_name = td_name.string
        club_points = int(td_points.string)
        club = club_repo.get_club_by_name(club_name)

        assert club is not None
        assert club.points == club_points
