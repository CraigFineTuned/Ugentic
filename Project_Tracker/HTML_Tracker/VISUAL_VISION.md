# UGENTIC - The Visual Vision

**Date:** August 15, 2025  
**Status:** Live Visualization (v2)

---

## 1. Purpose

This document serves as the narrative guide for the interactive visualization of the UGENTIC project's architecture, located in the `HTML_Tracker` directory. It explains the components and, critically, the flow of information and intelligence between them.

## 2. The Core Architecture: A Hybrid Model

The visualization represents our evolved hybrid architecture:

1.  **The LLM Core:** At the foundation of the entire system is the selected Large Language Model (e.g., from your Ollama server at `http://127.0.0.1:11434/`). This is not an agent itself, but the **cognitive engine** that powers every agent. Each agent is essentially a specialized persona and logic layer built on top of this core intelligence.

2.  **The Ubuntu Layer (Dialogue & Consensus):** Embodied by the five core **Departmental Agents**. This layer handles high-level strategy, perspective sharing, and achieving consensus, true to the Ubuntu philosophy.

3.  **The MCP Layer (Tool-Based Execution):** Embodied by the **MCP Toolset**. This layer provides the practical, real-world capabilities for the agents to perform work.

4.  **The Orchestrator:** The central agent that manages the primary workflow, bridging the dialogue and execution layers.

## 3. The Flow of Intelligence

The system operates on two distinct communication patterns, which are now represented in the visual diagram:

*   **Orchestration Flow (Solid Lines):** This is the primary, sequential workflow. The `Orchestrator` receives a goal, breaks it down, and delegates tasks to the departmental agents and their tools in a logical sequence. This ensures that work proceeds in an orderly fashion.

*   **Consultation Flow (Dotted Lines):** This represents the "Ubuntu" principle in action. At any point in the orchestrated workflow, agents can engage in **peer-to-peer dialogue** to resolve ambiguities or conflicts. For example, the `Finance` agent can directly consult the `Marketing` agent for clarification on a budget item *before* making a decision. This creates a collaborative, resilient system rather than a rigid, top-down one.

## 4. How to Use the Visualization

To explore the architecture in action, open the following file in your web browser:

**[./HTML_Tracker/index.html](./HTML_Tracker/index.html)**

### **Interactivity:**
*   **Click on any Agent or Tool:** A panel will appear, displaying its updated description, including its role in the communication flows.
*   **Visual Cues:** Note the new **LLM Core** at the bottom, with lines connecting to all agents, and the new **dotted lines** between departments, representing the consultation flow.

This visualization is for testing and alignment purposes and does not affect the core project code. It is our dynamic blueprint.