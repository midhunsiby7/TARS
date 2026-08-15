import os
import numpy as np
from typing import Optional
from tars.voice.wake_word.interface import WakeWordDetectorInterface

try:
    from openwakeword.model import Model
    OPENWAKEWORD_AVAILABLE = True
except ImportError:
    OPENWAKEWORD_AVAILABLE = False

class OpenWakeWordDetector(WakeWordDetectorInterface):
    def __init__(self, model_name: str = "hey_jarvis", sensitivity: float = 0.5):
        """
        model_name: The name of the built-in openwakeword model (e.g., 'hey_jarvis', 'alexa')
                    or an absolute path to a custom .onnx model in models/
        """
        self.model_name = model_name
        self.sensitivity = sensitivity
        self.model = None
        self._running = False

    def is_available(self) -> bool:
        return OPENWAKEWORD_AVAILABLE

    def start(self) -> bool:
        if not self.is_available():
            print("[WakeWord] openwakeword is not installed.")
            return False

        if self._running:
            return True

        try:
            print(f"[WakeWord] Initializing OpenWakeWord model: {self.model_name}")
            
            # If the model ends with .onnx or .tflite, we assume it's a custom path
            model_paths = None
            if (self.model_name.endswith(".onnx") or self.model_name.endswith(".tflite")) and os.path.exists(self.model_name):
                model_paths = [self.model_name]
                
            self.model = Model(
                wakeword_models=model_paths if model_paths else [self.model_name]
            )
            self._running = True
            print("[WakeWord] Detector started.")
            return True
        except Exception as e:
            print(f"[WakeWord Fatal] Failed to initialize detector: {e}")
            return False

    def stop(self) -> None:
        self._running = False
        self.model = None

    def listen(self, audio_chunk: np.ndarray) -> bool:
        if not self._running or self.model is None:
            return False

        if len(audio_chunk) == 0:
            return False

        # openwakeword requires 16-bit PCM numpy arrays (int16). 
        # Convert float32 from sounddevice to int16 if necessary.
        if audio_chunk.dtype == np.float32:
            chunk_int16 = (audio_chunk * 32767).astype(np.int16)
        else:
            chunk_int16 = audio_chunk

        try:
            # openwakeword predicts frame-by-frame
            prediction = self.model.predict(chunk_int16)
            
            # Prediction is a dict: {'model_name': score}
            for model, score in prediction.items():
                if score >= self.sensitivity:
                    return True
        except Exception as e:
            print(f"[WakeWord Error] Prediction failed: {e}")

        return False
