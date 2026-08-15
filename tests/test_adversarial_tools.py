import sys
import os
import unittest
from unittest.mock import patch, MagicMock

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.tools.interface import BaseTool
from tars.tools.permissions import PermissionCategory, PermissionManager
from tars.tools.registry import ToolRegistry
from tars.core.orchestrator import TarsOrchestrator
from tars.memory.session import SessionManager
from tars.llm.interface import LLMInterface

class DummyDangerousTool(BaseTool):
    @property
    def name(self): return "format_drive"
    @property
    def description(self): return "Formats a drive"
    @property
    def permission(self): return PermissionCategory.DANGEROUS
    def get_parameters_schema(self): return {"type": "object", "properties": {"drive": {"type": "string"}}}
    def _execute(self, drive="C"): 
        raise RuntimeError("THIS SHOULD NEVER EXECUTE")

class DummyFailingTool(BaseTool):
    @property
    def name(self): return "failing_tool"
    @property
    def description(self): return "Always fails"
    @property
    def permission(self): return PermissionCategory.SAFE_ACTION
    def get_parameters_schema(self): return {"type": "object", "properties": {}}
    def _execute(self): 
        raise ValueError("Simulated tool crash")

class TestAdversarialTools(unittest.TestCase):
    def setUp(self):
        self.manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        self.registry = ToolRegistry(self.manager)
        self.registry.register(DummyDangerousTool())
        self.registry.register(DummyFailingTool())
        
    def test_dangerous_tool_blocked(self):
        result = self.registry.execute_tool("format_drive", '{"drive": "C:"}')
        self.assertFalse(result.success)
        self.assertIn("Permission Denied", result.error)
        
    def test_hallucinated_tool(self):
        result = self.registry.execute_tool("does_not_exist", '{}')
        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)
        
    def test_malformed_arguments(self):
        # We test schema validation logic which is handled in BaseTool.execute_validated
        # To do this directly, let's grab a tool
        tool = DummyDangerousTool()
        
        # Invalid JSON
        res1 = tool.execute_validated('{"drive": "C:", }')
        self.assertFalse(res1.success)
        self.assertIn("Malformed JSON", res1.error)
        
        # We don't have strict schema property validation enforced by jsonschema in interface.py right now unless we added it?
        # Actually in Phase 2B, `interface.py` was supposed to use `jsonschema.validate`.
        # Let's see what happens if we pass wrong type
        res2 = tool.execute_validated('{"drive": 123}')
        # We should expect jsonschema to reject it, but since execute_validated catches all exceptions, it should return False
        self.assertFalse(res2.success)
        self.assertIn("Invalid arguments", res2.error)
        
    def test_tool_failure_caught(self):
        result = self.registry.execute_tool("failing_tool", '{}')
        self.assertFalse(result.success)
        self.assertIn("Simulated tool crash", result.error)
        
    def test_circuit_breaker(self):
        mock_llm = MagicMock(spec=LLMInterface)
        # Mock LLM to return a tool call every time
        mock_llm.generate.return_value = {
            "status": "success",
            "content": "",
            "tool_calls": [{"id": "1", "function": {"name": "failing_tool", "arguments": "{}"}}]
        }
        
        session = SessionManager(2048, "sys")
        orchestrator = TarsOrchestrator(llm=mock_llm, session=session, tool_registry=self.registry)
        
        # Run agent loop
        orchestrator._execute_agent_loop()
        
        # The loop should stop after MAX_TOOL_CALLS (which is 3)
        # So generate should be called 4 times (0, 1, 2, 3)
        self.assertEqual(mock_llm.generate.call_count, 4)
        
        # Check that circuit breaker message was injected
        messages = session.get_messages()
        self.assertEqual(messages[-1]["role"], "assistant")
        self.assertIn("internal tool limit", messages[-1]["content"])

if __name__ == '__main__':
    unittest.main()
