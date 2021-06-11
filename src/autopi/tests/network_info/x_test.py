"""Example test script."""

import unittest

from autopi.util import network_info


class TestRandom(unittest.TestCase):
    """Example unit test group."""

    def test_1(self):
        """Example unit test."""
        self.assertIn(network_info.get_mac("wlp3s0"), "54:27:1e:90:60:38")


if __name__ == "__main__":
    unittest.main()
