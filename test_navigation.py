from types import NoneType
import unittest

from anytree import Node
from agent import Agent

from location import Location
from navigation import (
    determine_sandbox_object_destination_from_root,
    perform_agent_movement,
)
from one_step_movement import get_node_one_step_closer_to_destination
from sandbox_object import SandboxObject
from sandbox_object_utils import find_all_sandbox_objects_in_environment_tree


class TestSandboxObjects(unittest.TestCase):
    def test_can_find_all_objects_in_environment_tree(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
            parent=house,
        )
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where people cook and eat meals"),
            parent=house,
        )

        stove = Node(
            SandboxObject(
                "stove", "stove", "an utensil that allows people to cook meals"
            ),
            parent=kitchen,
        )
        bed = Node(
            SandboxObject(
                "bed",
                "bed",
                "a piece of furniture where people sleep and have naughty time",
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
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
            parent=house,
        )

        agent = Agent("Aileen", 22, town, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_can_move_a_node_closer_to_destination_when_destination_is_ancestor(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
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
        town = Node(Location("town", "town", "a quaint town"))
        house_1 = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
            parent=house_1,
        )

        house_2 = Node(Location("house_2", "house 2", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where people cook and eat meals"),
            parent=house_2,
        )

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house_2.name.name)

    def test_same_branch_non_direct_ancestor_descendant(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
            parent=house,
        )
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where people cook and eat meals"),
            parent=house,
        )

        agent = Agent("Aileen", 22, kitchen, town)

        agent.set_destination_node(bedroom)

        node = get_node_one_step_closer_to_destination(agent)

        self.assertFalse(isinstance(node, NoneType))
        self.assertEqual(node.name.name, house.name.name)

    def test_destination_none(self):
        town = Node(Location("town", "town", "a quaint town"))
        agent = Agent("Aileen", 22, town, town)
        agent.set_destination_node(None)
        node = get_node_one_step_closer_to_destination(agent)
        self.assertTrue(isinstance(node, NoneType))


class TestDeterminingDestination(unittest.TestCase):
    def test_can_determine_a_sandbox_object_node_destination_from_root(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        agent.set_planned_action("Aileen is planning to cook a meal", silent=True)

        destination_node = determine_sandbox_object_destination_from_root(agent, town)

        self.assertFalse(isinstance(destination_node, NoneType))
        self.assertFalse(isinstance(destination_node.name, NoneType))
        self.assertTrue(isinstance(destination_node.name, SandboxObject))
        self.assertEqual(destination_node.name.name, poster.name.name)


class TestMoveOneNodeCloserToDestination(unittest.TestCase):
    def test_location_displacement_when_agent_was_away_from_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
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
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_destination_node(poster)

        perform_agent_movement(agent)

        # After moving one step, she should have entered the kitchen, where
        # the poster is located, so the destination should be poster
        self.assertEqual(agent.get_current_location_node(), poster)

    def test_sandbox_object_displacement_to_sandbox_object_when_same_parent(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        stove = Node(
            SandboxObject("stove", "stove", "a piece of furniture to cook meals"),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, poster, town)

        agent.set_destination_node(stove)

        perform_agent_movement(agent)

        # After moving one step, she should have entered the kitchen, where
        # the poster is located, so the destination should be poster
        self.assertEqual(agent.get_current_location_node(), stove)

    def test_movement_from_sandbox_object_to_adjacent_location(self):
        house = Node(Location("house", "house", "a two-story house"))
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, poster, house)

        agent.set_destination_node(house)

        perform_agent_movement(agent)

        # Given that she was at poster (and therefore at kitchen),
        # moving one step should have put her at house.
        self.assertEqual(agent.get_current_location_node(), house)


if __name__ == "__main__":
    unittest.main()
