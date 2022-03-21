import json
from flask import Flask, render_template, request, redirect, flash, url_for

from models import ClubException, CompetitionException
from repository import get_competition_repository, get_club_repository


app = Flask(__name__)
app.secret_key = "something_special"


club_repo = get_club_repository()
competition_repo = get_competition_repository()

competitions = competition_repo.competitions
clubs = club_repo.clubs


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][
        0
    ]
    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = club_repo.get_club_by_name(club)
    foundCompetition = competition_repo.get_competition_by_name(competition)

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form.get("competition", None)
    club_name = request.form.get("club", None)

    competition = competition_repo.get_competition_by_name(competition_name)
    club = club_repo.get_club_by_name(club_name)

    placesRequired = int(request.form["places"])

    try:
        competition.book_places(club, placesRequired)
        flash("Great-booking complete!")
    except (ClubException, CompetitionException) as e:
        flash(e.message)

    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
