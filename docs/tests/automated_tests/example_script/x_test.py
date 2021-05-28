"""Example test script."""

import unittest


class TestRandom(unittest.TestCase):
    """Example unit test group."""

    def test_1(self):
        """Example unit test."""
        self.assertTrue(True != False)  # noqa: E712

    def test_2(self):
        """Example unit test."""
        self.assertTrue(True == True)  # noqa: E712


if __name__ == "__main__":
    unittest.main()
