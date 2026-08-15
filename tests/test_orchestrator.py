import sys
import os
import unittest
from unittest.mock import MagicMock

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.core.orchestrator import TarsOrchestrator
from tars.memory.session import SessionManager

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.session = SessionManager(100, "Sys")
        self.orchestrator = TarsOrchestrator(self.mock_llm, self.session)

    def test_lifecycle_and_shutdown(self):
        self.mock_llm.start_server.return_value = True
        
        self.assertTrue(self.orchestrator.startup(15, 8080, 2048))
        self.assertTrue(self.orchestrator.running)
        self.mock_llm.start_server.assert_called_once_with(15, 8080, 2048)
        
        self.orchestrator.shutdown()
        self.assertFalse(self.orchestrator.running)
        self.mock_llm.stop_server.assert_called_once()

    def test_startup_failure(self):
        self.mock_llm.start_server.return_value = False
        self.assertFalse(self.orchestrator.startup(15, 8080, 2048))
        self.assertFalse(self.orchestrator.running)

    def test_fatal_backend_recovery(self):
        self.orchestrator._last_config = {"offload_layers": 15, "port": 8080, "context_size": 2048}
        
        # Mock stop/start for recovery
        self.mock_llm.stop_server = MagicMock()
        self.mock_llm.start_server = MagicMock(return_value=True)
        
        # Recovery should succeed
        self.assertTrue(self.orchestrator._attempt_backend_recovery())
        self.assertEqual(self.orchestrator._current_restarts, 1)
        self.mock_llm.stop_server.assert_called_once()
        self.mock_llm.start_server.assert_called_once_with(offload_layers=15, port=8080, context_size=2048)

if __name__ == '__main__':
    unittest.main()
