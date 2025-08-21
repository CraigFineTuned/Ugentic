# Defines and initializes the specialized departmental agents for the UGENTIC framework.

from ..core.agent_framework import Agent, Tool
from ..core.filesystem_tool import FilesystemTool
from ..core.time_tool import TimeTool
from ..core.fetch_tool import FetchTool
from ..core.research_tool import ResearchTool
from ..core.decision_tool import DecisionTool
from ..core.rag_core import RAGCore
from ..core.sequential_thinking_tool import SequentialThinkingTool
from ..core.git_tool import GitTool # Added GitTool import
from ..core.memory_tool import MemoryTool # Added MemoryTool import
from ..core.analysis_tool import AnalysisTool # Added AnalysisTool import

# --- Mock Tools for unimplemented features ---

# --- Initialization Function ---

def initialize_departmental_agents(rag_system_instance: RAGCore, llm_model=None):
    """
    Instantiates all tools and specialized agents, returning a dictionary of agents.
    """
    # Instantiate all available tools
    filesystem_tool = FilesystemTool()
    time_tool = TimeTool()
    fetch_tool = FetchTool()
    research_tool = ResearchTool(fetch_tool=fetch_tool, rag_system=rag_system_instance, llm_model=llm_model)
    decision_tool = DecisionTool(llm_model=llm_model)
    git_tool = GitTool() # Now using real tool
    sequential_thinking_tool = SequentialThinkingTool(llm_model=llm_model) # Now using real tool
    memory_tool = MemoryTool() # Now using real tool
    analysis_tool = AnalysisTool() # Instantiate AnalysisTool

    # Define agents and their toolkits based on the architecture
    finance_agent = Agent(
        name="FinanceAgent",
        persona="The analytical and risk-aware CFO of the collective. Focused on financial viability, ROI, and cash flow. Utilizes AnalysisTool for financial data interpretation and FilesystemTool to access and manage financial documents (e.g., budgets, reports). IMPORTANT: When using FilesystemTool or AnalysisTool, always use absolute paths for files, especially those in 'documents/policies/'.",
        tools=[research_tool, decision_tool, filesystem_tool, analysis_tool], # Add analysis_tool
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    hr_agent = Agent(
        name="HRAgent",
        persona="The culture guardian and people-centric core of the collective. Focused on talent, culture, and compliance. Uses FilesystemTool for creating and managing HR documents (e.g., training materials, policies) and ResearchTool for gathering information on HR best practices. IMPORTANT: When using FilesystemTool, always use absolute paths for files, especially those in 'documents/policies/'.",
        tools=[filesystem_tool, research_tool, decision_tool, time_tool],
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    operations_agent = Agent(
        name="OperationsAgent",
        persona="The pragmatic and process-oriented COO of the collective. Focused on technical feasibility, resource management, and process optimization. Uses GitTool for version control, FilesystemTool for managing project files and documents (e.g., operational plans, marketing materials), and SequentialThinkingTool for complex task breakdown. IMPORTANT: When using FilesystemTool, always use absolute paths for files, especially those in 'documents/policies/'.",
        tools=[git_tool, filesystem_tool, sequential_thinking_tool],
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    marketing_agent = Agent(
        name="MarketingAgent",
        persona="The external-facing voice and market analyst of the collective. Focused on brand, customer insights, and competitive analysis. Utilizes ResearchTool to gather and analyze market trends, customer behavior, and competitor strategies. IMPORTANT: When using FilesystemTool, always use absolute paths for files, especially those in 'documents/policies/'.",
        tools=[research_tool, decision_tool],
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    sales_agent = Agent(
        name="SalesAgent",
        persona="The growth-driver and customer-focused revenue engine of the collective. Focused on revenue generation and pipeline management. Leverages ResearchTool for market intelligence and lead generation, MemoryTool for managing customer interactions and preferences, and FilesystemTool for sales documentation. IMPORTANT: When using FilesystemTool, always use absolute paths for files, especially those in 'documents/policies/'.",
        tools=[research_tool, memory_tool, filesystem_tool, decision_tool],
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    return {
        "Finance": finance_agent,
        "HR": hr_agent,
        "Operations": operations_agent,
        "Marketing": marketing_agent,
        "Sales": sales_agent,
    }