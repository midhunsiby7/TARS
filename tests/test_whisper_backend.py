import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from tars.voice.stt.whisper_backend import WhisperSTTBackend, WHISPER_AVAILABLE

class TestWhisperBackend(unittest.TestCase):
    def setUp(self):
        self.backend = WhisperSTTBackend(device="cpu")

    def test_is_available(self):
        self.assertEqual(self.backend.is_available(), WHISPER_AVAILABLE)

    @unittest.skipIf(not WHISPER_AVAILABLE, "faster-whisper not installed")
    @patch('tars.voice.stt.whisper_backend.WhisperModel')
    def test_initialize(self, MockWhisperModel):
        self.assertTrue(self.backend.initialize())
        self.assertTrue(self.backend._initialized)
        self.assertIsNotNone(self.backend.model)

    @unittest.skipIf(not WHISPER_AVAILABLE, "faster-whisper not installed")
    @patch('tars.voice.stt.whisper_backend.WhisperModel')
    def test_transcribe(self, MockWhisperModel):
        mock_model = MagicMock()
        mock_segment = MagicMock()
        mock_segment.text = "Hello world"
        mock_model.transcribe.return_value = ([mock_segment], None)
        MockWhisperModel.return_value = mock_model
        
        audio = np.zeros(16000, dtype=np.float32)
        text = self.backend.transcribe(audio)
        self.assertEqual(text, "Hello world")

if __name__ == '__main__':
    unittest.main()
