import unittest
from agent import Agent

from sandbox_object import SandboxObject
from sandbox_object_utils import request_rating_from_agent_for_sandbox_object


class TestRequestingAgentsRatingOfSandboxObject(unittest.TestCase):
    def test_can_retrieve_an_agents_rating_of_sandbox_object_given_plan(self):
        sandbox_object = SandboxObject(
            "desk",
            "a piece of furniture where people read, write, or sit at a computer",
        )

        self.assertEqual(sandbox_object.name, "desk")

        agent = Agent("Eileen", 22, None, None)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer"
        )

        rating = request_rating_from_agent_for_sandbox_object(
            agent, "read and take notes for research paper", sandbox_object
        )

        self.assertTrue(isinstance(rating, int))
        self.assertGreaterEqual(rating, 0)
        self.assertLessEqual(rating, 10)


if __name__ == "__main__":
    unittest.main()
