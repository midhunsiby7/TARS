import sys
import os
import unittest
from unittest.mock import patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.tools.system_tools import GetSystemInfoTool, GetCurrentTimeTool, GetDiskUsageTool
from tars.tools.action_tools import OpenApplicationTool, OpenUrlTool

class TestTools(unittest.TestCase):
    def test_get_system_info(self):
        tool = GetSystemInfoTool()
        result = tool.execute_validated("{}")
        self.assertTrue(result.success)
        self.assertIn("os", result.data)
        
    def test_get_current_time(self):
        tool = GetCurrentTimeTool()
        result = tool.execute_validated("{}")
        self.assertTrue(result.success)
        self.assertIsInstance(result.data, str)
        
    def test_get_disk_usage(self):
        tool = GetDiskUsageTool()
        result = tool.execute_validated('{"drive": "C:"}')
        self.assertTrue(result.success)
        self.assertIn("Free", result.data)
        
    @patch('subprocess.Popen')
    def test_open_application_allowlist(self, mock_popen):
        tool = OpenApplicationTool()
        # Notepad is allowed
        res1 = tool.execute_validated('{"app_name": "notepad"}')
        self.assertTrue(res1.success)
        mock_popen.assert_called_once()
        
        # Fake is blocked
        res2 = tool.execute_validated('{"app_name": "malware"}')
        self.assertTrue(res2.success)
        self.assertIn("not in the approved", res2.data)
        
    @patch('webbrowser.open')
    def test_open_url_validation(self, mock_webbrowser):
        mock_webbrowser.return_value = True
        tool = OpenUrlTool()
        
        # Valid
        res1 = tool.execute_validated('{"url": "https://google.com"}')
        self.assertTrue(res1.success)
        
        # Invalid schema
        res2 = tool.execute_validated('{"url": "file:///C:/windows/system32/cmd.exe"}')
        self.assertTrue(res2.success)
        self.assertIn("Error", res2.data)
        
if __name__ == '__main__':
    unittest.main()
