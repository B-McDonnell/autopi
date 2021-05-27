"""Example test script."""

import os
import unittest


class TestRandom(unittest.TestCase):
    """Example unit test group."""

    def test_1(self):
        """Example unit test."""
        self.assertEqual(os.getcwd(), "/home/pi/autopi/tests/automated_tests/script1")

    def test_2(self):
        """Example unit test."""
        self.assertTrue(True)

    def test_3(self):
        """Example unit test."""
        self.fail()


if __name__ == "__main__":
    unittest.main()
