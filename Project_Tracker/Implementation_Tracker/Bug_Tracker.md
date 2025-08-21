# BUG TRACKER - Issues & Resolutions
## Tracking All Bugs, Issues, and Blockers

**Project:** UGENTIC Framework  
**Started:** August 14, 2025  

---

## 🐞 **CRITICAL BUGS** (Blocking Progress)

*   _No critical bugs currently._

---

## 🛠️ **ACTIVE ISSUES**

| ID      | Severity | Component                 | Description                                    | Status      | Assigned | Target Fix   |
|---------|----------|---------------------------|------------------------------------------------|-------------|----------|--------------|


---

## ✅ **RESOLVED ISSUES**

| ID      | Severity | Component         | Description                                      | Resolution                               | Resolved Date |
|---------|----------|-------------------|--------------------------------------------------|------------------------------------------|---------------|
| **TRK-1** | **High**   | Project Structure | Project Tracker files were missing or incomplete.  | Created and populated all tracker files. | Aug 15, 2025  |
| **ENV-1** | **Medium** | Development Environment   | Python virtual environment created.            | Virtual environment created.             | Aug 15, 2025  |
| **DEP-1** | **Low**    | Dependencies              | `requirements.txt` file populated.             | Dependencies installed.                  | Aug 15, 2025  |
| **SYN-1** | **High**   | `agent_framework.py` | `SyntaxError: f-string: unmatched '{'` in `decompose_goal` prompt. | Refactored example JSON creation out of the f-string to fix parser error. | Aug 18, 2025 |
| **SYN-2** | **High**   | `agent_framework.py` | `SyntaxError: f-string: unmatched '['` in `decompose_goal` validation. | Corrected nested quotes within the f-string to fix parser error. | Aug 19, 2025 |
| **RES-1** | **High**   | `research_tool.py` | ResearchTool iterating over URL string character-by-character instead of treating it as single URL. | Added type check to convert string sources to list before iteration. | Aug 19, 2025  |
| **LLM-1** | **High**   | `agent_framework.py` | Parameter name mismatch in `SequentialThinkingTool.decompose_goal`. | Renamed parameter to match LLM output. | Aug 21, 2025  |
| **LLM-2** | **Critical** | `agent_framework.py` | LLM hallucinating non-existent tool actions (e.g., `ResearchTool.llm_model`). | Implemented Tool Validator to prevent crashes and provide feedback. | Aug 21, 2025  |
| **LLM-3** | **Critical** | `agent_framework.py` | LLM missing required parameters for tool actions (e.g., `DecisionTool.make_choice` missing `options`). | Implemented Parameter Validator to prevent crashes and provide feedback. | Aug 21, 2025  |
| **FS-1**  | **High**   | `filesystem_tool.py` | `FilesystemTool.list_directory` defaulting to root for non-existent paths. | Modified to return explicit "Directory not found" error. | Aug 21, 2025  |
| **RT-1**  | **High**   | `research_tool.py` | `ResearchTool` passing local file names as URLs to `FetchTool`. | Modified `perform_research` to differentiate URLs from local documents. | Aug 21, 2025  |
| **LLM-4** | **High**   | LLM Prompting | LLM hallucinating arbitrary file paths for `AnalysisTool` and `FilesystemTool`. | Added explicit absolute path guidance to `_build_tool_prompt`. | Aug 21, 2025  |

---

## 템플릿 **BUG REPORT TEMPLATE**

```markdown
### **ISSUE-XXX: [Brief, Clear Title]**
**Date Reported:** [YYYY-MM-DD]
**Severity:** [Critical / High / Medium / Low]
**Component:** [e.g., Finance Agent, Consensus Engine, UI]
**Description:** [A clear and concise description of the issue.]

**Steps to Reproduce:**
1. [First Step]
2. [Second Step]
3. [Third Step]

**Expected Behavior:** [What you expected to happen.]
**Actual Behavior:** [What actually happened.]

**Impact:** [How this issue affects the project. e.g., Blocks development, minor UI glitch.]
**Assigned:** [Name]
**Status:** [To Do / In Progress / In Review / Done]
```

---
