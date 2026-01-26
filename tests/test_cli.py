import unittest
import sys
from io import StringIO
from utils.cli import ProgressBar

class TestProgressBar(unittest.TestCase):
    def test_progress_bar_output(self):
        # Capture stdout
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            total = 100
            pb = ProgressBar(total, width=10)

            # Test update at 50%
            pb.update(50)
            output = captured_output.getvalue()
            # Carriage return should be present
            self.assertTrue(output.startswith('\r'))
            self.assertIn("50.0%", output)
            self.assertIn("(50/100)", output)
            self.assertIn("█", output)

            # Reset capture
            captured_output.truncate(0)
            captured_output.seek(0)

            # Test finish
            pb.finish()
            output = captured_output.getvalue()
            self.assertEqual(output, "\n")

        finally:
            # Restore stdout
            sys.stdout = original_stdout

if __name__ == '__main__':
    unittest.main()
