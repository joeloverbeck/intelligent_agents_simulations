import unittest

from sandbox_object import SandboxObject


class TestSandboxObjects(unittest.TestCase):
    def test_can_create_sandbox_object(self):
        sandbox_object = SandboxObject(
            "desk",
            "desk",
            "a piece of furniture where people read, write, or sit at a computer",
        )

        self.assertEqual(sandbox_object.name, "desk")


if __name__ == "__main__":
    unittest.main()
