import datetime
import unittest

from simulation_variables import load_simulation_variables


class TestSimulationVariables(unittest.TestCase):
    def test_can_load_simulation_config(self):
        comparison_time = datetime.datetime(2023, 5, 12, 10, 55, 45)

        simulation_variables = load_simulation_variables("test_1")

        self.assertEqual(comparison_time, simulation_variables["current_timestamp"])


if __name__ == "__main__":
    unittest.main()
