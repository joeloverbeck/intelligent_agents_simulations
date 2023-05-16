import unittest

from environment import substitute_node

from anytree import Node

from location import Location
from sandbox_object import SandboxObject


class TestSubstituteNode(unittest.TestCase):
    def test_can_substitute_node_correctly(self):
        town = Node(Location("town", "town", "a quaint town"))
        house = Node(Location("house", "house", "a two-story house"), parent=town)
        bedroom = Node(
            Location(
                "bedroom", "bedroom", "a place where people sleep and have naughty time"
            ),
            parent=house,
        )
        kitchen = Node(
            Location("kitchen", "kitchen", "a place where people cook and eat meals"),
            parent=house,
        )

        Node(
            SandboxObject(
                "stove", "stove", "an utensil that allows people to cook meals"
            ),
            parent=kitchen,
        )
        Node(
            SandboxObject(
                "bed",
                "bed",
                "a piece of furniture where people sleep and have naughty time",
            ),
            parent=bedroom,
        )

        substitute_bedroom = Location("bedroom", "bedroomy", "new description")

        substitute_node(town, substitute_bedroom)

        self.assertEqual(len(house.children), 2)

        self.assertEqual(house.children[1].name.name, "bedroomy")
        self.assertEqual(house.children[1].name.description, "new description")

        substitution_bedroom = house.children[1]

        self.assertEqual(substitution_bedroom.children[0].name.name, "bed")


if __name__ == "__main__":
    unittest.main()
