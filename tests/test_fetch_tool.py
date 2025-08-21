
import unittest
from unittest.mock import patch, Mock
import requests
from src.ugentic.core.fetch_tool import FetchTool

class TestFetchTool(unittest.TestCase):

    def setUp(self):
        """Set up the FetchTool instance for testing."""
        self.fetch_tool = FetchTool()

    @patch('src.ugentic.core.fetch_tool.requests.get')
    def test_fetch_url_content_success(self, mock_get):
        """Test successful fetching of URL content."""
        # Configure the mock to return a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Success</h1></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Call the method
        result = self.fetch_tool.fetch_url_content("http://example.com")

        # Assertions
        mock_get.assert_called_once_with("http://example.com", timeout=10)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content"], "<html><body><h1>Success</h1></body></html>")

    @patch('src.ugentic.core.fetch_tool.requests.get')
    def test_fetch_url_content_http_error(self, mock_get):
        """Test handling of an HTTP error during fetch."""
        # Create a more realistic HTTPError with a response attribute
        mock_http_error = requests.exceptions.HTTPError("404 Client Error: Not Found for url: http://example.com/notfound")
        mock_http_error.response = Mock()
        mock_http_error.response.status_code = 404
        mock_http_error.response.reason = "Not Found"

        # Configure the mock response object
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = mock_http_error
        mock_get.return_value = mock_response

        # Call the method
        result = self.fetch_tool.fetch_url_content("http://example.com/notfound")

        # Assertions
        mock_get.assert_called_once_with("http://example.com/notfound", timeout=10)
        self.assertEqual(result["status"], "error")
        self.assertIn("Failed to fetch content due to an HTTP error: 404 Not Found", result["message"])

    @patch('src.ugentic.core.fetch_tool.requests.get')
    def test_fetch_url_content_request_exception(self, mock_get):
        """Test handling of a general request exception."""
        # Configure the mock to raise a RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        # Call the method
        result = self.fetch_tool.fetch_url_content("http://example.com/connect-error")

        # Assertions
        mock_get.assert_called_once_with("http://example.com/connect-error", timeout=10)
        self.assertEqual(result["status"], "error")
        self.assertIn("Connection Error", result["message"])

if __name__ == '__main__':
    unittest.main()
