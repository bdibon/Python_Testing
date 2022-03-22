from flask import url_for
from bs4 import BeautifulSoup


def test_club_cannot_book_more_than_they_own(
    competition_instance, club_instance, app, client
):
    with app.app_context(), app.test_request_context():
        book_url = url_for(
            "book",
            competition=competition_instance.name,
            club=club_instance.name,
        )

    html_doc = client.get(book_url).data
    soup = BeautifulSoup(html_doc, "html.parser")
    max_placesRequired = int(soup.select("input[type=number]")[0].attrs["max"])
    assert club_instance.places_budget == max_placesRequired
