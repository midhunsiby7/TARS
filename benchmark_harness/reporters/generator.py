import json
import os
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    def __init__(self, config_manager, system_specs):
        self.config = config_manager
        self.system_specs = system_specs
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = self.config.results_dir / f"run_{timestamp}"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        self.reports_dir = self.run_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        with open(self.run_dir / "system.json", "w") as f:
            json.dump(self.system_specs, f, indent=2)

    def save_llm_results(self, results):
        llm_dir = self.run_dir / "llm"
        llm_dir.mkdir(exist_ok=True)
        filename = f"{results['metadata']['model_name']}_{results['metadata']['quantization']}_ngl{results['metadata']['gpu_offload_layers']}.json"
        with open(llm_dir / filename, "w") as f:
            json.dump(results, f, indent=2)
            
    def _format_status(self, status):
        if status == "dry-run":
            return "🔲 Not tested (Dry-run)"
        elif status == "completed":
            return "✅ Implemented and Tested"
        elif status == "failed":
            return "❌ Failed (Dependency/Environment)"
        return "⚠️ Unavailable"

    def generate_markdown_report(self, all_llm_results, stt_results, tts_results, wakeword_results):
        report_path = self.reports_dir / "report.md"
        
        lines = [
            "# TARS Benchmark Harness Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 1. System Baseline",
            f"- **OS:** {self.system_specs.get('os')}",
            f"- **CPU:** {self.system_specs.get('cpu_architecture')} ({self.system_specs.get('cpu_cores_physical')} cores)",
            f"- **RAM:** {self.system_specs.get('ram_total_gb')} GB",
        ]
        
        gpus = self.system_specs.get("gpu_info", [])
        if gpus:
            for gpu in gpus:
                if "error" not in gpu:
                    gpu_name = gpu['name'].replace(" Ti", "")
                    lines.append(f"- **GPU {gpu['id']}:** {gpu_name} ({gpu['vram_total_gb']} GB VRAM)")
        
        lines.extend(["", "## 2. LLM Benchmark Results", ""])
        
        official_candidates = [r for r in all_llm_results if not r.get("is_smoke")]
        smoke_tests = [r for r in all_llm_results if r.get("is_smoke")]
        
        if smoke_tests:
            lines.append("### 🚬 Infrastructure Verification (Smoke Tests)")
            lines.append("> [!WARNING]")
            lines.append("> These models are used ONLY to verify the benchmark infrastructure and are EXCLUDED from the official TARS candidate ranking.")
            lines.append("")
            self._append_llm_results(lines, smoke_tests)
            lines.append("---")
            
        lines.append("### 🏆 Official TARS Candidates")
        self._append_llm_results(lines, official_candidates)

        lines.extend(["", "## 3. STT Benchmark Results (Whisper.cpp)", ""])
        for res in stt_results:
            meta = res.get("metadata", {})
            lines.append(f"### {meta.get('model_name')}")
            lines.append(f"Status: {self._format_status(res.get('status'))}")
            if res.get("status") == "completed":
                lines.append(f"- **Latency:** {res.get('metrics', {}).get('latency_seconds', 0):.2f} s")
                if "wer" in res.get("metrics", {}):
                    lines.append(f"- **Accuracy (WER):** {res.get('metrics')['wer']:.2%}")
            elif res.get("status") == "failed":
                lines.append(f"- **Error:** {res.get('error')}")

        lines.extend(["", "## 4. TTS Benchmark Results (Piper)", ""])
        for res in tts_results:
            meta = res.get("metadata", {})
            lines.append(f"### {meta.get('model_name')}")
            lines.append(f"Status: {self._format_status(res.get('status'))}")
            if res.get("status") == "completed":
                lines.append(f"- **Synthesis Time:** {res.get('metrics', {}).get('synthesis_time_seconds', 0):.2f} s")
            elif res.get("status") == "failed":
                lines.append(f"- **Error:** {res.get('error')}")

        lines.extend(["", "## 5. Wake Word Benchmark Results (openWakeWord)", ""])
        for res in wakeword_results:
            meta = res.get("metadata", {})
            lines.append(f"### {meta.get('model_name')}")
            lines.append(f"Status: {self._format_status(res.get('status'))}")
            if res.get("status") == "completed":
                lines.append(f"- **Load Time:** {res.get('metrics', {}).get('load_time_seconds', 0):.2f} s")
                lines.append(f"- **Processing Latency:** {res.get('metrics', {}).get('processing_latency_seconds', 0):.2f} s")
                lines.append(f"- **Detections:** {res.get('metrics', {}).get('detections', 0)}")
            elif res.get("status") == "failed":
                lines.append(f"- **Error:** {res.get('error')}")
            
        with open(report_path, "w") as f:
            f.write("\n".join(lines))
            
        with open(self.reports_dir / "summary.json", "w") as f:
            json.dump({
                "system": self.system_specs,
                "llm": all_llm_results,
                "stt": stt_results,
                "tts": tts_results,
                "wakeword": wakeword_results
            }, f, indent=2)
            
        return report_path

    def _append_llm_results(self, lines, results):
        if not results:
            lines.append("*No models benchmarked in this category.*")
            return
            
        for res in results:
            meta = res.get("metadata", {})
            impact = res.get("system_impact", {})
            
            lines.append(f"#### {meta.get('model_name')} ({meta.get('quantization')} | {meta.get('gpu_offload_layers')} GPU Layers)")
            lines.append(f"Status: {self._format_status(res.get('status'))}")
            
            if res.get("status") == "completed":
                lines.append(f"- **Load Time:** {meta.get('load_time_seconds', 0):.2f} s")
                if "gpu" in impact:
                    lines.append(f"- **Peak VRAM:** {impact['gpu']['vram_max_gb']:.2f} GB")
                lines.append(f"- **Peak RAM:** {impact['ram']['max_gb']:.2f} GB")
                lines.append("- **Test Metrics:**")
                for test in res.get("tests", []):
                    t_name = test.get("test_name", "Unknown")
                    t_stat = "SUCCESS" if test.get("status") == "success" else "FAILED"
                    lat = test.get("latency_seconds", 0)
                    tps = test.get("timings", {}).get("predicted_per_second", 0) if "timings" in test else 0
                    lines.append(f"  - {t_name}: {t_stat} ({lat:.2f}s, {tps:.2f} tok/s)")
            elif res.get("status") == "failed":
                lines.append(f"- **Error:** {res.get('error')}")
            lines.append("")
