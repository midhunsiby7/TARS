import sys
import os
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from benchmark_harness.config import ConfigManager

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = ConfigManager()
        
    def test_config_loads(self):
        # The models.json should be readable
        self.assertIn("llm", self.config.models_config)
        
    def test_model_validation(self):
        # We know Qwen3-4B is in the config and models dir
        model_path = self.config.get_model_file_path("Qwen3-4B", "Q4_K_M")
        
        # It should either be a string or None if not downloaded.
        # But we know it's downloaded on this machine.
        self.assertIsNotNone(model_path)
        self.assertTrue(model_path.endswith(".gguf"))
        
        # Test missing model
        missing_path = self.config.get_model_file_path("NonExistentModel", "Q4_K_M")
        self.assertIsNone(missing_path)

if __name__ == '__main__':
    unittest.main()
