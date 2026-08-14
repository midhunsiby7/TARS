# TARS Benchmark Harness Report
**Generated:** 2026-08-14 20:28:06

## 1. System Baseline
- **OS:** Windows 11 (10.0.26200)
- **CPU:** AMD64 (6 cores)
- **RAM:** 7.36 GB
- **GPU 0:** NVIDIA GeForce GTX 1650 (4.0 GB VRAM)

## 2. LLM Benchmark Results

### 🏆 Official TARS Candidates
#### Qwen3-4B (Q4_K_M | 20 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.09 s
- **Peak VRAM:** 2.98 GB
- **Peak RAM:** 7.36 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (6.80s, 5.00 tok/s)
  - Structured Output: SUCCESS (4.35s, 10.80 tok/s)
  - Tool Calling: SUCCESS (3.15s, 5.39 tok/s)
  - Multi-step Planning: SUCCESS (6.82s, 18.78 tok/s)
  - Ambiguous Request: SUCCESS (3.38s, 9.76 tok/s)
  - Safety-sensitive Request: SUCCESS (2.79s, 4.66 tok/s)

#### Qwen3-4B (Q4_K_M | 24 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 3.23 GB
- **Peak RAM:** 7.33 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (4.14s, 13.03 tok/s)
  - Structured Output: SUCCESS (4.29s, 10.96 tok/s)
  - Tool Calling: SUCCESS (2.99s, 5.69 tok/s)
  - Multi-step Planning: SUCCESS (6.90s, 18.55 tok/s)
  - Ambiguous Request: SUCCESS (3.35s, 9.86 tok/s)
  - Safety-sensitive Request: SUCCESS (2.75s, 4.73 tok/s)

#### Qwen3-4B (Q4_K_M | 28 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.02 s
- **Peak VRAM:** 3.48 GB
- **Peak RAM:** 7.16 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.51s, 9.69 tok/s)
  - Structured Output: SUCCESS (4.37s, 10.75 tok/s)
  - Tool Calling: SUCCESS (3.03s, 5.60 tok/s)
  - Multi-step Planning: SUCCESS (7.02s, 18.24 tok/s)
  - Ambiguous Request: SUCCESS (3.37s, 9.81 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.75 tok/s)

#### Qwen3-4B (Q4_K_M | 30 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.01 s
- **Peak VRAM:** 3.61 GB
- **Peak RAM:** 7.07 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.11s, 10.61 tok/s)
  - Structured Output: SUCCESS (5.16s, 9.10 tok/s)
  - Tool Calling: SUCCESS (3.19s, 5.33 tok/s)
  - Multi-step Planning: SUCCESS (6.41s, 19.96 tok/s)
  - Ambiguous Request: SUCCESS (3.52s, 9.38 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.75 tok/s)

#### Qwen3-4B (Q4_K_M | 32 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 3.73 GB
- **Peak RAM:** 6.94 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.12s, 10.88 tok/s)
  - Structured Output: SUCCESS (4.37s, 10.75 tok/s)
  - Tool Calling: SUCCESS (3.01s, 5.64 tok/s)
  - Multi-step Planning: SUCCESS (6.61s, 19.38 tok/s)
  - Ambiguous Request: SUCCESS (3.37s, 9.79 tok/s)
  - Safety-sensitive Request: SUCCESS (2.75s, 4.73 tok/s)

#### Qwen3-4B (Q4_K_M | 33 GPU Layers)
Status: ✅ Implemented and Tested
- **Load Time:** 1.03 s
- **Peak VRAM:** 3.79 GB
- **Peak RAM:** 6.51 GB
- **Test Metrics:**
  - Simple Reasoning: SUCCESS (3.13s, 10.88 tok/s)
  - Structured Output: SUCCESS (4.34s, 10.83 tok/s)
  - Tool Calling: SUCCESS (2.98s, 5.71 tok/s)
  - Multi-step Planning: SUCCESS (6.61s, 19.36 tok/s)
  - Ambiguous Request: SUCCESS (3.27s, 10.09 tok/s)
  - Safety-sensitive Request: SUCCESS (2.74s, 4.75 tok/s)


## 3. STT Benchmark Results (Whisper.cpp)


## 4. TTS Benchmark Results (Piper)


## 5. Wake Word Benchmark Results (openWakeWord)
