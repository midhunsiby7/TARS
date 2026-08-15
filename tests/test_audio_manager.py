import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from tars.audio.manager import AudioManager

class TestAudioManager(unittest.TestCase):
    def setUp(self):
        self.manager = AudioManager(sample_rate=16000, channels=1)

    @patch('tars.audio.manager.sd.query_devices')
    def test_list_input_devices(self, mock_query):
        mock_query.return_value = [
            {'name': 'Mic 1', 'max_input_channels': 2, 'default_samplerate': 44100},
            {'name': 'Speaker', 'max_input_channels': 0, 'default_samplerate': 44100}
        ]
        devices = self.manager.list_input_devices()
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['name'], 'Mic 1')

    @patch('tars.audio.manager.sd.rec')
    @patch('tars.audio.manager.sd.wait')
    def test_record_chunk(self, mock_wait, mock_rec):
        mock_rec.return_value = np.zeros((8000, 1), dtype=np.float32)
        chunk = self.manager.record_chunk(0.5)
        self.assertEqual(len(chunk), 8000)
        self.assertEqual(chunk.ndim, 1)

if __name__ == '__main__':
    unittest.main()
