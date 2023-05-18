"""This module contains the definition of the Simulation class

"""
import datetime
import os
from anytree import Node
from action_statuses import (
    determine_if_agent_will_use_sandbox_object,
    produce_action_statuses_for_agent_and_sandbox_object,
)
from agent_utils import (
    load_agents,
    update_agent_current_location_node,
)
from character_summaries import request_character_summary
from enums import ObservationType, UpdateType
from environment import (
    load_environment_tree_from_json,
)
from environment_tree_integrity import calculate_number_of_nodes_in_tree
from errors import AlgorithmError, DirectoryDoesntExistError, InvalidParameterError
from initialization import set_initial_state_of_agent
from navigation import perform_agent_movement
from observation_system import ObservationSystem
from process_updates import process_updates
from simulation_variables import load_simulation_variables, save_current_timestamp


class Simulation:
    """This class handles running a simulation."""

    def __init__(self, name):
        self.name = name

        # Crash directly if the appropriate directory for the simulation doesn't exist.
        simulation_path = f"simulations/{self.name.lower()}"

        if not os.path.exists(simulation_path):
            raise DirectoryDoesntExistError(
                f"The directory '{simulation_path}' does not exist."
            )

        self._environment_tree = None

        self._number_of_nodes_in_tree = None

        self._agents = []

        self._observation_system = None

        self.current_timestamp = None
        self._minutes_advanced_each_step = None

        self._load_environment_function = load_environment_tree_from_json
        self._request_character_summary_function = request_character_summary
        self._produce_action_statuses_for_agent_and_sandbox_object_function = (
            produce_action_statuses_for_agent_and_sandbox_object
        )

    def set_load_environment_function(self, load_environment_function):
        """Sets the function that will load the environment tree

        Args:
            load_environment_function (function): the function that loads the environment tree
        """
        self._load_environment_function = load_environment_function

    def set_request_character_summary_function(
        self, request_character_summary_function
    ):
        """Sets the request character summary function

        Args:
            request_character_summary_function (function): the request character summary function
        """
        self._request_character_summary_function = request_character_summary_function

    def set_produce_action_statuses_for_agent_and_sandbox_object_function(
        self, produce_action_statuses_for_agent_and_sandbox_object_function
    ):
        """Sets the function that produces statuses for agents and sandbox objects

        Args:
            produce_action_statuses_for_agent_and_sandbox_object_function (function): the function that produces action statuses for agents and sandbox objects
        """
        self._produce_action_statuses_for_agent_and_sandbox_object_function = (
            produce_action_statuses_for_agent_and_sandbox_object_function
        )

    def initialize(self):
        """Initializes the simulation"""
        self._load_simulation_variables()

        self._environment_tree = self._load_environment_function(
            self.name, "environment", self
        )

        self._number_of_nodes_in_tree = calculate_number_of_nodes_in_tree(
            self._environment_tree
        )

        self._observation_system = ObservationSystem(self.current_timestamp)

        self._agents = load_agents(self.name, self)

        # We need to ensure that the memories of each agent exist. If they don't,
        # we need to try to generate them from the 'seed_memories.txt'
        for agent in self._agents:
            if agent.get_action_status() is None:
                set_initial_state_of_agent(
                    agent,
                    self.current_timestamp,
                    self._request_character_summary_function,
                    self._produce_action_statuses_for_agent_and_sandbox_object_function,
                )

    def get_environment_tree(self):
        """Returns the simulation's environment tree

        Returns:
            Node: the root of the simulation's environment tree
        """
        return self._environment_tree

    def set_environment_tree(self, environment_tree: Node):
        """Sets the environment tree of the simulation"""
        if self._number_of_nodes_in_tree != calculate_number_of_nodes_in_tree(
            environment_tree
        ):
            error_message = f"The function {self.set_environment_tree.__name__} received an environment tree that violated the integrity. "
            error_message += f"Expected {self._number_of_nodes_in_tree} nodes, got {calculate_number_of_nodes_in_tree(environment_tree)}."
            raise AlgorithmError(error_message)

        self._environment_tree = environment_tree

    def get_agents(self):
        """Returns the list of agents of the simulation

        Returns:
            list: the list of agents of the simulation
        """
        return self._agents

    def _load_simulation_variables(self):
        simulation_variables = load_simulation_variables(self.name)

        self.current_timestamp = simulation_variables["current_timestamp"]
        self._minutes_advanced_each_step = simulation_variables[
            "minutes_advanced_each_step"
        ]

    def update(self, update_message: dict):
        """Receives an update from an observed instance

        Args:
            message (dict): the message attached to the update of an observed entity
        """
        # There could be various types of messages sent.
        # Depending on the 'type' attribute of the dict, we'll know
        # what to do and what attributes the passed dict has.
        if not isinstance(update_message, dict):
            raise InvalidParameterError(
                f"The function {self.update.__name__} expected 'message' to be a dict, but it was: {update_message}"
            )

        process_updates(self, update_message)

    def register_update(
        self, registered_update_type: ObservationType, update_data: dict
    ):
        """Registers an update with the observation system

        Args:
            registered_update_type (RegisteredUpdateType): the type of update that will get registered
            update_data (dict): the data associated with the update
        """
        self._observation_system.register_update(registered_update_type, update_data)

    def step(self):
        """Executes one step of the simulation, advancing in the process the current timestamp
        by the specified value loaded from the variables.
        """
        # Refresh the dict of updates
        self.current_timestamp = self.current_timestamp + datetime.timedelta(
            minutes=self._minutes_advanced_each_step
        )

        self._observation_system.check_timestamp(
            self.current_timestamp, self._minutes_advanced_each_step
        )

        save_current_timestamp(self.name, self.current_timestamp)

        for agent in self._agents:
            # If the agent was moving, we gotta move the agent to the next node.
            perform_agent_movement(agent)

            # After the movement, the agent should have its current location (that may be a Sandbox Object)
            # updated with the matching node values of the simulation's environment tree
            update_agent_current_location_node(agent, self.get_environment_tree())

            self._observation_system.determine_if_observation_triggers(
                agent, self.get_agents(), self.get_environment_tree()
            )

            # As long as the agent isn't already using an object, it must be checked if he or she should use one.
            if (
                agent.get_using_object() is None
                and agent.get_planned_action() is not None
            ):
                determine_if_agent_will_use_sandbox_object(agent, self.name)
            else:
                agent.notify(
                    {"type": UpdateType.AGENT_CONTINUES_USING_OBJECT, "agent": agent}
                )
