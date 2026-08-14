# TARS

TARS is a fully local/offline AI assistant project designed to sit between the user and their Windows laptop.

Phase 1 currently contains:
- Local AI benchmark infrastructure
- Hardware detection
- GPU/RAM/CPU telemetry
- llama.cpp integration
- Local LLM benchmarking
- STT/TTS/wake-word benchmark architecture
- Semantic task validation
- Production hardware profiling

Current selected production LLM:
**Qwen3-4B-Instruct-2507 Q4_K_M**

Current recommended GPU configuration:
**28 GPU layers**

Fallback:
**15 GPU layers**

Hardware:
- Windows 11
- Ryzen 5 4600H
- 8 GB RAM
- GTX 1650 4 GB VRAM

*Note: Model weights (.gguf files) and large native binaries (llama-server.exe, whisper.cpp) are intentionally excluded from this GitHub repository and must be acquired separately to run the benchmarks locally.*
