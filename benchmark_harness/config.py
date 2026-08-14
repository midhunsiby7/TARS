import json
import os
import hashlib
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODELS_DIR = BASE_DIR / "benchmark_models"
DEFAULT_RESULTS_DIR = BASE_DIR / "benchmark_results"

MODELS_CONFIG_FILE = BASE_DIR / "benchmark_harness" / "models.json"

class ConfigManager:
    def __init__(self, models_dir=None, results_dir=None):
        self.models_dir = Path(models_dir) if models_dir else DEFAULT_MODELS_DIR
        self.results_dir = Path(results_dir) if results_dir else DEFAULT_RESULTS_DIR
        self.models_config = self.load_models_config()

    def load_models_config(self):
        if not MODELS_CONFIG_FILE.exists():
            return {"llm": [], "stt": [], "tts": [], "wakeword": []}
        with open(MODELS_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_model_file_path(self, model_name, quantization=None):
        """Returns the absolute path to a model file, if it exists."""
        # Check LLM models (which use variants)
        for model in self.models_config.get("llm", []):
            if model["name"] == model_name:
                for variant in model.get("variants", []):
                    if quantization is None or variant.get("quantization") == quantization:
                        filename = variant.get("filename")
                        if filename:
                            full_path = self.models_dir / filename
                            if full_path.exists():
                                return str(full_path)
        
        # Check other model types (which have filename at the root)
        for category in ["stt", "tts", "wakeword"]:
            for model in self.models_config.get(category, []):
                if model["name"] == model_name:
                    filename = model.get("filename")
                    if filename:
                        full_path = self.models_dir / filename
                        if full_path.exists():
                            return str(full_path)
        return None

    def validate_llm_model(self, model_info):
        """
        Validates an LLM model before benchmarking:
        - model file exists
        - file is readable
        - format is supported
        """
        filename = model_info.get("filename")
        if not filename:
            return False, "No filename specified in config."
        
        path = self.models_dir / filename
        if not path.exists():
            return False, f"Model file not found: {path}"
        
        if not os.access(path, os.R_OK):
            return False, f"Model file is not readable: {path}"
            
        if path.suffix.lower() not in [".gguf"]:
            return False, f"Unsupported model format: {path.suffix}. Only .gguf is supported for llama.cpp."
            
        return True, "Valid"
        
    @staticmethod
    def calculate_file_hash(filepath, chunk_size=8192):
        """Calculates SHA-256 hash of a file for reproducibility."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"Hash calculation failed: {e}"

    @staticmethod
    def get_file_size(filepath):
        try:
            return os.path.getsize(filepath)
        except OSError:
            return 0
