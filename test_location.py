import unittest

from location import Location


class TestLocation(unittest.TestCase):
    def test_can_create_location(self):
        description = "a place in which to cook and eat meals"

        kitchen = Location("kitchen", "kitchen", description)

        self.assertEqual(kitchen.name, "kitchen")
        self.assertEqual(kitchen.description, description)


if __name__ == "__main__":
    unittest.main()
