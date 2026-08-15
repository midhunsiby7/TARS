import json
from typing import List, Dict, Any

class SessionManager:
    """Manages the conversation context, system prompt, and sliding window truncation."""
    
    def __init__(self, context_size: int, system_prompt: str, response_headroom: int = 512):
        self.context_size = context_size
        self.response_headroom = response_headroom
        self.system_prompt = system_prompt
        self.messages: List[Dict[str, Any]] = []
        
    def reset(self):
        """Clears the current conversation history."""
        self.messages = []
        
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self.trim_to_context()
        
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self.trim_to_context()

    def add_assistant_tool_calls(self, tool_calls: List[Dict[str, Any]]):
        """Adds an assistant message representing a tool call request."""
        self.messages.append({"role": "assistant", "content": None, "tool_calls": tool_calls})
        self.trim_to_context()

    def add_tool_result(self, tool_call_id: str, content: str):
        """Adds a tool message containing the execution result."""
        self.messages.append({"role": "tool", "content": content, "tool_call_id": tool_call_id})
        self.trim_to_context()

    def get_messages(self) -> List[Dict[str, Any]]:
        """Returns the full conversation payload including the system prompt."""
        payload = [{"role": "system", "content": self.system_prompt}]
        payload.extend(self.messages)
        return payload

    def _estimate_tokens(self, text: str) -> int:
        """Conservative token estimation heuristic. (approx 1.3 tokens per word)"""
        if not text:
            return 0
        return int(len(text.split()) * 1.3)

    def _calculate_total_tokens(self) -> int:
        """Calculates the estimated token count of the current payload."""
        total = self._estimate_tokens(self.system_prompt)
        for msg in self.messages:
            # Add a small buffer for the chat format wrappers (e.g. <|im_start|>user\n...)
            if msg.get("content"):
                total += self._estimate_tokens(msg["content"]) + 10
            elif msg.get("tool_calls"):
                # Estimate token cost of the JSON tool_calls block
                total += self._estimate_tokens(json.dumps(msg["tool_calls"])) + 10
            else:
                total += 10 # empty message wrapper
        return total

    def trim_to_context(self):
        """Removes the oldest user/assistant message pairs if we exceed the allowed context minus headroom."""
        max_allowed = self.context_size - self.response_headroom
        
        while self.messages and self._calculate_total_tokens() > max_allowed:
            # We want to remove pairs to maintain logical flow, but sometimes they aren't perfectly paired.
            # Pop the oldest message.
            popped = self.messages.pop(0)
            
            # If we just popped a user message, and the next is an assistant response, pop that too to keep history clean.
            if popped["role"] == "user" and self.messages and self.messages[0]["role"] == "assistant":
                # Only pop if it's not a tool call request, to avoid breaking tool call logic blindly,
                # though ideally we should clean up orphan tool calls too.
                if not self.messages[0].get("tool_calls"):
                    self.messages.pop(0)
