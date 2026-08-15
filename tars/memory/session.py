from typing import List, Dict

class SessionManager:
    """Manages the conversation context, system prompt, and sliding window truncation."""
    
    def __init__(self, context_size: int, system_prompt: str, response_headroom: int = 512):
        self.context_size = context_size
        self.response_headroom = response_headroom
        self.system_prompt = system_prompt
        self.messages: List[Dict[str, str]] = []
        
    def reset(self):
        """Clears the current conversation history."""
        self.messages = []
        
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self.trim_to_context()
        
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self.trim_to_context()

    def get_messages(self) -> List[Dict[str, str]]:
        """Returns the full conversation payload including the system prompt."""
        payload = [{"role": "system", "content": self.system_prompt}]
        payload.extend(self.messages)
        return payload

    def _estimate_tokens(self, text: str) -> int:
        """Conservative token estimation heuristic. (approx 1.3 tokens per word)"""
        return int(len(text.split()) * 1.3)

    def _calculate_total_tokens(self) -> int:
        """Calculates the estimated token count of the current payload."""
        total = self._estimate_tokens(self.system_prompt)
        for msg in self.messages:
            # Add a small buffer for the chat format wrappers (e.g. <|im_start|>user\n...)
            total += self._estimate_tokens(msg["content"]) + 10
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
                self.messages.pop(0)
