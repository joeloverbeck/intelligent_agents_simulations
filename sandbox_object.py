"""This module contains the definition of SandboxObject, which are objects
that can be interactable in the simulation
"""


class SandboxObject:
    """Represents an interactable object in a simulation
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self._action_status = None

    def set_action_status(self, action_status):
        """Sets the action status of the sandbox object

        Args:
            action_status (str): the new action status for the sandbox object
        """
        self._action_status = action_status

    def get_action_status(self):
        """Returns the sandbox object's action status

        Returns:
            str: the sandbox object's action status
        """
        return self._action_status

    def __str__(self):
        return f"Sandbox object: {self.name}"

    def __repr__(self) -> str:
        return f"Sandbox object: {self.name}"
