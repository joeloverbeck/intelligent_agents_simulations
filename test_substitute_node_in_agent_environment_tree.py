import unittest

from anytree import Node
from environment import substitute_node

from location import Location


class TestSubstituteNodeInAgentEnvironmentTree(unittest.TestCase):
    def test_can_substitute_a_location_node_in_agent_environment_tree(self):
        town = Node(Location("town", "town", "a quaint town"))

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        Node(Location("bedroom", "bedroom", "a place where people sleep"), parent=house)

        substitute_node(town, Location("house", "house_new", "a two-story house"))

        self.assertEqual(town.children[0].name.name, "house_new")

        house_new = town.children[0]

        self.assertEqual(house_new.children[0].name.name, "bedroom")


if __name__ == "__main__":
    unittest.main()
