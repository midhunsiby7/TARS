# TARS Benchmark Harness Report
**Generated:** 2026-08-14 19:44:52

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
- **Load Time:** 6.28 s
- **Peak VRAM:** 1.44 GB
- **Peak RAM:** 7.23 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (16.67s, 2.76 tok/s)
  - Structured Output: SUCCESS (4.71s, 9.99 tok/s)
  - Tool Calling: SUCCESS (14.47s, 1.17 tok/s)
  - Multi-step Planning: SUCCESS (17.41s, 7.35 tok/s)
  - Ambiguous Request: SUCCESS (3.73s, 8.85 tok/s)
  - Safety-sensitive Request: SUCCESS (2.88s, 4.51 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 2.01 GB
- **Peak RAM:** 7.29 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.07s, 8.36 tok/s)
  - Structured Output: SUCCESS (4.42s, 10.62 tok/s)
  - Tool Calling: SUCCESS (2.96s, 5.74 tok/s)
  - Multi-step Planning: SUCCESS (6.71s, 19.08 tok/s)
  - Ambiguous Request: SUCCESS (3.34s, 9.88 tok/s)
  - Safety-sensitive Request: SUCCESS (2.79s, 4.66 tok/s)

#### Qwen-2.5-1.5B-Instruct-SmokeTest (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 2.41 GB
- **Peak RAM:** 6.80 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.64s, 14.83 tok/s)
  - Structured Output: SUCCESS (4.43s, 10.60 tok/s)
  - Tool Calling: SUCCESS (2.96s, 5.75 tok/s)
  - Multi-step Planning: SUCCESS (6.60s, 19.38 tok/s)
  - Ambiguous Request: SUCCESS (3.26s, 10.11 tok/s)
  - Safety-sensitive Request: SUCCESS (2.77s, 4.70 tok/s)

---
### 🏆 Official TARS Candidates
#### Qwen3.5-4B (Q4_K_M | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.02 s
- **Peak VRAM:** 1.48 GB
- **Peak RAM:** 7.36 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.34s, 10.17 tok/s)
  - Structured Output: SUCCESS (5.12s, 9.19 tok/s)
  - Tool Calling: SUCCESS (3.44s, 4.94 tok/s)
  - Multi-step Planning: SUCCESS (6.96s, 18.40 tok/s)
  - Ambiguous Request: SUCCESS (3.41s, 9.69 tok/s)
  - Safety-sensitive Request: SUCCESS (2.78s, 4.68 tok/s)

#### Qwen3.5-4B (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 2.99 GB
- **Peak RAM:** 7.07 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.95s, 13.69 tok/s)
  - Structured Output: SUCCESS (4.72s, 9.95 tok/s)
  - Tool Calling: SUCCESS (2.88s, 5.91 tok/s)
  - Multi-step Planning: SUCCESS (7.53s, 16.99 tok/s)
  - Ambiguous Request: SUCCESS (3.52s, 9.37 tok/s)
  - Safety-sensitive Request: SUCCESS (2.82s, 4.61 tok/s)

#### Qwen3.5-4B (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 3.97 GB
- **Peak RAM:** 7.04 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.08s, 13.25 tok/s)
  - Structured Output: SUCCESS (4.89s, 9.60 tok/s)
  - Tool Calling: SUCCESS (19.65s, 0.86 tok/s)
  - Multi-step Planning: SUCCESS (7.04s, 18.18 tok/s)
  - Ambiguous Request: SUCCESS (3.35s, 9.84 tok/s)
  - Safety-sensitive Request: SUCCESS (2.85s, 4.56 tok/s)

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
- **Load Time:** 1.07 s
- **Peak VRAM:** 1.45 GB
- **Peak RAM:** 6.80 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.11s, 10.92 tok/s)
  - Structured Output: SUCCESS (4.41s, 10.65 tok/s)
  - Tool Calling: SUCCESS (3.13s, 5.44 tok/s)
  - Multi-step Planning: SUCCESS (6.82s, 18.77 tok/s)
  - Ambiguous Request: SUCCESS (3.26s, 10.12 tok/s)
  - Safety-sensitive Request: SUCCESS (2.75s, 4.72 tok/s)

#### Qwen3-4B (Q4_K_M | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 2.66 GB
- **Peak RAM:** 6.82 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.08s, 11.03 tok/s)
  - Structured Output: SUCCESS (4.41s, 10.65 tok/s)
  - Tool Calling: SUCCESS (3.14s, 5.41 tok/s)
  - Multi-step Planning: SUCCESS (6.60s, 19.40 tok/s)
  - Ambiguous Request: SUCCESS (3.24s, 10.18 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.75 tok/s)

#### Qwen3-4B (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 3.79 GB
- **Peak RAM:** 6.71 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.07s, 11.07 tok/s)
  - Structured Output: SUCCESS (4.29s, 10.95 tok/s)
  - Tool Calling: SUCCESS (3.04s, 5.59 tok/s)
  - Multi-step Planning: SUCCESS (6.40s, 20.01 tok/s)
  - Ambiguous Request: SUCCESS (3.46s, 9.54 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.75 tok/s)

#### Gemma-4-E4B (Q4_0 | 0 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.04 s
- **Peak VRAM:** 1.48 GB
- **Peak RAM:** 7.10 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (5.43s, 6.26 tok/s)
  - Structured Output: SUCCESS (5.05s, 9.31 tok/s)
  - Tool Calling: SUCCESS (3.15s, 5.39 tok/s)
  - Multi-step Planning: SUCCESS (6.57s, 19.50 tok/s)
  - Ambiguous Request: SUCCESS (3.35s, 9.84 tok/s)
  - Safety-sensitive Request: SUCCESS (2.82s, 4.61 tok/s)

#### Gemma-4-E4B (Q4_0 | 15 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.07 s
- **Peak VRAM:** 2.89 GB
- **Peak RAM:** 6.96 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (5.88s, 5.78 tok/s)
  - Structured Output: SUCCESS (4.36s, 10.77 tok/s)
  - Tool Calling: SUCCESS (2.95s, 5.77 tok/s)
  - Multi-step Planning: SUCCESS (6.36s, 20.14 tok/s)
  - Ambiguous Request: SUCCESS (3.53s, 9.35 tok/s)
  - Safety-sensitive Request: SUCCESS (2.78s, 4.67 tok/s)

#### Gemma-4-E4B (Q4_0 | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.05 s
- **Peak VRAM:** 3.80 GB
- **Peak RAM:** 6.91 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.28s, 8.61 tok/s)
  - Structured Output: SUCCESS (4.01s, 11.71 tok/s)
  - Tool Calling: SUCCESS (2.78s, 6.11 tok/s)
  - Multi-step Planning: SUCCESS (6.34s, 20.20 tok/s)
  - Ambiguous Request: SUCCESS (3.55s, 9.28 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.74 tok/s)


## 3. STT Benchmark Results (Whisper.cpp)


## 4. TTS Benchmark Results (Piper)


## 5. Wake Word Benchmark Results (openWakeWord)
