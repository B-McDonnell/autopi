"""wpa_interface test script."""

import unittest

from autopi.util import wpa_interface


class TestSSID(unittest.TestCase):
    """Tests for ensuring is_valid_ssid works."""

    def test_small(self):
        """Check too small."""
        self.assertFalse(wpa_interface.is_valid_ssid(""))

    def test_large(self):
        """Check too large."""
        self.assertFalse(wpa_interface.is_valid_ssid("a" * 100))
        self.assertFalse(wpa_interface.is_valid_ssid("a" * 33))
        self.assertFalse(wpa_interface.is_valid_ssid("dsbcdefgicalshgljd" * 2))

    def test_good(self):
        """Check valid SSIDs."""
        self.assertTrue(wpa_interface.is_valid_ssid("a"))
        self.assertTrue(wpa_interface.is_valid_ssid("a" * 32))
        self.assertTrue(wpa_interface.is_valid_ssid("!@#$%^&*()_+=-.!/?><\";:'\\|{}[]"))
        self.assertTrue(wpa_interface.is_valid_ssid("abcdefghijklmnopqrstuvwxyz"))
        self.assertTrue(wpa_interface.is_valid_ssid("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertTrue(wpa_interface.is_valid_ssid("0123456789"))


class TestPassword(unittest.TestCase):
    """Tests for ensuring is_valid_passwd works."""

    def test_small(self):
        """Check too small."""
        self.assertFalse(wpa_interface.is_valid_passwd(""))
        self.assertFalse(wpa_interface.is_valid_passwd("abcdabc"))

    def test_large(self):
        """Check too large."""
        self.assertFalse(wpa_interface.is_valid_passwd("a" * 1000))
        self.assertFalse(wpa_interface.is_valid_passwd("a" * 64))
        self.assertFalse(wpa_interface.is_valid_passwd("dsbcdefgicalshgljd" * 4))

    def test_good(self):
        """Check valid passwords."""
        self.assertTrue(wpa_interface.is_valid_passwd("a" * 8))
        self.assertTrue(wpa_interface.is_valid_passwd("a" * 63))
        self.assertTrue(
            wpa_interface.is_valid_passwd("!@#$%^&*()_+=-.!/?><\";:'\\|{}[]")
        )
        self.assertTrue(wpa_interface.is_valid_passwd("abcdefghijklmnopqrstuvwxyz"))
        self.assertTrue(wpa_interface.is_valid_passwd("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertTrue(wpa_interface.is_valid_passwd("0123456789"))


if __name__ == "__main__":
    unittest.main()
