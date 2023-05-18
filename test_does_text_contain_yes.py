import unittest

from regular_expression_utils import does_text_contain_yes


class TestDoesTextContainYes(unittest.TestCase):
    def test_text_that_contains_yes_returns_true(self):
        text = "this text contains yes the word"

        self.assertTrue(does_text_contain_yes(text))

    def test_text_that_contains_yes_right_at_beginning(self):
        text = "Yes."

        self.assertTrue(does_text_contain_yes(text))

    def test_text_that_doesnt_contain_yes_returns_false(self):
        text = "this text does not contain the needed word"

        self.assertFalse(does_text_contain_yes(text))

    def test_text_that_contains_yes_returns_true(self):
        self.assertTrue(does_text_contain_yes("Yes, I agree"))
        self.assertTrue(does_text_contain_yes("yes"))
        self.assertTrue(does_text_contain_yes("YES"))
        self.assertTrue(does_text_contain_yes("Hey, yes that's correct"))

    def test_text_that_doesnt_contain_yes_returns_false(self):
        self.assertFalse(does_text_contain_yes("No, I disagree"))
        self.assertFalse(does_text_contain_yes("maybe"))
        self.assertFalse(does_text_contain_yes("yesteryear"))
        self.assertFalse(does_text_contain_yes("Yessir"))


if __name__ == "__main__":
    unittest.main()
