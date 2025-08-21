# Memory Tool for UGENTIC Agents

class MemoryTool:
    def __init__(self):
        self.name = "MemoryTool"
        self.description = "Provides a persistent key-value store for agents to remember facts and information."
        self.memory_store = {}
        print(f"{self.name} initialized.")

    def store_fact(self, key, value):
        """Stores a fact (key-value pair) in the agent's memory."""
        self.memory_store[key] = value
        print(f"  [MemoryTool]: Stored fact '{key}'.")
        return {"status": "success", "message": f"Fact '{key}' stored."}

    def retrieve_fact(self, key):
        """Retrieves a fact from the agent's memory by its key."""
        value = self.memory_store.get(key)
        if value is not None:
            print(f"  [MemoryTool]: Retrieved fact '{key}'.")
            return {"status": "success", "value": value}
        else:
            print(f"  [MemoryTool]: Fact '{key}' not found.")
            return {"status": "error", "message": f"Fact '{key}' not found."}

    def list_facts(self):
        """Lists all stored facts (keys and values) in the agent's memory."""
        print(f"  [MemoryTool]: Listing all facts.")
        return {"status": "success", "facts": self.memory_store}

# Example Usage (for testing)
if __name__ == "__main__":
    memory_tool = MemoryTool()

    print("\n--- Testing store_fact ---")
    memory_tool.store_fact("project_name", "UGENTIC")
    memory_tool.store_fact("current_sprint", "Sprint 4")

    print("\n--- Testing retrieve_fact ---")
    project_name = memory_tool.retrieve_fact("project_name")
    print(f"Retrieved project name: {project_name}")

    non_existent_fact = memory_tool.retrieve_fact("non_existent_key")
    print(f"Retrieved non-existent fact: {non_existent_fact}")

    print("\n--- Testing list_facts ---")
    all_facts = memory_tool.list_facts()
    print(f"All stored facts: {all_facts}")
