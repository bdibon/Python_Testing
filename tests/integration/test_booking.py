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
    assert max_placesRequired <= club_instance.places_budget


def test_club_should_not_be_able_to_book_more_than_12_places(
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
    assert max_placesRequired <= 12


def test_places_are_correctly_deducted_from_the_competition(
    competition_instance, club_instance, client, competition_repo
):
    original_nb_of_places = competition_instance.numberOfPlaces
    nb_places_bought = 2
    expected_nb_of_places = original_nb_of_places - nb_places_bought
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_instance.name,
            "club": club_instance.name,
            "places": nb_places_bought,
        },
    )

    competition_after_request = competition_repo.get_competition_by_name(
        competition_instance.name
    )
    assert competition_after_request.numberOfPlaces == expected_nb_of_places
    assert b"Number of Places: %d" % expected_nb_of_places in response.data


def test_booking_places_in_the_past_displays_an_error(
    past_competition_instance, club_instance, app, client
):
    with app.app_context(), app.test_request_context():
        book_url = url_for(
            "book",
            competition=past_competition_instance.name,
            club=club_instance.name,
        )

    response = client.get(book_url)
    assert b"Registrations are closed" in response.data
