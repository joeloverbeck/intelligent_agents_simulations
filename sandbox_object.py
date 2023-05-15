"""This module contains the definition of SandboxObject, which are objects
that can be interactable in the simulation
"""


from errors import InvalidParameterError


class SandboxObject:
    """Represents an interactable object in a simulation"""

    def __init__(self, identifier, name, description):
        self.identifier = identifier
        self.name = name
        self.description = description

        self._action_status = None

        self._observers = []

    def to_dict(self):
        """Returns the sandbox object's data as a dict

        Returns:
            dict: the sandbox object's data as a dict
        """
        return {
            "identifier": self.identifier,
            "name": self.name,
            "description": self.description,
            "type": "SandboxObject",
            "action_status": self._action_status,
        }

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

    def subscribe(self, observer):
        if observer is not None:
            self._observers.append(observer)

    def notify(self, message):
        if not isinstance(message, dict):
            raise InvalidParameterError(
                f"The function {self.notify.__name__} expected 'message' to be a dict, but it was: {message}"
            )

        for observer in self._observers:
            observer.update(message)

    def __str__(self):
        return f"Sandbox object: {self.name} ({self.identifier})"

    def __repr__(self) -> str:
        return f"Sandbox object: {self.name} ({self.identifier})"
