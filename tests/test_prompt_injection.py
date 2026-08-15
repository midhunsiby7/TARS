import sys
import os
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.tools.interface import BaseTool
from tars.tools.permissions import PermissionCategory, PermissionManager
from tars.tools.registry import ToolRegistry

class DummyDangerousTool(BaseTool):
    @property
    def name(self): return "format_drive"
    @property
    def description(self): return "Formats a drive"
    @property
    def permission(self): return PermissionCategory.DANGEROUS
    def get_parameters_schema(self): return {"type": "object", "properties": {}}
    def _execute(self): 
        raise RuntimeError("THIS SHOULD NEVER EXECUTE")

class TestPromptInjection(unittest.TestCase):
    def setUp(self):
        self.manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        self.registry = ToolRegistry(self.manager)
        self.registry.register(DummyDangerousTool())
        
    def test_permission_bypassing(self):
        # Even if the LLM is somehow convinced to call a dangerous tool,
        # the ToolRegistry MUST block it.
        # This test ensures that the registry block happens purely at the programmatic layer,
        # ignoring any metadata the LLM might hallucinate.
        
        result = self.registry.execute_tool("format_drive", "{}")
        self.assertFalse(result.success)
        self.assertIn("Permission Denied", result.error)
        
        # Test that injecting a fake tool doesn't work either
        result2 = self.registry.execute_tool("unknown_malicious_tool", "{}")
        self.assertFalse(result2.success)
        self.assertIn("does not exist", result2.error)

if __name__ == '__main__':
    unittest.main()
