"""This module contains the definition of the Simulation class

"""
import datetime
from environment import load_environment_tree_from_json
from simulation_variables import load_simulation_variables


class Simulation:
    """This class handles running a simulation."""

    def __init__(self, name):
        self.name = name

        self.current_timestamp = None

        self._load_environment_function = load_environment_tree_from_json

        self._environment_tree = None

        self._minutes_advanced_each_step = None

    def set_load_environment_function(self, load_environment_function):
        """Sets the funciton that will load the environment tree

        Args:
            load_environment_function (function): the function that loads the environment tree
        """
        self._load_environment_function = load_environment_function

    def initialize(self):
        """Initializes the simulation"""
        self._load_simulation_variables()

        self._environment_tree = self._load_environment_function(self.name)

    def get_environment_tree(self):
        """Returns the simulation's environment tree

        Returns:
            Node: the root of the simulation's environment tree
        """
        return self._environment_tree

    def _load_simulation_variables(self):
        simulation_variables = load_simulation_variables(self.name)

        self.current_timestamp = simulation_variables["current_timestamp"]
        self._minutes_advanced_each_step = simulation_variables[
            "minutes_advanced_each_step"
        ]

    def step(self):
        """Executes one step of the simulation, advancing in the process the current timestamp
        by the specified value loaded from the variables.
        """
        self.current_timestamp = self.current_timestamp + datetime.timedelta(
            minutes=self._minutes_advanced_each_step
        )
