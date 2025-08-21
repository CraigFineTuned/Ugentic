
import pytest
from unittest.mock import Mock, MagicMock

from src.ugentic.core.agent_framework import Agent, Orchestrator
from src.ugentic.agents.departmental_agents import initialize_departmental_agents

@pytest.fixture
def mock_llm():
    """Provides a mock LLM for controlling agent decisions."""
    return Mock()

@pytest.fixture
def mock_rag_system():
    """Provides a mock RAG system."""
    return Mock()

@pytest.fixture
def full_agent_suite(mock_llm, mock_rag_system):
    """
    Initializes a full suite of departmental agents and ensures they are 
    registered with each other for consultation via an Orchestrator.
    """
    dept_agents = initialize_departmental_agents(
        rag_system_instance=mock_rag_system, 
        llm_model=mock_llm
    )
    
    # The Orchestrator's __init__ handles the peer registration
    Orchestrator(
        name="TestOrchestrator",
        persona="Test Orchestrator",
        departmental_agents=dept_agents,
        llm_model=mock_llm
    )
    
    # Return the dictionary of agents, which are now registered
    return dept_agents

class TestConsultationFlow:

    def test_finance_consults_marketing_for_budget(self, full_agent_suite, mock_llm):
        """ 
        Integration Test: Verifies that the Finance agent can consult the
        Marketing agent to get information needed for a task.
        """
        finance_agent = full_agent_suite["Finance"]
        # Get the marketing agent directly from the finance agent's directory
        marketing_agent_peer = finance_agent.agent_directory["Marketing"]

        # 1. Setup the scenario
        task_for_finance = "Create a budget for the new marketing campaign."
        question_for_marketing = "What is the projected cost of the new marketing campaign?"
        
        # 2. Mock the Finance agent's LLM to decide to consult Marketing
        llm_consult_decision = f'''{{
            "tool": "consult",
            "parameters": {{
                "target_agent_name": "Marketing",
                "question": "{question_for_marketing}"
            }}
        }}'''
        mock_llm.invoke.return_value = llm_consult_decision

        # 3. Replace the marketing agent's method with a simple mock to spy on it
        marketing_agent_peer.execute_task = MagicMock(return_value="Marketing response")

        # 4. Execute the initial task for the Finance agent
        finance_agent.execute_task(task_for_finance)

        # 5. Assertions
        # Check that the marketing agent was consulted with the correct question
        marketing_agent_peer.execute_task.assert_called_once_with(question_for_marketing)

