import unittest
import os
import tempfile
import json
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.config.manager import RuntimeConfigManager

class TestRuntimeConfig(unittest.TestCase):
    def setUp(self):
        self.temp_conf = tempfile.mktemp(suffix=".json")

    def tearDown(self):
        if os.path.exists(self.temp_conf):
            os.remove(self.temp_conf)

    def test_defaults(self):
        manager = RuntimeConfigManager(self.temp_conf)
        self.assertEqual(manager.production_gpu_layers, 28)
        self.assertEqual(manager.server_port, 8080)

    def test_valid_load(self):
        with open(self.temp_conf, "w") as f:
            json.dump({"production_gpu_layers": 30, "server_port": 8081}, f)
            
        manager = RuntimeConfigManager(self.temp_conf)
        self.assertEqual(manager.production_gpu_layers, 30)
        self.assertEqual(manager.server_port, 8081)

    def test_invalid_load(self):
        with open(self.temp_conf, "w") as f:
            json.dump({"production_gpu_layers": -5, "server_port": 999999}, f)
            
        manager = RuntimeConfigManager(self.temp_conf)
        # Should fallback to defaults
        self.assertEqual(manager.production_gpu_layers, 28)
        self.assertEqual(manager.server_port, 8080)

if __name__ == '__main__':
    unittest.main()
