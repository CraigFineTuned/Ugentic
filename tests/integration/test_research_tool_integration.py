
import pytest
from src.ugentic.core.research_tool import ResearchTool

@pytest.mark.integration
def test_research_tool_with_live_web_search():
    """
    Integration test to verify the ResearchTool can use the live DuckDuckGo API.
    This test makes a real network call.
    """
    # Initialize the tool; no mocks needed for this integration test
    research_tool = ResearchTool()

    # Perform a web search
    query = "latest advancements in AI"
    result = research_tool.perform_web_search(query)

    # Assertions
    assert result is not None
    assert result["status"] == "success"
    assert "data" in result
    # The perform_duckduckgo_search function returns a dictionary with a 'results' key
    assert "results" in result["data"]
    # We can't know the exact number of results, but there should be some
    assert isinstance(result["data"]["results"], list)
    # Let's check that if there are results, they have the expected keys
    if result["data"]["results"]:
        for item in result["data"]["results"]:
            assert "title" in item
            assert "snippet" in item
