from types import NoneType
import unittest

from agent_utils import load_agents

from anytree import Node

from location import Location
from sandbox_object import SandboxObject


class TestSimulation(unittest.TestCase):
    def test_can_load_agents(self):
        town = Node(Location("town", "town", "a quaint town"))

        park = Node(Location("park", "park", "a public park"), parent=town)

        bench = Node(
            SandboxObject("bench", "bench", "a bench on which to sit"), parent=park
        )

        house = Node(Location("house", "house", "a two-story house"), parent=town)

        agents = load_agents("test_2", town, None)

        self.assertEqual(agents[0].name, "Test 1")
        self.assertEqual(agents[0].age, 22)
        self.assertEqual(agents[0].get_action_status(), "reading")
        self.assertEqual(agents[0].get_current_location_node(), park)
        self.assertTrue(isinstance(agents[0].get_destination_node(), NoneType))
        self.assertEqual(agents[0].get_using_object(), bench)

        self.assertEqual(agents[1].name, "Test 2")
        self.assertEqual(agents[1].age, 32)
        self.assertEqual(agents[1].get_action_status(), "heading to house")
        self.assertEqual(agents[1].get_current_location_node(), town)
        self.assertEqual(agents[1].get_destination_node(), house)
        self.assertTrue(isinstance(agents[1].get_using_object(), NoneType))


if __name__ == "__main__":
    unittest.main()
