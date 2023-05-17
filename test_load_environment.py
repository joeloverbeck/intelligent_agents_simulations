import unittest

from environment import load_environment_tree_from_json


class TestLoadEnvironment(unittest.TestCase):
    def test_can_load_test_1_environment(self):
        environment_tree = load_environment_tree_from_json("test_1", "environment", None)

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
