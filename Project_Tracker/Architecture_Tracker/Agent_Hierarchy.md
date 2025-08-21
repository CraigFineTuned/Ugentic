# 🏢 AGENT HIERARCHY - UGENTIC DEPARTMENTAL STRUCTURE (v2)

**Version:** 2.0 (Revolutionary Integration Update)
**Principle:** A circular, tool-augmented collective, managed by an Orchestrator.

---

## 1. Architectural Overview

The UGENTIC hierarchy is not a top-down pyramid but a **tool-augmented circular collective**. A central **Orchestrator Agent** manages the primary workflow, but the five **Departmental Agents** have the autonomy to use their tools and consult with each other to achieve collective goals.

Each agent is a composite entity: **Persona + Toolkit**. The agent's intelligence lies in its ability to dynamically choose the right tool for a given task. This is not a hard-coded process; instead, the agent's core LLM reasons over the task description and the descriptions of its available tools to make an intelligent, in-the-moment decision on which tool to use and how to use it.

---

## 2. The MCP Toolkit (Legend)

This is the master list of practical capabilities available to the agents.

| Tool                 | Core Function                                      |
|----------------------|----------------------------------------------------|
| **Fetch**            | Retrieves raw data from **valid web URLs** (http/https).        |
| **Research**         | Synthesizes information from multiple sources, including **internal documents (via RAG)** and **external web content (via Fetch)**, into coherent analysis.    |
| **Filesystem**       | Reads from and writes to the local file system, **strictly adhering to provided or discovered absolute paths**.    |
| **Git**              | Interacts with Git repositories to analyze code.   |
| **Decision**         | Provides structured go/no-go or ranked-choice judgments. |
| **SequentialThinking** | Manages complex, multi-step workflows.             |
| **Memory**           | Provides a persistent key-value store for agents.  |
| **Time**             | Provides the current date and time.                |

---

## 3. The Core Agents

### **A. Orchestrator Agent**
*   **Persona:** The central nervous system and project manager.
*   **Core Function:** Interprets high-level goals, manages the primary sequential workflow, and synthesizes final outputs from the departmental agents.
*   **Toolkit:** Primarily uses `SequentialThinking` to manage workflows.

### **B. Departmental Agents**

#### **1. Finance Department Agent**
*   **Persona:** The analytical and risk-aware CFO of the collective.
*   **Expertise:** Financial viability, ROI, cash flow, and risk assessment.
*   **Concerns:** "Is this profitable?", "What is the ROI?", "Can we afford this?"
*   **Toolkit (MCP Capabilities):**
    *   `Fetch`: To get real-time market data and economic indicators.
    *   `Research`: To analyze financial reports and market trends.
    *   `Decision`: To support investment analysis and budget approvals.

#### **2. Human Resources Department Agent**
*   **Persona:** The culture guardian and people-centric core of the collective.
*   **Expertise:** Talent, culture, organizational development, and compliance.
*   **Concerns:** "How does this affect our people?", "Do we have the right skills?"
*   **Toolkit (MCP Capabilities):**
    *   `Filesystem`: To read and manage anonymized employee data, policies, and contracts.
    *   `Research`: To find information on labor laws and industry best practices.
    *   `Decision`: To assist in evaluating candidate profiles against job requirements.

#### **3. Operations Department Agent**
*   **Persona:** The pragmatic and process-oriented COO of the collective.
*   **Expertise:** Process execution, technical feasibility, and resource management.
*   **Concerns:** "Do we have the capacity?", "Is this technically feasible?", "What resources are needed?"
*   **Toolkit (MCP Capabilities):**
    *   `Git`: To analyze codebases for technical assessments.
    *   `Filesystem`: To manage project files, deployment scripts, and infrastructure documents.
    *   `SequentialThinking`: To plan and execute complex implementation processes.

#### **4. Marketing Department Agent**
*   **Persona:** The external-facing voice and market analyst of the collective.
*   **Expertise:** Brand, customer insights, and competitive analysis.
*   **Concerns:** "How does this affect our brand?", "What is the market demand?"
*   **Toolkit (MCP Capabilities):**
    *   `Fetch`: To scrape competitor websites and gather marketing data.
    *   `Research`: To conduct market analysis and synthesize customer feedback.
    *   `Decision`: To help evaluate the potential success of different campaign strategies.

#### **5. Sales Department Agent**
*   **Persona:** The growth-driver and customer-focused revenue engine of the collective.
*   **Expertise:** Revenue generation, customer relationships, and pipeline management.
*   **Concerns:** "Will this help us sell?", "What is the revenue impact?"
*   **Toolkit (MCP Capabilities):**
    *   `Fetch`: To enrich lead data from public sources (e.g., LinkedIn).
    *   `Research`: To understand a potential client's business and needs.
    *   `Memory`: To maintain a "scratchpad" of notes and key facts about leads.
    *   `Filesystem`: To manage sales collateral, proposals, and contracts.