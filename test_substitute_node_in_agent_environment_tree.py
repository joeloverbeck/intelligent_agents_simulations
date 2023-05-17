import unittest

from anytree import Node

from location import Location
from substitute_node import substitute_node


class TestSubstituteNodeInAgentEnvironmentTree(unittest.TestCase):
    def test_can_substitute_a_location_node_in_agent_environment_tree(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        Node(Location("bedroom", "bedroom", "a place where people sleep"), parent=house)

        town = substitute_node(
            town, Location("house", "house_new", "a two-story house")
        )

        self.assertEqual(town.children[0].name.name, "house_new")

        house_new = town.children[0]

        self.assertEqual(house_new.children[0].name.name, "bedroom")

        self.assertEqual(house_new.parent.name, town.name)

    def test_can_substitute_the_root_node_without_issues_in_an_agent_environment_tree(
        self,
    ):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        Node(Location("bedroom", "bedroom", "a place where people sleep"), parent=house)

        town = substitute_node(
            town, Location("town", "town_new", "a different quaint town")
        )

        self.assertEqual(house.parent.name.name, "town_new")
        self.assertEqual(house.parent.name.description, "a different quaint town")

        self.assertEqual(house.name.name, "house")
        self.assertEqual(house.name.description, "a two-story house")


if __name__ == "__main__":
    unittest.main()
