import time
import threading
import psutil
import pynvml

class HardwareMonitor:
    """Live resource tracking for CPU, RAM, and VRAM."""
    
    def __init__(self, interval=0.5):
        self.interval = interval
        self.is_monitoring = False
        self.thread = None
        self.samples = []
        
        # Check if NVML is available
        self.nvml_available = False
        try:
            pynvml.nvmlInit()
            self.nvml_available = True
        except Exception:
            self.nvml_available = False

    def start(self):
        self.samples = []
        self.is_monitoring = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_monitoring = False
        if self.thread:
            self.thread.join()
        
        # Compile results
        if not self.samples:
            return {}

        cpu_usages = [s["cpu_percent"] for s in self.samples]
        ram_usages = [s["ram_used_gb"] for s in self.samples]
        
        summary = {
            "duration_seconds": len(self.samples) * self.interval,
            "samples_count": len(self.samples),
            "cpu": {
                "min_percent": min(cpu_usages),
                "max_percent": max(cpu_usages),
                "avg_percent": sum(cpu_usages) / len(cpu_usages)
            },
            "ram": {
                "min_gb": min(ram_usages),
                "max_gb": max(ram_usages),
                "avg_gb": sum(ram_usages) / len(ram_usages)
            }
        }
        
        if self.nvml_available and "gpu_util_percent" in self.samples[0]:
            gpu_utils = [s["gpu_util_percent"] for s in self.samples if s.get("gpu_util_percent") is not None]
            vram_usages = [s["vram_used_gb"] for s in self.samples if s.get("vram_used_gb") is not None]
            
            if gpu_utils and vram_usages:
                summary["gpu"] = {
                    "min_util_percent": min(gpu_utils),
                    "max_util_percent": max(gpu_utils),
                    "avg_util_percent": sum(gpu_utils) / len(gpu_utils),
                    "vram_min_gb": min(vram_usages),
                    "vram_max_gb": max(vram_usages),
                    "vram_avg_gb": sum(vram_usages) / len(vram_usages)
                }
                
        return summary

    def _monitor_loop(self):
        while self.is_monitoring:
            sample = {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "ram_used_gb": psutil.virtual_memory().used / (1024 ** 3)
            }
            
            if self.nvml_available:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    sample["gpu_util_percent"] = util.gpu
                    sample["vram_used_gb"] = mem.used / (1024 ** 3)
                except Exception:
                    pass
            
            self.samples.append(sample)
            time.sleep(self.interval)

    def __del__(self):
        if self.nvml_available:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
