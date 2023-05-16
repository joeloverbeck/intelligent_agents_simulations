import datetime
import unittest

from anytree import Node
from actions import create_action
from agent import Agent
from location import Location
from sandbox_object import SandboxObject


def fake_load_agent_memories_function(_agent):
    index = None
    memories_raw_data = {}

    return index, memories_raw_data


def fake_update_memories_database_function(
    _agent, _current_timestamp, _actions, _index
):
    pass


def fake_request_what_action_to_take_now_function(
    _agent, _current_timestamp, _most_recent_memories
):
    return "action to take"


def fake_request_for_what_length_of_time_the_action_should_take_place_function(
    _agent, _action, _current_timestamp, _most_recent_memories
):
    return "length of time"


class TestCreateAction(unittest.TestCase):
    def test_after_creating_action_agent_gets_wiped_of_previous_action_attribute_values(
        self,
    ):
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

        current_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        agent.set_character_summary("character summary")
        agent.set_planned_action("planned action", silent=True)
        agent.set_action_status("action status", silent=True)
        agent.set_destination_node(bed, silent=True)
        agent.set_using_object(bed, silent=True)

        create_action(
            agent,
            current_timestamp,
            fake_load_agent_memories_function,
            fake_update_memories_database_function,
            fake_request_what_action_to_take_now_function,
            fake_request_for_what_length_of_time_the_action_should_take_place_function,
        )

        self.assertEqual(agent.get_planned_action(), None)
        self.assertEqual(agent.get_action_status(), None)
        self.assertEqual(agent.get_destination_node(), None)
        self.assertEqual(agent.get_using_object(), None)


if __name__ == "__main__":
    unittest.main()
