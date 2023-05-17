import unittest
from anytree import Node
from environment import find_node_by_identifier
from location import Location
from sandbox_object import SandboxObject


class TestFindNodeByIdentifier(unittest.TestCase):
    def test_can_locate_matching_node_in_environment_tree(self):
        plot_of_land = Node(Location("plot_of_land", "plot of land", "a plot of land"))
        barn = Node(Location("barn", "barn", "a barn"), parent=plot_of_land)
        tools = Node(SandboxObject("tools", "tools", "tools"), parent=barn)

        matching_node = find_node_by_identifier(
            plot_of_land, tools.name.get_identifier()
        )

        self.assertEqual(matching_node.name.name, "tools")
        self.assertEqual(matching_node.name.get_identifier(), "tools")
        self.assertEqual(matching_node.name.description, "tools")


if __name__ == "__main__":
    unittest.main()
