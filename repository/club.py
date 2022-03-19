"""Manage club records."""

import json

from models import Club


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


class ClubRepository:
    def __init__(self, clubs):
        self.clubs = clubs

    @property
    def clubs(self):
        return self._clubs

    @clubs.setter
    def clubs(self, clubs):
        self._clubs = []
        for club in clubs:
            self._clubs.append(
                Club(
                    club["name"],
                    club["email"],
                    club["points"],
                    source_ref=club,
                )
            )

    def get_club_by_name(self, name):
        try:
            club = next((c for c in self._clubs if c.name == name))
            return club
        except Exception:
            return None

    def get_club_by_email(self, email):
        try:
            club = next((c for c in self._clubs if c.email == email))
            return club
        except Exception:
            return None


def get_club_repository():
    clubs = loadClubs()
    return ClubRepository(clubs)
