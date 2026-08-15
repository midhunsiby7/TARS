import unittest
from tars.core.state import ConversationalState
from tars.memory.session import SessionManager

class TestConversationState(unittest.TestCase):
    def test_state_updates_on_user_message(self):
        state = ConversationalState()
        self.assertEqual(state.turn_count, 0)
        state.increment_turn()
        self.assertEqual(state.turn_count, 1)

    def test_state_tool_recording(self):
        session = SessionManager(2048, "System prompt")
        
        # Add a tool call
        session.add_assistant_tool_calls([{"function": {"name": "get_weather", "arguments": "{}"}}])
        self.assertEqual(session.state.last_tool_name, "get_weather")
        
        # Add result
        session.add_tool_result("call_1", "Sunny")
        self.assertEqual(session.state.last_tool_result, "Sunny")
        
        # Verify it injects into context
        sys_msg = session.get_messages()[0]["content"]
        self.assertIn("get_weather", sys_msg)
        self.assertIn("Sunny", sys_msg)

    def test_state_expiry(self):
        session = SessionManager(2048, "System prompt")
        session.add_assistant_tool_calls([{"function": {"name": "get_weather", "arguments": "{}"}}])
        self.assertEqual(session.state.last_tool_name, "get_weather")
        
        # Simulate 3 user turns without tools
        session.add_user_message("Turn 1")
        session.add_user_message("Turn 2")
        session.add_user_message("Turn 3")
        
        # Should be expired
        self.assertIsNone(session.state.last_tool_name)
        
        sys_msg = session.get_messages()[0]["content"]
        self.assertNotIn("get_weather", sys_msg)

if __name__ == "__main__":
    unittest.main()
