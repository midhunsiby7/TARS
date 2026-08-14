# TARS Benchmark Harness Report
**Generated:** 2026-08-14 16:53:02

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
- **Load Time:** 2.82 s
- **Peak VRAM:** 1.44 GB
- **Peak RAM:** 7.36 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (8.48s, 3.89 tok/s)
  - Structured Output: SUCCESS (6.16s, 7.64 tok/s)
  - Tool Calling: SUCCESS (4.12s, 4.12 tok/s)
  - Multi-step Planning: SUCCESS (10.46s, 12.24 tok/s)
  - Ambiguous Request: SUCCESS (6.43s, 5.13 tok/s)
  - Safety-sensitive Request: SUCCESS (6.45s, 2.02 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.01 s
- **Peak VRAM:** 2.01 GB
- **Peak RAM:** 6.01 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.19s, 12.90 tok/s)
  - Structured Output: SUCCESS (5.24s, 8.97 tok/s)
  - Tool Calling: SUCCESS (3.77s, 4.51 tok/s)
  - Multi-step Planning: SUCCESS (8.33s, 15.36 tok/s)
  - Ambiguous Request: SUCCESS (4.34s, 7.61 tok/s)
  - Safety-sensitive Request: SUCCESS (3.39s, 3.84 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 2.41 GB
- **Peak RAM:** 5.31 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.46s, 9.81 tok/s)
  - Structured Output: SUCCESS (5.71s, 8.24 tok/s)
  - Tool Calling: SUCCESS (3.88s, 4.38 tok/s)
  - Multi-step Planning: SUCCESS (8.15s, 15.70 tok/s)
  - Ambiguous Request: SUCCESS (4.32s, 7.65 tok/s)
  - Safety-sensitive Request: SUCCESS (3.40s, 3.82 tok/s)

---
### 🏆 Official TARS Candidates
#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q4_K_M.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q4_K_M.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q4_K_M.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\qwen3.5-4b-instruct-Q8_0.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf

#### None (None | None GPU Layers)
Status: ❌ Failed (Dependency/Environment)
- **Error:** Model file not found: D:\TARS\benchmark_models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf

#### Gemma-4-E4B (Q4_0 | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 1.48 GB
- **Peak RAM:** 7.06 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.26s, 10.43 tok/s)
  - Structured Output: SUCCESS (5.69s, 8.27 tok/s)
  - Tool Calling: SUCCESS (3.62s, 4.69 tok/s)
  - Multi-step Planning: SUCCESS (27.05s, 4.73 tok/s)
  - Ambiguous Request: SUCCESS (4.23s, 7.80 tok/s)
  - Safety-sensitive Request: SUCCESS (3.30s, 3.94 tok/s)

#### Gemma-4-E4B (Q4_0 | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.08 s
- **Peak VRAM:** 2.88 GB
- **Peak RAM:** 7.11 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.36s, 9.81 tok/s)
  - Structured Output: SUCCESS (5.91s, 7.95 tok/s)
  - Tool Calling: SUCCESS (3.26s, 5.22 tok/s)
  - Multi-step Planning: SUCCESS (15.56s, 8.23 tok/s)
  - Ambiguous Request: SUCCESS (4.55s, 7.25 tok/s)
  - Safety-sensitive Request: SUCCESS (3.41s, 3.81 tok/s)

#### Gemma-4-E4B (Q4_0 | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 3.79 GB
- **Peak RAM:** 7.04 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.54s, 8.26 tok/s)
  - Structured Output: SUCCESS (5.04s, 9.32 tok/s)
  - Tool Calling: SUCCESS (3.29s, 5.17 tok/s)
  - Multi-step Planning: SUCCESS (7.55s, 16.96 tok/s)
  - Ambiguous Request: SUCCESS (3.43s, 9.61 tok/s)
  - Safety-sensitive Request: SUCCESS (2.84s, 4.58 tok/s)


## 3. STT Benchmark Results (Whisper.cpp)


## 4. TTS Benchmark Results (Piper)


## 5. Wake Word Benchmark Results (openWakeWord)
