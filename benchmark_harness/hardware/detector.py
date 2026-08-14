import platform
import psutil
import pynvml
import subprocess

class HardwareDetector:
    """Detects and logs static hardware specifications."""
    
    @staticmethod
    def get_system_specs():
        specs = {
            "os": f"{platform.system()} {platform.release()} ({platform.version()})",
            "cpu_architecture": platform.machine(),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "gpu_info": [],
            "cuda_available": False,
            "cuda_version": None,
            "nvidia_driver": None
        }

        # Attempt to detect NVIDIA GPUs via NVML
        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            specs["nvidia_driver"] = pynvml.nvmlSystemGetDriverVersion()
            
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                specs["gpu_info"].append({
                    "id": i,
                    "name": name if isinstance(name, str) else name.decode('utf-8'),
                    "vram_total_gb": round(mem.total / (1024 ** 3), 2)
                })
            
            pynvml.nvmlShutdown()
        except Exception as e:
            specs["gpu_info"].append({"error": f"NVML not available or failed: {str(e)}"})

        # Check for CUDA via nvcc or nvidia-smi as fallback
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                specs["cuda_available"] = True
                # Very rough parse for CUDA version
                for line in result.stdout.split('\n'):
                    if "CUDA Version:" in line:
                        parts = line.split("CUDA Version:")
                        if len(parts) > 1:
                            specs["cuda_version"] = parts[1].split()[0].strip()
        except FileNotFoundError:
            pass

        return specs

if __name__ == "__main__":
    import json
    print(json.dumps(HardwareDetector.get_system_specs(), indent=2))
