import datetime
import unittest
from anytree import Node
from agent import Agent

from location import Location
from process_observation import ProcessObservationParametersKey, process_observation
from sandbox_object import SandboxObject


class FakeIndex:
    def unload(self):
        pass


def fake_load_agent_memories_function(_agent):
    return FakeIndex(), None


def fake_update_memories_database_function(
    _agent, _current_timestamp, _new_memories, _index
):
    pass


def fake_request_if_should_stop_action_function(_agent, _observation_data):
    return "yes"


def fake_request_appropriate_reaction_for_observation_function(
    _agent, _observation_data
):
    return "do something else"


class TestProcessObservation(unittest.TestCase):
    def test_can_process_observation(self):
        current_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("Lilly", 22, bedroom, house)

        agent.set_character_summary("Character summary", silent=True)

        observation = "Lilly witnesses a poster falling from the wall"

        process_observation(
            {
                ProcessObservationParametersKey.OBSERVATION: observation,
                ProcessObservationParametersKey.CURRENT_TIMESTAMP: current_timestamp,
                ProcessObservationParametersKey.LOAD_AGENT_MEMORIES_FUNCTION: fake_load_agent_memories_function,
                ProcessObservationParametersKey.AGENT: agent,
                ProcessObservationParametersKey.REQUEST_IF_SHOULD_STOP_ACTION_FUNCTION: fake_request_if_should_stop_action_function,
                ProcessObservationParametersKey.UPDATE_MEMORIES_DATABASE_FUNCTION: fake_update_memories_database_function,
                ProcessObservationParametersKey.REQUEST_APPROPRIATE_REACTION_FOR_OBSERVATION_FUNCTION: fake_request_appropriate_reaction_for_observation_function,
                ProcessObservationParametersKey.OBSERVATION_DATA: {},
            }
        )

        self.assertEqual(agent.get_observation(), observation)


if __name__ == "__main__":
    unittest.main()
