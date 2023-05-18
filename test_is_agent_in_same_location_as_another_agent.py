import unittest
from anytree import Node
from agent import Agent

from agent_utils import is_agent_in_same_location_as_another_agent
from location import Location
from sandbox_object import SandboxObject


class TestIsAgentInSameLocationAsAnotherAgent(unittest.TestCase):
    def test_when_in_same_containing_location_it_should_return_true(self):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, bedroom, house)

        jill = Agent("jill", 22, bedroom, house)

        is_in_same_location, second_agent = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertTrue(is_in_same_location)

        self.assertEqual(second_agent.name, "jill")

    def test_when_secondary_agent_in_same_containing_location_but_one_in_sandbox_object(
        self,
    ):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, bedroom, house)

        jill = Agent("jill", 22, bed, house)

        is_in_same_location, second_agent = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertTrue(is_in_same_location)

        self.assertEqual(second_agent.name, "jill")

    def test_when_primary_agent_in_same_containing_location_but_one_in_sandbox_object(
        self,
    ):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, bed, house)

        jill = Agent("jill", 22, bedroom, house)

        is_in_same_location, second_agent = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertTrue(is_in_same_location)

        self.assertEqual(second_agent.name, "jill")

    def test_when_both_agents_in_same_containing_location_but_both_in_sandbox_objects(
        self,
    ):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        desk = Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, bed, house)

        jill = Agent("jill", 22, desk, house)

        is_in_same_location, second_agent = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertTrue(is_in_same_location)

        self.assertEqual(second_agent.name, "jill")

    def test_in_different_locations(self):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, house, house)

        jill = Agent("jill", 22, bedroom, house)

        is_in_same_location, _ = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertFalse(is_in_same_location)

    def test_in_different_locations_with_second_agent_in_sandbox_object(self):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)
        Node(SandboxObject("desk", "desk", "desk"), parent=bedroom)

        agent = Agent("bill", 22, house, house)

        jill = Agent("jill", 22, bed, house)

        is_in_same_location, _ = is_agent_in_same_location_as_another_agent(
            agent, "jill", [agent, jill]
        )

        self.assertFalse(is_in_same_location)

    def test_when_agents_have_same_name(self):
        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, house, house)
        second_agent_same_name = Agent("bill", 23, bedroom, house)

        is_in_same_location, _ = is_agent_in_same_location_as_another_agent(
            agent, "bill", [agent, second_agent_same_name]
        )

        self.assertFalse(is_in_same_location)


if __name__ == "__main__":
    unittest.main()
