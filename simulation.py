"""This module contains the definition of the Simulation class

"""
import datetime
from action_statuses import produce_action_statuses_for_agent_and_sandbox_object
from agent_utils import load_agents
from character_summaries import request_character_summary
from environment import load_environment_tree_from_json
from initialization import set_initial_state_of_agent
from simulation_variables import load_simulation_variables


class Simulation:
    """This class handles running a simulation."""

    def __init__(self, name):
        self.name = name

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

    def update(self, message: dict):
        """Receives an update from an observed instance

        Args:
            message (dict): the message attached to the update of an observed entity
        """
        # There could be various types of messages sent.
        # Depending on the 'type' attribute of the dict, we'll know
        # what to do and what attributes the passed dict has.

    def step(self):
        """Executes one step of the simulation, advancing in the process the current timestamp
        by the specified value loaded from the variables.
        """
        self.current_timestamp = self.current_timestamp + datetime.timedelta(
            minutes=self._minutes_advanced_each_step
        )
