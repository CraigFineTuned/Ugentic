
import unittest
from datetime import datetime
from src.ugentic.core.time_tool import TimeTool

class TestTimeTool(unittest.TestCase):

    def setUp(self):
        """Set up the TimeTool instance for testing."""
        self.time_tool = TimeTool()

    def test_get_current_datetime(self):
        """Test that get_current_datetime returns a valid and recent datetime string."""
        result = self.time_tool.get_current_datetime()
        self.assertEqual(result["status"], "success")
        
        # Check that the datetime key exists and is a string
        self.assertIn("datetime", result)
        self.assertIsInstance(result["datetime"], str)
        
        # Check if the format is correct (YYYY-MM-DD HH:MM:SS)
        try:
            dt_from_tool = datetime.strptime(result["datetime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("Datetime string from tool does not match format YYYY-MM-DD HH:MM:SS")
        
        # Check if the time is recent (within a small delta, e.g., 2 seconds)
        time_difference = datetime.now() - dt_from_tool
        self.assertTrue(abs(time_difference.total_seconds()) < 2)

    def test_get_current_timestamp(self):
        """Test that get_current_timestamp returns a valid and recent timestamp float."""
        result = self.time_tool.get_current_timestamp()
        self.assertEqual(result["status"], "success")
        
        # Check that the timestamp key exists and is a float
        self.assertIn("timestamp", result)
        self.assertIsInstance(result["timestamp"], float)
        
        # Check if the timestamp is recent (within a small delta, e.g., 2 seconds)
        current_timestamp = datetime.now().timestamp()
        self.assertAlmostEqual(result["timestamp"], current_timestamp, delta=2)

if __name__ == '__main__':
    unittest.main()
