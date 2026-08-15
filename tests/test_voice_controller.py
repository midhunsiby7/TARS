import unittest
from unittest.mock import MagicMock, patch
from tars.voice.controller import VoiceController
from tars.voice.state import VoiceState

class TestVoiceController(unittest.TestCase):
    def setUp(self):
        self.mock_orchestrator = MagicMock()
        self.mock_orchestrator.running = True
        self.config = {
            "max_recording_seconds": 1.0,
            "silence_duration": 0.5,
            "stt_model": "tiny.en",
            "stt_device": "cpu"
        }
        self.controller = VoiceController(self.mock_orchestrator, self.config)
        
        # Mock dependencies
        self.controller.audio = MagicMock()
        self.controller.vad = MagicMock()
        self.controller.stt = MagicMock()
        self.controller.tts = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.controller.state, VoiceState.IDLE)
        self.assertIsNotNone(self.controller.audio)
        
    @patch('tars.voice.controller.input', return_value='exit')
    def test_manual_loop_exit(self, mock_input):
        self.controller.stt.initialize.return_value = True
        self.controller.tts.initialize.return_value = True
        self.controller.start_manual_loop()
        self.assertFalse(self.mock_orchestrator.running)

    def test_process_utterance_empty_audio(self):
        self.controller.audio.record_chunk.return_value = []
        self.controller._process_single_utterance()
        # Should transition to listening and then return
        self.assertEqual(self.controller.state, VoiceState.LISTENING)

if __name__ == '__main__':
    unittest.main()
