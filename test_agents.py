import unittest

from anytree import Node
from agent import Agent

from location import Location


class TestCanCreateAgentsProperly(unittest.TestCase):
    def setUp(self):
        pass

    def test_can_create_an_agent_properly(self):
        town_node = Node(Location("town"))
        house_node = Node(Location("house"), parent=town_node)

        agent = Agent("Aileen", 22, house_node, town_node)

        self.assertEqual(agent.name, "Aileen")
        self.assertEqual(agent.current_location.name.name, "house")
        self.assertEqual(agent.environment_tree.name.name, "town")


if __name__ == "__main__":
    unittest.main()
