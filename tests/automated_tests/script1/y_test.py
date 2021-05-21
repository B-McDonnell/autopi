import unittest
import os


class TestRandom(unittest.TestCase):
    def test_1(self):
        self.assertEqual(os.getcwd(),"/home/pi/autopi/tests/automated_tests/script1")

    def test_2(self):
        self.assertTrue(True)

    def test_3(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
