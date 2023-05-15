"""Contains the Agent class, which defines an intelligent agent involved in a simulation.

"""
from errors import MissingCharacterSummaryError


class Agent:
    """An intelligent agent involved in a simulation."""

    def __init__(self, name, age, current_location_node, environment_tree):
        self.name = name
        self.age = age

        self.environment_tree = environment_tree

        self._current_location_node = current_location_node
        self._action_status = None
        self._destination_node = None
        self._using_object = None

        self._character_summary = None

    def set_current_location_node(self, current_location_node):
        """Sets the agent's current location

        Args:
            current_location_node (Node): the node that will be set as the current ocation
        """
        self._current_location_node = current_location_node

    def get_current_location_node(self):
        """Retrieves the agent's current location node

        Returns:
            Node: the agent's current location node
        """
        return self._current_location_node

    def set_action_status(self, action_status):
        """Sets the agent's action status

        Args:
            action_status (str): the action status for the agent
        """
        self._action_status = action_status

    def get_action_status(self):
        """Returns the agent's action status

        Returns:
            str: the agent's action status
        """
        return self._action_status

    def set_character_summary(self, character_summary):
        """Sets the character summary of the agent.

        Args:
            character_summary (str): the character summary in text format.
        """
        self._character_summary = character_summary

    def set_using_object(self, sandbox_object_node):
        """Sets the object node that the agent will be marked as using.

        Args:
            sandbox_object_node (Node): the sandbox object node that the agent will be marked as using
        """
        self._using_object = sandbox_object_node

    def get_using_object(self):
        """Returns the agent's 'using_object' value

        Returns:
            Node: the agent's 'using_object' value
        """
        return self._using_object

    def has_character_summary(self):
        """Determines whether or not the agent has a character summary set.

        Returns:
            bool: True if the character summary is set, False otherwise
        """

        if self._character_summary is None:
            return False

        return True

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

    def set_destination_node(self, node):
        """Sets the destination node of the agent.

        Args:
            node (Node): the node that will be set as the destination node
        """
        self._destination_node = node

    def get_destination_node(self):
        """Retrieves the agent's destination node

        Returns:
            Node: the agent's destination node
        """
        return self._destination_node

    def __str__(self):
        return f"Agent: {self.name} ({self.age}) | Current location: {self._current_location_node.name.name}"
