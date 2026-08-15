import unittest
import os
import tempfile
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.personality.profile import PersonalityProfile
from tars.personality.manager import PersonalityManager

class TestPersonality(unittest.TestCase):
    def setUp(self):
        self.temp_id = tempfile.mktemp(suffix=".json")
        self.manager = PersonalityManager(self.temp_id)

    def tearDown(self):
        if os.path.exists(self.temp_id):
            os.remove(self.temp_id)

    def test_profile_clamping(self):
        p = PersonalityProfile(humor=-10, honesty=150)
        self.assertEqual(p.humor, 0)
        self.assertEqual(p.honesty, 100)

    def test_manager_persistence(self):
        self.manager.update_profile({"humor": 95, "verbosity": 15})
        
        # Reload
        manager2 = PersonalityManager(self.temp_id)
        self.assertEqual(manager2.profile.humor, 95)
        self.assertEqual(manager2.profile.verbosity, 15)

    def test_invalid_updates(self):
        self.manager.update_profile({"invalid_key": 50, "humor": "abc"})
        self.assertEqual(self.manager.profile.humor, 50) # Fallback to 50 on invalid type

    def test_prompt_generation(self):
        self.manager.update_profile({"humor": 90, "honesty": 90})
        prompt = self.manager.get_personality_prompt()
        self.assertIn("Humor:", prompt)
        self.assertIn("Directness:", prompt)

if __name__ == '__main__':
    unittest.main()
