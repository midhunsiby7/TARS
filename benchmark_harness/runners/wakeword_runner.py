import time
import os
import openwakeword
from openwakeword.model import Model
import numpy as np
import soundfile as sf
from .base import BaseRunner
from hardware.monitor import HardwareMonitor

class WakeWordRunner(BaseRunner):
    def __init__(self, config_manager):
        super().__init__(config_manager)
        
    def run_benchmark(self, model_info, wav_path):
        model_path = self.config.get_model_file_path(model_info.get("name"))
        if not model_path:
            return {"error": "Model path not resolved.", "status": "failed"}

        results = {
            "metadata": {
                "model_name": model_info.get("name"),
                "model_path": model_path,
                "wav_file": wav_path
            },
            "system_impact": {},
            "metrics": {}
        }

        if not os.path.exists(wav_path):
            return {"error": f"WAV file not found: {wav_path}", "status": "failed"}

        try:
            audio_data, samplerate = sf.read(wav_path, dtype='int16')
            if samplerate != 16000:
                return {"error": f"Audio must be 16000 Hz, got {samplerate}", "status": "failed"}
                
            # If stereo, convert to mono
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]
                
        except Exception as e:
            return {"error": f"Audio reading failed: {str(e)}", "status": "failed"}

        monitor = HardwareMonitor(interval=0.05)
        monitor.start()

        start_time = time.time()
        try:
            # openWakeWord downloads model by default if it's a string, but here we pass the exact path.
            # openWakeWord 0.6.0 allows `model_paths=[path]`
            oww_model = Model(wakeword_models=[model_path], inference_framework="onnx")
            results["metrics"]["load_time_seconds"] = time.time() - start_time
            
            # Predict
            chunk_size = 1280 # 80 ms at 16000 Hz
            detections = []
            process_start = time.time()
            
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i+chunk_size]
                if len(chunk) < chunk_size:
                    chunk = np.pad(chunk, (0, chunk_size - len(chunk)), 'constant')
                    
                prediction = oww_model.predict(chunk)
                # prediction is a dict mapping model name to score
                for mw, score in prediction.items():
                    if score > 0.5:
                        detections.append((i / 16000.0, score))
                        
            process_end = time.time()
            results["metrics"]["processing_latency_seconds"] = process_end - process_start
            results["metrics"]["detections"] = len(detections)
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)

        results["system_impact"] = monitor.stop()
        return results
