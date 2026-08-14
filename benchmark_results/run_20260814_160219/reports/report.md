# TARS Benchmark Harness Report
**Generated:** 2026-08-14 16:04:20

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
- **Load Time:** 1.06 s
- **Peak VRAM:** 1.44 GB
- **Peak RAM:** 7.01 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.85s, 8.84 tok/s)
  - Structured Output: SUCCESS (4.74s, 9.91 tok/s)
  - Tool Calling: SUCCESS (4.24s, 4.01 tok/s)
  - Multi-step Planning: SUCCESS (7.40s, 17.30 tok/s)
  - Ambiguous Request: SUCCESS (4.66s, 7.09 tok/s)
  - Safety-sensitive Request: SUCCESS (3.25s, 4.00 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 2.01 GB
- **Peak RAM:** 7.07 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.40s, 10.01 tok/s)
  - Structured Output: SUCCESS (6.03s, 7.79 tok/s)
  - Tool Calling: SUCCESS (3.96s, 4.29 tok/s)
  - Multi-step Planning: SUCCESS (8.17s, 15.66 tok/s)
  - Ambiguous Request: SUCCESS (4.25s, 7.77 tok/s)
  - Safety-sensitive Request: SUCCESS (3.33s, 3.91 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 2.41 GB
- **Peak RAM:** 6.89 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.75s, 8.81 tok/s)
  - Structured Output: SUCCESS (5.22s, 9.00 tok/s)
  - Tool Calling: SUCCESS (3.86s, 4.41 tok/s)
  - Multi-step Planning: SUCCESS (8.08s, 15.85 tok/s)
  - Ambiguous Request: SUCCESS (4.26s, 7.75 tok/s)
  - Safety-sensitive Request: SUCCESS (3.58s, 3.63 tok/s)

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
