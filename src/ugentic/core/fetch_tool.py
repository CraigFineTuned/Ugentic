# Fetch Tool for UGENTIC Agents

import requests

class FetchTool:
    def __init__(self):
        self.name = "FetchTool"
        self.description = "Retrieves raw data from web pages and APIs."
        print(f"{self.name} initialized.")

    def fetch_url_content(self, url):
        """Fetches the content of a given URL, handling HTTP errors gracefully."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            print(f"  [FetchTool]: Successfully fetched content from '{url}'.")
            return {"status": "success", "content": response.text}
        except requests.exceptions.HTTPError as e:
            print(f"  [FetchTool]: HTTP Error fetching '{url}': {e.response.status_code} {e.response.reason}")
            return {"status": "error", "message": f"Failed to fetch content due to an HTTP error: {e.response.status_code} {e.response.reason}"}
        except requests.exceptions.RequestException as e:
            print(f"  [FetchTool]: Error fetching '{url}': {e}")
            return {"status": "error", "message": f"Failed to fetch content: {e}"}

# Example Usage (for testing)
if __name__ == "__main__":
    fetch_tool = FetchTool()
    
    # Example: Fetch content from a public website
    test_url = "https://www.example.com"
    content_result = fetch_tool.fetch_url_content(test_url)
    
    if content_result["status"] == "success":
        print(f"Fetched content (first 200 chars):\n{content_result['content'][:200]}...")
    else:
        print(f"Error: {content_result['message']}")

