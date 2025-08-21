# Main framework for UGENTIC agents

from .filesystem_tool import FilesystemTool
from .time_tool import TimeTool
from .rag_core import RAGCore, get_ollama_embeddings, get_text_splitter
from .fetch_tool import FetchTool
from .research_tool import ResearchTool
from .decision_tool import DecisionTool

import os
import json
import inspect

from langchain_community.llms import Ollama  # Import Ollama for live LLM interaction


class Tool:
    """Base class for all MCP tools."""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Tool must implement __call__ method.")


class Agent:
    def __init__(self, name, persona, tools=None, rag_system=None, llm_model=None):
        self.name = name
        self.persona = persona
        self.tools = {tool.name: tool for tool in tools} if tools is not None else {}
        self.rag_system = rag_system
        self.llm_model = llm_model  # Store the LLM model
        self.agent_directory = None # To be populated by the Orchestrator
        print(f"Agent '{self.name}' initialized.")

    def register_peers(self, agent_directory):
        """Registers the directory of all agents for consultation."""
        self.agent_directory = agent_directory

    def consult(self, target_agent_name: str, question: str):
        """Consults a peer agent with a specific question."""
        if not self.agent_directory:
            return "Error: Agent directory not registered. Cannot consult peers."
        
        # Prevent an agent from consulting itself
        if target_agent_name == self.name:
            return "Error: An agent cannot consult itself."

        peer_agent = self.agent_directory.get(target_agent_name)
        if not peer_agent:
            return f"Error: Agent '{target_agent_name}' not found in directory."

        print(f"  [{self.name}]: Consulting with {target_agent_name} about: '{question}'")
        # The result of a consultation is the direct result of the peer's task execution
        return peer_agent.execute_task(question)

    def _build_tool_prompt(self):
        """Builds the part of the prompt listing available tools and actions."""
        prompt = "You have the following tools and abilities available:\n"
        
        # Add standard tools
        for tool_name, tool_obj in self.tools.items():
            prompt += f"- {tool_name}: {tool_obj.description}\n"
            # Filter to include only public, callable methods (actions)
            actions = [method for method in dir(tool_obj) if callable(getattr(tool_obj, method)) and not method.startswith("_")]
            for action_name in actions:
                # Ensure the method is not an internal attribute like llm_model
                if action_name != "llm_model": # Explicitly exclude llm_model
                    prompt += f"  - Action: {action_name} (Description: {getattr(tool_obj, action_name).__doc__})\n"

        # Add special, built-in abilities
        if self.agent_directory:
            peer_names = [name for name in self.agent_directory.keys() if name != self.name]
            prompt += f"- consult: Ask a peer agent a question to get their expert opinion or data. Use this when you need information from another department. Parameters: target_agent_name: str (must be one of {peer_names}), question: str\n"

        # Add available policy documents for RAG
        policy_documents = ["budget.csv", "HR_Policy_2025.md", "market_research.md"]
        if policy_documents:
            prompt += f"\nAvailable Policy Documents (for use with RAG-enabled tools like ResearchTool): {', '.join(policy_documents)}\n"

        # Guidance for FilesystemTool and AnalysisTool
        prompt += "\nIMPORTANT: When using Filesystem Tool or AnalysisTool, only use file paths that are explicitly provided to you, or that you have discovered using list_directory. Do NOT invent file paths. For example, if you need to analyze 'budget.csv', use 'budget.csv' directly if it's listed as available, or first use list_directory to find it. If you need to analyze a CSV, ensure it's a real file you have access to.\n"
        prompt += fr"\nKnown absolute paths to policy documents: \n- C:\Users\craig\Desktop\MainProjects\DISSERTATION_FINAL\documents\policies\budget.csv\n- C:\Users\craig\Desktop\MainProjects\DISSERTATION_FINAL\documents\policies\HR_Policy_2025.md\n- C:\Users\craig\Desktop\MainProjects\DISSERTATION_FINAL\documents\policies\market_research.md\n"

        return prompt

    def _interact_with_llm(self, prompt_text):
        """Interacts with the live LLM to get a response."""
        if self.llm_model is None:
            return '{"tool": "none", "response": "No LLM configured."}'

        print(f"  [{self.name} LLM]: Processing prompt: '{prompt_text[:100]}...' ")

        example_format = {"tool": "tool_name", "action": "action_name", "parameters": {"key": "value"}}
        example_no_tool = {"tool": "none", "response": "Your natural language response here."}

        llm_prompt = f"""YOUR RESPONSE MUST BE ONLY A JSON OBJECT. DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION.\n\nYou are a helpful AI assistant. Your task is to select the best tool and action from the available tools that *most appropriately* fulfills the request: '{prompt_text}'.\n\n{self._build_tool_prompt()}\n\nRespond with ONLY a JSON object in the format: \n{json.dumps(example_format)} \n\nIf no tool is appropriate, respond with: {json.dumps(example_no_tool)}\n"""

        try:
            response = self.llm_model.invoke(llm_prompt)
            # Robust JSON parsing logic...
            cleaned_str = response.strip().removeprefix("```json").removesuffix("```").strip()
            json_start = cleaned_str.find("{")
            json_end = cleaned_str.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = cleaned_str[json_start:json_end]
                json.loads(json_str) # Validate
                return json_str
            return '' # Return empty for malformed or no JSON
        except Exception as e:
            print(f"  [{self.name} LLM]: Error invoking LLM: {e}")
            return '{"tool": "none", "response": "Error communicating with LLM."}'

    def retrieve_info_from_rag(self, query, top_k=3):
        """Retrieves information from the RAG system based on a query."""
        if self.rag_system:
            retrieved_chunks = self.rag_system.retrieve(query, top_k=top_k)
            if retrieved_chunks:
                return "\n".join([chunk["chunk_text"] for chunk in retrieved_chunks])
            return "No relevant information found."
        return "RAG system not initialized."

    def execute_task(self, task_description):
        """Executes a given task by reasoning over available tools with an LLM."""
        print(f"\n  [{self.name}]: Executing task: '{task_description}'")
        llm_response_str = self._interact_with_llm(task_description)
        
        print(f"DEBUG: LLM Response String: {llm_response_str}") # DEBUG
        try:
            decision = json.loads(llm_response_str)
            print(f"DEBUG: Parsed Decision: {decision}") # DEBUG
        except json.JSONDecodeError:
            decision = {"tool": "none", "response": f"I was unable to process the request due to an internal error (invalid JSON: {llm_response_str})"}
            print(f"DEBUG: JSON Decode Error. Decision: {decision}") # DEBUG

        tool_name = decision.get("tool")
        print(f"DEBUG: Tool Name: {tool_name}") # DEBUG
        parameters = decision.get("parameters", {})

        if tool_name == "consult":
            print("DEBUG: Entering CONSULT branch") # DEBUG
            target_agent = parameters.get("target_agent_name")
            question = parameters.get("question")
            if target_agent and question:
                return self.consult(target_agent, question)
            else:
                return "Error: 'consult' action requires 'target_agent_name' and 'question'."
        
        elif tool_name in self.tools:
            print("DEBUG: Entering TOOL branch with validation") # DEBUG
            tool_to_use = self.tools[tool_name]
            action_name = decision.get("action")

            if action_name is None:
                return f"Error: Tool '{tool_name}' selected, but no action was specified."

            if not hasattr(tool_to_use, action_name) or not callable(getattr(tool_to_use, action_name)):
                available_actions = [method for method in dir(tool_to_use) if callable(getattr(tool_to_use, method)) and not method.startswith("_")]
                return f"Error: Action '{action_name}' not found or not callable on tool '{tool_name}'. Available actions: {', '.join(available_actions)}"

            action = getattr(tool_to_use, action_name)
            expected_params = inspect.signature(action).parameters
            filtered_parameters = {}
            missing_params = []

            for param_name, param_obj in expected_params.items():
                if param_obj.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and param_obj.default == inspect.Parameter.empty:
                    # This is a required parameter
                    if param_name not in parameters:
                        missing_params.append(param_name)
                    else:
                        filtered_parameters[param_name] = parameters[param_name]
                elif param_name in parameters:
                    # This is an optional parameter provided by the LLM
                    filtered_parameters[param_name] = parameters[param_name]

            if missing_params:
                return f"Error: Action '{action_name}' on tool '{tool_name}' is missing required parameters: {', '.join(missing_params)}. Please provide them."
            
            return action(**filtered_parameters)
        
        else: # No tool found or tool is 'none'
            print("DEBUG: Entering NO TOOL branch") # DEBUG
            return decision.get("response", "No action taken.")


