import unittest

from regular_expression_utils import extract_importance_from_text


class TestCanExtractImportanceFromText(unittest.TestCase):
    def test_can_extract_importance_from_text_that_has_number(self):
        text = "this text contains 7 a number somewhere."
        importance = extract_importance_from_text(text)

        self.assertEqual(importance, 7)


if __name__ == "__main__":
    unittest.main()
