# Git Tool for UGENTIC Agents

import subprocess

class GitTool:
    def __init__(self):
        self.name = "GitTool"
        self.description = "Interacts with Git repositories to analyze code and manage versions."
        print(f"{self.name} initialized.")

    def _run_git_command(self, command_args):
        """Helper to run a git command and return its output."""
        try:
            result = subprocess.run(
                ["git"] + command_args,
                capture_output=True,
                text=True, # Capture output as text
                check=True # Raise an exception for non-zero exit codes
            )
            return {"status": "success", "output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Git command failed: {e.stderr.strip()}"}
        except FileNotFoundError:
            return {"status": "error", "message": "Git command not found. Is Git installed and in PATH?"}
        except Exception as e:
            return {"status": "error", "message": f"An unexpected error occurred: {e}"}

    def get_status(self):
        """Returns the current status of the Git repository."""
        print(f"  [GitTool]: Getting git status.")
        return self._run_git_command(["status"])

    def get_log(self, num_commits=5):
        """Returns the recent commit history."""
        print(f"  [GitTool]: Getting git log (last {num_commits} commits).")
        return self._run_git_command(["log", f"-{num_commits}", "--oneline"])

    def get_diff(self, file_path=None):
        """Returns the differences between files or the entire working tree."""
        print(f"  [GitTool]: Getting git diff.")
        if file_path:
            return self._run_git_command(["diff", file_path])
        else:
            return self._run_git_command(["diff"])

# Example Usage (for testing)
if __name__ == "__main__":
    git_tool = GitTool()

    print("\n--- Testing get_status ---")
    status_result = git_tool.get_status()
    print(f"Status Result: {status_result}")

    print("\n--- Testing get_log ---")
    log_result = git_tool.get_log(num_commits=3)
    print(f"Log Result: {log_result}")

    # Note: get_diff will only show output if there are uncommitted changes
    print("\n--- Testing get_diff (no changes expected) ---")
    diff_result = git_tool.get_diff()
    print(f"Diff Result: {diff_result}")

    # Example of diff for a specific file (assuming it exists and has changes)
    # with open("test_file_for_diff.txt", "w") as f:
    #     f.write("This is a test file.\n")
    #     f.write("Adding a new line.\n")
    # diff_file_result = git_tool.get_diff("test_file_for_diff.txt")
    # print(f"Diff File Result: {diff_file_result}")
    # os.remove("test_file_for_diff.txt")
