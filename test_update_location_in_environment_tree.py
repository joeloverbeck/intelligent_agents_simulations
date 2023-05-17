import unittest

from anytree import Node

from location import Location
from sandbox_object import SandboxObject
from update_location_in_environment_tree import update_node_in_environment_tree

class TestUpdateCurrentLocationInEnvironmentTree(unittest.TestCase):

    def test_after_updating_current_location_the_values_of_previous_location_and_children_sandbox_objects_are_updated(self):

        house = Node(Location("house", "house", "a two-story house"))

        bedroom = Node(Location("bedroom", "bedroom", "a room where people sleep"), parent=house)

        bed = Node(SandboxObject("bed", "bed", "a piece of furniture that people use to sleep"), parent=bedroom)

        bed.name.set_action_status("action status")

        new_bedroom = Node(Location("bedroom", "bedroom_2", "a room where people sleep"))
        Node(SandboxObject("bed", "bed_2", "a piece of furniture that people use to sleep"), parent=new_bedroom)

        update_node_in_environment_tree(new_bedroom, house)

        self.assertEqual(bedroom.name.name, "bedroom_2")
        self.assertEqual(bed.name.name, "bed_2")
        self.assertEqual(bed.name.get_action_status(), None)

        # Ensure that the values of the replacement node haven't changed
        self.assertEqual(new_bedroom.name.name, "bedroom_2")

    def test_after_updating_current_sandbox_object_the_values_of_previous_sandbox_object_are_updated(self):
        house = Node(Location("house", "house", "a two-story house"))

        bedroom = Node(Location("bedroom", "bedroom", "a room where people sleep"), parent=house)

        bed = Node(SandboxObject("bed", "bed", "a piece of furniture that people use to sleep"), parent=bedroom)

        bed.name.set_action_status("action status")

        new_bedroom = Node(Location("bedroom", "bedroom_2", "a room where people sleep"))
        new_bed = Node(SandboxObject("bed", "bed_2", "a piece of furniture that people use to sleep"), parent=new_bedroom)

        update_node_in_environment_tree(new_bed, house)

        self.assertEqual(bedroom.name.name, "bedroom")
        self.assertEqual(bed.name.name, "bed_2")
        self.assertEqual(bed.name.get_action_status(), None)

        # Ensure that the values of the replacement node haven't changed
        self.assertEqual(new_bedroom.name.name, "bedroom_2")

if __name__ == "__main__":
    unittest.main()
