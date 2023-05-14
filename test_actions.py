import datetime
from types import NoneType
import unittest
from actions import create_action

from agent import Agent


def fake_load_agent_memories_function(_agent):
    index = None
    memories_raw_data = {
        "0": {
            "description": "Memory 1",
            "creation_timestamp": datetime.datetime(2023, 5, 11, 10, 30, 45),
        },
        "1": {
            "description": "Memory 2",
            "creation_timestamp": datetime.datetime(2023, 5, 11, 10, 30, 45),
        },
        "2": {
            "description": "Memory 3",
            "creation_timestamp": datetime.datetime(2023, 5, 11, 10, 30, 45),
        },
    }

    return index, memories_raw_data


def fake_update_memories_database_function(
    _agent, _current_timestamp, _new_memories, _index
):
    pass


class TestCanCreateAgentAction(unittest.TestCase):
    def test_can_create_action_for_agent(self):
        agent = Agent("Aileen", 22, None, None)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        current_time = datetime.datetime(2023, 5, 11, 10, 30, 45)

        action = create_action(
            agent,
            current_time,
            fake_load_agent_memories_function,
            fake_update_memories_database_function,
        )

        self.assertFalse(isinstance(action, NoneType))
        self.assertTrue(isinstance(action, str))


if __name__ == "__main__":
    unittest.main()
