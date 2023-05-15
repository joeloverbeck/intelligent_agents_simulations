import unittest

from anytree import Node
from agent import Agent

from location import Location
from sandbox_object import SandboxObject
from sandbox_object_utils import determine_sandbox_object_node_to_use


class TestDetermineSandboxObjectForAction(unittest.TestCase):
    def test_given_an_action_can_determine_a_single_sandbox_object_node_to_use(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where meals are cooked and eaten"),
            parent=house,
        )

        stove = Node(
            SandboxObject(
                "stove", "stove", "an utensil that allows people to cook meals"
            ),
            parent=kitchen,
        )

        Node(
            SandboxObject(
                "poster", "poster", "a poster on the wall. The poster depicts guitars."
            ),
            parent=kitchen,
        )

        agent = Agent("Aileen", 22, house, town)

        agent.set_character_summary(
            f"Name: {agent.name} (age: {agent.age})\nInnate traits: shy, studious, creative, wannabe-singer.\n"
        )

        sandbox_object_node_chosen = determine_sandbox_object_node_to_use(
            agent, "Aileen is going to cook breakfast", kitchen
        )

        self.assertEqual(sandbox_object_node_chosen, stove)


if __name__ == "__main__":
    unittest.main()
