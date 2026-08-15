from enum import Enum
from functools import total_ordering

@total_ordering
class PermissionCategory(Enum):
    READ_ONLY = 1
    SAFE_ACTION = 2
    SENSITIVE = 3
    DANGEROUS = 4
    FORBIDDEN = 5

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class PermissionDeniedError(Exception):
    pass

class PermissionManager:
    """Manages which tools are allowed to execute based on clearance level."""
    
    def __init__(self, max_allowed: PermissionCategory = PermissionCategory.SAFE_ACTION):
        self.max_allowed = max_allowed
        
    def is_allowed(self, category: PermissionCategory) -> bool:
        """Returns True if the tool's category is <= the max_allowed level."""
        return category <= self.max_allowed
        
    def enforce(self, category: PermissionCategory, tool_name: str):
        """Raises PermissionDeniedError if the category exceeds the clearance limit."""
        if not self.is_allowed(category):
            raise PermissionDeniedError(
                f"Permission Denied: Tool '{tool_name}' requires {category.name} clearance. "
                f"Maximum allowed is {self.max_allowed.name}."
            )
