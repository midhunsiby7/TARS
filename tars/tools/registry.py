from typing import Dict, List, Optional
from .interface import BaseTool, ToolResult
from .permissions import PermissionManager, PermissionDeniedError, PermissionCategory

class ToolRegistry:
    """Centralized registration and lookup for all TARS tools."""
    
    def __init__(self, permission_manager: PermissionManager):
        self.permission_manager = permission_manager
        self._tools: Dict[str, BaseTool] = {}
        self._enabled_state: Dict[str, bool] = {}

    def register(self, tool: BaseTool, enabled: bool = True):
        """Registers a tool in the registry."""
        self._tools[tool.name] = tool
        self._enabled_state[tool.name] = enabled

    def unregister(self, tool_name: str):
        """Removes a tool from the registry."""
        if tool_name in self._tools:
            del self._tools[tool_name]
            del self._enabled_state[tool_name]

    def set_enabled(self, tool_name: str, enabled: bool):
        """Enables or disables a registered tool."""
        if tool_name in self._tools:
            self._enabled_state[tool_name] = enabled

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Returns the tool if it exists."""
        return self._tools.get(tool_name)

    def list_tools(self) -> List[str]:
        """Lists all registered tool names."""
        return list(self._tools.keys())

    def get_enabled_schemas(self) -> List[dict]:
        """Returns the schemas for all currently enabled tools."""
        schemas = []
        for name, tool in self._tools.items():
            if self._enabled_state.get(name, False):
                schemas.append(tool.get_schema())
        return schemas

    def execute_tool(self, tool_name: str, arguments_json: str) -> ToolResult:
        """Looks up, checks permission, and executes a tool."""
        tool = self.get_tool(tool_name)
        
        # Check existence
        if not tool:
            return ToolResult(
                success=False,
                tool_name=tool_name,
                error=f"Error: Tool '{tool_name}' does not exist or is not registered."
            )
            
        # Check enabled state
        if not self._enabled_state.get(tool_name, False):
            return ToolResult(
                success=False,
                tool_name=tool_name,
                error=f"Error: Tool '{tool_name}' is currently disabled."
            )
            
        # Check permission
        try:
            self.permission_manager.enforce(tool.permission, tool.name)
        except PermissionDeniedError as e:
            return ToolResult(
                success=False,
                tool_name=tool_name,
                error=str(e)
            )
            
        # Validated Execution
        return tool.execute_validated(arguments_json)
