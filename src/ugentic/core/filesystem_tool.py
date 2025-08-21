# Filesystem Tool for UGENTIC Agents

import os

class FilesystemTool:
    def __init__(self, base_path='.'):
        self.name = "Filesystem Tool"
        self.description = "Provides secure access to read from and write to the local file system."
        self.base_path = os.path.abspath(base_path)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        print(f"{self.name} initialized with base path: {self.base_path}")

    def _get_safe_path(self, file_path):
        """Joins the base path with the provided file path and ensures it's safe."""
        # Normalize the path to prevent directory traversal issues (e.g., ../../)
        safe_path = os.path.abspath(os.path.join(self.base_path, file_path))
        if not safe_path.startswith(self.base_path):
            raise ValueError("Attempted to access a path outside the designated base directory.")
        return safe_path

    def read_file(self, file_path):
        """Reads the content of a specified file within the base path."""
        try:
            safe_path = self._get_safe_path(file_path)
            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"  [FilesystemTool]: Read file '{safe_path}'.")
            return {"status": "success", "content": content}
        except FileNotFoundError:
            print(f"  [FilesystemTool]: Error: File not found at '{file_path}'.")
            return {"status": "error", "message": "File not found"}
        except (Exception, ValueError) as e:
            print(f"  [FilesystemTool]: Error reading '{file_path}': {e}")
            return {"status": "error", "message": str(e)}

    def write_file(self, file_path, content):
        """Writes content to a specified file within the base path."""
        try:
            safe_path = self._get_safe_path(file_path)
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(safe_path), exist_ok=True)
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [FilesystemTool]: Wrote to file '{safe_path}'.")
            return {"status": "success", "message": "File written successfully"}
        except (Exception, ValueError) as e:
            print(f"  [FilesystemTool]: Error writing to '{file_path}': {e}")
            return {"status": "error", "message": str(e)}

    def list_directory(self, dir_path='.'):
        """Lists the contents of a specified directory within the base path."""
        try:
            safe_path = self._get_safe_path(dir_path)
            if not os.path.exists(safe_path):
                print(f"  [FilesystemTool]: Error: Directory not found at '{dir_path}'.")
                return {"status": "error", "message": f"Directory not found at '{dir_path}'"}
            if not os.path.isdir(safe_path):
                print(f"  [FilesystemTool]: Error: '{dir_path}' is not a directory.")
                return {"status": "error", "message": f"'{dir_path}' is not a directory."}
            contents = os.listdir(safe_path)
            print(f"  [FilesystemTool]: Listed directory '{safe_path}'.")
            return {"status": "success", "contents": contents}
        except (Exception, ValueError) as e:
            print(f"  [FilesystemTool]: Error listing directory '{dir_path}': {e}")
            return {"status": "error", "message": str(e)}

    def delete_file(self, file_path):
        """Deletes a specified file within the base path."""
        try:
            safe_path = self._get_safe_path(file_path)
            if not os.path.isfile(safe_path):
                return {"status": "error", "message": "File not found"}
            os.remove(safe_path)
            print(f"  [FilesystemTool]: Deleted file '{safe_path}'.")
            return {"status": "success", "message": "File deleted successfully"}
        except (Exception, ValueError) as e:
            print(f"  [FilesystemTool]: Error deleting file '{file_path}': {e}")
            return {"status": "error", "message": str(e)}

# Example Usage (for testing)
if __name__ == "__main__":
    # This demonstrates usage within a temporary, safe directory
    temp_dir_for_demo = "temp_fs_tool_demo"
    fs_tool = FilesystemTool(base_path=temp_dir_for_demo)
    test_file = "test_output.txt"
    
    print("\n--- Writing and Reading ---")
    write_result = fs_tool.write_file(test_file, "Hello, UGENTIC Filesystem!\nThis is a test.")
    print(f"Write Result: {write_result}")
    read_result = fs_tool.read_file(test_file)
    print(f"Read Result: {read_result}")

    print("\n--- Listing Directory ---")
    list_result = fs_tool.list_directory('.')
    print(f"List Result: {list_result}")

    print("\n--- Deleting File ---")
    delete_result = fs_tool.delete_file(test_file)
    print(f"Delete Result: {delete_result}")

    # Clean up the temporary directory
    if os.path.exists(temp_dir_for_demo):
        os.rmdir(temp_dir_for_demo)
        print(f"\nCleaned up demo directory: {temp_dir_for_demo}")