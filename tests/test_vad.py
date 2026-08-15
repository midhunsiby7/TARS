import unittest
import numpy as np
from tars.audio.vad import VAD

class TestVAD(unittest.TestCase):
    def setUp(self):
        self.vad = VAD(energy_threshold=0.01)

    def test_silence(self):
        audio = np.zeros(16000, dtype=np.float32)
        self.assertFalse(self.vad.is_speech(audio))

    def test_speech(self):
        audio = np.ones(16000, dtype=np.float32) * 0.5
        self.assertTrue(self.vad.is_speech(audio))

    def test_empty(self):
        audio = np.array([], dtype=np.float32)
        self.assertFalse(self.vad.is_speech(audio))

if __name__ == '__main__':
    unittest.main()
