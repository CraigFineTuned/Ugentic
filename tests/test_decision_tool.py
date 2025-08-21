
import unittest
from unittest.mock import MagicMock
import json
from src.ugentic.core.decision_tool import DecisionTool

class TestDecisionTool(unittest.TestCase):

    def setUp(self):
        """Set up the DecisionTool instance with a mock LLM."""
        self.mock_llm = MagicMock()
        self.decision_tool = DecisionTool(llm_model=self.mock_llm)

    def test_make_choice_success(self):
        """Test successful operation of make_choice."""
        mock_response = {
            "best_option": "Option C",
            "justification": "It is the most efficient."
        }
        self.mock_llm.invoke.return_value = json.dumps(mock_response)

        result = self.decision_tool.make_choice("question", ["A", "B", "C"])

        self.mock_llm.invoke.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_judge_proposal_success(self):
        """Test successful operation of judge_proposal."""
        mock_response = {
            "judgment": "Go",
            "justification": "The plan is solid and well-researched."
        }
        self.mock_llm.invoke.return_value = json.dumps(mock_response)

        result = self.decision_tool.judge_proposal("A solid plan.")

        self.mock_llm.invoke.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_llm_json_error_handling(self):
        """Test that the tool handles malformed JSON from the LLM gracefully."""
        self.mock_llm.invoke.return_value = "This is not JSON."

        result = self.decision_tool.make_choice("question", ["A", "B", "C"])

        self.assertIn("error", result)
        self.assertEqual(result["error"], "LLM did not return valid JSON.")

if __name__ == '__main__':
    unittest.main()
