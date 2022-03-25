"""Manage competition records."""

import json

from models import Competition


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


class CompetitionRepository:
    def __init__(self, competitions, use_source_ref=True):
        self.use_source_ref = use_source_ref
        self.competitions = competitions

    @property
    def competitions(self):
        return self._competitions

    @competitions.setter
    def competitions(self, competitions):
        self._competitions = []
        for competition in competitions:
            source_ref = competition if self.use_source_ref else None
            self._competitions.append(
                Competition(
                    competition["name"],
                    competition["date"],
                    competition["numberOfPlaces"],
                    source_ref=source_ref,
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
