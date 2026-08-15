import unittest
import tempfile
import os
from datetime import datetime, timedelta
from tars.memory.manager import MemoryManager

class TestMemoryRanking(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.config = {
            "ranking_weights": {
                "lexical_relevance": 1.0,
                "importance": 2.0,
                "recency": 1.5,
                "category_match": 1.0
            }
        }
        self.manager = MemoryManager(self.db_path, config=self.config)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_ranking_by_lexical_relevance(self):
        # Create memories with varying lexical relevance
        self.manager.remember("info", "dog", "The dog is brown", importance=0.5)
        self.manager.remember("info", "cat", "The cat is black", importance=0.5)
        
        # Searching for 'dog' should rank the dog memory higher
        results = self.manager.retrieve_relevant_memories(query="dog")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0].key, "dog")

    def test_ranking_by_importance(self):
        # Both match lexically (neither matches the query well, or both match equally if query is generic)
        self.manager.remember("fact", "fact1", "Water is wet", importance=0.1)
        self.manager.remember("fact", "fact2", "Water is a liquid", importance=0.9)
        
        results = self.manager.retrieve_relevant_memories(query="water")
        self.assertTrue(len(results) == 2)
        self.assertEqual(results[0].key, "fact2") # High importance ranks first

    def test_ranking_by_recency(self):
        # Create an old memory manually
        m1 = self.manager.remember("fact", "fact_old", "Python is a language", importance=0.5)
        # Hack the date to be 20 days old
        old_date = datetime.now() - timedelta(days=20)
        conn = self.manager.storage._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE memories SET updated_at = ? WHERE key = ?", (old_date, "fact_old"))
        conn.commit()
        conn.close()
        
        self.manager.remember("fact", "fact_new", "Python is popular", importance=0.5)
        
        results = self.manager.retrieve_relevant_memories(query="python")
        self.assertTrue(len(results) == 2)
        self.assertEqual(results[0].key, "fact_new") # More recent ranks first

if __name__ == "__main__":
    unittest.main()
