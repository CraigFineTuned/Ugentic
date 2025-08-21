
import pytest
from unittest.mock import Mock

# Imports for type checking
from src.ugentic.core.agent_framework import Agent
from src.ugentic.core.filesystem_tool import FilesystemTool
from src.ugentic.core.time_tool import TimeTool
from src.ugentic.core.fetch_tool import FetchTool
from src.ugentic.core.research_tool import ResearchTool
from src.ugentic.core.decision_tool import DecisionTool
from src.ugentic.core.sequential_thinking_tool import SequentialThinkingTool
from src.ugentic.core.git_tool import GitTool
from src.ugentic.core.memory_tool import MemoryTool
from src.ugentic.core.analysis_tool import AnalysisTool

# Function to be tested
from src.ugentic.agents.departmental_agents import initialize_departmental_agents

@pytest.fixture
def mock_rag_system():
    """Provides a mock RAG system instance."""
    return Mock()

@pytest.fixture
def mock_llm():
    """Provides a mock LLM model instance."""
    return Mock()

@pytest.fixture
def departmental_agents(mock_rag_system, mock_llm):
    """Fixture to initialize and return the agents dictionary."""
    return initialize_departmental_agents(mock_rag_system, mock_llm)

class TestDepartmentalAgents:

    def test_initialization_structure(self, departmental_agents):
        """Tests that the main dictionary of agents is structured correctly."""
        assert isinstance(departmental_agents, dict)
        assert len(departmental_agents) == 5
        expected_keys = ["Finance", "HR", "Operations", "Marketing", "Sales"]
        assert all(key in departmental_agents for key in expected_keys)
        assert all(isinstance(agent, Agent) for agent in departmental_agents.values())

    def test_finance_agent_config(self, departmental_agents):
        """Tests the configuration of the FinanceAgent."""
        agent = departmental_agents["Finance"]
        assert agent.name == "FinanceAgent"
        assert agent.persona

        tool_types = {type(tool) for tool in agent.tools.values()}
        expected_tools = {ResearchTool, DecisionTool, FilesystemTool, AnalysisTool}
        assert tool_types == expected_tools

    def test_hr_agent_config(self, departmental_agents):
        """Tests the configuration of the HRAgent."""
        agent = departmental_agents["HR"]
        assert agent.name == "HRAgent"
        assert agent.persona

        tool_types = {type(tool) for tool in agent.tools.values()}
        expected_tools = {FilesystemTool, ResearchTool, DecisionTool, TimeTool}
        assert tool_types == expected_tools

    def test_operations_agent_config(self, departmental_agents):
        """Tests the configuration of the OperationsAgent."""
        agent = departmental_agents["Operations"]
        assert agent.name == "OperationsAgent"
        assert agent.persona

        tool_types = {type(tool) for tool in agent.tools.values()}
        expected_tools = {GitTool, FilesystemTool, SequentialThinkingTool}
        assert tool_types == expected_tools

    def test_marketing_agent_config(self, departmental_agents):
        """Tests the configuration of the MarketingAgent."""
        agent = departmental_agents["Marketing"]
        assert agent.name == "MarketingAgent"
        assert agent.persona

        tool_types = {type(tool) for tool in agent.tools.values()}
        expected_tools = {ResearchTool, DecisionTool}
        assert tool_types == expected_tools

    def test_sales_agent_config(self, departmental_agents):
        """Tests the configuration of the SalesAgent."""
        agent = departmental_agents["Sales"]
        assert agent.name == "SalesAgent"
        assert agent.persona

        tool_types = {type(tool) for tool in agent.tools.values()}
        expected_tools = {ResearchTool, MemoryTool, FilesystemTool, DecisionTool}
        assert tool_types == expected_tools
