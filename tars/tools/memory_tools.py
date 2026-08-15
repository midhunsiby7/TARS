from typing import Dict, Any, Type
from tars.tools.interface import BaseTool
from tars.tools.permissions import PermissionCategory
from tars.memory.manager import MemoryManager

class RememberTool(BaseTool):
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "remember"

    @property
    def description(self) -> str:
        return "Stores a piece of information persistently across sessions."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.SAFE_ACTION

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "High-level grouping, e.g., 'preference', 'fact'."},
                "key": {"type": "string", "description": "Unique identifier within the category, e.g., 'favorite_language'."},
                "content": {"type": "string", "description": "The information to store."}
            },
            "required": ["category", "key", "content"]
        }

    def _execute(self, category: str, key: str, content: str) -> str:
        mem = self.memory_manager.remember(category, key, content)
        return f"Successfully stored memory [{mem.category} | {mem.key}]."


class RecallTool(BaseTool):
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "recall"

    @property
    def description(self) -> str:
        return "Searches for relevant stored memories based on a query or category."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.READ_ONLY

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword to search for in keys and contents."},
                "category": {"type": "string", "description": "Optional category filter."}
            }
        }

    def _execute(self, query: str = "", category: str = None) -> str:
        mems = self.memory_manager.retrieve_relevant_memories(query, category)
        if not mems:
            return "No matching memories found."
        
        lines = []
        for m in mems:
            lines.append(f"[{m.category} | {m.key}] {m.content}")
        return "\n".join(lines)


class ListMemoriesTool(BaseTool):
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "list_memories"

    @property
    def description(self) -> str:
        return "Lists recent stored memories safely."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.READ_ONLY

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Maximum number of memories to return (default 10)."}
            }
        }

    def _execute(self, limit: int = 10) -> str:
        mems = self.memory_manager.list_memories(limit)
        if not mems:
            return "No memories stored."
        
        lines = []
        for m in mems:
            lines.append(f"[{m.category} | {m.key}] {m.content}")
        return "\n".join(lines)


class ForgetTool(BaseTool):
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "forget"

    @property
    def description(self) -> str:
        return "Deletes a specific memory by category and key."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.SAFE_ACTION

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "key": {"type": "string"}
            },
            "required": ["category", "key"]
        }

    def _execute(self, category: str, key: str) -> str:
        success = self.memory_manager.forget(category, key)
        if success:
            return f"Successfully deleted memory [{category} | {key}]."
        return f"Memory not found: [{category} | {key}]."
