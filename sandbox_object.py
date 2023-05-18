"""This module contains the definition of SandboxObject, which are objects
that can be interactable in the simulation
"""


from enums import UpdateMessageKey, UpdateType
from errors import InvalidParameterError


class SandboxObject:
    """Represents an interactable object in a simulation"""

    def __init__(self, identifier, name, description):
        if identifier is None:
            raise InvalidParameterError(
                "Attempted to initialize a SandboxObject with a None identifier."
            )

        self._identifier = identifier
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
            "identifier": self._identifier,
            "name": self.name,
            "description": self.description,
            "type": "SandboxObject",
            "action_status": self._action_status,
        }

    def get_identifier(self):
        """Returns the identifier of the SandboxObject

        Returns:
            str: the identifier of the SandboxObject
        """
        return self._identifier

    def set_action_status(
        self, action_status: str, triggering_agent_name: str, silent=False
    ):
        """Sets the action status of the SandboxObject

        Args:
            action_status (str): the new action status for the SandboxObject
            triggering_agent_identifier (str): the identifier of the agent that triggers the change
            silent (bool, optional): whether or not the change should be notified to subscribers. Defaults to False.
        """
        self._action_status = action_status

        # Note: set_action_status also gets called while building the environment tree.
        # We don't want to notify anyone of that.
        if not silent:
            self._notify(
                {
                    UpdateMessageKey.TYPE: UpdateType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS,
                    UpdateMessageKey.SANDBOX_OBJECT: self,
                    UpdateMessageKey.OBSERVED_AGENT_NAME: triggering_agent_name,
                }
            )

    def get_action_status(self):
        """Returns the sandbox object's action status

        Returns:
            str: the sandbox object's action status
        """
        return self._action_status

    def subscribe(self, observer):
        """Allows an object to subscribe to this Agent

        Args:
            observer (Object): the instance that will subscribe to this instance
        """
        if observer is not None:
            self._observers.append(observer)

    def _notify(self, message: dict):
        """Notifies the subscribers of an update

        Args:
            message (dict): data relevant to the update

        Raises:
            InvalidParameterError: if the message passed is not a dict
        """
        if not isinstance(message, dict):
            raise InvalidParameterError(
                f"The function {self._notify.__name__} expected 'message' to be a dict, but it was: {message}"
            )

        for observer in self._observers:
            observer.update(message)

    def __str__(self):
        return f"Sandbox object: {self.name} ({self._identifier}) | description: {self.description}"

    def __repr__(self) -> str:
        return f"Sandbox object: {self.name} ({self._identifier}) | description: {self.description}"
