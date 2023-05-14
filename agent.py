"""Contains the Agent class, which defines an intelligent agent involved in a simulation.

"""
from errors import MissingCharacterSummaryError


class Agent:
    """An intelligent agent involved in a simulation."""

    def __init__(self, name, age, current_location, environment_tree):
        self.name = name
        self.age = age
        self.current_location = current_location
        self.environment_tree = environment_tree

        self._character_summary = None

    def set_character_summary(self, character_summary):
        """Sets the character summary of the agent.

        Args:
            character_summary (str): the character summary in text format.
        """
        self._character_summary = character_summary

    def get_character_summary(self):
        """Returns the agent's character summary.

        Raises:
            MissingCharacterSummaryError: if attempted to retrieve the character summary when it didn't exist.

        Returns:
            str: the character's summary description.
        """
        if self._character_summary is None:
            raise MissingCharacterSummaryError(
                f"Requested the character summary of agent {self.name}, but it hadn't been set."
            )

        return self._character_summary

    def __str__(self):
        return f"Agent: {self.name} ({self.age}) | Current location: {self.current_location.name.name}"
