from flask import Flask, render_template, request, redirect, flash, url_for

from models import ClubException, CompetitionException
from repository import get_competition_repository, get_club_repository


def create_app(club_repo=None, competition_repo=None):
    app = Flask(__name__)
    app.secret_key = "something_special"

    if club_repo is None:
        club_repo = get_club_repository()

    if competition_repo is None:
        competition_repo = get_competition_repository()
    competitions = competition_repo.competitions

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        email = request.form.get("email", None)
        club = club_repo.get_club_by_email(email)

        if club:
            return render_template(
                "welcome.html", club=club, competitions=competitions
            )
        else:
            flash("Invalid credentials.")
            return render_template("index.html")

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        foundClub = club_repo.get_club_by_name(club)
        foundCompetition = competition_repo.get_competition_by_name(
            competition
        )

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

        competition = competition_repo.get_competition_by_name(
            competition_name
        )
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

    @app.route("/displayPoints")
    def displayPoints():
        return render_template("points_board.html", clubs=club_repo.all())

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app


app = create_app()
