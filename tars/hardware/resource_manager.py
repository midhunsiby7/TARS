import psutil
import subprocess
import os

class ResourceManager:
    def __init__(self):
        pass

    def get_cpu_usage(self) -> float:
        """Returns current CPU usage percentage."""
        return psutil.cpu_percent(interval=None)

    def get_ram_usage(self) -> dict:
        """Returns RAM usage statistics in MB."""
        mem = psutil.virtual_memory()
        return {
            "total_mb": mem.total / (1024 * 1024),
            "used_mb": mem.used / (1024 * 1024),
            "available_mb": mem.available / (1024 * 1024),
            "percent": mem.percent
        }

    def get_gpu_vram_usage(self) -> dict:
        """
        Attempts to read NVIDIA GPU VRAM usage via nvidia-smi.
        Returns a dict with 'total_mb' and 'used_mb', or None if unavailable.
        """
        try:
            # --query-gpu=memory.total,memory.used --format=csv,nounits,noheader
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total,memory.used", "--format=csv,nounits,noheader"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    # Assuming single GPU for now
                    total, used = lines[0].split(',')
                    return {
                        "total_mb": float(total.strip()),
                        "used_mb": float(used.strip())
                    }
        except Exception:
            pass
        return None
