import sys
import os
import unittest
from unittest.mock import patch, MagicMock

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.llm.llama_backend import LlamaBackend

class TestLlamaBackend(unittest.TestCase):
    def setUp(self):
        self.backend = LlamaBackend("fake_exe.exe", "fake_model.gguf")

    @patch('os.path.exists')
    def test_missing_executable_or_model(self, mock_exists):
        mock_exists.side_effect = lambda path: False
        self.assertFalse(self.backend.start_server(15, 8080, 2048))
        
    @patch('os.path.exists')
    @patch('tars.llm.llama_backend.LlamaBackend._is_port_in_use')
    @patch('subprocess.Popen')
    @patch('tars.llm.llama_backend.LlamaBackend.is_healthy')
    def test_server_startup_success(self, mock_healthy, mock_popen, mock_port, mock_exists):
        mock_exists.return_value = True
        mock_port.return_value = False
        mock_healthy.return_value = True
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        self.assertTrue(self.backend.start_server(15, 8080, 2048))
        mock_popen.assert_called_once()
        self.assertEqual(self.backend.process, mock_process)

    @patch('os.path.exists')
    @patch('tars.llm.llama_backend.LlamaBackend._is_port_in_use')
    @patch('subprocess.Popen')
    @patch('tars.llm.llama_backend.LlamaBackend.is_healthy')
    def test_server_startup_health_failure(self, mock_healthy, mock_popen, mock_port, mock_exists):
        mock_exists.return_value = True
        mock_port.return_value = False
        mock_healthy.return_value = False
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Test will timeout after 60s, so we mock time.time in the method or just mock the while loop via side effect?
        # A bit tricky to mock time, let's use a patch on time.time.
        with patch('time.time', side_effect=[0, 1, 62]):
            with patch('time.sleep'):
                self.assertFalse(self.backend.start_server(15, 8080, 2048))
                
    def test_shutdown_terminate_then_kill(self):
        mock_process = MagicMock()
        self.backend.process = mock_process
        self.backend.process.poll.return_value = None # Process is running
        
        # Simulate timeout on wait
        import subprocess
        self.backend.process.wait.side_effect = [subprocess.TimeoutExpired(cmd="fake", timeout=5), None]
        
        self.backend.stop_server()
        
        mock_process.terminate.assert_called_once()
        mock_process.kill.assert_called_once()

    @patch('requests.post')
    def test_successful_request(self, mock_post):
        self.backend.process = MagicMock()
        self.backend.process.poll.return_value = None
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
        mock_post.return_value = mock_response
        
        with patch.object(self.backend, 'is_healthy', return_value=True):
            result = self.backend.generate([{"role": "user", "content": "hi"}])
            
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content"], "Test response")
        self.assertFalse(result["fatal"])

    @patch('requests.post')
    def test_request_timeout(self, mock_post):
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Timeout")
        
        with patch.object(self.backend, 'is_healthy', return_value=True):
            result = self.backend.generate([{"role": "user", "content": "hi"}])
            
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["fatal"]) # Timeout is not fatal

if __name__ == '__main__':
    unittest.main()
