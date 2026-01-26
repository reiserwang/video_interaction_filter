import unittest
from core.comparator import Comparator

class TestComparator(unittest.TestCase):
    def test_hybrid_method_crash(self):
        """Test that using 'hybrid' method does not crash."""
        comparator = Comparator()
        # This triggers the bug if 'hybrid' is not in stats
        try:
            comparator.update('hybrid', True, True, False)
        except KeyError:
            self.fail("Comparator.update raised KeyError for 'hybrid' method")

    def test_dynamic_method_names(self):
        """Test that arbitrary method names work."""
        comparator = Comparator()
        comparator.update('new_method', True, True, True)
        self.assertIn('new_method', comparator.stats)
        self.assertEqual(comparator.stats['new_method']['triggers'], 1)

if __name__ == '__main__':
    unittest.main()
