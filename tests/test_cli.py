import unittest
from utils.cli import ProgressBar

class TestProgressBar(unittest.TestCase):
    def test_initialization(self):
        pb = ProgressBar(total=100)
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.processed, 0)

    def test_bar_string_format(self):
        pb = ProgressBar(total=100, length=10)
        # iteration 50 -> 50% -> 5 chars filled
        bar_str = pb.get_bar_string(50)
        self.assertIn('|█████-----|', bar_str)
        self.assertIn('50.0%', bar_str)

    def test_bar_string_complete(self):
        pb = ProgressBar(total=100, length=10)
        bar_str = pb.get_bar_string(100)
        self.assertIn('|██████████|', bar_str)
        self.assertIn('100.0%', bar_str)

    def test_zero_total(self):
        # Edge case: avoid division by zero
        pb = ProgressBar(total=0)
        try:
            bar_str = pb.get_bar_string(0)
            self.assertIn('100.0%', bar_str)
        except ZeroDivisionError:
            self.fail("ProgressBar raised ZeroDivisionError with total=0")

if __name__ == '__main__':
    unittest.main()
