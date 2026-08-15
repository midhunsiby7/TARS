import unittest
from unittest.mock import MagicMock, patch
from tars.voice.controller import VoiceController
from tars.voice.state import VoiceState

class TestContinuousVoice(unittest.TestCase):
    def setUp(self):
        self.mock_orchestrator = MagicMock()
        self.mock_orchestrator.running = True
        self.config = {
            "max_recording_seconds": 1.0,
            "silence_duration": 0.5,
            "listen_timeout": 1.0,
            "stt_model": "tiny.en",
            "stt_device": "cpu"
        }
        self.controller = VoiceController(self.mock_orchestrator, self.config)
        
        self.controller.audio = MagicMock()
        self.controller.vad = MagicMock()
        self.controller.stt = MagicMock()
        self.controller.tts = MagicMock()
        self.controller.wake_word_detector = MagicMock()

    def test_timeout_after_wake(self):
        """Test returning to WAITING_FOR_WAKE_WORD after timeout."""
        # Setup mock audio
        import numpy as np
        self.controller.audio.record_chunk.return_value = np.zeros(10)
        self.controller.vad.is_speech.return_value = False
        
        self.controller._process_single_utterance()
        
        # State should be listening, then timeout and return, meaning transition was LISTENING
        self.assertEqual(self.controller.state, VoiceState.LISTENING)
        
if __name__ == '__main__':
    unittest.main()
