import sys
import os
import unittest
import json

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.memory.session import SessionManager

class TestAdversarialMemory(unittest.TestCase):
    def setUp(self):
        self.session = SessionManager(context_size=1000, system_prompt="system", response_headroom=100)

    def test_large_tool_payload(self):
        # A payload that exceeds context
        huge_result = "A " * 5000 
        
        self.session.add_user_message("Query")
        self.session.add_assistant_tool_calls([{"id": "1", "function": {"name": "test"}}])
        self.session.add_tool_result("1", huge_result)
        
        self.assertEqual(len(self.session.messages), 0)
        
    def test_dangling_tool_calls(self):
        # Simulate assistant calling tool, but tool fails or we inject a user message before tool result
        self.session.add_user_message("Query")
        self.session.add_assistant_tool_calls([{"id": "1", "function": {"name": "test"}}])
        self.session.add_user_message("Wait, stop")
        
        # Should not crash.
        messages = self.session.get_messages()
        self.assertEqual(messages[-1]["content"], "Wait, stop")
        
    def test_empty_responses(self):
        self.session.add_assistant_message("")
        self.session.add_user_message("")
        
        self.assertTrue(len(self.session.messages) >= 2)
        
    def test_malformed_openai_sequence_prevention(self):
        # Fill it up so it trims
        for i in range(50):
            self.session.add_user_message(f"User {i}")
            self.session.add_assistant_tool_calls([{"id": f"t_{i}", "function": {"name": "t"}}])
            self.session.add_tool_result(f"t_{i}", f"Result {i}")
            
        messages = self.session.messages
        # The first message shouldn't be an orphan tool result.
        if messages:
            self.assertNotEqual(messages[0]["role"], "tool")

if __name__ == '__main__':
    unittest.main()
