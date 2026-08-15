import numpy as np

class VAD:
    def __init__(self, energy_threshold: float = 0.01):
        self.energy_threshold = energy_threshold

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """
        Simple RMS energy-based voice activity detection.
        Returns True if the RMS energy exceeds the threshold.
        """
        if len(audio_chunk) == 0:
            return False
            
        # Calculate Root Mean Square energy
        rms = np.sqrt(np.mean(np.square(audio_chunk)))
        return rms > self.energy_threshold
