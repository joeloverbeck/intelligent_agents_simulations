import datetime
from anytree import Node
from agent import Agent
from agent_utils import determine_agent_containing_location_identifier
from enums import ObservationType
from errors import AlgorithmError
from registered_updates import (
    AgentMovedToLocation,
    AgentUsingObject,
    SandboxObjectUpdated,
)


class ObservationSystem:
    """Class that handles the observation system of the simulation"""

    def __init__(self, current_timestamp):
        self._updates = []

        self._registered_update_handlers = {
            ObservationType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS: SandboxObjectUpdated(),
            ObservationType.AGENT_MOVED_TO_LOCATION: AgentMovedToLocation(),
            ObservationType.AGENT_USING_OBJECT: AgentUsingObject(),
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
        self, registered_update_type: ObservationType, update_data: dict
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
