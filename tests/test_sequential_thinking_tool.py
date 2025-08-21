
import unittest
from unittest.mock import MagicMock
import json
from src.ugentic.core.sequential_thinking_tool import SequentialThinkingTool

class TestSequentialThinkingTool(unittest.TestCase):

    def setUp(self):
        self.mock_llm = MagicMock()
        self.seq_tool = SequentialThinkingTool(llm_model=self.mock_llm)

    def test_decompose_goal_success(self):
        mock_response = [
            {"step": 1, "task": "Task A", "agent": "AgentX"},
            {"step": 2, "task": "Task B", "agent": "AgentY"}
        ]
        self.mock_llm.invoke.return_value = json.dumps(mock_response)

        result = self.seq_tool.decompose_goal("High-level goal")

        self.mock_llm.invoke.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_decompose_goal_invalid_json(self):
        self.mock_llm.invoke.return_value = "Invalid JSON"

        result = self.seq_tool.decompose_goal("High-level goal")

        self.mock_llm.invoke.assert_called_once()
        self.assertEqual(result, [])

    def test_execute_sequence(self):
        sequence = [
            {"step": 1, "task": "Task A", "agent": "AgentX"},
            {"step": 2, "task": "Task B", "agent": "AgentY"}
        ]
        result = self.seq_tool.execute_sequence(sequence)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["executed_tasks"], 2)

if __name__ == '__main__':
    unittest.main()
