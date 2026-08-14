import os
import subprocess
import time
import json
from .base import BaseRunner
from hardware.monitor import HardwareMonitor

class STTRunner(BaseRunner):
    def __init__(self, config_manager, whisper_path="main.exe"):
        super().__init__(config_manager)
        self.executable_path = whisper_path
        
    def run_benchmark(self, model_info, wav_path, reference_text=None):
        model_path = self.config.get_model_file_path(model_info.get("name"))
        if not model_path:
            return {"error": "Model path not resolved.", "status": "failed"}

        # Gather metadata
        file_size = self.config.get_file_size(model_path)
        file_hash = self.config.calculate_file_hash(model_path)
        
        results = {
            "metadata": {
                "model_name": model_info.get("name"),
                "model_path": model_path,
                "file_size_bytes": file_size,
                "sha256": file_hash,
                "wav_file": wav_path
            },
            "system_impact": {},
            "metrics": {},
            "transcription": ""
        }

        if not os.path.exists(wav_path):
            return {"error": f"WAV file not found: {wav_path}", "status": "failed"}

        cmd = [
            self.executable_path,
            "-m", model_path,
            "-f", wav_path,
            "-nt" # Do not print timestamps
        ]

        monitor = HardwareMonitor(interval=0.2)
        monitor.start()

        start_time = time.time()
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                timeout=120
            )
            latency = time.time() - start_time
            
            if process.returncode == 0:
                results["status"] = "completed"
                # Strip stdout for transcription
                results["transcription"] = process.stdout.strip()
                results["metrics"]["latency_seconds"] = latency
                
                # Basic Word Error Rate if reference provided
                if reference_text:
                    ref_words = reference_text.lower().split()
                    hyp_words = results["transcription"].lower().split()
                    
                    # Simple Levenshtein distance based WER calculation
                    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
                    for i in range(len(ref_words) + 1):
                        d[i][0] = i
                    for j in range(len(hyp_words) + 1):
                        d[0][j] = j
                        
                    for i in range(1, len(ref_words) + 1):
                        for j in range(1, len(hyp_words) + 1):
                            if ref_words[i - 1] == hyp_words[j - 1]:
                                d[i][j] = d[i - 1][j - 1]
                            else:
                                d[i][j] = min(
                                    d[i - 1][j] + 1,      # deletion
                                    d[i][j - 1] + 1,      # insertion
                                    d[i - 1][j - 1] + 1   # substitution
                                )
                    
                    if len(ref_words) > 0:
                        wer = d[len(ref_words)][len(hyp_words)] / len(ref_words)
                    else:
                        wer = 1.0
                    results["metrics"]["wer"] = wer
            else:
                results["status"] = "failed"
                results["error"] = process.stderr
        except FileNotFoundError:
            results["status"] = "failed"
            results["error"] = f"Executable not found: {self.executable_path}"
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)

        results["system_impact"] = monitor.stop()
        return results
