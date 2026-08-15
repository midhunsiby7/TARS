from typing import Optional, Any, Dict

class ConversationalState:
    def __init__(self):
        self.last_tool_name: Optional[str] = None
        self.last_tool_args: Optional[str] = None
        self.last_tool_result: Optional[str] = None
        
        # Bounded context tracking
        self.current_topic: Optional[str] = None
        self.pending_clarification: bool = False
        
        self.turn_count: int = 0

    def record_tool_call(self, name: str, args: str):
        self.last_tool_name = name
        self.last_tool_args = args

    def record_tool_result(self, result: str):
        self.last_tool_result = result
        
    def increment_turn(self):
        self.turn_count += 1
        
        # Expire tool context if no new tools have been called for 3 user turns
        # to prevent stale context bleed.
        if self.turn_count >= 3:
            self.last_tool_name = None
            self.last_tool_args = None
            self.last_tool_result = None
            self.turn_count = 0

    def reset(self):
        self.last_tool_name = None
        self.last_tool_args = None
        self.last_tool_result = None
        self.current_topic = None
        self.pending_clarification = False
        self.turn_count = 0

    def to_prompt_context(self) -> str:
        """Serializes active state into a string to inject into the system prompt."""
        parts = []
        if self.last_tool_name and self.last_tool_result:
            parts.append(f"- Recent Tool Executed: '{self.last_tool_name}' returned: {self.last_tool_result}")
        if self.current_topic:
            parts.append(f"- Current Topic: {self.current_topic}")
            
        if not parts:
            return ""
            
        return "Conversational State:\n" + "\n".join(parts)
