import unittest
from tars.voice.state import VoiceState

class TestVoiceState(unittest.TestCase):
    def test_state_enum(self):
        self.assertEqual(VoiceState.IDLE.name, "IDLE")
        self.assertEqual(VoiceState.LISTENING.name, "LISTENING")
        self.assertEqual(VoiceState.TRANSCRIBING.name, "TRANSCRIBING")
        self.assertEqual(VoiceState.THINKING.name, "THINKING")
        self.assertEqual(VoiceState.SPEAKING.name, "SPEAKING")
        self.assertEqual(VoiceState.ERROR.name, "ERROR")

if __name__ == '__main__':
    unittest.main()
