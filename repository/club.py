"""Manage club records."""

import json

from models import Club


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


class ClubRepository:
    def __init__(self, clubs, use_source_ref=True):
        self.use_source_ref = use_source_ref
        self.clubs = clubs

    @property
    def clubs(self):
        return self._clubs

    @clubs.setter
    def clubs(self, clubs):
        self._clubs = []
        for club in clubs:
            source_ref = club if self.use_source_ref else None
            self._clubs.append(
                Club(
                    club["name"],
                    club["email"],
                    club["points"],
                    source_ref=source_ref,
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

    def all(self):
        return (club for club in self.clubs)


def get_club_repository():
    clubs = loadClubs()
    return ClubRepository(clubs)
