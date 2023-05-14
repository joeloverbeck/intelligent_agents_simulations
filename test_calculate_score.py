import unittest

from math_utils import calculate_score


class TestCalculateScore(unittest.TestCase):
    def test_calculate_score_returns_same_values_as_in_paper(self):
        result_1 = calculate_score(0.91, 0.63, 0.80)
        result_2 = calculate_score(0.87, 0.63, 0.71)
        result_3 = calculate_score(0.85, 0.73, 0.62)

        self.assertAlmostEqual(result_1, 2.34)
        self.assertAlmostEqual(result_2, 2.21)
        self.assertAlmostEqual(result_3, 2.20)


if __name__ == "__main__":
    unittest.main()
