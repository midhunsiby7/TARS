from enum import Enum, auto

class VoiceState(Enum):
    IDLE = auto()
    WAITING_FOR_WAKE_WORD = auto()
    LISTENING = auto()
    TRANSCRIBING = auto()
    THINKING = auto()
    SPEAKING = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()
