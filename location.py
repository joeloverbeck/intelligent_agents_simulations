"""A location involved in a simulation

"""


from errors import InvalidParameterError


class Location:
    """A location involved in a simulation."""

    def __init__(self, identifier, name, description):
        if identifier is None:
            raise InvalidParameterError(
                "Attempted to set a None identifier for a Location."
            )

        self._identifier = identifier
        self.name = name
        self.description = description

    def get_identifier(self):
        return self._identifier

    def to_dict(self):
        """Returns the data of a Location instance as a dict

        Returns:
            dict: the data of the location as a dict
        """
        return {
            "identifier": self._identifier,
            "name": self.name,
            "description": self.description,
            "type": "Location",
        }

    def __str__(self):
        return f"Location: {self.name} ({self._identifier})"
