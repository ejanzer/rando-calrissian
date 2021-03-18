import unittest
from rando import picker


class TestRando(unittest.TestCase):
    def test_parse_int_seed(self):
        self.assertEqual(picker.parse_seed('3'), 3)
        self.assertEqual(picker.parse_seed('11'), 11)

    def test_parse_complex_seed(self):
        self.assertEqual(picker.parse_seed('16b'), 16)


if __name__ == '__main__':
    unittest.main()
