"""Contains the Agent class, which defines an intelligent agent involved in a simulation.

"""
from anytree import Node
from environment_tree_integrity import calculate_number_of_nodes_in_tree
from errors import AlgorithmError, InvalidParameterError, MissingCharacterSummaryError
from update_type import UpdateType


class Agent:
    """An intelligent agent involved in a simulation."""

    def __init__(self, name, age, current_location_node, environment_tree):
        if current_location_node is None:
            raise InvalidParameterError(
                "An agent should be initialized with a 'current_location_node'."
            )
        if environment_tree is None:
            raise InvalidParameterError(
                "An agent should be loaded with an 'environment_tree'."
            )

        self.name = name
        self.age = age

        self._environment_tree = environment_tree

        self._number_of_nodes_in_tree = calculate_number_of_nodes_in_tree(
            self._environment_tree
        )

        self._current_location_node = current_location_node

        self._planned_action = None
        self._action_status = None
        self._destination_node = None
        self._using_object = None

        self._character_summary = None

        self._observers = []

    def set_environment_tree(self, environment_tree):
        """Sets the environment tree of the agent.

        Args:
            environment_tree (Node): the root of the environment tree for the agent
        """
        # Careful: we need to ensure that we won't set an environment tree that violates
        # the integrity of what we expected.
        if self._number_of_nodes_in_tree != calculate_number_of_nodes_in_tree(
            environment_tree
        ):
            error_message = f"The function {self.set_environment_tree.__name__} received an 'environment_tree' that would violate the integrity of the tree."
            error_message += f" Expected {self._number_of_nodes_in_tree} nodes, and got {calculate_number_of_nodes_in_tree(environment_tree)}."
            raise AlgorithmError()

        self._environment_tree = environment_tree

    def get_environment_tree(self):
        """Returns the environment tree of the agent

        Returns:
            Node: returns the root node of the agent's environment tree
        """
        return self._environment_tree

    def set_current_location_node(self, current_location_node):
        """Sets the agent's current location

        Args:
            current_location_node (Node): the node that will be set as the current ocation
        """
        if not isinstance(current_location_node, Node):
            error_message = f"The function {self.set_current_location_node.__name__} expected 'current_location_node' to be a Node, but it was: {current_location_node}"
            raise InvalidParameterError(error_message)

        self._current_location_node = current_location_node

        # Needs to notify the update
        self.notify(
            {
                "type": UpdateType.AGENT_CHANGED_CURRENT_LOCATION_NODE,
                "agent": self,
            }
        )

    def get_current_location_node(self):
        """Retrieves the agent's current location node

        Returns:
            Node: the agent's current location node
        """
        return self._current_location_node

    def set_planned_action(self, planned_action: str, silent=False):
        """Sets the planned action for the agent

        Args:
            planned_action (str): the planned action, in natural English
            silent (bool, optional): if silent, the update won't be notified to subscribers. Defaults to False.
        """
        self._planned_action = planned_action

        if not silent:
            # needs to notify about the update
            self.notify(
                {"type": UpdateType.AGENT_CHANGED_PLANNED_ACTION, "agent": self}
            )

    def get_planned_action(self):
        """Returns the agent's planned action

        Returns:
            str: the agent's planned action
        """
        return self._planned_action

    def set_action_status(self, action_status, silent=False):
        """Sets the agent's action status

        Args:
            action_status (str): the action status for the agent
        """
        self._action_status = action_status

        if not silent:
            # needs to notify about the update.
            self.notify({"type": UpdateType.AGENT_CHANGED_ACTION_STATUS, "agent": self})

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

        # Needs to notify of this update
        self.notify({"type": UpdateType.AGENT_CHANGED_CHARACTER_SUMMARY, "agent": self})

    def set_using_object(self, sandbox_object_node, silent=False):
        """Sets the object node that the agent will be marked as using.

        Args:
            sandbox_object_node (Node): the sandbox object node that the agent will be marked as using
        """
        self._using_object = sandbox_object_node

        if not silent:
            # notify of this change
            self.notify({"type": UpdateType.AGENT_CHANGED_USING_OBJECT, "agent": self})

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

    def set_destination_node(self, node: Node, silent=False):
        """Sets the destination node of the agent

        Args:
            node (Node): the node that will be set as the destination node of the agent
            silent (bool, optional): if silent, this update won't be notified to subscribers. Defaults to False.

        Raises:
            AlgorithmError: if the node attempted to set as destination node would be the same as the current location node
        """
        # Note: if the destination node about to be set is equal to the
        # current location node, that should never happen
        if node is not None:
            if self._current_location_node.name == node.name:
                error_message = (
                    f"Was going to set the node {node} as the destination node, "
                )
                error_message += f"even though it's the same as the current location node: {self._current_location_node}"
                raise AlgorithmError(error_message)

        self._destination_node = node

        if not silent:
            # notify of this change
            self.notify(
                {"type": UpdateType.AGENT_CHANGED_DESTINATION_NODE, "agent": self}
            )

    def get_destination_node(self):
        """Retrieves the agent's destination node

        Returns:
            Node: the agent's destination node
        """
        return self._destination_node

    def subscribe(self, observer):
        """Allows an object to subscribe to this Agent

        Args:
            observer (Object): the instance that will subscribe to this instance
        """
        if observer is not None:
            self._observers.append(observer)

    def notify(self, message: dict):
        """Notifies the subscribers of an update

        Args:
            message (dict): data relevant to the update

        Raises:
            InvalidParameterError: if the message passed is not a dict
        """
        if not isinstance(message, dict):
            raise InvalidParameterError(
                f"The function {self.notify.__name__} expected 'message' to be a dict, but it was: {message}"
            )

        for observer in self._observers:
            observer.update(message)

    def to_dict(self):
        """Converts an instance of this class into a dict for serialization

        Returns:
            dict: the dict version of an instance of this class
        """
        return {
            "age": self.age,
            "planned_action": self._planned_action,
            "action_status": self._action_status,
            "current_location_node": self._current_location_node.name.get_identifier()
            if self._current_location_node
            else None,
            "destination_node": self._destination_node.name.get_identifier()
            if self._destination_node
            else None,
            "using_object": self._using_object.name.get_identifier()
            if self._using_object
            else None,
        }

    def __str__(self):
        return f"Agent: {self.name} ({self.age}) | Current location: {self._current_location_node.name.name}"
