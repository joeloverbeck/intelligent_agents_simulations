import unittest

from agent_utils import load_agents

from anytree import Node

from location import Location


class TestSimulation(unittest.TestCase):
    def test_can_load_agents(self):
        town = Node(Location("town", "town", "a quaint town"))

        agents = load_agents("test_2", town, None)

        self.assertEqual(agents[0].name, "Test 1")
        self.assertEqual(agents[0].age, 22)
        self.assertEqual(agents[1].name, "Test 2")
        self.assertEqual(agents[1].age, 32)


if __name__ == "__main__":
    unittest.main()
