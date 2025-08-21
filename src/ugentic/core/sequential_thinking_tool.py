# Sequential Thinking Tool for UGENTIC Agents

import json

from langchain_community.llms import Ollama # Import Ollama for live LLM interaction

class SequentialThinkingTool:
    def __init__(self, llm_model=None):
        self.name = "SequentialThinkingTool"
        self.description = "Manages complex, multi-step workflows by decomposing goals into actionable sequences."
        self.llm_model = llm_model

    def _interact_with_llm(self, prompt_text):
        """Interacts with the live LLM to get a response for decomposition."""
        if self.llm_model is None:
            return '{"error": "LLM model not provided."}'

        print(f"  [SequentialThinkingTool LLM]: Processing prompt: '{prompt_text[:100]}...' ")

        try:
            response = self.llm_model.invoke(prompt_text)
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json_str
            else:
                print(f"  [SequentialThinkingTool LLM]: Could not find JSON array in LLM response: {response[:100]}...")
                return "[]"
        except Exception as e:
            print(f"  [SequentialThinkingTool LLM]: Error invoking LLM: {e}")
            return "[]"

    def decompose_goal(self, goal):
        """Decomposes a high-level goal into a sequence of smaller, actionable steps."""
        prompt = f"""
        Decompose the following high-level goal into a sequence of actionable steps:
        Goal: {goal}
        Respond with ONLY a JSON array of objects, where each object has 'step', 'task', and 'agent' keys.
        """
        response_str = self._interact_with_llm(prompt)
        try:
            return json.loads(response_str)
        except json.JSONDecodeError:
            print(f"  [SequentialThinkingTool]: Error decoding LLM response for decomposition.")
            return []

    def execute_sequence(self, sequence_of_tasks):
        """Executes a given sequence of tasks in order."""
        print(f"  [SequentialThinkingTool]: Executing sequence of {len(sequence_of_tasks)} tasks.")
        for task_info in sequence_of_tasks:
            print(f"    - Step {task_info.get('step', '')}: Task '{task_info.get('task', '')}' (Agent: {task_info.get('agent', '')})")
            # In a real system, this would involve delegating to the specified agent/tool
        print(f"  [SequentialThinkingTool]: Sequence execution complete.")
        return {"status": "success", "message": "Sequence executed.", "executed_tasks": len(sequence_of_tasks)}

# Example Usage (for testing)
if __name__ == "__main__":
    seq_tool = SequentialThinkingTool()

    print("\n--- Testing decompose_goal ---")
    goal = "Launch a new product."
    decomposed_steps = seq_tool.decompose_goal(goal)
    print(f"Decomposed Steps: {decomposed_steps}")

    print("\n--- Testing execute_sequence ---")
    if decomposed_steps:
        seq_tool.execute_sequence(decomposed_steps)
    else:
        print("No steps to execute.")

