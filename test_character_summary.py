import unittest

from anytree import Node
from agent import Agent
from character_summaries import request_character_summary
from location import Location
from vector_storage import load_agent_memories


class TestCanLoadSeedMemories(unittest.TestCase):
    def setUp(self):
        town_node = Node(Location("town"))
        house_node = Node(Location("house"), parent=town_node)

        self.agent = Agent("test", 22, house_node, town_node)

        self.index, self.memories_raw_data = load_agent_memories(self.agent)

    def test_can_create_character_summary(self):
        character_summary = request_character_summary(self.agent, self.memories_raw_data, self.index)

        self.assertTrue(isinstance(character_summary, str))

        self.agent.set_character_summary(character_summary)

        self.assertEqual(character_summary, self.agent.get_character_summary())


if __name__ == "__main__":
    unittest.main()
