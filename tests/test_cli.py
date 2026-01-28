import unittest
from unittest.mock import patch
import sys
import io
import time
from utils.cli import ProgressBar

class TestProgressBar(unittest.TestCase):
    def test_init(self):
        pb = ProgressBar(total=100)
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.prefix, 'Progress')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_deterministic(self, mock_stdout):
        # Test with known total
        pb = ProgressBar(total=100, length=10)
        # Mock time to avoid flaky tests based on speed
        pb.start_time = time.time() - 10 # 10 seconds ago

        # Force update regardless of throttling
        pb.last_update_time = 0

        pb.update(50)
        output = mock_stdout.getvalue()

        # Check basic components
        self.assertIn('Progress', output)
        self.assertIn('50.0%', output)
        self.assertIn('FPS:', output)
        self.assertIn('ETA:', output)
        self.assertIn('|', output) # Bar borders

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_indeterminate(self, mock_stdout):
        # Test without known total
        pb = ProgressBar(total=0)
        pb.start_time = time.time() - 10

        pb.last_update_time = 0
        pb.update(50)
        output = mock_stdout.getvalue()

        self.assertIn('Progress', output)
        self.assertIn('50 frames', output)
        self.assertIn('FPS:', output)
        self.assertNotIn('%', output) # No percentage in indeterminate mode

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_finish(self, mock_stdout):
        pb = ProgressBar(total=100)
        pb.finish()
        self.assertEqual(mock_stdout.getvalue(), '\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_log(self, mock_stdout):
        pb = ProgressBar(total=100)
        pb.log("Test Log")
        output = mock_stdout.getvalue()
        # Should contain Clear Line code, Message, and Newline
        self.assertIn('\r\033[K', output)
        self.assertIn('Test Log\n', output)

if __name__ == '__main__':
    unittest.main()
