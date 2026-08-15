import abc
import json
import jsonschema
from typing import Any, Dict, Optional
from dataclasses import dataclass

from .permissions import PermissionCategory

@dataclass
class ToolResult:
    """Structured representation of a tool execution result."""
    success: bool
    tool_name: str
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def serialize(self) -> str:
        """Serializes the result into a concise string for the LLM context window."""
        if self.success:
            if isinstance(self.data, dict) or isinstance(self.data, list):
                return json.dumps(self.data)
            return str(self.data)
        else:
            return f"Error executing {self.tool_name}: {self.error}"

class BaseTool(abc.ABC):
    """Abstract foundation for all TARS Phase 2B tools."""
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass
        
    @property
    @abc.abstractmethod
    def permission(self) -> PermissionCategory:
        pass
        
    @abc.abstractmethod
    def get_parameters_schema(self) -> dict:
        """Returns the JSON schema for the arguments this tool accepts."""
        pass
        
    def get_schema(self) -> dict:
        """Returns the fully compliant OpenAI function calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters_schema()
            }
        }
        
    @abc.abstractmethod
    def _execute(self, **kwargs) -> Any:
        """Internal execution logic implemented by subclasses."""
        pass
        
    def execute_validated(self, arguments_json: str) -> ToolResult:
        """Validates arguments against the schema before execution."""
        try:
            # Parse arguments
            if not arguments_json or arguments_json.strip() == "":
                args = {}
            else:
                args = json.loads(arguments_json)
                
            # Validate against schema
            jsonschema.validate(instance=args, schema=self.get_parameters_schema())
            
            # Execute safely
            result_data = self._execute(**args)
            return ToolResult(
                success=True,
                tool_name=self.name,
                data=result_data
            )
            
        except json.JSONDecodeError as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                error=f"Malformed JSON arguments: {str(e)}"
            )
        except jsonschema.exceptions.ValidationError as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                error=f"Invalid arguments. {e.message}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                error=f"Tool execution failed: {str(e)}"
            )
