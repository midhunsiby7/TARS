import os
import sys
import subprocess
import time
import socket
import atexit
import requests
import json
from typing import Dict, List, Optional, Any

from .interface import LLMInterface

class LlamaBackend(LLMInterface):
    """Production backend for llama-server.exe in TARS Phase 2A."""
    
    def __init__(self, executable_path: str, model_path: str):
        self.executable_path = executable_path
        self.model_path = model_path
        self.port = 8080
        self.base_url = ""
        self.process = None
        
        # Register atexit handler to prevent orphaned processes if Python crashes
        atexit.register(self._emergency_cleanup)

    def _is_port_in_use(self, port: int) -> bool:
        """Check if the port is already bound."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def start_server(self, offload_layers: int, port: int, context_size: int) -> bool:
        """Starts the llama-server.exe process."""
        self.port = port
        self.base_url = f"http://127.0.0.1:{self.port}"
        
        if not os.path.exists(self.executable_path):
            print(f"[Backend Error] Executable not found: {self.executable_path}")
            return False
            
        if not os.path.exists(self.model_path):
            print(f"[Backend Error] Model file not found: {self.model_path}")
            return False

        if self._is_port_in_use(self.port):
            print(f"[Backend Error] Port {self.port} is already in use. Cannot start llama-server safely.")
            return False

        cmd = [
            self.executable_path,
            "-m", self.model_path,
            "--port", str(self.port),
            "-c", str(context_size),
            "-ngl", str(offload_layers)
        ]
        
        try:
            print(f"[LlamaBackend] Starting server on port {self.port} with {offload_layers} GPU layers and {context_size} context...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                # Use CREATE_NO_WINDOW and CREATE_NEW_PROCESS_GROUP on Windows for proper termination
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Wait for health
            start_time = time.time()
            timeout = 60
            while time.time() - start_time < timeout:
                if self.is_healthy():
                    print("[LlamaBackend] Server is healthy and ready.")
                    return True
                time.sleep(1)
                
            print("[Backend Error] Server failed to become healthy within the timeout period.")
            self.stop_server()
            return False
            
        except Exception as e:
            print(f"[Backend Error] Failed to launch subprocess: {e}")
            self.stop_server()
            return False

    def is_healthy(self) -> bool:
        """Ping the /health endpoint to ensure the server is responsive."""
        if self.process is None or self.process.poll() is not None:
            return False
            
        try:
            response = requests.get(f"{self.base_url}/health", timeout=1)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def stop_server(self) -> None:
        """Gracefully terminate the subprocess."""
        if self.process and self.process.poll() is None:
            print("[LlamaBackend] Shutting down llama-server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("[LlamaBackend] Server did not exit gracefully. Force killing.")
                self.process.kill()
                self.process.wait()
        
        self.process = None

    def _emergency_cleanup(self):
        """Atexit fallback to catch abrupt script terminations."""
        if self.process and self.process.poll() is None:
            self.process.kill()

    def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Sends a generation request to /v1/chat/completions."""
        if not self.is_healthy():
            return {
                "status": "failed",
                "error": "Backend process is dead or unresponsive.",
                "fatal": True
            }
            
        payload = {
            "messages": messages,
            # No hardcoded max_tokens, let the context dictate it, but we can set a generous limit for output
            "max_tokens": 512,
            "temperature": 0.3,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools

        endpoint = f"{self.base_url}/v1/chat/completions"
        
        try:
            response = requests.post(endpoint, json=payload, timeout=90) # 90s timeout for generation
            if response.status_code == 200:
                data = response.json()
                message = data.get("choices", [{}])[0].get("message", {})
                return {
                    "status": "success",
                    "content": message.get("content", "") or "",
                    "tool_calls": message.get("tool_calls", []),
                    "fatal": False
                }
            else:
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "fatal": False # HTTP error doesn't necessarily mean the server crashed, could be bad prompt
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "failed",
                "error": "Request timed out.",
                "fatal": False # Could just be a slow generation
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "failed",
                "error": "Connection refused. Server may have crashed during generation.",
                "fatal": True # Connection error implies the server process died
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "fatal": False
            }
