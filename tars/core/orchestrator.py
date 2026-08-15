import time
from typing import Optional

from tars.llm.interface import LLMInterface
from tars.memory.session import SessionManager

class TarsOrchestrator:
    def __init__(self, llm: LLMInterface, session: SessionManager):
        self.llm = llm
        self.session = session
        self.running = False
        
        # Configuration for restarts
        self._max_restarts = 3
        self._current_restarts = 0
        self._last_config = {}

    def startup(self, offload_layers: int, port: int, context_size: int) -> bool:
        """Initializes the backend and session."""
        print("[TARS] Initializing Phase 2A Runtime...")
        
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

    def chat_loop(self):
        """The main Read-Eval-Print-Loop (REPL) for the interactive text session."""
        print("\n" + "="*50)
        print("TARS Core Runtime - Phase 2A")
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

            # 1. Add to session
            self.session.add_user_message(user_input)
            messages = self.session.get_messages()
            
            # 2. Generate response
            print("\nTARS: ", end="", flush=True)
            response = self.llm.generate(messages=messages)
            
            # 3. Handle result
            if response["status"] == "success":
                content = response["content"]
                print(content)
                self.session.add_assistant_message(content)
                
            else:
                print(f"[Error: {response['error']}]")
                # Remove the user message since it failed to process, so they can try again.
                if self.session.messages and self.session.messages[-1]["role"] == "user":
                    self.session.messages.pop()
                    
                if response.get("fatal", False):
                    # Only restart if there's strong evidence the backend died
                    print("[TARS System] Detected fatal backend failure.")
                    if not self._attempt_backend_recovery():
                        break

        self.shutdown()
