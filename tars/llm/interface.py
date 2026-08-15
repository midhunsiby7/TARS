import abc
from typing import Dict, List, Optional, Any

class LLMInterface(abc.ABC):
    """Abstract interface for the TARS LLM Backend.
    Provides a decoupled abstraction from the underlying process management.
    """
    
    @abc.abstractmethod
    def start_server(self, offload_layers: int, port: int, context_size: int) -> bool:
        """Starts the LLM backend server.
        Returns True if successful, False otherwise.
        """
        pass
        
    @abc.abstractmethod
    def stop_server(self) -> None:
        """Gracefully shuts down the LLM backend server."""
        pass
        
    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Checks if the LLM backend is responsive."""
        pass
        
    @abc.abstractmethod
    def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Generates a response from the LLM based on the conversation history.
        
        Args:
            messages: List of message dictionaries containing "role" and "content"
            tools: Optional list of tool definitions (OpenAI JSON schema format)
            
        Returns:
            A dictionary containing:
            - status: "success" or "failed"
            - content: The text response (if successful, might be empty if tools are called)
            - tool_calls: A list of tool calls (if the model requested any)
            - error: The error message (if failed)
            - fatal: Boolean indicating if this is an irrecoverable backend failure
        """
        pass
