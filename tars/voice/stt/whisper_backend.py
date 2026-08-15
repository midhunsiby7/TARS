import os
from typing import Optional
import numpy as np
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

class WhisperSTTBackend:
    def __init__(self, model_size: str = "tiny.en", model_dir: str = "models", device: str = "cpu"):
        self.model_size = model_size
        self.model_dir = model_dir
        self.device = device
        self.model = None
        self._initialized = False

    def is_available(self) -> bool:
        return WHISPER_AVAILABLE

    def initialize(self) -> bool:
        """Loads the Whisper model into memory (CPU by default)."""
        if not self.is_available():
            print("[WhisperSTT] faster-whisper is not installed.")
            return False
            
        if self._initialized:
            return True
            
        print(f"[WhisperSTT] Loading {self.model_size} model on {self.device}...")
        try:
            # Setting download_root ensures models download locally instead of hidden cache
            os.makedirs(self.model_dir, exist_ok=True)
            self.model = WhisperModel(
                self.model_size, 
                device=self.device, 
                compute_type="int8" if self.device == "cpu" else "float16",
                download_root=self.model_dir
            )
            self._initialized = True
            print("[WhisperSTT] Model loaded successfully.")
            return True
        except Exception as e:
            print(f"[WhisperSTT Fatal] Failed to initialize model: {e}")
            return False

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcribes the raw audio array to text."""
        if not self._initialized:
            if not self.initialize():
                return ""
                
        if len(audio) == 0:
            return ""
            
        try:
            segments, info = self.model.transcribe(audio, beam_size=1)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"[WhisperSTT Error] Transcription failed: {e}")
            return ""
