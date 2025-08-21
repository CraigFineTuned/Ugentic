# Research Tool for UGENTIC Agents

from .fetch_tool import FetchTool
import requests
import json

def perform_duckduckgo_search(query: str):
    """Performs a web search using the DuckDuckGo Instant Answer API."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Format the results to be similar to the expected google_web_search output
        results = []
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", query),
                "snippet": data.get("AbstractText"),
            })
        for related_topic in data.get("RelatedTopics", []):
            if related_topic.get("Text"):
                results.append({
                    "title": related_topic.get("Text"),
                    "snippet": related_topic.get("FirstURL", ""),
                })
        return {"results": results}
    except requests.exceptions.RequestException as e:
        print(f"  [DuckDuckGo Search]: Network error occurred: {e}")
        return {"results": []}

class ResearchTool:
    def __init__(self, fetch_tool: FetchTool = None, rag_system=None, llm_model=None):
        self.name = "ResearchTool"
        self.description = "Synthesizes information from multiple sources, including web searches and internal documents, into a coherent analysis."
        self.fetch_tool = fetch_tool if fetch_tool else FetchTool()
        self.rag_system = rag_system
        self.llm_model = llm_model
        print(f"{self.name} initialized.")

    def perform_web_search(self, query):
        """Performs a web search using the available web search tool."""
        print(f"  [ResearchTool]: Performing web search for query: '{query}'")
        try:
            # Call the new, internal search function
            result = perform_duckduckgo_search(query=query)
            print(
                f"  [ResearchTool]: Web search returned {len(result.get('results', []))} results."
            )
            return {"status": "success", "data": result}
        except Exception as e:
            print(f"  [ResearchTool]: Web search failed: {e}")
            return {"status": "error", "message": str(e)}

    def perform_research(self, query, sources=None):
        """Performs research based on a query, optionally using specified sources or web search."""
        print(f"  [ResearchTool]: Performing research for query: '{query}'")
        all_information = []

        # Step 1: Use RAG system if available and query is suitable
        if self.rag_system:
            print("  [ResearchTool]: Querying RAG system for internal documents.")
            rag_context = self.rag_system.retrieve(query)
            if rag_context:
                for chunk in rag_context:
                    all_information.append(
                        f"Internal Document Context: {chunk['chunk_text']}"
                    )
            else:
                all_information.append("No relevant internal documents found.")

        # Step 2: Process provided sources
        if sources:
            if isinstance(sources, str):
                sources = [sources]
            for source_item in sources:
                if source_item.startswith("http://") or source_item.startswith("https://"):
                    # Treat as a URL for FetchTool
                    print(f"  [ResearchTool]: Fetching content from URL: {source_item}")
                    fetch_result = self.fetch_tool.fetch_url_content(source_item)
                    if fetch_result["status"] == "success":
                        all_information.append(f"Content from {source_item}: {fetch_result['content'][:200]}...")
                    else:
                        all_information.append(f"Failed to fetch from {source_item}: {fetch_result['message']}")
                elif self.rag_system:
                    # Treat as a local document name for RAG system
                    print(f"  [ResearchTool]: Querying RAG system for local document: {source_item}")
                    # Assuming RAG system can retrieve by document name or content related to it
                    rag_context = self.rag_system.retrieve(source_item)
                    if rag_context:
                        for chunk in rag_context:
                            all_information.append(f"Internal Document Context ({source_item}): {chunk['chunk_text']}")
                    else:
                        all_information.append(f"No relevant internal documents found for '{source_item}'.")
                else:
                    all_information.append(f"Source '{source_item}' not recognized as URL or internal document, and RAG system not available.")
        else:
            # Step 3: Perform web search if no specific sources are provided
            web_search_result = self.perform_web_search(query)
            if (
                web_search_result["status"] == "success"
                and web_search_result["data"]["results"]
            ):
                for res in web_search_result["data"]["results"]:
                    all_information.append(
                        f"Web Search Result: {res['title']} - {res['snippet']}"
                    )
            else:
                all_information.append("No relevant web search results found.")

        # Step 4: Synthesize all gathered information using LLM
        if not all_information:
            return {
                "status": "success",
                "summary": "No information found for the query.",
            }

        synthesis_prompt = (
            "YOUR RESPONSE MUST BE ONLY A JSON OBJECT. DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION.\n"
            f"You have been asked to research the query: '{query}'.\n"
            "Synthesize the following pieces of information into a coherent summary that DIRECTLY addresses the research query. "            "CRITICAL: If a piece of information seems irrelevant to the query (e.g., an HR policy for a market research query), you MUST ignore it. "            "When using the FetchTool, ensure that any 'sources' provided are valid URLs starting with 'http://' or 'https://'. Do NOT invent URLs or use generic terms like 'web search' or 'internal documents' as URLs. "            "Base your summary and key findings ONLY on the relevant information.\n\n"
            "Information:\n"
            "{}".format("\n".join(all_information))
            + '\n\nRespond with ONLY a JSON object in the format: {{"summary": "your_summary", "key_findings": ["finding1", "finding2"]}}'
        )
        try:
            response = self.llm_model.invoke(synthesis_prompt)
            print(
                f"  [ResearchTool LLM - Raw Response]: {response[:500]}..."
            )  # Added debug print

            # --- Robust JSON Parsing (copied from Agent._interact_with_llm) ---
            cleaned_str = response.strip()
            if cleaned_str.startswith("```json"):
                cleaned_str = cleaned_str[7:]
            if cleaned_str.endswith("```"):
                cleaned_str = cleaned_str[:-3]

            json_start = cleaned_str.find("{")
            if json_start == -1:
                json_start = cleaned_str.find("[")

            json_end = cleaned_str.rfind("}")
            if json_end == -1:
                json_end = cleaned_str.rfind("]")

            if json_start == -1 or json_end == -1:
                raise json.JSONDecodeError(
                    "No JSON object or array found in response.", cleaned_str, 0
                )

            json_str = cleaned_str[json_start : json_end + 1]
            print(
                f"  [ResearchTool LLM - JSON String to Parse]: {json_str[:500]}..."
            )  # Debug print

            synthesis_data = json.loads(json_str)
            return {
                "status": "success",
                "summary": synthesis_data.get("summary"),
                "key_findings": synthesis_data.get("key_findings", []),
            }
        except json.JSONDecodeError as e:
            print(f"  [ResearchTool LLM]: Failed to parse JSON from LLM response: {e}")
            print(f"  [ResearchTool LLM]: Raw LLM response was: {response}")
            return {
                "status": "error",
                "message": "Failed to synthesize information due to invalid LLM response.",
                "raw_response": response,
            }
        except Exception as e:
            print(f"  [ResearchTool LLM]: Error invoking LLM for synthesis: {e}")
            return {
                "status": "error",
                "message": f"Failed to synthesize due to LLM error: {e}",
            }
            return {
                "status": "error",
                "message": "Failed to synthesize information due to invalid LLM response.",
            }


# Example Usage (for testing)
if __name__ == "__main__":
    from unittest.mock import MagicMock
    from .rag_core import RAGCore, get_text_splitter

    # Mock FetchTool
    mock_fetch_tool = MagicMock()
    mock_fetch_tool.fetch_url_content.return_value = {
        "status": "success",
        "content": "Mock content from URL.",
        "message": "",
    }

    # Mock RAG system
    mock_embeddings = MagicMock()
    mock_embeddings.embed_documents.return_value = [[0.1, 0.2]]
    mock_embeddings.embed_query.return_value = [0.1, 0.2]
    mock_rag_system = RAGCore(mock_embeddings, get_text_splitter())
    mock_rag_system.add_document("internal_doc", "Internal policy details.")

    research_tool = ResearchTool(fetch_tool=mock_fetch_tool, rag_system=mock_rag_system)

    print("\n--- Testing perform_research with web search (no sources) ---")
    web_research_result = research_tool.perform_research(query="Latest AI trends")
    print(f"Web Research Result: {web_research_result}")

    print("\n--- Testing perform_research with specific sources ---")
    sourced_research_result = research_tool.perform_research(
        query="Company financial report", sources=["http://example.com/report.pdf"]
    )
    print(f"Sourced Research Result: {sourced_research_result}")

    print("\n--- Testing perform_research with internal document query ---")
    internal_research_result = research_tool.perform_research(
        query="internal document about internal policy details"
    )
    print(f"Internal Research Result: {internal_research_result}")
