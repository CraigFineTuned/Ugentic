# UGENTIC Project: Seamless Continuation Guide

This document serves as the central, immutable guide for seamlessly continuing work on the UGENTIC project. It provides a high-level overview of the project's current state and directs to relevant files for detailed context.

## 1. Project Overview & Vision
*   **Project Vision:** Refer to `NEVER_CHANGING_VISION.md` for the enduring vision of the UGENTIC framework.
*   **Current State:** The UGENTIC application is operational. Key components include:
    *   Orchestrator for goal decomposition and agent delegation.
    *   Departmental Agents (Finance, HR, Operations, Marketing, Sales).
    *   RAG system for document retrieval.
    *   Integration with Ollama LLMs.

## 2. How to Resume Work
To resume work on this project:
1.  **Activate Virtual Environment:** Navigate to the project root (`C:\Users\craig\Desktop\MainProjects\Ugentic`) and activate the Python virtual environment:
    ```bash
    & ./.venv/Scripts/Activate.ps1  # For PowerShell
    # or
    # ./.venv/Scripts/activate      # For Git Bash/WSL
    ```
2.  **Start Application:** Run the main application:
    ```bash
    python app.py
    ```
    (You may need to select an Ollama model if the configured one is not found.)
3.  **Provide Goal:** Enter a high-level goal for the Orchestrator. A comprehensive test prompt is available in `test_orchestrator_prompt.txt`.

## 3. Key Project Files & Directories
*   **Application Entry Point:** `app.py`
*   **Source Code:** `src/` directory contains core logic, agents, and tools.
*   **RAG Documents:** `documents/policies/` contains internal policy documents and data for the RAG system.
*   **Logging:** The `logs/` directory is designated for application logs (implementation pending).
*   **Test Prompt:** `test_orchestrator_prompt.txt` contains a single-line prompt for comprehensive system testing.

## 4. Project Tracking & Planning
For detailed project information, plans, and progress:
*   **Architecture:** Refer to `Architecture_Tracker/` for system architecture details.
*   **Implementation Details:** Refer to `Implementation_Tracker/` for specific implementation notes.
*   **Progress & Checkpoints:** Refer to `Progress_Tracker/` and `Project_Checklist-Checkpoint_Tracker/`.
*   **Project Planning:** Refer to `Project_Planning_Tracker/` for detailed plans, including `Project_Planning_Tracker/Logging_Strategy_Plan.md` for the logging feature.
*   **Research:** Refer to `Research_Tracker/` for research notes.

## 5. Version Control
This project is managed with Git. All changes are committed and pushed to the remote GitHub repository: `https://github.com/CraigFineTuned/Ugentic`.

---
*Last Updated: Thursday, 21 August 2025*