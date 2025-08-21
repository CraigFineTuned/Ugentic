# Decision Tool for UGENTIC Agents

import json

from langchain_community.llms import Ollama # Import Ollama for live LLM interaction

class DecisionTool:
    def __init__(self, llm_model=None):
        self.name = "DecisionTool"
        self.description = "Provides structured go/no-go or ranked-choice judgments based on LLM reasoning."
        self.llm_model = llm_model

    def _interact_with_llm(self, prompt_text):
        """Interacts with the live LLM to get a response for decision-making."""
        if self.llm_model is None:
            # This should not happen in production; the tool should always be initialized with an LLM.
            # Returning an error makes the dependency explicit.
            return '{"error": "LLM model not provided."}'

        print(f"  [DecisionTool LLM]: Processing prompt: '{prompt_text[:100]}...' ")

        try:
            response = self.llm_model.invoke(prompt_text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json_str
            else:
                print(f"  [DecisionTool LLM]: Could not find JSON in LLM response: {response[:100]}...")
                return '''{"error": "LLM did not return valid JSON."}'''
        except Exception as e:
            print(f"  [DecisionTool LLM]: Error invoking LLM: {e}")
            return '''{"error": "Failed to get decision due to LLM error."}'''

    def make_choice(self, question, options):
        """Selects the best option from a list based on a question."""
        prompt = f"""
        Question: {question}
        Options: {options}
        Which is the best option and why?
        Respond with ONLY a JSON object: {{"best_option": "chosen_option", "justification": "your_reasoning"}}
        """
        response_str = self._interact_with_llm(prompt)
        try:
            return json.loads(response_str)
        except json.JSONDecodeError:
            return {"error": "Failed to get a valid decision from the LLM."}

    def judge_proposal(self, proposal_text):
        """Evaluates a proposal and provides a judgment (Go, No-Go, Revise)."""
        prompt = f"""
        Please evaluate this proposal: "{proposal_text}"
        Should the decision be Go, No-Go, or Revise? Provide a justification.
        Respond with ONLY a JSON object: {{"judgment": "your_judgment", "justification": "your_reasoning"}}
        """
        response_str = self._interact_with_llm(prompt)
        try:
            return json.loads(response_str)
        except json.JSONDecodeError:
            return {"error": "Failed to get a valid judgment from the LLM."}

# Example Usage (for testing)
if __name__ == "__main__":
    decision_tool = DecisionTool()

    print("\n--- Testing make_choice ---")
    choice_result = decision_tool.make_choice(
        question="Which cloud provider should we use for the new project?",
        options=["AWS", "Azure", "GCP"]
    )
    print(f"Choice Result: {choice_result}")

    print("\n--- Testing judge_proposal ---")
    judgment_result = decision_tool.judge_proposal(
        proposal_text="Launch a new marketing campaign targeting students."
    )
    print(f"Judgment Result: {judgment_result}")

