import unittest

from anytree import Node
from agent import Agent
from agent_utils import wipe_previous_action_attribute_values_from_agent
from location import Location
from sandbox_object import SandboxObject


class TestWipePreviousActionAttributeValuesFromAgent(unittest.TestCase):
    def test_can_wipe_used_object_action_status(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location("bedroom", "bedroom", "a place where people sleep"), parent=house
        )
        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture where people sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, house, town)
        agent.set_destination_node(None, silent=True)

        agent.set_character_summary("character summary")
        agent.set_planned_action("planned action", silent=True)
        agent.set_action_status("action status", silent=True)
        agent.set_destination_node(bed, silent=True)
        agent.set_using_object(bed, silent=True)

        bed.name.set_action_status("being used", agent.name)

        wipe_previous_action_attribute_values_from_agent(agent)

        self.assertEqual(agent.get_planned_action(), None)
        self.assertEqual(agent.get_action_status(), None)
        self.assertEqual(agent.get_destination_node(), None)
        self.assertEqual(agent.get_using_object(), None)
        self.assertEqual(bed.name.get_action_status(), "idle")


if __name__ == "__main__":
    unittest.main()
