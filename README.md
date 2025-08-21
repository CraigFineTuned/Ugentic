# 🌍 UGENTIC - Ubuntu-Driven Departmental Collective Intelligence

<div align="center">

![Python](https://img.shields.io/badge/python-v3.9.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active_Development-blue.svg)

**"I am because we are" - Departments that exist through each other**

</div>

---

## 📖 Overview

UGENTIC is an AI framework that transforms traditional hierarchical business structures into Ubuntu-driven departmental collective intelligence systems. Unlike conventional AI implementations, UGENTIC operationalizes African Ubuntu philosophy through authentic departmental agents that mirror real SME structures while embodying collaborative interdependence.

**Key Innovation:** Real departments (Finance, HR, Operations, Marketing, Sales) as specialized AI agents that reach consensus through natural dialogue, not voting or mathematical calculation.

---

## 🎯 Goals

*   To implement the philosophy of Ubuntu in a practical multi-agent AI system.
*   To create a powerful, flexible, and configurable framework for SME transformation.
*   To build a system that fosters collective intelligence and data-driven decision making.
*   To democratize access to advanced AI tools for small and medium-sized businesses.

---

## 🏗️ Architecture

*Note: The following is a high-level conceptual diagram. For detailed architecture, see `Project_Tracker/Architecture_Tracker/`.*

```
        🤝 Ubuntu Consensus 🤝
                ↑
    ┌──────────┼──────────┐
    ↓          ↓          ↓
[Finance] ←→ [HR] ←→ [Operations]
    ↑                      ↑
    └─── [Marketing] ←→ [Sales]
    
"Each department exists through others"
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9.11
- Ollama (for local LLM)
- 8GB+ RAM
- Windows/Linux/MacOS

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CraigFineTuned/Ugentic.git
    cd Ugentic
    ```

2.  **Configure the Models:**
    *   Before running, open `config.json` and ensure the `reasoning_model` and `embedding_model` point to the Ollama models you wish to use by default.

3.  **Download Your Ollama Models:**
    *   Make sure you have pulled the models specified in `config.json`.
    *   **Example:**
        ```bash
        ollama pull llama3
        ollama pull nomic-embed-text
        ```

4.  **Run the Application (Windows):**
    *   Simply execute the run script. It will handle creating the virtual environment (if needed), installing dependencies, and starting the application.
        ```bash
        run_ugentic.bat
        ```

---

## ⚙️ Configuration

The `config.json` file in the root directory controls the core model dependencies for the UGENTIC framework.

```json
{
  "reasoning_model": "llama3",
  "embedding_model": "nomic-embed-text"
}
```

*   `reasoning_model`: This is the primary LLM that the agents use for thinking, planning, and generating responses.
*   `embedding_model`: This model is used by the RAG system to vectorize documents and queries for semantic retrieval.

The application will automatically use the `reasoning_model` from this file. If the model is not found on your system, it will fall back to an interactive prompt where you can choose from any of your available Ollama models.

---

## 🤝 Contributing

This project is currently under active development. Feedback, ideas, and insights are welcome, especially from:
- Ubuntu philosophy experts
- Multi-agent system researchers
- South African SME owners
- AI ethics specialists

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.