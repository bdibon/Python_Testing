"""Define the club objects."""

PLACE_POINTS_COST = 1


class ClubException(Exception):
    """Exception raised by the club module."""

    def __init__(self, message):
        self.message = message


class Club:
    """Club model."""

    def __init__(self, name, email, points, source_ref=None):
        self.name = name
        self.email = email
        self.points = points

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
            raise ClubException("Club name must be a non-empty string.")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        email = str(email)

        if isinstance(email, str) and len(email):
            self._email = email
        else:
            raise ClubException("Club email must be a non-empty string.")

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        # Prevent direct update on points.
        if hasattr(self, "_points"):
            return

        try:
            self._points = int(points)
        except ValueError:
            raise ClubException("Points must be an integer.")

    @property
    def places_budget(self):
        return self._points // PLACE_POINTS_COST

    def credit_points(self, points):
        try:
            self._points += points
        except TypeError:
            raise ClubException("Points must be an integer.")

    def debit_points(self, points):
        try:
            if self._points - points >= 0:
                self._points -= points
            else:
                raise ClubException(
                    f"Club has {self._points}, cannot debit {points}."
                )
        except TypeError:
            raise ClubException("Points must be an integer.")

    def has_enough_points(self, number_of_places):
        return PLACE_POINTS_COST * number_of_places <= self._points

    def buy_places(self, number_of_places):
        if self.has_enough_points(number_of_places):
            self._points -= PLACE_POINTS_COST * number_of_places
        else:
            raise ClubException(
                f"{self._name} has {self._points} points, cannot buy {number_of_places} places."  # noqa E501
            )

    def save(self):
        if self._source_ref is not None:
            self._source_ref["name"] = self._name
            self._source_ref["email"] = self._email
            self._source_ref["points"] = self._points
