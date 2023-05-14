import unittest

from string_utils import end_string_with_period


class TestEndStringWithPeriodWorksProperly(unittest.TestCase):
    def test_when_original_text_doesnt_end_with_period_the_function_places_a_period(
        self,
    ):
        text = "Seed memory"

        treated_text = end_string_with_period(text)

        self.assertEqual("Seed memory.", treated_text)

    def test_when_original_text_ends_with_period_the_function_doesnt_place_extra_period(
        self,
    ):
        text = "Seed memory."

        treated_text = end_string_with_period(text)

        self.assertEqual(text, treated_text)


if __name__ == "__main__":
    unittest.main()
