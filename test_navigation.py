from types import NoneType
import unittest

from anytree import Node
from agent import Agent
from errors import EmptyEnvironmentTreeError

from location import Location
from navigation import (
    find_all_sandbox_objects_in_environment_tree,
    get_node_one_step_closer_to_destination,
)
from sandbox_object import SandboxObject


class TestSandboxObjects(unittest.TestCase):
    def test_can_find_all_objects_in_environment_tree(self):
        town = Node(Location("town"))
        house = Node(Location("house"), parent=town)
        bedroom = Node(Location("bedroom"), parent=house)
        kitchen = Node(Location("kitchen"), parent=house)

        stove = Node(
            SandboxObject("stove", "an utensil that allows people to cook meals"),
            parent=kitchen,
        )
        bed = Node(
            SandboxObject(
                "bed", "a piece of furniture where people sleep and have naughty time"
            ),
            parent=bedroom,
        )

        nodes_that_contain_sandbox_objects = (
            find_all_sandbox_objects_in_environment_tree(town)
        )

        self.assertEqual(
            nodes_that_contain_sandbox_objects[1].name.name, stove.name.name
        )
        self.assertEqual(nodes_that_contain_sandbox_objects[0].name.name, bed.name.name)




class TestMovementTowardsDestination(unittest.TestCase):
    def test_can_move_a_node_closer_to_destination(self):
        town = Node(Location("town"))
        house = Node(Location("house"), parent=town)
        bedroom = Node(Location("bedroom"), parent=house)

        agent = Agent("Aileen", 22, town, town)

        agent.set_destination(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_can_move_a_node_closer_to_destination_when_destination_is_ancestor(self):

        town = Node(Location("town"))
        house = Node(Location("house"), parent=town)
        bedroom = Node(Location("bedroom"), parent=house)

        agent = Agent("Aileen", 22, bedroom, town)

        agent.set_destination(town)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_can_move_a_node_closer_to_destination_when_they_are_on_different_branches(self):
        town = Node(Location("town"))
        house_1 = Node(Location("house"), parent=town)
        bedroom = Node(Location("bedroom"), parent=house_1)

        house_2 = Node(Location("house 2"), parent=town)
        kitchen = Node(Location("kitchen"), parent=house_2)

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house_2.name.name)

    def test_same_current_and_destination_location(self):
        town = Node(Location("town"))
        house = Node(Location("house"), parent=town)

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination(house)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertTrue(isinstance(node, NoneType))

    def test_same_branch_non_direct_ancestor_descendant(self):
        town = Node(Location("town"))
        house = Node(Location("house"), parent=town)
        bedroom = Node(Location("bedroom"), parent=house)
        kitchen = Node(Location("kitchen"), parent=house)

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_single_node_tree(self):
        town = Node(Location("town"))
        agent = Agent("Aileen", 22, town, town)
        agent.set_destination(town)
        node = get_node_one_step_closer_to_destination(agent)
        self.assertTrue(isinstance(node, NoneType))
    
    def test_destination_none(self):
        town = Node(Location("town"))
        agent = Agent("Aileen", 22, town, town)
        agent.set_destination(None)
        node = get_node_one_step_closer_to_destination(agent)
        self.assertTrue(isinstance(node, NoneType))



if __name__ == "__main__":
    unittest.main()
