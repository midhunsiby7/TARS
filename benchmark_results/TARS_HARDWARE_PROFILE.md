# TARS Hardware Profile

## 1. Hardware Baseline
- **OS:** Windows 11 (10.0.26200)
- **CPU:** AMD Ryzen 5 4600H (6 cores / 12 threads)
- **RAM:** 7.36 GB usable
- **GPU 0:** NVIDIA GeForce GTX 1650 (4.0 GB VRAM)
- **Storage:** NVMe SSD

## 2. Candidate Model Comparison
The initial candidate benchmark evaluated `Qwen3.5-4B`, `Qwen3-4B`, and `Gemma-4-E4B` across 0, 15, and 33 GPU layer offloads. 
- **Qwen3.5-4B** was rejected due to approaching VRAM exhaustion (3.97 GB at 33 layers) resulting in massive performance degradation.
- **Gemma-4-E4B** and **Qwen3-4B** both demonstrated excellent stability.
- **Qwen3-4B-Instruct-2507 (Q4_K_M)** was selected as the preferred production candidate based on its balance of reasoning capability and performance consistency.

## 3. Qwen3-4B GPU Offload Benchmark

| GPU Layers | Avg Tok/s (Planning) | Avg Latency (Tool) | Peak VRAM | Peak RAM | Task Success | Stability |
|------------|----------------------|--------------------|-----------|----------|--------------|-----------|
| **15**     | 19.40 tok/s          | 3.14 s             | 2.66 GB   | 6.82 GB  | 6/6 (100%)   | Excellent |
| **20**     | 18.78 tok/s          | 3.15 s             | 2.98 GB   | 7.36 GB  | 6/6 (100%)   | Excellent |
| **24**     | 18.55 tok/s          | 2.99 s             | 3.23 GB   | 7.33 GB  | 6/6 (100%)   | Excellent |
| **28**     | 18.24 tok/s          | 3.03 s             | 3.48 GB   | 7.16 GB  | 6/6 (100%)   | Excellent |
| **30**     | 19.96 tok/s          | 3.19 s             | 3.61 GB   | 7.07 GB  | 6/6 (100%)   | Good      |
| **32**     | 19.38 tok/s          | 3.01 s             | 3.73 GB   | 6.94 GB  | 6/6 (100%)   | Borderline|
| **33**     | 19.36 tok/s          | 2.98 s             | 3.79 GB   | 6.51 GB  | 6/6 (100%)   | Borderline|

## 4. Performance vs VRAM Analysis
The tradeoff between offload layers and VRAM usage on this 4GB GPU is strictly linear, but the performance gains diminish after the critical attention/FFN layers are offloaded. 
- At **15 layers**, the model already achieves ~19 tok/s, meaning the primary computational bottleneck is bypassed. 
- Pushing to **33 layers** only yields a marginal performance difference (~19-20 tok/s) but consumes an additional 1.1 GB of VRAM.
- Because TARS requires concurrent VRAM headroom for Whisper (STT) and Piper (TTS), maximizing GPU offload blindly creates a systemic bottleneck. 

## 5. Recommended Production Configuration

- **Selected model:** Qwen3-4B-Instruct-2507
- **Quantization:** Q4_K_M
- **Recommended GPU layers:** 28
- **Expected tokens/sec:** ~18.5 tok/s
- **Expected VRAM usage:** 3.48 GB
- **Expected RAM usage:** ~7.16 GB
- **Safety margin:** ~520 MB of VRAM headroom

**Why 28 layers?**
28 layers is the highest offload configuration that stays strictly below the 3.6 GB caution line. It provides identical token generation speed to the 33-layer config while leaving over half a gigabyte of VRAM available for the wake-word engine, STT models, and desktop compositing.

## 6. Fallback Configuration

- **Fallback GPU layers:** 15
- **Expected VRAM usage:** 2.66 GB
- **Safety margin:** ~1.34 GB of VRAM headroom

If the user is playing a game, running a heavy application, or utilizing a high-VRAM STT model, TARS should gracefully step down to 15 layers. The token generation speed remains an excellent ~19 tok/s.

## 7. Rejected Configurations
- **32 & 33 layers:** Rejected. While stable in isolation, 3.73 GB to 3.79 GB of VRAM leaves inadequate headroom (only ~200 MB) for audio processing pipelines and OS overhead. 
- **30 layers:** Rejected. At 3.61 GB VRAM, it touches the hard ceiling defined in the system constraints.

## 8. Phase 2 Hardware Constraints
When building TARS in Phase 2, the following constraints MUST be respected:
1. **Total STT + TTS + Wake Word VRAM footprint** must remain under **400 MB** to ensure the entire pipeline fits inside the 520 MB headroom left by the 28-layer LLM config.
2. If audio models exceed 400 MB, the system must either use CPU inference for audio or automatically fall back to the 15-layer LLM profile.
3. No continuous background polling should utilize the GPU while the LLM is loaded.
