import sys
import os
import json
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.tools.interface import BaseTool, ToolResult
from tars.tools.permissions import PermissionCategory, PermissionManager
from tars.tools.registry import ToolRegistry

class DummySafeTool(BaseTool):
    @property
    def name(self): return "dummy_safe"
    @property
    def description(self): return "A safe tool"
    @property
    def permission(self): return PermissionCategory.SAFE_ACTION
    def get_parameters_schema(self): return {"type": "object", "properties": {"val": {"type": "string"}}, "required": ["val"]}
    def _execute(self, val): return f"Done {val}"

class DummySensitiveTool(BaseTool):
    @property
    def name(self): return "dummy_sensitive"
    @property
    def description(self): return "A sensitive tool"
    @property
    def permission(self): return PermissionCategory.SENSITIVE
    def get_parameters_schema(self): return {"type": "object", "properties": {}}
    def _execute(self): return "Secret"

class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        self.registry = ToolRegistry(self.manager)
        
    def test_registration_and_list(self):
        tool = DummySafeTool()
        self.registry.register(tool)
        self.assertIn("dummy_safe", self.registry.list_tools())
        
    def test_enable_disable(self):
        tool = DummySafeTool()
        self.registry.register(tool)
        
        schemas = self.registry.get_enabled_schemas()
        self.assertEqual(len(schemas), 1)
        
        self.registry.set_enabled("dummy_safe", False)
        schemas = self.registry.get_enabled_schemas()
        self.assertEqual(len(schemas), 0)
        
    def test_schema_generation(self):
        tool = DummySafeTool()
        self.registry.register(tool)
        schema = self.registry.get_enabled_schemas()[0]
        self.assertEqual(schema["type"], "function")
        self.assertEqual(schema["function"]["name"], "dummy_safe")
        
    def test_execute_nonexistent(self):
        result = self.registry.execute_tool("fake_tool", "{}")
        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)
        
    def test_execute_disabled(self):
        self.registry.register(DummySafeTool(), enabled=False)
        result = self.registry.execute_tool("dummy_safe", '{"val": "x"}')
        self.assertFalse(result.success)
        self.assertIn("disabled", result.error)
        
    def test_execute_permission_denied(self):
        self.registry.register(DummySensitiveTool())
        result = self.registry.execute_tool("dummy_sensitive", "{}")
        self.assertFalse(result.success)
        self.assertIn("Permission Denied", result.error)
        
    def test_execute_malformed_json(self):
        self.registry.register(DummySafeTool())
        result = self.registry.execute_tool("dummy_safe", '{"val": }') # Invalid JSON
        self.assertFalse(result.success)
        self.assertIn("Malformed JSON", result.error)
        
    def test_execute_invalid_args(self):
        self.registry.register(DummySafeTool())
        result = self.registry.execute_tool("dummy_safe", '{}') # Missing required 'val'
        self.assertFalse(result.success)
        self.assertIn("Invalid arguments", result.error)
        
    def test_execute_success(self):
        self.registry.register(DummySafeTool())
        result = self.registry.execute_tool("dummy_safe", '{"val": "xyz"}')
        self.assertTrue(result.success)
        self.assertEqual(result.data, "Done xyz")

if __name__ == '__main__':
    unittest.main()
