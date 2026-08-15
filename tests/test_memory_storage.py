import unittest
import os
import tempfile
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.memory.storage import MemoryStorage

class TestMemoryStorage(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.mktemp(suffix=".db")
        self.storage = MemoryStorage(self.temp_db)

    def tearDown(self):
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

    def test_create_and_read(self):
        self.storage.create("pref", "lang", "Python", 0.9)
        mem = self.storage.read("pref", "lang")
        self.assertIsNotNone(mem)
        self.assertEqual(mem.content, "Python")
        self.assertEqual(mem.importance, 0.9)

    def test_update(self):
        self.storage.create("pref", "lang", "Python")
        self.storage.update("pref", "lang", "Rust", 0.8)
        mem = self.storage.read("pref", "lang")
        self.assertEqual(mem.content, "Rust")
        self.assertEqual(mem.importance, 0.8)

    def test_delete(self):
        self.storage.create("pref", "lang", "Python")
        self.assertTrue(self.storage.delete("pref", "lang"))
        self.assertIsNone(self.storage.read("pref", "lang"))
        self.assertFalse(self.storage.delete("pref", "lang"))

    def test_search(self):
        self.storage.create("pref", "lang1", "Python")
        self.storage.create("pref", "lang2", "Rust")
        self.storage.create("fact", "lang3", "Python is snake")
        
        mems = self.storage.search(query="Python")
        self.assertEqual(len(mems), 2)
        
        mems_cat = self.storage.search(query="Python", category="pref")
        self.assertEqual(len(mems_cat), 1)

    def test_sql_injection_defense(self):
        # We try to use a malicious category string
        malicious = "pref'; DROP TABLE memories;--"
        self.storage.create(malicious, "lang", "Python")
        # Should just be a normal row
        mems = self.storage.list_all()
        self.assertTrue(any(m.category == malicious for m in mems))

if __name__ == '__main__':
    unittest.main()
