
import unittest
from src.ugentic.core.memory_tool import MemoryTool

class TestMemoryTool(unittest.TestCase):

    def setUp(self):
        self.memory_tool = MemoryTool()

    def test_store_and_retrieve_fact(self):
        key = "test_key"
        value = "test_value"
        
        store_result = self.memory_tool.store_fact(key, value)
        self.assertEqual(store_result["status"], "success")
        self.assertEqual(store_result["message"], f"Fact '{key}' stored.")

        retrieve_result = self.memory_tool.retrieve_fact(key)
        self.assertEqual(retrieve_result["status"], "success")
        self.assertEqual(retrieve_result["value"], value)

    def test_retrieve_non_existent_fact(self):
        key = "non_existent_key"
        retrieve_result = self.memory_tool.retrieve_fact(key)
        self.assertEqual(retrieve_result["status"], "error")
        self.assertEqual(retrieve_result["message"], f"Fact '{key}' not found.")

    def test_list_facts(self):
        self.memory_tool.store_fact("key1", "value1")
        self.memory_tool.store_fact("key2", "value2")

        list_result = self.memory_tool.list_facts()
        self.assertEqual(list_result["status"], "success")
        self.assertEqual(list_result["facts"], {"key1": "value1", "key2": "value2"})

    def test_list_empty_facts(self):
        list_result = self.memory_tool.list_facts()
        self.assertEqual(list_result["status"], "success")
        self.assertEqual(list_result["facts"], {})

if __name__ == '__main__':
    unittest.main()
