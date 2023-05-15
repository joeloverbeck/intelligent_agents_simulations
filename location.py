"""A location involved in a simulation

"""


class Location:
    """A location involved in a simulation."""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Location: {self.name}"
