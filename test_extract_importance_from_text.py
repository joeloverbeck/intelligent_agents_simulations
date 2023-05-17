import unittest

from regular_expression_utils import extract_rating_from_text


class TestCanExtractImportanceFromText(unittest.TestCase):
    def test_can_extract_importance_from_text_that_has_number(self):
        text = "this text contains 7 a number somewhere."
        importance = extract_rating_from_text(text, "prompt", silent=True)

        self.assertEqual(importance, 7)

    def test_can_extract_importance_from_text_that_doesnt_have_number(self):
        text = "this text does not contain a number"
        importance = extract_rating_from_text(text, "prompt", silent=True)

        self.assertEqual(importance, 5)

if __name__ == "__main__":
    unittest.main()
