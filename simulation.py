"""This module contains the definition of the Simulation class

"""
import datetime
import os
from action_statuses import (
    determine_if_agent_will_use_sandbox_object,
    produce_action_statuses_for_agent_and_sandbox_object,
)
from agent_utils import load_agents, save_agents_to_json, substitute_agent
from character_summaries import request_character_summary
from environment import (
    find_node_by_identifier,
    load_environment_tree_from_json,
    save_environment_tree_to_json,
    substitute_node,
)
from errors import DirectoryDoesntExistError, InvalidParameterError
from initialization import set_initial_state_of_agent
from logging_messages import log_simulation_message
from navigation import perform_agent_movement
from simulation_variables import load_simulation_variables, save_current_timestamp
from update_type import UpdateType


class Simulation:
    """This class handles running a simulation."""

    def __init__(self, name):
        self.name = name

        # Crash directly if the appropriate directory for the simulation doesn't exist.
        simulation_path = f"simulations/{self.name.lower()}"

        if not os.path.exists(simulation_path):
            raise DirectoryDoesntExistError(f"The directory '{simulation_path}' does not exist.")

        self._environment_tree = None
        self._agents = []

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

        self._environment_tree = self._load_environment_function(self.name, self)

        self._agents = load_agents(self.name, self._environment_tree, self)

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

        if update_message["type"] == UpdateType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS:
            message = f"{self.current_timestamp.isoformat()} {update_message['sandbox_object'].name} "
            message += f"changed action status to: {update_message['sandbox_object'].get_action_status()}"
            log_simulation_message(self.name, message)

            # Just in case there is some weird "value updated in agent's node but not in the simulation's" stuff going on,
            # we exchange the node in the simulation for the one passed in this message.
            substitute_node(self._environment_tree, update_message["sandbox_object"])
            save_environment_tree_to_json(self.name, self._environment_tree)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_CURRENT_LOCATION_NODE:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed "
            message += f"the current location node to: {update_message['agent'].get_current_location_node()}"
            log_simulation_message(self.name, message)

            substitute_agent(self._agents, update_message["agent"])
            save_agents_to_json(self.name, self._agents)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_ACTION_STATUS:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed the action status to: {update_message['agent'].get_action_status()}"
            log_simulation_message(self.name, message)

            substitute_agent(self._agents, update_message["agent"])
            save_agents_to_json(self.name, self._agents)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_CHARACTER_SUMMARY:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed the character "
            message += f"summary to: {update_message['agent'].get_character_summary()}"
            log_simulation_message(self.name, message)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_USING_OBJECT:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed using object to: {update_message['agent'].get_using_object()}"
            log_simulation_message(self.name, message)

            substitute_agent(self._agents, update_message["agent"])
            save_agents_to_json(self.name, self._agents)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_DESTINATION_NODE:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed destination node to: {update_message['agent'].get_destination_node()}"
            log_simulation_message(self.name, message)

            substitute_agent(self._agents, update_message["agent"])
            save_agents_to_json(self.name, self._agents)
        elif update_message["type"] == UpdateType.AGENT_REACHED_DESTINATION:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} reached the destination: {update_message['destination_node'].name}"
            log_simulation_message(self.name, message)
        elif update_message["type"] == UpdateType.AGENT_PRODUCED_ACTION:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} produced action: {update_message['action']}"
            log_simulation_message(self.name, message)
        elif update_message["type"] == UpdateType.AGENT_NEEDS_TO_MOVE:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} needs to move to: {update_message['agent'].get_destination_node()}"
            log_simulation_message(self.name, message)
        elif update_message["type"] == UpdateType.AGENT_WILL_USE_SANDBOX_OBJECT:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} will use sandbox object: {update_message['agent'].get_current_location_node()}"
            log_simulation_message(self.name, message)
        elif update_message["type"] == UpdateType.AGENT_CHANGED_PLANNED_ACTION:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} changed planned action: {update_message['agent'].get_planned_action()}"
            log_simulation_message(self.name, message)

            substitute_agent(self._agents, update_message["agent"])
            save_agents_to_json(self.name, self._agents)
        elif update_message["type"] == UpdateType.AGENT_CONTINUES_USING_OBJECT:
            message = f"{self.current_timestamp.isoformat()} {update_message['agent'].name} continues using object: {update_message['agent'].get_using_object()}"
            log_simulation_message(self.name, message)

    def step(self):
        """Executes one step of the simulation, advancing in the process the current timestamp
        by the specified value loaded from the variables.
        """
        self.current_timestamp = self.current_timestamp + datetime.timedelta(
            minutes=self._minutes_advanced_each_step
        )

        save_current_timestamp(self.name, self.current_timestamp)

        for agent in self._agents:
            # if the agent was moving, we gotta move the agent to the next node.
            perform_agent_movement(agent)

            # substitute the current_location_node of the agent by a fresh one from the environment tree,
            # which presumably is updated
            matching_node = find_node_by_identifier(
                self._environment_tree,
                agent.get_current_location_node().name.identifier,
            )

            substitute_node(agent.get_environment_tree(), matching_node.name)

            # As long as the agent isn't already using an object, it must be checked if he or she should
            if agent.get_using_object() is None and agent.get_planned_action() is not None:
                determine_if_agent_will_use_sandbox_object(agent)
            else:
                agent.notify(
                    {"type": UpdateType.AGENT_CONTINUES_USING_OBJECT, "agent": agent}
                )
