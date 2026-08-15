import argparse
import sys
import os

# Add the project root to sys.path so we can import from benchmark_harness
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from benchmark_harness.config import ConfigManager
from tars.llm.llama_backend import LlamaBackend
from tars.memory.session import SessionManager
from tars.core.orchestrator import TarsOrchestrator

DEFAULT_SYSTEM_PROMPT = (
    "You are TARS, a helpful, precise, and concise AI assistant running locally. "
    "You provide clear and accurate answers. "
    "Do not fabricate capabilities; you currently only have access to text chatting."
)

from tars.tools.registry import ToolRegistry
from tars.tools.permissions import PermissionManager, PermissionCategory
from tars.tools.system_tools import register_system_tools
from tars.tools.action_tools import register_action_tools

def main():
    parser = argparse.ArgumentParser(description="TARS Phase 2B Core Runtime")
    parser.add_argument("--fallback", action="store_true", help="Use 15-layer fallback configuration instead of 28")
    parser.add_argument("--port", type=int, default=8080, help="Local port for llama-server")
    parser.add_argument("--context-size", type=int, default=2048, help="Context window size in tokens")
    args = parser.parse_args()

    offload_layers = 15 if args.fallback else 28
    port = args.port
    context_size = args.context_size
    
    # 1. Load config and resolve model path using Phase 1 logic
    try:
        config = ConfigManager()
    except Exception as e:
        print(f"[Fatal] Could not initialize config manager: {e}")
        sys.exit(1)
        
    model_name = "Qwen3-4B"
    quantization = "Q4_K_M"
    model_path = config.get_model_file_path(model_name, quantization)
    
    if not model_path:
        print(f"[Fatal] Could not locate model: {model_name} ({quantization})")
        print("Please ensure it is downloaded and configured in models.json.")
        sys.exit(1)
        
    executable_path = os.path.join(project_root, "tools", "llama", "llama-server.exe")
    if not os.path.exists(executable_path):
        print(f"[Fatal] Could not locate llama-server.exe at {executable_path}")
        sys.exit(1)

    # 2. Initialize Core Components & Tools
    llm = LlamaBackend(executable_path=executable_path, model_path=model_path)
    session = SessionManager(
        context_size=context_size,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        response_headroom=512
    )
    
    permission_manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
    tool_registry = ToolRegistry(permission_manager)
    register_system_tools(tool_registry)
    register_action_tools(tool_registry)
    
    orchestrator = TarsOrchestrator(llm=llm, session=session, tool_registry=tool_registry)
    
    # 3. Start Lifecycle
    try:
        if orchestrator.startup(offload_layers=offload_layers, port=port, context_size=context_size):
            orchestrator.chat_loop()
    except KeyboardInterrupt:
        print("\n[TARS System] Received interrupt signal.")
        orchestrator.shutdown()
    except Exception as e:
        print(f"\n[TARS Fatal Error] {e}")
        orchestrator.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
