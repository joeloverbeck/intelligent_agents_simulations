from types import NoneType
import unittest

from agent_utils import load_agents


class TestSimulation(unittest.TestCase):
    def test_can_load_agents(self):
        agents = load_agents("test_2", None)

        self.assertEqual(agents[0].name, "Test 1")
        self.assertEqual(agents[0].age, 22)
        self.assertEqual(agents[0].get_action_status(), "reading")
        self.assertEqual(agents[0].get_current_location_node().name.name, "park")
        self.assertTrue(isinstance(agents[0].get_destination_node(), NoneType))
        self.assertEqual(agents[0].get_using_object().name.name, "bench")

        self.assertEqual(agents[1].name, "Test 2")
        self.assertEqual(agents[1].age, 32)
        self.assertEqual(agents[1].get_action_status(), "heading to house")
        self.assertEqual(agents[1].get_current_location_node().name.name, "town")
        self.assertEqual(agents[1].get_destination_node().name.name, "house")
        self.assertTrue(isinstance(agents[1].get_using_object(), NoneType))


if __name__ == "__main__":
    unittest.main()
