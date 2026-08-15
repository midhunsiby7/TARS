import os
import platform
import datetime
import subprocess
from typing import Any

from .interface import BaseTool
from .permissions import PermissionCategory

class GetSystemInfoTool(BaseTool):
    @property
    def name(self) -> str: return "get_system_info"
    @property
    def description(self) -> str: return "Returns general information about the operating system and hardware."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        return {
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }

class GetCurrentTimeTool(BaseTool):
    @property
    def name(self) -> str: return "get_current_time"
    @property
    def description(self) -> str: return "Returns the current local date and time."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class GetCpuUsageTool(BaseTool):
    @property
    def name(self) -> str: return "get_cpu_usage"
    @property
    def description(self) -> str: return "Returns the current CPU usage percentage."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        try:
            # Using PowerShell to get CPU usage without needing psutil installed
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "(Get-WmiObject Win32_Processor).LoadPercentage"],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            val = result.stdout.strip()
            # If multiple CPUs, it might return multiple lines, take the first or average
            val = val.split('\n')[0].strip()
            return f"{val}%"
        except Exception:
            return "Unable to determine CPU usage."

class GetMemoryUsageTool(BaseTool):
    @property
    def name(self) -> str: return "get_memory_usage"
    @property
    def description(self) -> str: return "Returns the current RAM usage."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json"],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            import json
            data = json.loads(result.stdout)
            total_mb = int(data["TotalVisibleMemorySize"]) / 1024
            free_mb = int(data["FreePhysicalMemory"]) / 1024
            used_mb = total_mb - free_mb
            return f"Used: {used_mb:.0f} MB / Total: {total_mb:.0f} MB ({(used_mb/total_mb)*100:.1f}%)"
        except Exception:
            return "Unable to determine memory usage."

class GetGpuInfoTool(BaseTool):
    @property
    def name(self) -> str: return "get_gpu_info"
    @property
    def description(self) -> str: return "Returns GPU information and utilization if available."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        try:
            # Simple fallback using nvidia-smi if available
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu", "--format=csv,noheader"],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            return result.stdout.strip()
        except Exception:
            return "Unable to query GPU info (nvidia-smi may not be available)."

class GetDiskUsageTool(BaseTool):
    @property
    def name(self) -> str: return "get_disk_usage"
    @property
    def description(self) -> str: return "Returns disk space usage for a given drive (default 'C:')."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "drive": {
                    "type": "string",
                    "description": "The drive letter to check, e.g. 'C:'"
                }
            }
        }
    
    def _execute(self, drive: str = "C:") -> Any:
        if not drive.endswith(":"):
            drive += ":"
            
        try:
            import shutil
            total, used, free = shutil.disk_usage(f"{drive}\\")
            total_gb = total / (2**30)
            used_gb = used / (2**30)
            free_gb = free / (2**30)
            return f"Drive {drive} - Used: {used_gb:.1f} GB, Free: {free_gb:.1f} GB, Total: {total_gb:.1f} GB"
        except Exception as e:
            return f"Unable to check disk usage for {drive}. Error: {str(e)}"

class GetRunningProcessesTool(BaseTool):
    @property
    def name(self) -> str: return "get_running_processes"
    @property
    def description(self) -> str: return "Returns a short list of top memory-consuming running processes."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, @{Name='Memory(MB)';Expression={[math]::Round($_.WorkingSet/1MB,1)}} | Format-Table -AutoSize"],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            return result.stdout.strip()
        except Exception:
            return "Unable to retrieve running processes."

class GetNetworkInfoTool(BaseTool):
    @property
    def name(self) -> str: return "get_network_info"
    @property
    def description(self) -> str: return "Returns basic network connectivity info (IP addresses)."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict: return {"type": "object", "properties": {}}
    
    def _execute(self) -> Any:
        import socket
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return {"hostname": hostname, "ip_address": ip}
        except Exception:
            return "Unable to determine network info."

class ListDirectoryTool(BaseTool):
    @property
    def name(self) -> str: return "list_directory"
    @property
    def description(self) -> str: return "Lists the contents of a directory."
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.READ_ONLY
    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list. Defaults to current directory."
                }
            }
        }
    
    def _execute(self, path: str = ".") -> Any:
        try:
            items = os.listdir(path)
            return {"path": os.path.abspath(path), "items": items[:50]} # Cap to 50 items to save context
        except Exception as e:
            return f"Error listing directory: {str(e)}"

# Helper function to register all
def register_system_tools(registry):
    tools = [
        GetSystemInfoTool(), GetCurrentTimeTool(), GetCpuUsageTool(),
        GetMemoryUsageTool(), GetGpuInfoTool(), GetDiskUsageTool(),
        GetRunningProcessesTool(), GetNetworkInfoTool(), ListDirectoryTool()
    ]
    for t in tools:
        registry.register(t)
