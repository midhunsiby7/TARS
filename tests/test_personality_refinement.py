import unittest
import tempfile
import os
from tars.personality.manager import PersonalityManager

class TestPersonalityRefinement(unittest.TestCase):
    def setUp(self):
        self.id_fd, self.id_path = tempfile.mkstemp()
        self.manager = PersonalityManager(self.id_path)

    def tearDown(self):
        os.close(self.id_fd)
        os.unlink(self.id_path)

    def test_concise_directives(self):
        self.manager.update_profile({"honesty": 100})
        prompt = self.manager.get_personality_prompt()
        self.assertIn("Never knowingly fabricate information", prompt)
        
        self.manager.update_profile({"honesty": 20})
        prompt = self.manager.get_personality_prompt()
        self.assertIn("Be tactful", prompt)
        
    def test_humor_directives(self):
        self.manager.update_profile({"humor": 90})
        prompt = self.manager.get_personality_prompt()
        self.assertIn("Naturally humorous", prompt)

if __name__ == "__main__":
    unittest.main()
