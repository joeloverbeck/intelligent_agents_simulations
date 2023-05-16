import unittest
from anytree import Node
from agent import Agent
from errors import AlgorithmError

from location import Location
from navigation import perform_agent_movement
from sandbox_object import SandboxObject


class TestPerformAgentMovement(unittest.TestCase):
    def test_if_agent_has_no_destination_nothing_changes(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bedroom, town)

        agent.set_destination_node(None, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, bedroom.name)
        self.assertEqual(agent.get_destination_node(), None)

    def test_if_agent_destination_node_is_equal_to_current_location_destination_becomes_none(
        self,
    ):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bedroom, town)

        with self.assertRaises(AlgorithmError):
            agent.set_destination_node(bedroom, silent=True)

    def test_if_agent_has_moved_to_destination_node_then_destination_is_none(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bedroom, town)

        agent.set_destination_node(house, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, house.name)
        self.assertEqual(agent.get_destination_node(), None)

    def test_if_agent_has_moved_to_location_with_sandbox_object_then_at_the_end_already_at_destination(
        self,
    ):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination_node(bed, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, bed.name)
        self.assertEqual(agent.get_destination_node(), None)

    def test_can_move_up_environment_tree_from_sandbox_object_without_issues(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bed, town)

        agent.set_destination_node(town, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, house.name)
        self.assertEqual(agent.get_destination_node(), town)

    def test_can_move_up_environment_tree_without_issues(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )

        Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination_node(town, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, town.name)
        self.assertEqual(agent.get_destination_node(), None)

    def test_agent_moves_correctly_to_descendant_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )
        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, town, town)
        agent.set_destination_node(bed, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, house.name)
        self.assertEqual(agent.get_destination_node(), bed)

    def test_agent_moves_correctly_to_ancestor_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )
        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bed, town)
        agent.set_destination_node(town, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, house.name)
        self.assertEqual(agent.get_destination_node(), town)

    def test_agent_stays_in_same_place_when_no_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )
        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bed, town)
        agent.set_destination_node(None, silent=True)

        perform_agent_movement(agent)

        self.assertEqual(agent.get_current_location_node().name, bed.name)
        self.assertEqual(agent.get_destination_node(), None)


if __name__ == "__main__":
    unittest.main()
