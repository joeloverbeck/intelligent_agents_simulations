import unittest

from anytree import Node

from location import Location
from sandbox_object import SandboxObject
from substitute_node import substitute_node


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

        town = substitute_node(town, substitute_bedroom)

        self.assertEqual(len(house.children), 2)

        self.assertEqual(house.children[1].name.name, "bedroomy")
        self.assertEqual(house.children[1].name.description, "new description")

        substitution_bedroom = house.children[1]

        self.assertEqual(substitution_bedroom.children[0].name.name, "bed")

    def test_can_substitute_root_node_correctly(self):

        plot_of_land = Node(Location("plot_of_land", "plot of land", "a plot of land with a farmhouse and some crops"))

        Node(Location("farmhouse", "farmhouse", "a three-story farmhouse"), parent=plot_of_land)
        Node(Location("barn", "barn", "a big, bulky barn"), parent=plot_of_land)
        Node(Location("field", "field", "a field with multiple crops"), parent=plot_of_land)

        plot_of_land = substitute_node(plot_of_land, Location("plot_of_land", "new plot of land", "a new plot of land"))

        self.assertEqual(plot_of_land.name.name, "new plot of land")
        self.assertEqual(plot_of_land.name.description, "a new plot of land")

        self.assertEqual(len(plot_of_land.children), 3)

if __name__ == "__main__":
    unittest.main()
