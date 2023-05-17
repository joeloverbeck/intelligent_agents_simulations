import datetime
from types import NoneType
import unittest

from anytree import Node
from location import Location
from simulation import Simulation


def fake_request_character_summary_function(
    agent, _current_timestamp, _memories_raw_data, _index
):
    return f"{agent.name} (Age: {agent.age})"


def fake_produce_action_statuses_for_agent_and_sandbox_object_function(
    _agent,
    _current_timestamp,
    _create_action_function,
    _determine_sandbox_object_destination_from_root_function,
):
    pass


class TestSimulation(unittest.TestCase):
    def test_can_create_simulation(self):
        comparison_time = datetime.datetime(2023, 5, 12, 10, 55, 45)

        simulation = Simulation("test_1")

        simulation.set_request_character_summary_function(
            fake_request_character_summary_function
        )
        simulation.set_produce_action_statuses_for_agent_and_sandbox_object_function(
            fake_produce_action_statuses_for_agent_and_sandbox_object_function
        )

        simulation.initialize()

        self.assertEqual(simulation.name, "test_1")

    def test_can_retrieve_a_simulations_environment_tree(self):
        town = Node(Location("town", "town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name, _self):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)
        simulation.set_request_character_summary_function(
            fake_request_character_summary_function
        )
        simulation.set_produce_action_statuses_for_agent_and_sandbox_object_function(
            fake_produce_action_statuses_for_agent_and_sandbox_object_function
        )

        simulation.initialize()

        environment_tree = simulation.get_environment_tree()

        self.assertEqual(town.name, environment_tree.name)


    def test_can_retrieve_agents_from_simulation(self):
        town = Node(Location("town", "town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name, _self):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)
        simulation.set_request_character_summary_function(
            fake_request_character_summary_function
        )
        simulation.set_produce_action_statuses_for_agent_and_sandbox_object_function(
            fake_produce_action_statuses_for_agent_and_sandbox_object_function
        )

        simulation.initialize()

        agents = simulation.get_agents()

        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0].name, "Test")

    def test_can_retrieve_current_location_node_from_loaded_agent(self):
        town = Node(Location("town", "town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name, _self):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)
        simulation.set_request_character_summary_function(
            fake_request_character_summary_function
        )
        simulation.set_produce_action_statuses_for_agent_and_sandbox_object_function(
            fake_produce_action_statuses_for_agent_and_sandbox_object_function
        )

        simulation.initialize()

        agents = simulation.get_agents()

        self.assertFalse(isinstance(agents[0].get_current_location_node(), NoneType))
        self.assertTrue(isinstance(agents[0].get_current_location_node(), Node))
        self.assertEqual(agents[0].get_current_location_node().name.name, "town")

    def test_after_initializing_simulation_the_agents_character_summaries_should_be_set(
        self,
    ):
        town = Node(Location("town", "town", "a quaint town"))

        simulation = Simulation("test_1")

        def fake_load_environment_function(_simulation_name, _self):
            return town

        simulation.set_load_environment_function(fake_load_environment_function)
        simulation.set_request_character_summary_function(
            fake_request_character_summary_function
        )
        simulation.set_produce_action_statuses_for_agent_and_sandbox_object_function(
            fake_produce_action_statuses_for_agent_and_sandbox_object_function
        )

        simulation.initialize()

        agents = simulation.get_agents()

        self.assertTrue(agents[0].has_character_summary())


if __name__ == "__main__":
    unittest.main()
