import os
import subprocess
import time
from .base import BaseRunner
from hardware.monitor import HardwareMonitor

class TTSRunner(BaseRunner):
    def __init__(self, config_manager, piper_path="piper.exe"):
        super().__init__(config_manager)
        self.executable_path = piper_path
        
    def run_benchmark(self, model_info, text_input, output_wav="output.wav"):
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
                "text_input": text_input
            },
            "system_impact": {},
            "metrics": {}
        }

        # Piper syntax: echo 'text' | piper --model model.onnx --output_file output.wav
        cmd = [
            self.executable_path,
            "--model", model_path,
            "--output_file", output_wav
        ]

        monitor = HardwareMonitor(interval=0.1)
        monitor.start()

        start_time = time.time()
        try:
            process = subprocess.run(
                cmd,
                input=text_input.encode('utf-8'),
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                timeout=120
            )
            latency = time.time() - start_time
            
            if process.returncode == 0:
                results["status"] = "completed"
                results["metrics"]["synthesis_time_seconds"] = latency
                # Ideally, parse stdout for first audio latency or load time if piper outputs it
                results["output_file"] = output_wav
            else:
                results["status"] = "failed"
                results["error"] = process.stderr.decode('utf-8')
        except FileNotFoundError:
            results["status"] = "failed"
            results["error"] = f"Executable not found: {self.executable_path}"
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)

        results["system_impact"] = monitor.stop()
        return results
