import unittest
import os
import tempfile
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.memory.manager import MemoryManager
from tars.tools.memory_tools import RememberTool, RecallTool, ListMemoriesTool, ForgetTool

class TestMemoryTools(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.mktemp(suffix=".db")
        self.manager = MemoryManager(self.temp_db)

    def tearDown(self):
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

    def test_remember_tool(self):
        tool = RememberTool(self.manager)
        res = tool.execute_validated('{"category": "fact", "key": "sky", "content": "blue"}')
        self.assertTrue(res.success)
        self.assertIn("Successfully stored", res.data)
        
    def test_recall_tool(self):
        self.manager.remember("fact", "sky", "blue")
        tool = RecallTool(self.manager)
        res = tool.execute_validated('{"query": "sky"}')
        self.assertTrue(res.success)
        self.assertIn("blue", res.data)
        
    def test_list_tool(self):
        self.manager.remember("fact", "sky", "blue")
        tool = ListMemoriesTool(self.manager)
        res = tool.execute_validated('{"limit": 10}')
        self.assertTrue(res.success)
        self.assertIn("blue", res.data)
        
    def test_forget_tool(self):
        self.manager.remember("fact", "sky", "blue")
        tool = ForgetTool(self.manager)
        res = tool.execute_validated('{"category": "fact", "key": "sky"}')
        self.assertTrue(res.success)
        self.assertIn("Successfully deleted", res.data)

if __name__ == '__main__':
    unittest.main()
