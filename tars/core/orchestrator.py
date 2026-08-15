import time
import json
from typing import Optional

from tars.llm.interface import LLMInterface
from tars.memory.session import SessionManager
from tars.tools.registry import ToolRegistry

class TarsOrchestrator:
    def __init__(self, llm: LLMInterface, session: SessionManager, tool_registry: Optional[ToolRegistry] = None):
        self.llm = llm
        self.session = session
        self.tool_registry = tool_registry
        self.running = False
        
        # Configuration for restarts
        self._max_restarts = 3
        self._current_restarts = 0
        self._last_config = {}

    def startup(self, offload_layers: int, port: int, context_size: int) -> bool:
        """Initializes the backend and session."""
        print("[TARS] Initializing Phase 2B Runtime...")
        
        self._last_config = {
            "offload_layers": offload_layers,
            "port": port,
            "context_size": context_size
        }
        
        if not self.llm.start_server(offload_layers, port, context_size):
            print("[TARS Fatal] Backend failed to start. Aborting.")
            return False
            
        self.running = True
        return True
        
    def _attempt_backend_recovery(self) -> bool:
        """Attempts to restart the backend if a fatal error occurs, avoiding infinite loops."""
        if self._current_restarts >= self._max_restarts:
            print("[TARS Fatal] Maximum backend recovery attempts exceeded. Shutting down.")
            return False
            
        self._current_restarts += 1
        print(f"[TARS System] Attempting backend recovery ({self._current_restarts}/{self._max_restarts})...")
        
        self.llm.stop_server()
        time.sleep(2) # Give the OS time to clear the port
        
        if self.llm.start_server(**self._last_config):
            print("[TARS System] Backend recovered successfully.")
            return True
        else:
            return False

    def shutdown(self):
        """Cleans up resources and stops the backend."""
        print("[TARS] Shutting down...")
        self.running = False
        self.llm.stop_server()

    def _execute_agent_loop(self) -> bool:
        """Executes the tool-calling loop. Returns True if successful, False if fatal error."""
        MAX_TOOL_CALLS = 3
        calls_made = 0
        
        while calls_made <= MAX_TOOL_CALLS:
            messages = self.session.get_messages()
            tools_schema = self.tool_registry.get_enabled_schemas() if self.tool_registry else None
            
            # Print indicator that we are generating
            if calls_made == 0:
                print("TARS: ", end="", flush=True)
            else:
                print("\n[TARS Thinking...] ", end="", flush=True)
                
            response = self.llm.generate(messages=messages, tools=tools_schema)
            
            if response["status"] != "success":
                print(f"[Error: {response['error']}]")
                if response.get("fatal", False):
                    print("[TARS System] Detected fatal backend failure.")
                    if not self._attempt_backend_recovery():
                        return False
                return True # Recoverable error, return to REPL
                
            content = response.get("content", "")
            tool_calls = response.get("tool_calls", [])
            
            if content:
                print(content, end="", flush=True)
                
            if not tool_calls:
                # Normal response finished
                if content:
                    self.session.add_assistant_message(content)
                print() # Newline
                return True
                
            # Handle tool calls
            calls_made += 1
            if calls_made > MAX_TOOL_CALLS:
                print("\n[TARS System] Tool call limit reached. Stopping execution loop to prevent infinite loops.")
                self.session.add_assistant_message("I've reached my internal tool limit for this request. Please ask again.")
                return True
                
            self.session.add_assistant_tool_calls(tool_calls)
            
            for call in tool_calls:
                call_id = call.get("id")
                func = call.get("function", {})
                name = func.get("name")
                args_json = func.get("arguments", "{}")
                
                print(f"\n[Executing Tool: {name}]...", end="", flush=True)
                
                if not self.tool_registry:
                    result_msg = f"Error: No tools are configured. Cannot execute {name}."
                else:
                    tool_result = self.tool_registry.execute_tool(name, args_json)
                    result_msg = tool_result.serialize()
                    
                print(" Done.")
                self.session.add_tool_result(call_id, result_msg)
                
        return True

    def chat_loop(self):
        """The main Read-Eval-Print-Loop (REPL) for the interactive text session."""
        print("\n" + "="*50)
        print("TARS Core Runtime - Phase 2B (Agent Mode)")
        print("Type 'exit' or 'quit' to close. Type '/reset' to clear conversation context.")
        print("="*50 + "\n")
        
        while self.running:
            try:
                user_input = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                break
                
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if user_input.lower() == "/reset":
                self.session.reset()
                print("\nTARS: Conversation reset.")
                continue

            self.session.add_user_message(user_input)
            
            if not self._execute_agent_loop():
                # Fatal error that couldn't be recovered
                break

        self.shutdown()
