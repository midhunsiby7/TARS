import sys
import os
import unittest
from unittest.mock import patch, MagicMock

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.core.orchestrator import TarsOrchestrator
from tars.memory.session import SessionManager
from tars.llm.interface import LLMInterface
from tars.tools.registry import ToolRegistry
from tars.tools.permissions import PermissionManager, PermissionCategory

class TestAdversarialBackend(unittest.TestCase):
    def setUp(self):
        self.manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        self.registry = ToolRegistry(self.manager)
        self.session = SessionManager(2048, "sys")
        self.mock_llm = MagicMock(spec=LLMInterface)
        self.orchestrator = TarsOrchestrator(llm=self.mock_llm, session=self.session, tool_registry=self.registry)
        # Mock configuration so _attempt_backend_recovery doesn't actually try to start llama.cpp
        self.orchestrator._last_config = {"offload_layers": 15, "port": 8080, "context_size": 2048}
        
    def test_backend_fatal_error_recovery(self):
        # Simulate fatal error from backend
        self.mock_llm.generate.return_value = {
            "status": "failed",
            "error": "Connection refused",
            "fatal": True
        }
        self.mock_llm.start_server.return_value = True
        
        # When orchestrator runs agent loop, it should detect fatal error and attempt recovery
        result = self.orchestrator._execute_agent_loop()
        
        # It should return True because recovery (supposedly) succeeded
        self.assertTrue(result)
        self.assertEqual(self.orchestrator._current_restarts, 1)
        self.mock_llm.stop_server.assert_called_once()
        self.mock_llm.start_server.assert_called_with(offload_layers=15, port=8080, context_size=2048)
        
    def test_backend_recovery_exhaustion(self):
        self.mock_llm.generate.return_value = {
            "status": "failed",
            "error": "Connection refused",
            "fatal": True
        }
        self.mock_llm.start_server.return_value = False
        
        # First failure fails to restart
        result = self.orchestrator._execute_agent_loop()
        self.assertFalse(result)
        
    def test_malformed_llm_response(self):
        # Non-fatal error should just return to REPL safely
        self.mock_llm.generate.return_value = {
            "status": "failed",
            "error": "Malformed JSON",
            "fatal": False
        }
        
        result = self.orchestrator._execute_agent_loop()
        self.assertTrue(result) # Recoverable error returns True to keep REPL going
        self.assertEqual(self.orchestrator._current_restarts, 0)
        
if __name__ == '__main__':
    unittest.main()
