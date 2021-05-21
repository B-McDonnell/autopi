import unittest


class TestRandom(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True != False)

    def test_2(self):
        self.assertTrue(True == True)

if __name__ == '__main__':
    unittest.main()
