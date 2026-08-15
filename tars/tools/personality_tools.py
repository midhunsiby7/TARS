from typing import Dict, Any
from tars.tools.interface import BaseTool
from tars.tools.permissions import PermissionCategory
from tars.personality.manager import PersonalityManager

class GetPersonalityTool(BaseTool):
    def __init__(self, personality_manager: PersonalityManager):
        self.pm = personality_manager

    @property
    def name(self) -> str:
        return "get_personality"

    @property
    def description(self) -> str:
        return "Returns the current 0-100 values for all personality parameters."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.READ_ONLY

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    def _execute(self) -> str:
        p = self.pm.profile
        return f"Humor: {p.humor}\nHonesty: {p.honesty}\nEmotion: {p.emotional_expression}\nVerbosity: {p.verbosity}\nFormality: {p.formality}\nProactivity: {p.proactivity}"


class SetPersonalityTool(BaseTool):
    def __init__(self, personality_manager: PersonalityManager):
        self.pm = personality_manager

    @property
    def name(self) -> str:
        return "set_personality"

    @property
    def description(self) -> str:
        return "Updates one or more personality parameters (0-100 scale)."

    @property
    def permission(self) -> PermissionCategory:
        return PermissionCategory.SAFE_ACTION

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "humor": {"type": "integer"},
                "honesty": {"type": "integer"},
                "emotional_expression": {"type": "integer"},
                "verbosity": {"type": "integer"},
                "formality": {"type": "integer"},
                "proactivity": {"type": "integer"}
            }
        }

    def _execute(self, **kwargs) -> str:
        updates = {k: v for k, v in kwargs.items() if v is not None}
        if not updates:
            return "No parameters provided to update."
            
        changed = self.pm.update_profile(updates)
        if changed:
            return "Personality updated successfully."
        return "Personality update failed or no changes were made."
