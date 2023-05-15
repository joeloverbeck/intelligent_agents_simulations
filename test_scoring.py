import unittest
from agent import Agent
from anytree import Node

from location import Location
from scoring import request_rating_from_agent_for_location_node


class TestRequestingRatingFromAgentForLocation(unittest.TestCase):
    def test_can_receive_a_rating_from_agent_for_location(self):
        bedroom = Location(
            "bedroom", "bedroom", "a place where people sleep, and have naughty times"
        )

        agent = Agent("Aileen", 22, None, None)

        plan = "Aileen is planning to cook a meal"

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer"
        )

        rating = request_rating_from_agent_for_location_node(agent, plan, Node(bedroom))

        self.assertTrue(isinstance(rating, int))
        self.assertGreaterEqual(rating, 1)
        self.assertLessEqual(rating, 10)


if __name__ == "__main__":
    unittest.main()
