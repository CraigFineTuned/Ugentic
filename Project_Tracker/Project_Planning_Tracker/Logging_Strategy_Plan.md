# Logging Strategy Plan for UGENTIC

## 1. Introduction
This document outlines a comprehensive logging strategy for the UGENTIC framework, designed to provide deep insights into application workflow, agent behavior, tool usage, and error handling. The strategy prioritizes structured logging for future scalability and compatibility with centralized log aggregation systems.

## 2. Core Principles
*   **Structured Logging:** All logs will be emitted in a structured format (JSON Lines - `.jsonl`). This makes them easily machine-readable and ingestible by log aggregation tools.
*   **Centralized Configuration:** Utilize Python's built-in `logging` module for its flexibility and power.
*   **Hierarchical Loggers:** Create specific loggers for different components (e.g., `ugentic.orchestrator`, `ugentic.agent.finance`, `ugentic.tool.research`, `ugentic.llm`). This allows for fine-grained control over what gets logged where.
*   **Contextual Information:** Logs will include rich, dynamic context relevant to the event (e.g., `agent_id`, `task_id`, `tool_name`, `llm_model_used`).
*   **Pluggable Handlers:** Design the system to easily swap between local file handlers and network handlers (for centralized aggregation) in the future.

## 3. Logging Levels
Standard Python logging levels will be used:
*   `DEBUG`: Detailed information for diagnosis.
*   `INFO`: General confirmation of operations.
*   `WARNING`: Potential issues or unexpected events.
*   `ERROR`: Functional failures.
*   `CRITICAL`: Severe errors, potentially leading to application shutdown.

## 4. Log Destinations & File Structure (Initial Phase)
All log files will reside within a new `logs` directory at the project root (`C:\Users\craig\Desktop\MainProjects\Ugentic\logs`).

*   **Console Output:** For immediate feedback during development.
*   **Structured JSON Files:** Logs will be written to JSON Lines (`.jsonl`) files.
*   **File Structure:**
    *   `logs/main.jsonl`: Comprehensive log of all messages (INFO and above) from all loggers.
    *   `logs/workflow.jsonl`: High-level orchestration steps, goal decomposition, and task assignments.
    *   `logs/llm_interactions.jsonl`: Detailed logs of all LLM calls, prompts, and responses.
    *   `logs/tools.jsonl`: Records of all tool executions, including tool name, parameters, and results.
    *   `logs/errors.jsonl`: Dedicated file for all `ERROR` and `CRITICAL` level messages.
    *   **`logs/agents/` (subdirectory):**
        *   `logs/agents/orchestrator.jsonl`
        *   `logs/agents/finance.jsonl`
        *   `logs/agents/hr.jsonl`
        *   `logs/agents/operations.jsonl`
        *   `logs/agents/marketing.jsonl`
        *   `logs/agents/sales.jsonl`
        *   `logs/agents/unison.jsonl`: (Optional, for inter-agent communication/synchronization).

## 5. Log Format (JSON Lines - `.jsonl`)
Each line in the log file will be a self-contained JSON object. This is ideal for streaming and parsing.

Example Log Entry:
```json
{
    "timestamp": "YYYY-MM-DDTHH:MM:SS.sssZ",
    "level": "INFO",
    "logger_name": "ugentic.orchestrator",
    "message": "Orchestrator received goal",
    "context": {
        "goal": "Launch new product line",
        "orchestrator_id": "MainOrchestrator",
        "task_id": "xyz123",
        "source_file": "orchestrator.py",
        "line_number": 123
    }
}
```
The `context` field will be a flexible dictionary containing dynamic, relevant key-value pairs for the specific log event.

## 6. Log Rotation
`logging.handlers.RotatingFileHandler` will be implemented for all file handlers to prevent log files from growing indefinitely. This will automatically create new log files when the current one reaches a certain size, keeping a backup of older logs.

## 7. Future Scalability (Centralized Aggregation)
*   The structured JSON logs are directly compatible with tools like Logstash, Fluentd, or cloud-native logging services (e.g., AWS CloudWatch, Google Cloud Logging).
*   Transitioning to network-based logging (e.g., sending logs to a Kafka topic, a Redis queue, or directly to a log aggregation service endpoint) would be a straightforward change of handlers, without requiring a fundamental change to how logs are generated.

## 8. Benefits
*   **Enhanced Visibility:** Gain deep insights into the application's internal workings, agent decision-making, and tool interactions.
*   **Improved Debugging & Troubleshooting:** Quickly identify the root cause of errors and unexpected behavior with detailed, contextual information.
*   **Performance Monitoring:** Analyze log data to identify bottlenecks and optimize performance.
*   **Auditing & Compliance:** Maintain a clear record of system activities.
*   **Future-Proofing:** Lay the groundwork for seamless integration with advanced log analysis and monitoring platforms.

## 9. High-Level Implementation Steps
1.  **Create `logs` directory:** Ensure the `logs` directory exists at the project root.
2.  **Centralized Logging Configuration:** Implement a `logging_config.py` module or configure logging directly in `app.py` using `logging.config.dictConfig`.
3.  **Custom JSON Formatter:** Develop a custom formatter to output logs in JSON format.
4.  **Integrate Loggers:** Instantiate and use specific loggers (`ugentic.orchestrator`, `ugentic.agent.finance`, etc.) throughout the codebase.
5.  **Add Contextual Information:** Pass relevant context (e.g., `agent_id`, `task_id`) to log messages using `extra` parameter in logging calls.
6.  **Error Handling:** Ensure critical errors are logged with appropriate detail.
7.  **Testing:** Thoroughly test the logging system to ensure all desired information is captured correctly.
