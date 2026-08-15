import threading
from typing import Optional
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

class Pyttsx3TTSBackend:
    def __init__(self, rate: int = 150, volume: float = 1.0):
        self.rate = rate
        self.volume = volume
        self.engine = None
        self._is_speaking = False
        self._interrupted = False
        self._lock = threading.Lock()

    def is_available(self) -> bool:
        return PYTTSX3_AVAILABLE

    def initialize(self) -> bool:
        if not self.is_available():
            print("[Pyttsx3TTS] pyttsx3 is not installed.")
            return False
            
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Setup interrupt hook
            def on_word(name, location, length):
                if self._interrupted:
                    self.engine.stop()
                    
            self.engine.connect('started-word', on_word)
            return True
        except Exception as e:
            print(f"[Pyttsx3TTS Fatal] Initialization failed: {e}")
            return False

    def is_speaking(self) -> bool:
        return self._is_speaking

    def speak(self, text: str):
        if not self.engine and not self.initialize():
            return
            
        with self._lock:
            self._is_speaking = True
            self._interrupted = False
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[Pyttsx3TTS Error] Synthesis failed: {e}")
        finally:
            with self._lock:
                self._is_speaking = False
                self._interrupted = False

    def stop(self):
        """Interrupts current speech."""
        with self._lock:
            if self._is_speaking:
                self._interrupted = True
