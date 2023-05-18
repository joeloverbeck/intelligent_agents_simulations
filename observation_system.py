import datetime
from abc import ABC, abstractmethod
from enum import Enum
from anytree import Node
from agent import Agent
from agent_utils import (
    determine_agent_containing_location_identifier,
    is_agent_in_same_location_as_another_agent,
)
from environment import find_node_by_identifier
from errors import AlgorithmError
from registered_update_type import RegisteredUpdateType


class RegisteredUpdateDataKey(Enum):
    """Identifies the key names of the dict that contains the registered update data"""

    IDENTIFIER = 1
    UPDATE_AGENT_NAME = 2


class RegisteredUpdate(ABC):
    """The abstract class for a registered update

    Args:
        ABC (ABC): the class that allows creating abstract classes using inheritance
    """

    @abstractmethod
    def handle_update(
        self,
        agent: Agent,
        update_data: dict,
        agent_containing_location_identifier: str,
        agents: list[Agent],
        environment_tree: Node,
    ):
        """Handles a registered update

        Args:
            agent (Agent): the agent for whom whether an observation triggers will be determined
            update_data (dict): the data associated with the update
            agent_containing_location_identifier (str): the identifier of the location that contains the agent
            agents (list): all the agents involved in the associated simulation
            environment_tree (Node): the main environment tree
        """

    def _does_observation_trigger(self, agent, update_data, agents):
        if update_data[RegisteredUpdateDataKey.UPDATE_AGENT_NAME] != agent.name:
            (
                is_agent_in_same_location,
                update_agent,
            ) = is_agent_in_same_location_as_another_agent(
                agent, update_data[RegisteredUpdateDataKey.UPDATE_AGENT_NAME], agents
            )

            if is_agent_in_same_location:
                return True, update_agent

        return False, None


class SandboxObjectUpdated(RegisteredUpdate):
    """A class that handles the case that a sandbox object has updated

    Args:
        RegisteredUpdate (RegisteredUpdate): the base registered update class
    """

    def handle_update(
        self,
        agent,
        update_data,
        agent_containing_location_identifier,
        _agents,
        environment_tree,
    ):
        # The identifier belongs to a sandbox object. Must locate the sandbox object's containing location
        matching_node = find_node_by_identifier(
            environment_tree, update_data[RegisteredUpdateDataKey.IDENTIFIER]
        )

        if (
            matching_node.parent.name.get_identifier()
            == agent_containing_location_identifier
        ):
            test_message = f"TEST: Agent {agent.name} witnessed RegisteredUpdateType.SANDBOX_OBJECT_UPDATED for sandbox object "
            test_message += (
                f"{matching_node.name.name}: {matching_node.name.get_action_status()}"
            )

            return {
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_IDENTIFIER: matching_node.name.get_identifier(),
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_ACTION_STATUS: matching_node.name.get_action_status(),
            }

        return {}


class AgentMovedToLocation(RegisteredUpdate):
    """The registered update for the case when an agent moved to a location

    Args:
        RegisteredUpdate (RegisteredUpdate): the abstract class for a registered update
    """

    def handle_update(
        self,
        agent,
        update_data,
        _agent_containing_location_identifier,
        agents,
        _environment_tree,
    ):
        does_observation_trigger, update_agent = self._does_observation_trigger(
            agent, update_data, agents
        )

        if does_observation_trigger:
            test_message = (
                f"TEST: Agent {agent.name} witnessed {self.__class__} for agent "
            )
            test_message += f"{update_agent.name}: {update_agent.get_action_status()}"

            return {
                ObservationTriggersResultKey.UPDATE_AGENT_NAME: update_agent.name,
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS: update_agent.get_action_status(),
            }

        return {}


class AgentUsingObject(RegisteredUpdate):
    """The registered update for the case of an agent using an object

    Args:
        RegisteredUpdate (RegisteredUpdate): the abstract class for a registered update
    """

    def handle_update(
        self,
        agent,
        update_data,
        agent_containing_location_identifier,
        agents,
        environment_tree,
    ):
        does_observation_trigger, update_agent = self._does_observation_trigger(
            agent, update_data, agents
        )

        if does_observation_trigger:
            test_message = (
                f"TEST: Agent {agent.name} witnessed {self.__class__} for agent "
            )
            test_message += f"{update_agent.name}: {update_agent.get_action_status()}"

            return {
                ObservationTriggersResultKey.UPDATE_AGENT_NAME: update_agent.name,
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS: update_agent.get_action_status(),
            }

        return {}


class ObservationTriggersResultKey(Enum):
    """The keys for the results of the determination of whether an observation triggers

    Args:
        Enum (Enum): the base Enum type
    """

    UPDATE_AGENT_NAME = 1
    UPDATE_AGENT_ACTION_STATUS = 2
    UPDATE_SANDBOX_OBJECT_IDENTIFIER = 3
    UPDATE_SANDBOX_OBJECT_ACTION_STATUS = 4


class ObservationSystem:
    """Class that handles the observation system of the simulation"""

    def __init__(self, current_timestamp):
        self._updates = []

        self._registered_update_handlers = {
            RegisteredUpdateType.SANDBOX_OBJECT_UPDATED: SandboxObjectUpdated(),
            RegisteredUpdateType.AGENT_MOVED_TO_LOCATION: AgentMovedToLocation(),
            RegisteredUpdateType.AGENT_USING_OBJECT: AgentUsingObject(),
        }

        self.last_update_timestamp = current_timestamp

    def check_timestamp(
        self, current_timestamp: datetime.datetime, minutes_advanced_each_step: int
    ):
        """Checks a timestamp. If that timestamp is greater than timestamp - minutes advanced each step,
        then the updates list must be rebuilt.

        Args:
            current_timestamp (datetime.datetime): the current timestamp
            minutes_advanced_each_step (int): how many minutes are advanced in each step of the simulation
        """
        if self.last_update_timestamp < current_timestamp - datetime.timedelta(
            minutes=minutes_advanced_each_step
        ):
            # must rebuild the updates list
            self.last_update_timestamp = current_timestamp

            self._updates = []

    def register_update(
        self, registered_update_type: RegisteredUpdateType, update_data: dict
    ):
        """Registers an update that happened in the simulation

        Args:
            registered_update_type (RegisteredUpdateType): the type of update that will be registered
            update_data (dict): the data associated with the update
        """
        self._updates.append((registered_update_type, update_data))

    def determine_if_observation_triggers(
        self,
        agent: Agent,
        agents: list[Agent],
        environment_tree: Node,
    ):
        """Determines if an observation will trigger given the registered updates

        Args:
            agent (Agent): the agent for whom an observation may trigger
            agents (list): all the agents involved in a simulation
            environment_tree (Node): the main environment tree
        """
        if len(agents) == 0:
            raise AlgorithmError(
                f"The function {self.determine_if_observation_triggers.__name__} received empty list of agents."
            )

        agent_containing_location_identifier = (
            determine_agent_containing_location_identifier(agent)
        )

        for registered_update_type, update_data in self._updates:
            handler = self._registered_update_handlers[registered_update_type]

            return handler.handle_update(
                agent,
                update_data,
                agent_containing_location_identifier,
                agents,
                environment_tree,
            )

        return {}
