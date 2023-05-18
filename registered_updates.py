from abc import ABC, abstractmethod
from anytree import Node
from agent import Agent
from agent_utils import is_agent_in_same_location_as_another_agent
from enums import ObservationDataKey, RegisteredUpdateDataKey
from environment import find_node_by_identifier


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
                ObservationDataKey.OBSERVED_SANDBOX_OBJECT_IDENTIFIER: matching_node.name.get_identifier(),
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
                ObservationDataKey.OBSERVED_AGENT_NAME: update_agent.name,
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS: update_agent.get_action_status(),
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
                ObservationDataKey.OBSERVED_AGENT_NAME: update_agent.name,
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS: update_agent.get_action_status(),
            }

        return {}
