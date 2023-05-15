import json
import os
import unittest

from anytree import Node
from environment import build_environment_tree, serialize_environment_tree

from location import Location
from sandbox_object import SandboxObject
from vector_storage import create_json_file


class TestLoadEnvironment(unittest.TestCase):
    def test_can_serialize_environment_tree(self):
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

        json_str = serialize_environment_tree(town)

        full_path = "testing/serialize_environment_tree.json"

        if os.path.isfile(full_path):
            os.remove(full_path)

        create_json_file(full_path, json_str)

        # Now load the created file and make sure it has created the intended structure.
        with open(full_path, "r", encoding="utf8") as file:
            data = json.load(file)

        environment_tree = build_environment_tree(data, None)

        self.assertEqual(environment_tree.name.name, "town")
        self.assertEqual(len(environment_tree.children), 1)

        house_node = environment_tree.children[0]

        self.assertEqual(house_node.name.name, "house")
        self.assertEqual(len(house_node.children), 2)

        bedroom_node = house_node.children[0]

        self.assertEqual(bedroom_node.name.name, "bedroom")
        self.assertEqual(len(bedroom_node.children), 1)

        bed_node = bedroom_node.children[0]

        self.assertEqual(bed_node.name.name, "bed")

        kitchen_node = house_node.children[1]

        self.assertEqual(kitchen_node.name.name, "kitchen")
        self.assertEqual(len(kitchen_node.children), 1)

        stove_node = kitchen_node.children[0]

        self.assertEqual(stove_node.name.name, "stove")
        self.assertEqual(len(stove_node.children), 0)


if __name__ == "__main__":
    unittest.main()
