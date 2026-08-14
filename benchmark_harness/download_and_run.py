import urllib.request
import os
import subprocess
import time

MODELS_DIR = r"D:\TARS\benchmark_models"

CANDIDATES = [
    {
        "name": "Gemma-4-E4B",
        "url": "https://huggingface.co/ggml-org/gemma-4-E4B-it-GGUF/resolve/main/gemma-4-E4B-it-Q4_0.gguf?download=true",
        "filename": "gemma-4-E4B-it-Q4_0.gguf"
    },
    {
        "name": "Qwen3-4B-Instruct-2507",
        "url": "https://huggingface.co/oakdream/Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen3-4B-Instruct-2507-Q4_K_M.gguf?download=true",
        "filename": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
    },
    {
        "name": "Qwen3.5-4B-Instruct",
        "url": "https://huggingface.co/openresearchtools/Qwen3.5-4B-Instruct-GGUF/resolve/main/qwen3.5-4b-instruct-Q4_K_M.gguf?download=true",
        "filename": "qwen3.5-4b-instruct-Q4_K_M.gguf"
    }
]

def download_file(url, filepath):
    if os.path.exists(filepath):
        print(f"[SKIP] File {filepath} already exists. Skipping download.")
        return True
        
    print(f"[DOWNLOAD] Starting download for {filepath}...")
    try:
        # Use a custom user agent to avoid blocking
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            # Simple chunked download with progress
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 8192 * 4
            last_print = 0
            
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                out_file.write(buffer)
                downloaded += len(buffer)
                
                # Print progress every ~100MB
                if downloaded - last_print > 100 * 1024 * 1024:
                    print(f"  ... downloaded {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB")
                    last_print = downloaded
                    
        print(f"[DOWNLOAD SUCCESS] Downloaded {os.path.getsize(filepath) / (1024*1024):.2f} MB")
        return True
    except Exception as e:
        print(f"[DOWNLOAD FAILED] Error downloading {url}: {e}")
        return False

def run_benchmark():
    print(f"[BENCHMARK] Running main.py --llm...")
    python_exe = r"D:\TARS\.venv\Scripts\python.exe"
    benchmark_script = r"D:\TARS\benchmark_harness\main.py"
    
    process = subprocess.Popen(
        [python_exe, benchmark_script, "--llm"],
        cwd=r"D:\TARS",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    for line in process.stdout:
        print(line, end="")
        
    process.wait()
    print(f"[BENCHMARK] Finished with return code {process.returncode}")

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    for candidate in CANDIDATES:
        print(f"\n{'='*50}")
        print(f"PROCESSING CANDIDATE: {candidate['name']}")
        print(f"{'='*50}")
        
        filepath = os.path.join(MODELS_DIR, candidate["filename"])
        
        # 1. Download
        success = download_file(candidate["url"], filepath)
        if not success:
            print(f"Skipping benchmark for {candidate['name']} due to download failure.")
            continue
            
        # 2. Benchmark
        run_benchmark()
        
        # Give system a moment to settle
        time.sleep(5)

if __name__ == "__main__":
    main()
