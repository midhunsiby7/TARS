import unittest
from unittest.mock import patch, MagicMock
from tars.voice.tts.pyttsx3_backend import Pyttsx3TTSBackend, PYTTSX3_AVAILABLE

class TestPyttsx3Backend(unittest.TestCase):
    def setUp(self):
        self.backend = Pyttsx3TTSBackend()

    def test_is_available(self):
        self.assertEqual(self.backend.is_available(), PYTTSX3_AVAILABLE)

    @unittest.skipIf(not PYTTSX3_AVAILABLE, "pyttsx3 not installed")
    @patch('tars.voice.tts.pyttsx3_backend.pyttsx3.init')
    def test_initialize(self, mock_init):
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        self.assertTrue(self.backend.initialize())
        self.assertIsNotNone(self.backend.engine)

    @unittest.skipIf(not PYTTSX3_AVAILABLE, "pyttsx3 not installed")
    @patch('tars.voice.tts.pyttsx3_backend.pyttsx3.init')
    def test_speak_and_stop(self, mock_init):
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        
        self.backend.initialize()
        # Mock speak just calling runAndWait immediately
        self.backend.speak("Test text")
        mock_engine.say.assert_called_with("Test text")
        mock_engine.runAndWait.assert_called_once()
        
        self.backend.stop()
        self.assertFalse(self.backend.is_speaking())

if __name__ == '__main__':
    unittest.main()
