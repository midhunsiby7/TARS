# TARS Benchmark Harness Report
**Generated:** 2026-08-14 17:08:51

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
- **Load Time:** 1.10 s
- **Peak VRAM:** 1.44 GB
- **Peak RAM:** 7.33 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.26s, 12.67 tok/s)
  - Structured Output: SUCCESS (5.28s, 8.90 tok/s)
  - Tool Calling: SUCCESS (4.43s, 3.84 tok/s)
  - Multi-step Planning: SUCCESS (8.06s, 15.87 tok/s)
  - Ambiguous Request: SUCCESS (4.21s, 7.84 tok/s)
  - Safety-sensitive Request: SUCCESS (3.37s, 3.86 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 2.01 GB
- **Peak RAM:** 6.96 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.24s, 10.17 tok/s)
  - Structured Output: SUCCESS (5.96s, 7.88 tok/s)
  - Tool Calling: SUCCESS (3.23s, 5.27 tok/s)
  - Multi-step Planning: SUCCESS (7.97s, 16.07 tok/s)
  - Ambiguous Request: SUCCESS (4.21s, 7.84 tok/s)
  - Safety-sensitive Request: SUCCESS (3.37s, 3.86 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 2.41 GB
- **Peak RAM:** 6.81 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.85s, 14.02 tok/s)
  - Structured Output: SUCCESS (6.09s, 7.72 tok/s)
  - Tool Calling: SUCCESS (3.80s, 4.47 tok/s)
  - Multi-step Planning: SUCCESS (7.87s, 16.26 tok/s)
  - Ambiguous Request: SUCCESS (4.84s, 6.82 tok/s)
  - Safety-sensitive Request: SUCCESS (3.33s, 3.91 tok/s)

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

#### Qwen3-4B (Q4_K_M | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 1.45 GB
- **Peak RAM:** 7.33 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.12s, 13.10 tok/s)
  - Structured Output: SUCCESS (5.19s, 9.06 tok/s)
  - Tool Calling: SUCCESS (7.99s, 2.13 tok/s)
  - Multi-step Planning: SUCCESS (30.18s, 4.24 tok/s)
  - Ambiguous Request: SUCCESS (4.91s, 6.73 tok/s)
  - Safety-sensitive Request: SUCCESS (3.39s, 3.84 tok/s)

#### Qwen3-4B (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 2.66 GB
- **Peak RAM:** 7.22 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.36s, 10.12 tok/s)
  - Structured Output: SUCCESS (7.77s, 6.05 tok/s)
  - Tool Calling: SUCCESS (2.92s, 5.82 tok/s)
  - Multi-step Planning: SUCCESS (22.92s, 5.59 tok/s)
  - Ambiguous Request: SUCCESS (4.74s, 6.97 tok/s)
  - Safety-sensitive Request: SUCCESS (3.29s, 3.95 tok/s)

#### Qwen3-4B (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 3.79 GB
- **Peak RAM:** 7.00 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.33s, 10.22 tok/s)
  - Structured Output: SUCCESS (5.36s, 8.76 tok/s)
  - Tool Calling: SUCCESS (3.74s, 4.54 tok/s)
  - Multi-step Planning: SUCCESS (8.06s, 15.88 tok/s)
  - Ambiguous Request: SUCCESS (4.21s, 7.83 tok/s)
  - Safety-sensitive Request: SUCCESS (3.36s, 3.87 tok/s)

#### Gemma-4-E4B (Q4_0 | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 1.48 GB
- **Peak RAM:** 6.93 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.23s, 10.21 tok/s)
  - Structured Output: SUCCESS (5.15s, 9.13 tok/s)
  - Tool Calling: SUCCESS (3.20s, 5.32 tok/s)
  - Multi-step Planning: SUCCESS (7.76s, 16.49 tok/s)
  - Ambiguous Request: SUCCESS (4.87s, 6.77 tok/s)
  - Safety-sensitive Request: SUCCESS (3.34s, 3.89 tok/s)

#### Gemma-4-E4B (Q4_0 | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 2.89 GB
- **Peak RAM:** 6.98 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.17s, 10.72 tok/s)
  - Structured Output: SUCCESS (7.30s, 6.43 tok/s)
  - Tool Calling: SUCCESS (3.71s, 4.58 tok/s)
  - Multi-step Planning: SUCCESS (8.19s, 15.62 tok/s)
  - Ambiguous Request: SUCCESS (4.18s, 7.89 tok/s)
  - Safety-sensitive Request: SUCCESS (3.27s, 3.97 tok/s)

#### Gemma-4-E4B (Q4_0 | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.07 s
- **Peak VRAM:** 3.79 GB
- **Peak RAM:** 7.09 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.24s, 10.51 tok/s)
  - Structured Output: SUCCESS (4.86s, 9.68 tok/s)
  - Tool Calling: SUCCESS (3.06s, 5.56 tok/s)
  - Multi-step Planning: SUCCESS (6.70s, 19.11 tok/s)
  - Ambiguous Request: SUCCESS (3.37s, 9.78 tok/s)
  - Safety-sensitive Request: SUCCESS (2.78s, 4.68 tok/s)


## 3. STT Benchmark Results (Whisper.cpp)


## 4. TTS Benchmark Results (Piper)


## 5. Wake Word Benchmark Results (openWakeWord)
