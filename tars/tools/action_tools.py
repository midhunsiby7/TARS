import os
import subprocess
import webbrowser
import urllib.parse
from typing import Any

from .interface import BaseTool
from .permissions import PermissionCategory

# Explicit allowlist of applications the LLM is permitted to launch
APP_ALLOWLIST = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "browser": "msedge.exe", # Default to edge for web browsing explicitly if needed
    "cmd": "cmd.exe",
}

class OpenApplicationTool(BaseTool):
    @property
    def name(self) -> str: return "open_application"
    
    @property
    def description(self) -> str: 
        return f"Opens a registered safe application. Allowed apps: {', '.join(APP_ALLOWLIST.keys())}."
        
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.SAFE_ACTION
    
    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application to open from the allowed list."
                }
            },
            "required": ["app_name"]
        }
    
    def _execute(self, app_name: str) -> Any:
        app_name = app_name.lower().strip()
        if app_name not in APP_ALLOWLIST:
            return f"Error: '{app_name}' is not in the approved application allowlist."
            
        executable = APP_ALLOWLIST[app_name]
        try:
            # We use Popen so we don't block waiting for the GUI app to close
            subprocess.Popen(
                [executable], 
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS if os.name == 'nt' else 0
            )
            return f"Successfully launched {app_name}."
        except Exception as e:
            return f"Failed to launch {app_name}: {str(e)}"

class OpenUrlTool(BaseTool):
    @property
    def name(self) -> str: return "open_url"
    
    @property
    def description(self) -> str: return "Opens a URL in the default web browser."
    
    @property
    def permission(self) -> PermissionCategory: return PermissionCategory.SAFE_ACTION
    
    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL to open, starting with http:// or https://"
                }
            },
            "required": ["url"]
        }
    
    def _execute(self, url: str) -> Any:
        # Validate URL scheme to prevent file:// or other unsafe protocol abuse
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ["http", "https"]:
            return f"Error: Invalid or unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed."
            
        try:
            # Use webbrowser module which safely opens the default system browser
            # without executing shell commands
            success = webbrowser.open(url)
            if success:
                return f"Successfully opened {url} in the default browser."
            else:
                return f"Failed to open {url}."
        except Exception as e:
            return f"Error opening URL: {str(e)}"

def register_action_tools(registry):
    tools = [OpenApplicationTool(), OpenUrlTool()]
    for t in tools:
        registry.register(t)
