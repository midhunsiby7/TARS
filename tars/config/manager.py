import json
import os
from typing import Dict, Any

class RuntimeConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {
            "production_gpu_layers": 28,
            "fallback_gpu_layers": 15,
            "context_size": 2048,
            "server_port": 8080,
            "selected_model": "Qwen3-4B",
            "db_path": "data/tars/memory.db"
        }
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            self.config["voice"] = {
                "enabled": True,
                "sample_rate": 16000,
                "channels": 1,
                "silence_threshold": 0.01,
                "silence_duration": 1.5,
                "max_recording_seconds": 10.0,
                "stt_model": "tiny.en",
                "stt_device": "cpu",
                "tts_enabled": True,
                "tts_rate": 150,
                "tts_volume": 1.0
            }
            self._save_config()
            return

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                
            # Validation
            if isinstance(data.get("production_gpu_layers"), int) and data["production_gpu_layers"] >= 0:
                self.config["production_gpu_layers"] = data["production_gpu_layers"]
            
            if isinstance(data.get("fallback_gpu_layers"), int) and data["fallback_gpu_layers"] >= 0:
                self.config["fallback_gpu_layers"] = data["fallback_gpu_layers"]
                
            if isinstance(data.get("context_size"), int) and data["context_size"] > 0:
                self.config["context_size"] = data["context_size"]
                
            if isinstance(data.get("server_port"), int) and 1 <= data["server_port"] <= 65535:
                self.config["server_port"] = data["server_port"]
                
            if isinstance(data.get("selected_model"), str) and data["selected_model"]:
                self.config["selected_model"] = data["selected_model"]
                
            if isinstance(data.get("db_path"), str) and data["db_path"]:
                self.config["db_path"] = data["db_path"]

            self.config["voice"] = data.get("voice", {
                "enabled": True,
                "sample_rate": 16000,
                "channels": 1,
                "silence_threshold": 0.01,
                "silence_duration": 1.5,
                "max_recording_seconds": 10.0,
                "stt_model": "tiny.en",
                "stt_device": "cpu",
                "tts_enabled": True,
                "tts_rate": 150,
                "tts_volume": 1.0
            })

        except Exception as e:
            print(f"[Warning] Failed to load {self.config_path}. Using safe defaults. Error: {e}")

    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[Warning] Failed to save {self.config_path}. Error: {e}")

    @property
    def production_gpu_layers(self) -> int: return self.config["production_gpu_layers"]
    @property
    def fallback_gpu_layers(self) -> int: return self.config["fallback_gpu_layers"]
    @property
    def context_size(self) -> int: return self.config["context_size"]
    @property
    def server_port(self) -> int: return self.config["server_port"]
    @property
    def selected_model(self) -> str: return self.config["selected_model"]
    @property
    def db_path(self) -> str: return self.config["db_path"]
    @property
    def voice_config(self) -> dict: return self.config.get("voice", {})
