import unittest
from unittest.mock import patch
from tars.hardware.resource_manager import ResourceManager

class TestResourceManager(unittest.TestCase):
    def setUp(self):
        self.manager = ResourceManager()

    @patch('tars.hardware.resource_manager.psutil.cpu_percent')
    def test_get_cpu_usage(self, mock_cpu):
        mock_cpu.return_value = 15.5
        self.assertEqual(self.manager.get_cpu_usage(), 15.5)

    @patch('tars.hardware.resource_manager.psutil.virtual_memory')
    def test_get_ram_usage(self, mock_mem):
        class MemMock:
            total = 8 * 1024 * 1024 * 1024
            used = 4 * 1024 * 1024 * 1024
            available = 4 * 1024 * 1024 * 1024
            percent = 50.0
        mock_mem.return_value = MemMock()
        
        usage = self.manager.get_ram_usage()
        self.assertEqual(usage["total_mb"], 8192.0)
        self.assertEqual(usage["percent"], 50.0)

if __name__ == '__main__':
    unittest.main()
