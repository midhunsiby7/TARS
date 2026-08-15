import time
import sys
from typing import Optional

from tars.audio.manager import AudioManager
from tars.audio.vad import VAD
from tars.voice.stt.whisper_backend import WhisperSTTBackend
from tars.voice.tts.pyttsx3_backend import Pyttsx3TTSBackend
from tars.voice.state import VoiceState
from tars.core.orchestrator import TarsOrchestrator

class VoiceController:
    def __init__(self, orchestrator: TarsOrchestrator, config: dict):
        self.orchestrator = orchestrator
        self.config = config
        self.state = VoiceState.IDLE
        
        self.audio = AudioManager(
            sample_rate=config.get("sample_rate", 16000),
            channels=config.get("channels", 1)
        )
        self.vad = VAD(energy_threshold=config.get("silence_threshold", 0.01))
        
        self.stt = WhisperSTTBackend(
            model_size=config.get("stt_model", "tiny.en"),
            device=config.get("stt_device", "cpu")
        )
        
        self.tts = Pyttsx3TTSBackend(
            rate=config.get("tts_rate", 150),
            volume=config.get("tts_volume", 1.0)
        )
        
    def _transition(self, new_state: VoiceState):
        self.state = new_state
        print(f"[Voice] State -> {self.state.name}")
        
    def start_manual_loop(self):
        """Push-to-talk loop as per Phase 2D requirements."""
        print("\n" + "="*50)
        print("TARS Voice Mode (Phase 2D - Manual Activation)")
        print("Press ENTER to speak. Type 'exit' to quit.")
        print("="*50 + "\n")
        
        # Pre-initialize models to avoid delay on first voice interaction
        if not self.stt.initialize():
            print("[Voice Fatal] STT failed to initialize. Voice mode unavailable.")
            return
        if not self.tts.initialize():
            print("[Voice Fatal] TTS failed to initialize. Voice mode unavailable.")
            return
            
        while self.orchestrator.running:
            self._transition(VoiceState.IDLE)
            try:
                user_input = input("\n[Press ENTER to start recording, or type 'exit']: ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    self.orchestrator.running = False
                    break
            except (KeyboardInterrupt, EOFError):
                self.orchestrator.running = False
                break
                
            self._process_single_utterance()
            
    def _process_single_utterance(self):
        self._transition(VoiceState.LISTENING)
        print("Recording... (Speak now, auto-stops after silence)")
        
        # A simple recording loop that stops after silence
        chunk_duration = 0.5
        max_duration = self.config.get("max_recording_seconds", 10.0)
        silence_duration_limit = self.config.get("silence_duration", 1.5)
        
        audio_chunks = []
        silence_accumulated = 0.0
        speech_started = False
        
        # Record until silence threshold met after speech started, or max duration
        for _ in range(int(max_duration / chunk_duration)):
            chunk = self.audio.record_chunk(chunk_duration)
            if len(chunk) == 0:
                break
                
            audio_chunks.append(chunk)
            
            is_speech = self.vad.is_speech(chunk)
            if is_speech:
                speech_started = True
                silence_accumulated = 0.0
            elif speech_started:
                silence_accumulated += chunk_duration
                
            if speech_started and silence_accumulated >= silence_duration_limit:
                break
                
        if not audio_chunks:
            print("[Voice] No audio captured.")
            return
            
        # Import numpy here just for concatenation
        import numpy as np
        full_audio = np.concatenate(audio_chunks)
        
        self._transition(VoiceState.TRANSCRIBING)
        transcription = self.stt.transcribe(full_audio, self.audio.sample_rate)
        
        if not transcription:
            print("[Voice] Could not transcribe audio.")
            return
            
        print(f"\nUser (Voice): {transcription}")
        
        self._transition(VoiceState.THINKING)
        
        # Pass to orchestrator identically to text input
        self.orchestrator.session.add_user_message(transcription)
        if not self.orchestrator._execute_agent_loop():
            self._transition(VoiceState.ERROR)
            return
            
        # Get the assistant's text response for TTS
        response_text = self._get_last_assistant_response()
        
        if response_text:
            self._transition(VoiceState.SPEAKING)
            self.tts.speak(response_text)
            
    def _get_last_assistant_response(self) -> Optional[str]:
        messages = self.orchestrator.session.get_messages()
        for msg in reversed(messages):
            if msg["role"] == "assistant" and msg.get("content"):
                return msg["content"]
        return None
