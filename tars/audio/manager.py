import sounddevice as sd
import numpy as np
from typing import List, Dict, Optional

class AudioManager:
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.default_device = None

    def list_input_devices(self) -> List[Dict]:
        devices = []
        try:
            for i, dev in enumerate(sd.query_devices()):
                if dev['max_input_channels'] > 0:
                    devices.append({
                        "id": i,
                        "name": dev['name'],
                        "channels": dev['max_input_channels'],
                        "default_samplerate": dev['default_samplerate']
                    })
        except Exception as e:
            print(f"[AudioManager] Failed to list devices: {e}")
        return devices

    def set_input_device(self, device_id: Optional[int]):
        self.default_device = device_id

    def record_chunk(self, duration: float) -> np.ndarray:
        """Records for a specific duration in seconds and returns mono numpy array."""
        try:
            frames = int(duration * self.sample_rate)
            audio = sd.rec(
                frames, 
                samplerate=self.sample_rate, 
                channels=self.channels, 
                dtype='float32',
                device=self.default_device
            )
            sd.wait()
            # If stereo is returned, flatten to mono by averaging
            if self.channels > 1:
                return np.mean(audio, axis=1)
            return audio.flatten()
        except Exception as e:
            print(f"[AudioManager Fatal] Audio capture failed: {e}")
            return np.array([])
