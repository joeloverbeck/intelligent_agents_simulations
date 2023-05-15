"""A location involved in a simulation

"""


class Location:
    """A location involved in a simulation."""

    def __init__(self, identifier, name, description):
        self.identifier = identifier
        self.name = name
        self.description = description

    def to_dict(self):
        """Returns the data of a Location instance as a dict

        Returns:
            dict: the data of the location as a dict
        """
        return {
            "identifier": self.identifier,
            "name": self.name,
            "description": self.description,
            "type": "Location",
        }

    def __str__(self):
        return f"Location: {self.name} ({self.identifier})"
