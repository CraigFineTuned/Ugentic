

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, create_autospec

from src.ugentic.core.agent_framework import Tool, Agent, Orchestrator

# --- Fixtures ---

@pytest.fixture
def mock_llm():
    llm = Mock()
    llm.invoke = MagicMock(return_value='{"tool": "none", "response": "Default mock response."}')
    return llm

@pytest.fixture
def mock_rag_system():
    rag = Mock()
    rag.retrieve = MagicMock(return_value=[{"chunk_text": "Relevant context from RAG."}])
    return rag

@pytest.fixture
def mock_tool():
    class MockToolImpl(Tool):
        def __init__(self):
            super().__init__("TestTool", "A tool for testing.")
        def test_action(self, query: str):
            """Performs a test action. Parameters: query: str"""
            return "Real action executed."
    tool_instance = MockToolImpl()
    tool_instance.test_action = create_autospec(tool_instance.test_action, return_value="Action executed successfully.")
    return tool_instance

@pytest.fixture
def basic_agent(mock_llm, mock_rag_system, mock_tool):
    return Agent(
        name="TestAgent",
        persona="A testing persona",
        tools=[mock_tool],
        rag_system=mock_rag_system,
        llm_model=mock_llm
    )

@pytest.fixture
def consultable_orchestrator(mock_llm, mock_rag_system):
    """Orchestrator with real, consultable agents."""
    finance_agent = Agent(name="Finance", persona="Finance Persona", llm_model=mock_llm)
    hr_agent = Agent(name="HR", persona="HR Persona", llm_model=mock_llm)
    
    dept_agents = {
        "Finance": finance_agent,
        "HR": hr_agent
    }
    
    orchestrator = Orchestrator(
        name="MainOrchestrator",
        persona="The main orchestrator",
        departmental_agents=dept_agents,
        llm_model=mock_llm
    )
    return orchestrator

# --- Test Cases ---

class TestCoreComponents:
    def test_tool_init(self):
        tool = Tool("MyTool", "My description")
        assert tool.name == "MyTool"

    def test_agent_init(self, mock_tool):
        agent = Agent("InitAgent", "Init Persona", tools=[mock_tool])
        assert agent.name == "InitAgent"
        assert "TestTool" in agent.tools

class TestAgentExecution:
    def test_execute_task_tool_selection(self, basic_agent, mock_llm, mock_tool):
        llm_response = '{"tool": "TestTool", "action": "test_action", "parameters": {"query": "Execute the test"}}'
        mock_llm.invoke.return_value = llm_response
        basic_agent.execute_task("A task for the tool")
        mock_tool.test_action.assert_called_once_with(query="Execute the test")

    def test_execute_task_no_tool_found(self, basic_agent, mock_llm):
        llm_response = '{"tool": "none", "response": "I will handle this myself."}'
        mock_llm.invoke.return_value = llm_response
        result = basic_agent.execute_task("A task for the tool")
        assert result == "I will handle this myself."

class TestOrchestrator:
    def test_orchestrator_init_and_peer_registration(self, mock_llm):
        """Tests Orchestrator initializes and registers peers correctly."""
        mock_finance_agent = Mock(spec=Agent)
        mock_hr_agent = Mock(spec=Agent)
        dept_agents = {"Finance": mock_finance_agent, "HR": mock_hr_agent}
        
        orchestrator = Orchestrator("Orchestrator", "Persona", dept_agents, llm_model=mock_llm)
        
        assert orchestrator.name == "Orchestrator"
        # Check that register_peers was called on each agent
        mock_finance_agent.register_peers.assert_called_once_with(dept_agents)
        mock_hr_agent.register_peers.assert_called_once_with(dept_agents)

    def test_orchestrate_delegation(self, consultable_orchestrator):
        orchestrator = consultable_orchestrator
        decomposed_tasks = [{"agent": "Finance", "task": "Task 1"}]
        orchestrator.decompose_goal = MagicMock(return_value=decomposed_tasks)
        
        finance_agent = orchestrator.departmental_agents["Finance"]
        finance_agent.execute_task = MagicMock(return_value="Finance task done")
        
        orchestrator.orchestrate("A high level goal")
        finance_agent.execute_task.assert_called_once_with("Task 1")

class TestConsultation:
    def test_build_prompt_with_consult(self, consultable_orchestrator):
        """Tests that the consult ability is added to the prompt."""
        finance_agent = consultable_orchestrator.departmental_agents["Finance"]
        prompt = finance_agent._build_tool_prompt()
        assert "- consult: Ask a peer agent a question" in prompt
        assert "'HR'" in prompt # Check that HR is listed as a peer
        assert "'Finance'" not in prompt # Should not list itself

    def test_consult_success(self, consultable_orchestrator):
        """Tests a successful consultation between two agents."""
        finance_agent = consultable_orchestrator.departmental_agents["Finance"]
        hr_agent = consultable_orchestrator.departmental_agents["HR"]
        
        # Mock the HR agent's response
        hr_agent.execute_task = MagicMock(return_value="The salary data is X.")
        
        result = finance_agent.consult("HR", "What is the salary data for a new hire?")
        
        hr_agent.execute_task.assert_called_once_with("What is the salary data for a new hire?")
        assert result == "The salary data is X."

    def test_consult_agent_not_found(self, consultable_orchestrator):
        finance_agent = consultable_orchestrator.departmental_agents["Finance"]
        result = finance_agent.consult("Marketing", "A question")
        assert "Error: Agent 'Marketing' not found" in result

    def test_consult_self(self, consultable_orchestrator):
        finance_agent = consultable_orchestrator.departmental_agents["Finance"]
        result = finance_agent.consult("Finance", "A question")
        assert "Error: An agent cannot consult itself" in result

    def test_execute_task_chooses_consult(self, consultable_orchestrator, mock_llm):
        """Tests that the agent correctly executes a consult action decided by the LLM."""
        finance_agent = consultable_orchestrator.departmental_agents["Finance"]
        hr_agent = consultable_orchestrator.departmental_agents["HR"]
        
        # Mock the LLM to return a 'consult' decision
        llm_response = '{"tool": "consult", "parameters": {"target_agent_name": "HR", "question": "What is our hiring policy?"}}'
        mock_llm.invoke.return_value = llm_response
        
        # Mock the peer's response
        hr_agent.execute_task = MagicMock(return_value="Our policy is XYZ.")
        
        # Execute the task
        result = finance_agent.execute_task("I need to know the hiring policy.")
        
        # Assert that the consultation happened correctly
        hr_agent.execute_task.assert_called_once_with("What is our hiring policy?")
        assert result == "Our policy is XYZ."


