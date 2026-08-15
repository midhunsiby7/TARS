import sys
import os
import unittest
from unittest.mock import patch

# Adjust path to import tars modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.memory.session import SessionManager

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.session = SessionManager(
            context_size=100, 
            system_prompt="System", 
            response_headroom=20
        )
        # Max allowed tokens will be 80.
        # "System" is ~1.3 tokens. 
        # Each message adds content length * 1.3 + 10 overhead.

    def test_message_ordering_and_reset(self):
        self.session.add_user_message("Hello")
        self.session.add_assistant_message("Hi there")
        
        msgs = self.session.get_messages()
        self.assertEqual(len(msgs), 3)
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[1]["role"], "user")
        self.assertEqual(msgs[2]["role"], "assistant")
        
        self.session.reset()
        self.assertEqual(len(self.session.get_messages()), 1)
        self.assertEqual(self.session.get_messages()[0]["role"], "system")

    def test_context_trimming(self):
        # We need to add enough messages to exceed the context limit.
        # Max allowed = 80 tokens.
        # System: ~1.3
        # Msg 1: 10 words * 1.3 + 10 = 23
        # Msg 2: 10 words * 1.3 + 10 = 23
        # Msg 3: 10 words * 1.3 + 10 = 23
        # Msg 4: 10 words * 1.3 + 10 = 23
        # Total with 4 messages = 1.3 + 4 * 23 = 93.3 > 80. Should trim.
        
        long_text = "word " * 10
        self.session.add_user_message(long_text)
        self.session.add_assistant_message(long_text)
        
        # Currently 47.3 tokens. Should not trim.
        self.assertEqual(len(self.session.messages), 2)
        
        self.session.add_user_message(long_text)
        self.session.add_assistant_message(long_text)
        
        # Now we added two more, it should have trimmed the oldest pair.
        self.assertEqual(len(self.session.messages), 2)

if __name__ == '__main__':
    unittest.main()
