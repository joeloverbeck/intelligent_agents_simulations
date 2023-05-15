import datetime
import unittest

from anytree import Node
from location import Location
from simulation import Simulation


class TestSimulation(unittest.TestCase):
    def test_can_create_simulation(self):
        comparison_time = datetime.datetime(2023, 5, 12, 10, 55, 45)

        simulation = Simulation("test_1")

        simulation.initialize()

        self.assertEqual(simulation.name, "test_1")
        self.assertEqual(simulation.current_timestamp, comparison_time)

    def test_can_retrieve_a_simulations_environment_tree(self):
        town = Node(Location("town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)

        simulation.initialize()

        environment_tree = simulation.get_environment_tree()

        self.assertEqual(town.name, environment_tree.name)

    def test_can_step_the_simulation(self):
        town = Node(Location("town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)

        simulation.initialize()

        simulation.step()

        comparison_time = datetime.datetime(2023, 5, 12, 11, 25, 45)

        self.assertEqual(simulation.current_timestamp, comparison_time)


if __name__ == "__main__":
    unittest.main()
