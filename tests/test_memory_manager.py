import unittest
import os
import tempfile
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.memory.manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.mktemp(suffix=".db")
        self.manager = MemoryManager(self.temp_db)

    def tearDown(self):
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

    def test_manager_methods(self):
        self.manager.remember("pref", "color", "blue")
        mem = self.manager.recall("pref", "color")
        self.assertEqual(mem.content, "blue")
        
        self.manager.remember("pref", "color", "red")
        mem2 = self.manager.recall("pref", "color")
        self.assertEqual(mem2.content, "red") # Updated
        
        self.assertTrue(self.manager.forget("pref", "color"))
        self.assertIsNone(self.manager.recall("pref", "color"))

    def test_context_formatting(self):
        self.manager.remember("cat1", "k1", "val1")
        self.manager.remember("cat2", "k2", "val2")
        
        mems = self.manager.list_memories()
        formatted = self.manager.format_memories_for_context(mems)
        self.assertIn("<retrieved_memories>", formatted)
        self.assertIn("val1", formatted)
        self.assertIn("val2", formatted)
        self.assertIn("</retrieved_memories>", formatted)

if __name__ == '__main__':
    unittest.main()
