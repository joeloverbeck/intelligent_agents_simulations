import datetime
from types import NoneType
import unittest

from anytree import Node
from action_statuses import produce_action_statuses_for_agent_and_sandbox_object

from agent import Agent
from datetime_utils import format_date
from location import Location
from sandbox_object import SandboxObject


def fake_create_action_function(
    agent,
    current_timestamp,
    _load_agent_memories_function,
    _update_memories_database_function,
    _request_what_action_to_take_now_function,
    _request_for_what_length_of_time_the_action_should_take_place_function,
):
    return (
        f"{agent.name} is planning to cook a meal at {format_date(current_timestamp)}."
    )


def fake_request_what_action_to_take_now_function(
    _agent, _current_timestamp, _most_recent_memories
):
    return "Action to take"


def fake_request_for_what_length_of_time_the_action_should_take_place_function(
    _agent, _action, _current_timestamp, _most_recent_memories
):
    return "30 minutes from 10 am"


def fake_produce_action_statuses_for_agent_based_on_destination_node_function(
    agent, _destination_node
):
    agent.set_action_status("action status", silent=True)


class TestDetermineActionStatusesForAction(unittest.TestCase):
    def test_can_produce_movement_action_status_if_not_at_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        def fake_determine_sandbox_object_destination_function(
            _agent, _environment_root
        ):
            return poster

        current_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        produce_action_statuses_for_agent_and_sandbox_object(
            agent,
            current_timestamp,
            fake_create_action_function,
            fake_determine_sandbox_object_destination_function,
            fake_produce_action_statuses_for_agent_based_on_destination_node_function,
            fake_request_what_action_to_take_now_function,
            fake_request_for_what_length_of_time_the_action_should_take_place_function,
        )

        self.assertFalse(isinstance(agent.get_action_status(), NoneType))

        # the sandbox object's action status should be none, given
        # that it won't be used until the agent gets there.
        self.assertTrue(isinstance(poster.name.get_action_status(), NoneType))

    def test_can_produce_using_object_action_statuses_for_at_destination(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        poster = Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, poster, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        def fake_determine_sandbox_object_destination_function(
            _agent, _environment_root
        ):
            return poster

        current_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        produce_action_statuses_for_agent_and_sandbox_object(
            agent,
            current_timestamp,
            fake_create_action_function,
            fake_determine_sandbox_object_destination_function,
            fake_produce_action_statuses_for_agent_based_on_destination_node_function,
            fake_request_what_action_to_take_now_function,
            fake_request_for_what_length_of_time_the_action_should_take_place_function,
        )

        self.assertFalse(isinstance(agent.get_action_status(), NoneType))
        self.assertFalse(isinstance(agent.get_action_status(), NoneType))


if __name__ == "__main__":
    unittest.main()
