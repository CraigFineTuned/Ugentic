

import unittest
from unittest.mock import patch, MagicMock
import subprocess
from src.ugentic.core.git_tool import GitTool

class TestGitTool(unittest.TestCase):

    def setUp(self):
        self.git_tool = GitTool()

    @patch('src.ugentic.core.git_tool.subprocess.run')
    def test_get_status_success(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "On branch master\nnothing to commit, working tree clean\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        result = self.git_tool.get_status()

        mock_subprocess_run.assert_called_once_with(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("On branch master", result["output"])

    @patch('src.ugentic.core.git_tool.subprocess.run')
    def test_get_log_success(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "abcde Commit 1\nfghij Commit 2\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        result = self.git_tool.get_log(num_commits=2)

        mock_subprocess_run.assert_called_once_with(
            ["git", "log", "-2", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("Commit 1", result["output"])

    @patch('src.ugentic.core.git_tool.subprocess.run')
    def test_get_diff_success(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "diff --git a/file.txt b/file.txt\nindex 123..456 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-old line\n+new line\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        result = self.git_tool.get_diff("file.txt")

        mock_subprocess_run.assert_called_once_with(
            ["git", "diff", "file.txt"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("new line", result["output"])

    @patch('src.ugentic.core.git_tool.subprocess.run')
    def test_git_command_failure(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "status"],
            stderr="fatal: not a git repository (or any of the parent directories): .git\n"
        )

        result = self.git_tool.get_status()

        self.assertEqual(result["status"], "error")
        self.assertIn("Git command failed", result["message"])

    @patch('src.ugentic.core.git_tool.subprocess.run')
    def test_git_not_found(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = FileNotFoundError("git: command not found")

        result = self.git_tool.get_status()

        self.assertEqual(result["status"], "error")
        self.assertIn("Git command not found", result["message"])

if __name__ == '__main__':
    unittest.main()