class Orchestrator(Agent):
    def __init__(self, name, persona, departmental_agents, rag_system=None, tools=None, llm_model=None):
        super().__init__(name, persona, tools=tools, rag_system=rag_system, llm_model=llm_model)
        self.departmental_agents = departmental_agents
        # After all agents are created, register them with each other
        for agent in self.departmental_agents.values():
            agent.register_peers(self.departmental_agents)
        print("Orchestrator initialized and all agents registered for consultation.")

    def decompose_goal(self, high_level_goal):
        print(f"  [Orchestrator]: Decomposing goal: '{high_level_goal}'")

        # Define the JSON schema for the expected output
        json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent": {
                        "type": "string",
                        "description": "Name of the departmental agent (e.g., Marketing, Finance, HR)",
                    },
                    "task": {
                        "type": "string",
                        "description": "Specific task for the agent to perform",
                    },
                },
                "required": ["agent", "task"],
            },
        }

        # Create the example JSON string outside the f-string to avoid syntax errors
        example_data = [
            {"agent": "Marketing", "task": "Research market trends"},
            {"agent": "Finance", "task": "Analyze budget"},
        ]
        example_json = json.dumps(example_data, indent=2)

        # Construct the prompt for the LLM to decompose the goal
        llm_prompt = (
            f"""YOUR RESPONSE MUST BE ONLY A JSON ARRAY. DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION. NO PREAMBLE, NO EXPLANATION, JUST THE JSON.\n"
            "            ""You are an expert orchestrator. Your task is to decompose the following high-level goal\n"
            "into a list of smaller, highly specific, and actionable tasks. Each task must be assigned to\n"
            "ONE relevant departmental agent from the following EXACT list: {', '.join(self.departmental_agents.keys())}.\n\n"
            "High-level goal: '{high_level_goal}'\n\n"
            "YOUR RESPONSE MUST BE ONLY A JSON ARRAY, WRAPPED IN A 'json' MARKDOWN BLOCK (e.g., ```json...```). DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION.\nThe JSON array must conform to the following JSON schema:\n'''{json.dumps(json_schema, indent=2)}'''\n\nExample: ```json\n{example_json}\n```\n\nIMPORTANT: You MUST use agent names ONLY from the provided list. If you are unsure, or if a task seems to fit multiple agents, choose the most appropriate one. Do NOT invent new agent names or misspell existing ones. For example, use 'Operations' not 'Opereations'."""
        )

        try:
            # FIX: Call the LLM directly, bypassing the flawed Agent._interact_with_llm
            print(
                f"  [MainOrchestrator LLM]: Processing prompt: '{llm_prompt[:100]}...'"
            )
            llm_response_str = self.llm_model.invoke(llm_prompt)
            print(
                f"  [Orchestrator Debug]: Raw LLM response for decomposition: '{llm_response_str}'"
            )

            # --- Robust JSON Parsing ---
            # Clean the string: remove markdown, leading/trailing whitespace
            cleaned_str = llm_response_str.strip()
            if cleaned_str.startswith("```json"):
                cleaned_str = cleaned_str[7:]
            if cleaned_str.endswith("```"):
                cleaned_str = cleaned_str[:-3]

            # Find the start and end of the JSON content
            json_start = cleaned_str.find("[")
            if json_start == -1:
                json_start = cleaned_str.find("{")

            json_end = cleaned_str.rfind("]")
            if json_end == -1:
                json_end = cleaned_str.rfind("}")

            if json_start == -1 or json_end == -1:
                raise json.JSONDecodeError(
                    "No JSON object or array found in response.", cleaned_str, 0
                )

            json_str = cleaned_str[json_start : json_end + 1]

            # If the response is a single JSON object or multiple objects, wrap it in a list
            if not json_str.startswith("["):
                json_str = f"[{json_str}]"

            decomposed_tasks = json.loads(json_str)

            # If the result is a single dictionary that was parsed into a list, ensure it's correct
            if isinstance(decomposed_tasks, dict):
                decomposed_tasks = [decomposed_tasks]

            # Define common agent name misspellings and their corrections
            agent_name_corrections = {
                "Opereations": "Operations",
                "Operation": "Operations",
                "Finace": "Finance",
                "Markting": "Marketing",
                "Sale": "Sales",
                "Human Resources": "HR" # Example for multi-word agent names
            }

            # Apply corrections to agent names
            for task_item in decomposed_tasks:
                if "agent" in task_item and task_item["agent"] in agent_name_corrections:
                    task_item["agent"] = agent_name_corrections[task_item["agent"]]

            # Basic validation of the decomposed tasks against the schema (can be more robust)
            if not isinstance(decomposed_tasks, list):
                raise ValueError("LLM response is not a list.")

            for task_item in decomposed_tasks:
                if (
                    not isinstance(task_item, dict)
                    or "agent" not in task_item
                    or "task" not in task_item
                ):
                    raise ValueError(
                        "Each task item must be an object with 'agent' and 'task'."
                    )
                if task_item["agent"] not in self.departmental_agents:
                    print(
                        f"  [Orchestrator Warning]: LLM proposed unknown agent: {task_item['agent']}. Skipping this task."
                    )
                    # Optionally, you could re-prompt the LLM or assign to a default agent
                    continue  # Skip this invalid task

            return [
                task
                for task in decomposed_tasks
                if task["agent"] in self.departmental_agents
            ]  # Filter out invalid agents
        except json.JSONDecodeError as e:
            print(f"  [Orchestrator Error]: Failed to parse LLM response as JSON: {e}")
            print(f"  [Orchestrator Error]: LLM response was: {llm_response_str}")
            return [
                {
                    "agent": "HR",
                    "task": f"Error decomposing goal: {high_level_goal}. The system's planning module failed to generate a valid JSON plan.",
                }
            ]
        except ValueError as e:
            print(f"  [Orchestrator Error]: LLM response validation failed: {e}")
            print(f"  [Orchestrator Error]: LLM response was: {llm_response_str}")
            return [
                {
                    "agent": "HR",
                    "task": f"Error decomposing goal: {high_level_goal}. The system's planning module response was invalid.",
                }
            ]
        except Exception as e:
            print(
                f"  [Orchestrator Error]: An unexpected error occurred during goal decomposition: {e}"
            )
            return [
                {
                    "agent": "HR",
                    "task": f"Unexpected error decomposing goal: {high_level_goal}.",
                }
            ]

    def orchestrate(self, high_level_goal):
        print(f"\n>>> Orchestrator received high-level goal: '{high_level_goal}' <<<")
        workflow_steps = self.decompose_goal(high_level_goal)
        for step in workflow_steps:
            agent_name = step.get("agent")
            task = step.get("task")
            if agent_name in self.departmental_agents:
                agent = self.departmental_agents[agent_name]
                print(f"[Orchestrator]: Delegating task '{task}' to {agent_name}.")
                result = agent.execute_task(task)
                print(f"  [{agent_name} Response]: {result}")
            else:
                print(f"[Orchestrator]: Warning: Agent '{agent_name}' not found.")
        print(f"[Orchestrator]: Goal '{high_level_goal}' orchestration complete.")