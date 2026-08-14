# TARS Benchmark Harness Report
**Generated:** 2026-08-14 15:56:46

## 1. System Baseline
- **OS:** Windows 11 (10.0.26200)
- **CPU:** AMD64 (6 cores)
- **RAM:** 7.36 GB
- **GPU 0:** NVIDIA GeForce GTX 1650 (4.0 GB VRAM)

## 2. LLM Benchmark Results

### 🚬 Infrastructure Verification (Smoke Tests)
> [!WARNING]
> These models are used ONLY to verify the benchmark infrastructure and are EXCLUDED from the official TARS candidate ranking.

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 1.43 GB
- **Peak RAM:** 7.17 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.71s, 29.67 tok/s)
  - Structured Output: SUCCESS (5.51s, 15.26 tok/s)
  - Tool Calling: SUCCESS (8.12s, 21.99 tok/s)
  - Multi-step Planning: SUCCESS (8.21s, 22.64 tok/s)
  - Ambiguous Request: SUCCESS (4.32s, 11.98 tok/s)
  - Safety-sensitive Request: SUCCESS (8.23s, 22.44 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 2.01 GB
- **Peak RAM:** 7.07 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.59s, 30.65 tok/s)
  - Structured Output: SUCCESS (5.34s, 13.31 tok/s)
  - Tool Calling: SUCCESS (8.09s, 22.02 tok/s)
  - Multi-step Planning: SUCCESS (8.18s, 22.35 tok/s)
  - Ambiguous Request: SUCCESS (4.23s, 11.65 tok/s)
  - Safety-sensitive Request: SUCCESS (8.32s, 22.09 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.02 s
- **Peak VRAM:** 2.40 GB
- **Peak RAM:** 6.91 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.46s, 31.30 tok/s)
  - Structured Output: SUCCESS (5.34s, 13.29 tok/s)
  - Tool Calling: SUCCESS (8.80s, 19.60 tok/s)
  - Multi-step Planning: SUCCESS (8.08s, 22.47 tok/s)
  - Ambiguous Request: SUCCESS (4.22s, 12.02 tok/s)
  - Safety-sensitive Request: SUCCESS (8.35s, 22.00 tok/s)

---
### 🏆 Official TARS Candidates
#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q5_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q5_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q5_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3-4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\gemma4-e4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\gemma4-e4b-q4_k_m.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\gemma4-e4b-q4_k_m.gguf


## 3. STT Benchmark Results (Whisper.cpp)


## 4. TTS Benchmark Results (Piper)


## 5. Wake Word Benchmark Results (openWakeWord)
