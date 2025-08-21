# Main application entry point for the UGENTIC framework.

import os
import json
from unittest.mock import MagicMock

from src.ugentic.core.rag_core import RAGCore, get_text_splitter, get_ollama_embeddings
from src.ugentic.core.agent_framework import Orchestrator
from src.ugentic.agents.departmental_agents import initialize_departmental_agents

from langchain_ollama.llms import OllamaLLM as Ollama # Import Ollama for live LLM interaction

def run_demo():
    """Runs a demonstration of the UGENTIC framework."""
    print("--- Initializing UGENTIC Framework Demonstration ---")

    # --- Live LLM Setup ---
    available_models = get_available_models()
    if not available_models:
        print("No Ollama models found. Please ensure Ollama is running and models are pulled.")
        print("Exiting.")
        return

    selected_model_name = get_configured_model()

    if selected_model_name and selected_model_name in available_models:
        print(f"Using configured model from config.json: {selected_model_name}")
    else:
        if selected_model_name:
            print(f"Warning: Configured model '{selected_model_name}' not found.")
        selected_model_name = select_model_interactively(available_models)

    if selected_model_name is None:
        print("Exiting due to no LLM model selection.")
        return

    llm_model = Ollama(model=selected_model_name) # Use a live LLM model

    # --- RAG System Setup ---
    # Initialize live Ollama embeddings for RAG
    ollama_embeddings = get_ollama_embeddings()
    rag_system_instance = RAGCore(ollama_embeddings, get_text_splitter())

    # Load policy documents from the dedicated directory
    policy_documents_path = os.path.join(os.path.dirname(__file__), 'documents', 'policies')
    rag_system_instance.load_documents_from_directory(policy_documents_path, file_extensions=['.md', '.txt', '.csv'])


    # Pass the live LLM model to initialize_departmental_agents
    departmental_agents = initialize_departmental_agents(rag_system_instance, llm_model)

    # Pass the live LLM model to the Orchestrator
    orchestrator = Orchestrator("MainOrchestrator", "The Project Manager", departmental_agents, rag_system_instance, llm_model=llm_model)

    # --- Test Execution ---
    while True:
        user_input = input("\nEnter a high-level goal for the Orchestrator (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        if user_input:
            orchestrator.orchestrate(user_input)

    print("\n--- UGENTIC Framework Demonstration Complete ---")

def get_available_models():
    """Gets a list of available models from the Ollama server."""
    ollama_models_output = os.popen("ollama list").read()
    models = []
    for line in ollama_models_output.splitlines():
        if "NAME" in line or not line.strip():
            continue
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models

def get_configured_model():
    """Reads the reasoning model from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get("reasoning_model")
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def select_model_interactively(available_models):
    """Prompts the user to select a model from a list."""
    print("\n--- Please Select an Available Ollama Model ---")
    for i, model_name in enumerate(available_models):
        print(f"{i+1}. {model_name}")

    while True:
        try:
            choice = input("Enter the number of the LLM model you want to use: ")
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(available_models):
                return available_models[choice_index]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    run_demo()
