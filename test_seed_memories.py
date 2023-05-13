import unittest

from agent import Agent
from seed_memories import load_seed_memories


class TestCanLoadSeedMemoriesFromFile(unittest.TestCase):
    def setUp(self):
        agent_name = "Test"

        agent = Agent(agent_name, 22, None, None)

        self.seed_memories_cleaned = load_seed_memories(agent)

    def test_seed_memories_load_correctly(self):
        self.assertEqual(len(self.seed_memories_cleaned), 4)
        self.assertEqual(self.seed_memories_cleaned[0], "Memory 1.")
        self.assertEqual(self.seed_memories_cleaned[1], "Memory 2.")
        self.assertEqual(self.seed_memories_cleaned[2], "Memory 3.")
        self.assertEqual(self.seed_memories_cleaned[3], "Memory 4.")


if __name__ == "__main__":
    unittest.main()
