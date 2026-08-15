from abc import ABC, abstractmethod
import numpy as np

class WakeWordDetectorInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def listen(self, audio_chunk: np.ndarray) -> bool:
        """Returns True if the wake word is detected in the audio chunk."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
