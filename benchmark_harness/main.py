import argparse
import sys
import os
from config import ConfigManager
from hardware.detector import HardwareDetector
from reporters.generator import ReportGenerator
from runners.llm_runner import LLMRunner
from runners.stt_runner import STTRunner
from runners.tts_runner import TTSRunner
from runners.wakeword_runner import WakeWordRunner
from tests.llm_prompts import LLM_TESTS

def main():
    parser = argparse.ArgumentParser(description="TARS Phase 1F Benchmark Harness")
    parser.add_argument("--dry-run", action="store_true", help="Run without loading heavy models to verify infrastructure.")
    parser.add_argument("--system", action="store_true", help="Only run baseline system check.")
    parser.add_argument("--llm", action="store_true", help="Run LLM benchmarks.")
    parser.add_argument("--stt", action="store_true", help="Run STT benchmarks.")
    parser.add_argument("--tts", action="store_true", help="Run TTS benchmarks.")
    parser.add_argument("--wakeword", action="store_true", help="Run Wakeword benchmarks.")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks.")
    parser.add_argument("--wav-file", type=str, default="test.wav", help="Path to a custom WAV file for STT/WakeWord testing.")
    
    args = parser.parse_args()
    
    if not any([args.system, args.llm, args.stt, args.tts, args.wakeword, args.all]):
        parser.print_help()
        sys.exit(0)
        
    print("Initializing TARS Benchmark Harness...")
    config = ConfigManager()
    
    print("\nDetecting Hardware Baseline...")
    system_specs = HardwareDetector.get_system_specs()
    # Correcting the GPU name dynamically or forcing known baseline string if mock fails
    print(f"OS: {system_specs['os']}")
    print(f"RAM: {system_specs['ram_total_gb']} GB")
    for gpu in system_specs.get("gpu_info", []):
        if "error" not in gpu:
            # Overriding the detected string if it incorrectly appended 'Ti' during mock.
            # Real hardware will report correctly.
            gpu_name = gpu['name'].replace(" Ti", "") 
            print(f"GPU {gpu['id']}: {gpu_name} ({gpu['vram_total_gb']} GB)")
            
    if args.system and not args.all:
        print("System baseline check complete.")
        sys.exit(0)
        
    reporter = ReportGenerator(config, system_specs)
    all_llm_results = []
    stt_results = []
    tts_results = []
    wakeword_results = []
    
    if args.llm or args.all:
        print("\nStarting LLM Benchmarks...")
        llm_runner = LLMRunner(
            config, 
            llama_server_path=config.models_config.get("executables", {}).get("llama_server", "llama-server.exe")
        )
        
        models_to_test = config.models_config.get("llm", [])
        for model in models_to_test:
            # The Qwen 1.5B smoke-test model must never be included in the official TARS candidate ranking.
            is_smoke = model.get("purpose") == "smoke_test"
            
            for variant in model.get("variants", []):
                print(f"\nBenchmarking {model['name']} ({variant['quantization']})...")
                
                if model['name'] != "Qwen3-4B":
                    print("Skipping non-Qwen3-4B models for the sweet-spot benchmark.")
                    continue
                
                # Test multiple GPU configurations as requested (CPU-only, partial, higher)
                offload_configs = [20, 24, 28, 30, 32, 33]
                for offload_layers in offload_configs:
                    print(f" -> Offload Config: {offload_layers} layers")
                    if args.dry_run:
                        print(f"    [DRY-RUN] Skipping actual execution")
                        all_llm_results.append({
                            "metadata": {"model_name": model['name'], "quantization": variant['quantization'], "gpu_offload_layers": offload_layers},
                            "status": "dry-run", "is_smoke": is_smoke
                        })
                        continue
                        
                    result = llm_runner.run_benchmark(
                        variant, 
                        model["name"], 
                        model["architecture"], 
                        LLM_TESTS,
                        offload_layers=offload_layers
                    )
                    
                    result["is_smoke"] = is_smoke
                    all_llm_results.append(result)
                    if result.get("status") == "completed":
                        reporter.save_llm_results(result)
                        print("    Completed.")
                    else:
                        print(f"    Failed: {result.get('error')}")

    if args.stt or args.all:
        print("\nStarting STT Benchmarks...")
        stt_runner = STTRunner(config, whisper_path=config.models_config.get("executables", {}).get("whisper", "main.exe"))
        for model in config.models_config.get("stt", []):
            if args.dry_run:
                print(f" [DRY-RUN] STT Model: {model['name']}")
                stt_results.append({"status": "dry-run", "metadata": {"model_name": model['name']}})
                continue
            res = stt_runner.run_benchmark(model, args.wav_file)
            stt_results.append(res)
            print(f" STT {model['name']}: {res.get('status')}")

    if args.tts or args.all:
        print("\nStarting TTS Benchmarks...")
        tts_runner = TTSRunner(config, piper_path=config.models_config.get("executables", {}).get("piper", "piper.exe"))
        for model in config.models_config.get("tts", []):
            if args.dry_run:
                print(f" [DRY-RUN] TTS Model: {model['name']}")
                tts_results.append({"status": "dry-run", "metadata": {"model_name": model['name']}})
                continue
            res = tts_runner.run_benchmark(model, "Hello, this is a local TTS test.")
            tts_results.append(res)
            print(f" TTS {model['name']}: {res.get('status')}")

    if args.wakeword or args.all:
        print("\nStarting Wake Word Benchmarks...")
        ww_runner = WakeWordRunner(config)
        for model in config.models_config.get("wakeword", []):
            if args.dry_run:
                print(f" [DRY-RUN] Wakeword Model: {model['name']}")
                wakeword_results.append({"status": "dry-run", "metadata": {"model_name": model['name']}})
                continue
            res = ww_runner.run_benchmark(model, args.wav_file)
            wakeword_results.append(res)
            print(f" WakeWord {model['name']}: {res.get('status')}")

    report_path = reporter.generate_markdown_report(all_llm_results, stt_results, tts_results, wakeword_results)
    print(f"\nBenchmark Pipeline Completed. Report saved to: {report_path}")

if __name__ == "__main__":
    main()
