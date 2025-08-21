"""
Unit tests for the ResearchTool component.
Tests the research synthesis capabilities including RAG integration and source fetching.
"""

import unittest
from unittest.mock import MagicMock, patch, Mock
import json
from src.ugentic.core.research_tool import ResearchTool
from src.ugentic.core.fetch_tool import FetchTool
from src.ugentic.core.rag_core import RAGCore

class TestResearchTool(unittest.TestCase):

    def setUp(self):
        self.mock_fetch_tool = MagicMock(spec=FetchTool)
        self.mock_rag_system = MagicMock(spec=RAGCore)
        self.mock_llm = MagicMock()
        self.research_tool = ResearchTool(
            fetch_tool=self.mock_fetch_tool,
            rag_system=self.mock_rag_system,
            llm_model=self.mock_llm
        )

    @patch('src.ugentic.core.research_tool.requests.get')
    def test_perform_web_search(self, mock_get):
        """Test web search functionality with a mocked backend."""
        mock_response = Mock()
        mock_response.json.return_value = {"AbstractText": "Test snippet"}
        mock_get.return_value = mock_response

        result = self.research_tool.perform_web_search("test query")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("results", result["data"])

    @patch('src.ugentic.core.research_tool.requests.get')
    def test_perform_research_no_sources(self, mock_get):
        """Test perform_research when it falls back to web search."""
        mock_response = Mock()
        mock_response.json.return_value = {"AbstractText": "Test snippet"}
        mock_get.return_value = mock_response
        self.mock_rag_system.retrieve.return_value = []

        self.research_tool.perform_research(query="test query", sources=None)
        mock_get.assert_called_once()

class TestResearchToolBugFixes(unittest.TestCase):
    
    def test_res_1_bug_string_iteration_fix(self):
        """Test fix for RES-1: URL string being iterated character by character."""
        mock_fetch = MagicMock(spec=FetchTool)
        mock_fetch.fetch_url_content.return_value = {"status": "success", "content": "Test content"}
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = json.dumps({"summary": "Test", "key_findings": []})
        research_tool = ResearchTool(fetch_tool=mock_fetch, llm_model=mock_llm)
        
        url_string = "https://example.com/report.pdf"
        with patch('src.ugentic.core.research_tool.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {}
            research_tool.perform_research("test", sources=url_string)
        
        mock_fetch.fetch_url_content.assert_called_once_with(url_string)

