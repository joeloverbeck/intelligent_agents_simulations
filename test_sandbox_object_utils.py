import unittest
from agent import Agent

from anytree import Node
from location import Location
from sandbox_object import SandboxObject
from sandbox_object_utils import request_rating_from_agent_for_sandbox_object_node


class TestRequestingAgentsRatingOfSandboxObject(unittest.TestCase):
    def test_can_retrieve_an_agents_rating_of_sandbox_object_given_plan(self):
        sandbox_object = SandboxObject(
            "desk",
            "desk",
            "a piece of furniture where people read, write, or sit at a computer",
        )

        location_node = Node(Location("house", "house", "a two-story house"))

        sandbox_object_node = Node(sandbox_object, parent=location_node)

        self.assertEqual(sandbox_object.name, "desk")

        town = Node(Location("town", "town", "town"))

        agent = Agent("Eileen", 22, town, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer"
        )

        agent.set_planned_action("read and take notes for research paper", silent=True)

        rating = request_rating_from_agent_for_sandbox_object_node(
            agent, sandbox_object_node
        )

        self.assertTrue(isinstance(rating, int))
        self.assertGreaterEqual(rating, 0)
        self.assertLessEqual(rating, 10)


if __name__ == "__main__":
    unittest.main()
