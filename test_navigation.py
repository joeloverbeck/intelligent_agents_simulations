from types import NoneType
import unittest

from anytree import Node
from agent import Agent

from location import Location
from navigation import (
    determine_sandbox_object_destination_from_root,
    get_node_one_step_closer_to_destination,
    perform_agent_movement,
)
from sandbox_object import SandboxObject
from sandbox_object_utils import find_all_sandbox_objects_in_environment_tree


class TestSandboxObjects(unittest.TestCase):
    def test_can_find_all_objects_in_environment_tree(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "a place where people sleep and have naughty time"),
            parent=house,
        )
        kitchen = Node(
            Location("kitchen", "a place where people cook and eat meals"), parent=house
        )

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
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "a place where people sleep and have naughty time"),
            parent=house,
        )

        agent = Agent("Aileen", 22, town, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_can_move_a_node_closer_to_destination_when_destination_is_ancestor(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "a place where people sleep and have naughty time"),
            parent=house,
        )

        agent = Agent("Aileen", 22, bedroom, town)

        agent.set_destination_node(town)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_can_move_a_node_closer_to_destination_when_they_are_on_different_branches(
        self,
    ):
        town = Node(Location("town", "a quaint town"))
        house_1 = Node(Location("house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "a place where people sleep and have naughty time"),
            parent=house_1,
        )

        house_2 = Node(Location("house 2", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "a place where people cook and eat meals"),
            parent=house_2,
        )

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house_2.name.name)

    def test_same_current_and_destination_location(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination_node(house)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertTrue(isinstance(node, NoneType))

    def test_same_branch_non_direct_ancestor_descendant(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "a place where people sleep and have naughty time"),
            parent=house,
        )
        kitchen = Node(
            Location("kitchen", "a place where people cook and eat meals"), parent=house
        )

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_single_node_tree(self):
        town = Node(Location("town", "a quaint town"))
        agent = Agent("Aileen", 22, town, town)
        agent.set_destination_node(town)
        node = get_node_one_step_closer_to_destination(agent)
        self.assertTrue(isinstance(node, NoneType))

    def test_destination_none(self):
        town = Node(Location("town", "a quaint town"))
        agent = Agent("Aileen", 22, town, town)
        agent.set_destination_node(None)
        node = get_node_one_step_closer_to_destination(agent)
        self.assertTrue(isinstance(node, NoneType))


class TestDeterminingDestination(unittest.TestCase):
    def test_can_determine_a_sandbox_object_node_destination_from_root(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        destination_node = determine_sandbox_object_destination_from_root(
            agent, "Aileen is planning to cook a meal", town
        )

        self.assertFalse(isinstance(destination_node, NoneType))
        self.assertFalse(isinstance(destination_node.name, NoneType))
        self.assertTrue(isinstance(destination_node.name, SandboxObject))
        self.assertEqual(destination_node.name.name, poster.name.name)


class TestMoveOneNodeCloserToDestination(unittest.TestCase):
    def test_location_displacement_when_agent_was_away_from_destination(self):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, town, town)

        agent.set_destination_node(poster)

        perform_agent_movement(agent)

        # After moving one step, the agent should now be at 'house'
        self.assertEqual(agent.get_current_location_node(), house)

    def test_location_displacement_to_sandbox_object_node_when_at_location_that_contains_it(
        self,
    ):
        town = Node(Location("town", "a quaint town"))
        house = Node(Location("house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination_node(poster)

        perform_agent_movement(agent)

        # After moving one step, she should have entered the kitchen, where
        # the poster is located, so the destination should be poster
        self.assertEqual(agent.get_current_location_node(), poster)


if __name__ == "__main__":
    unittest.main()
