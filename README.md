# TARS

TARS is a fully local/offline AI assistant project designed to sit between the user and their Windows laptop.

## Phase 2A: Core Runtime (Current)
We have implemented the first version of the Phase 2A core text-based runtime. It successfully hosts a conversational Read-Eval-Print-Loop (REPL) using `llama-server.exe` as the backend.

### How to Start TARS
Ensure you have downloaded the required `llama-server.exe` and `Qwen3-4B-Instruct-2507` model to their respective paths configured in `models.json`.

Then, from the root of the repository, run:
```powershell
python tars\main.py
```

### Interactive Commands
- **exit / quit**: Shuts down the backend and terminates TARS cleanly.
- **/reset**: Clears the conversation history context and resets the session.

### Configuration Options
By default, TARS launches with the production 28-layer GPU offload profile.
- **`--fallback`**: Launches TARS with the 15-layer GPU offload profile (useful if playing a game or running VRAM-heavy workloads).
- **`--port <port>`**: Override the default 8080 port.
- **`--context-size <tokens>`**: Override the default 2048 token context window.

### Known Limitations (Phase 2A)
- 🎙️ **Voice (STT/TTS)** is NOT implemented yet in the production runtime.
- 🗣️ **Wake Word activation** is NOT implemented yet.
- 🧠 **Persistent Memory** across restarts is NOT implemented yet.
- ⚙️ **System Control Tools** and autonomous behaviors are NOT active.
- 🌐 **Web Access/Cloud APIs** are strictly excluded.

## Phase 1: Hardware & Baseline
Phase 1 established the `benchmark_harness/` which evaluated multiple local LLMs and hardware configurations. 

Current selected production LLM:
**Qwen3-4B-Instruct-2507 Q4_K_M**

Hardware:
- Windows 11
- Ryzen 5 4600H
- 8 GB RAM
- GTX 1650 4 GB VRAM

*Note: Model weights (.gguf files) and large native binaries (llama-server.exe, whisper.cpp) are intentionally excluded from this GitHub repository and must be acquired separately to run the benchmarks locally.*
