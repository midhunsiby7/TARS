import argparse
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from benchmark_harness.config import ConfigManager as BenchmarkConfigManager
from tars.llm.llama_backend import LlamaBackend
from tars.memory.session import SessionManager
from tars.core.orchestrator import TarsOrchestrator
from tars.tools.registry import ToolRegistry
from tars.tools.permissions import PermissionManager, PermissionCategory
from tars.tools.system_tools import register_system_tools
from tars.tools.action_tools import register_action_tools
from tars.config.manager import RuntimeConfigManager
from tars.memory.manager import MemoryManager
from tars.personality.manager import PersonalityManager
from tars.tools.memory_tools import RememberTool, RecallTool, ListMemoriesTool, ForgetTool
from tars.tools.personality_tools import GetPersonalityTool, SetPersonalityTool

def main():
    parser = argparse.ArgumentParser(description="TARS Phase 2C Core Runtime")
    parser.add_argument("--fallback", action="store_true", help="Use fallback configuration instead of production")
    args = parser.parse_args()

    # 1. Load Configurations
    config_path = os.path.join(project_root, "tars", "config", "runtime.json")
    runtime_config = RuntimeConfigManager(config_path)

    offload_layers = runtime_config.fallback_gpu_layers if args.fallback else runtime_config.production_gpu_layers
    port = runtime_config.server_port
    context_size = runtime_config.context_size
    db_path = os.path.join(project_root, runtime_config.db_path)
    identity_path = os.path.join(project_root, "tars", "config", "identity.json")

    # Resolve model path using Phase 1 logic for consistency
    try:
        benchmark_config = BenchmarkConfigManager()
    except Exception as e:
        print(f"[Fatal] Could not initialize benchmark config manager: {e}")
        sys.exit(1)
        
    model_name = runtime_config.selected_model
    # Hack for quantization parsing (since benchmark config separates it). Assuming standard format Model-Q4_K_M etc.
    quantization = "Q4_K_M"
    model_path = benchmark_config.get_model_file_path(model_name, quantization)
    
    if not model_path:
        print(f"[Fatal] Could not locate model: {model_name} ({quantization})")
        sys.exit(1)
        
    executable_path = os.path.join(project_root, "tools", "llama", "llama-server.exe")
    if not os.path.exists(executable_path):
        print(f"[Fatal] Could not locate llama-server.exe at {executable_path}")
        sys.exit(1)

    # 2. Initialize Core Subsystems
    memory_manager = MemoryManager(db_path)
    personality_manager = PersonalityManager(identity_path)
    
    llm = LlamaBackend(executable_path=executable_path, model_path=model_path)
    session = SessionManager(
        context_size=context_size,
        system_prompt="", # Orchestrator will rebuild this dynamically
        response_headroom=512
    )
    
    permission_manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
    tool_registry = ToolRegistry(permission_manager)
    
    # Register core tools
    register_system_tools(tool_registry)
    register_action_tools(tool_registry)
    
    # Register Phase 2C tools
    tool_registry.register(RememberTool(memory_manager))
    tool_registry.register(RecallTool(memory_manager))
    tool_registry.register(ListMemoriesTool(memory_manager))
    tool_registry.register(ForgetTool(memory_manager))
    tool_registry.register(GetPersonalityTool(personality_manager))
    tool_registry.register(SetPersonalityTool(personality_manager))
    
    orchestrator = TarsOrchestrator(
        llm=llm, 
        session=session, 
        tool_registry=tool_registry,
        memory_manager=memory_manager,
        personality_manager=personality_manager
    )
    
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
