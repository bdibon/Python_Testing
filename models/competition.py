"""Define the competition logic."""

from datetime import datetime


class CompetitionException(Exception):
    """Exception raised by the competition module."""

    def __init__(self, message):
        self.message = message


class Competition:
    def __init__(self, name, date, numberOfPlaces, source_ref=None):
        self.name = name
        self.date = date
        self.numberOfPlaces = numberOfPlaces

        self._source_ref = source_ref

    # Retrocompatibility with dict behavior.
    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        name = str(name)

        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise CompetitionException(
                "Competition name must be a non-empty string."
            )

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        try:
            d = datetime.fromisoformat(date)
            self._date = d
        except ValueError:
            raise CompetitionException("Invalid date.")

    @property
    def numberOfPlaces(self):
        return self._numberOfPlaces

    @numberOfPlaces.setter
    def numberOfPlaces(self, numberOfPlaces):
        # Prevent direct update on numberOfPlaces.
        if hasattr(self, "_numberOfPlaces"):
            return

        try:
            self._numberOfPlaces = int(numberOfPlaces)
        except ValueError:
            raise CompetitionException("Number of places must be an integer.")

    def _withdraw_places(self, placesRequired):
        self._numberOfPlaces -= placesRequired
        self.save()

    def book_places(self, club, placesRequired):
        if self.is_over():
            raise CompetitionException("Competition is over.")

        if self._numberOfPlaces >= placesRequired:
            club.buy_places(placesRequired)
            club.save()
            self._withdraw_places(placesRequired)
        else:
            raise CompetitionException("Not enough places left.")

    def is_over(self):
        return self._date < datetime.now()

    def save(self):
        if self._source_ref is not None:
            self._source_ref["name"] = self._name
            self._source_ref["date"] = self._date.isoformat(sep=" ")
            self._source_ref["numberOfPlaces"] = self._numberOfPlaces
