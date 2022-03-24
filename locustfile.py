import json

from locust import HttpUser, task, between


with open("clubs.json") as club_file:
    club_list = json.load(club_file)["clubs"]


with open("competitions.json") as competition_file:
    competition_list = json.load(competition_file)["competitions"]


class SecretaryUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post(
            "/showSummary",
            data={
                "email": club_list[0]["email"],
            },
        )

    @task
    def book(self):
        competition_name = competition_list[0]["name"]
        club_name = club_list[0]["name"]
        self.client.get(f"/book/{competition_name}/{club_name}")

    @task
    def purchasePlaces(self):
        competition_name = competition_list[0]["name"]
        club_name = club_list[0]["name"]
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": competition_name,
                "club": club_name,
                "places": 1,
            },
        )

    @task
    def displayPoints(self):
        self.client.get("/displayPoints")

    @task
    def logout(self):
        self.client.get("/logout")
