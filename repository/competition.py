"""Manage competition records."""

import json

from models import Competition


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


class CompetitionRepository:
    def __init__(self, competitions):
        self.competitions = competitions

    @property
    def competitions(self):
        return self._competitions

    @competitions.setter
    def competitions(self, competitions):
        self._competitions = []
        for competition in competitions:
            self._competitions.append(
                Competition(
                    competition["name"],
                    competition["date"],
                    competition["numberOfPlaces"],
                    source_ref=competition,
                )
            )

    def get_competition_by_name(self, name):
        try:
            competition = next(
                (c for c in self._competitions if c.name == name)
            )
            return competition
        except Exception:
            return None


def get_competition_repository():
    competitions = loadCompetitions()
    return CompetitionRepository(competitions)
