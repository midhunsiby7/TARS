import json
from typing import List, Dict, Any, Optional
from tars.core.state import ConversationalState

class SessionManager:
    """Manages the conversation context, system prompt, and sliding window truncation."""
    
    def __init__(self, context_size: int, system_prompt: str, response_headroom: int = 512):
        self.context_size = context_size
        self.response_headroom = response_headroom
        self.system_prompt = system_prompt
        self.messages: List[Dict[str, Any]] = []
        self.state = ConversationalState()
        
    def reset(self):
        """Clears the current conversation history."""
        self.messages = []
        self.state.reset()
        
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self.state.increment_turn()
        self.trim_to_context()
        
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self.trim_to_context()

    def add_assistant_tool_calls(self, tool_calls: List[Dict[str, Any]]):
        """Adds an assistant message representing a tool call request."""
        self.messages.append({"role": "assistant", "content": None, "tool_calls": tool_calls})
        if tool_calls:
            first_call = tool_calls[0]
            func = first_call.get("function", {})
            self.state.record_tool_call(func.get("name", "unknown"), func.get("arguments", "{}"))
        self.trim_to_context()

    def add_tool_result(self, tool_call_id: str, content: str):
        """Adds a tool message containing the execution result."""
        self.messages.append({"role": "tool", "content": content, "tool_call_id": tool_call_id})
        self.state.record_tool_result(content)
        self.trim_to_context()

    def get_messages(self) -> List[Dict[str, Any]]:
        """Returns the full message history formatted for the LLM."""
        sys_msg = self.system_prompt
        state_context = self.state.to_prompt_context()
        if state_context:
            sys_msg += "\n\n" + state_context
            
        final_msgs = [{"role": "system", "content": sys_msg}]
        final_msgs.extend(self.messages)
        return final_msgs

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
            popped = self.messages.pop(0)
            
            # If we popped a user message, pop the corresponding assistant message too
            if popped["role"] == "user" and self.messages and self.messages[0]["role"] == "assistant":
                popped_assistant = self.messages.pop(0)
                # If that assistant message had tool calls, we must also pop the tool results
                if popped_assistant.get("tool_calls"):
                    while self.messages and self.messages[0]["role"] == "tool":
                        self.messages.pop(0)
                        
            # If we just popped an assistant message that had tool calls, pop the results
            elif popped["role"] == "assistant" and popped.get("tool_calls"):
                while self.messages and self.messages[0]["role"] == "tool":
                    self.messages.pop(0)
                    
            # If we somehow popped a tool result (maybe left over), keep popping if there are more
            elif popped["role"] == "tool":
                while self.messages and self.messages[0]["role"] == "tool":
                    self.messages.pop(0)
