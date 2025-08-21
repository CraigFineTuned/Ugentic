
import unittest
import os
import shutil
from src.ugentic.core.filesystem_tool import FilesystemTool

class TestFilesystemTool(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = "test_temp_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.fs_tool = FilesystemTool(base_path=self.test_dir)
        self.test_file_name = "test_file.txt"
        self.test_file_content = "Hello, world!"

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_write_and_read_file(self):
        """Test writing to a file and then reading from it."""
        # Test write
        write_result = self.fs_tool.write_file(self.test_file_name, self.test_file_content)
        self.assertEqual(write_result["status"], "success")
        
        # Verify file exists
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, self.test_file_name)))

        # Test read
        read_result = self.fs_tool.read_file(self.test_file_name)
        self.assertEqual(read_result["status"], "success")
        self.assertEqual(read_result["content"], self.test_file_content)

    def test_read_file_not_found(self):
        """Test reading a file that does not exist."""
        read_result = self.fs_tool.read_file("non_existent_file.txt")
        self.assertEqual(read_result["status"], "error")
        self.assertIn("File not found", read_result["message"])

    def test_list_directory(self):
        """Test listing the contents of a directory."""
        # Create a dummy file and a subdirectory
        with open(os.path.join(self.test_dir, self.test_file_name), "w") as f:
            f.write(self.test_file_content)
        os.makedirs(os.path.join(self.test_dir, "subdir"))

        list_result = self.fs_tool.list_directory(".") # List the base test directory
        self.assertEqual(list_result["status"], "success")
        self.assertIn(self.test_file_name, list_result["contents"])
        self.assertIn("subdir", list_result["contents"])
        self.assertEqual(len(list_result["contents"]), 2)

    def test_delete_file(self):
        """Test deleting a file."""
        file_path = os.path.join(self.test_dir, self.test_file_name)
        with open(file_path, "w") as f:
            f.write(self.test_file_content)
        
        self.assertTrue(os.path.exists(file_path))

        delete_result = self.fs_tool.delete_file(self.test_file_name)
        self.assertEqual(delete_result["status"], "success")
        
        self.assertFalse(os.path.exists(file_path))

    def test_delete_file_not_found(self):
        """Test deleting a file that does not exist."""
        delete_result = self.fs_tool.delete_file("non_existent_file.txt")
        self.assertEqual(delete_result["status"], "error")
        self.assertIn("File not found", delete_result["message"])

if __name__ == '__main__':
    unittest.main()
