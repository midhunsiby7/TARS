import unittest
from unittest.mock import patch, MagicMock
from tars.voice.wake_word.detector import OpenWakeWordDetector
import numpy as np

class TestWakeWordDetector(unittest.TestCase):
    def setUp(self):
        self.detector = OpenWakeWordDetector(model_name="hey_jarvis", sensitivity=0.5)

    @patch('tars.voice.wake_word.detector.OPENWAKEWORD_AVAILABLE', True)
    @patch('tars.voice.wake_word.detector.Model')
    def test_start_stop(self, mock_model):
        self.assertTrue(self.detector.start())
        self.assertTrue(self.detector._running)
        self.detector.stop()
        self.assertFalse(self.detector._running)

    @patch('tars.voice.wake_word.detector.OPENWAKEWORD_AVAILABLE', True)
    @patch('tars.voice.wake_word.detector.Model')
    def test_listen_detect(self, mock_model):
        mock_instance = MagicMock()
        mock_instance.predict.return_value = {"hey_jarvis": 0.6}
        mock_model.return_value = mock_instance
        
        self.detector.start()
        chunk = np.zeros(100, dtype=np.float32)
        
        self.assertTrue(self.detector.listen(chunk))
        
    @patch('tars.voice.wake_word.detector.OPENWAKEWORD_AVAILABLE', True)
    @patch('tars.voice.wake_word.detector.Model')
    def test_listen_no_detect(self, mock_model):
        mock_instance = MagicMock()
        mock_instance.predict.return_value = {"hey_jarvis": 0.1}
        mock_model.return_value = mock_instance
        
        self.detector.start()
        chunk = np.zeros(100, dtype=np.float32)
        
        self.assertFalse(self.detector.listen(chunk))

if __name__ == '__main__':
    unittest.main()
