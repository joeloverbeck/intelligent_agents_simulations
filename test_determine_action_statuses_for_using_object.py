import unittest

from anytree import Node
from action_statuses import determine_action_statuses_for_using_object
from agent import Agent
from location import Location
from sandbox_object import SandboxObject


def fake_request_agent_action_status_for_using_object(_agent):
    return "new action status"


def fake_request_used_object_action_status(_agent):
    return "new action status"


class TestDetermineActionStatusesForUsingObject(unittest.TestCase):
    def test_after_determining_action_statuses_for_using_object_planned_action_should_be_none(
        self,
    ):
        house = Node(Location("house", "house", "a two-story house"))

        bedroom = Node(
            Location("bedroom", "bedroom", "a room in which to sleep"), parent=house
        )

        bed = Node(
            SandboxObject("bed", "bed", "a piece of furniture in which to sleep"),
            parent=bedroom,
        )

        agent = Agent("Aileen", 22, bed, house)

        agent.set_planned_action("Aileen plans to do something", silent=True)

        determine_action_statuses_for_using_object(
            agent,
            fake_request_agent_action_status_for_using_object,
            fake_request_used_object_action_status,
        )

        self.assertEqual(agent.get_planned_action(), None)


if __name__ == "__main__":
    unittest.main()
