import subprocess
import time
import os
import sys

def run_tars(inputs):
    print("Starting TARS...")
    p = subprocess.Popen([sys.executable, "tars/main.py", "--fallback"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(15) # Wait for load
    
    out_lines = []
    for cmd in inputs:
        print(f"Sending: {cmd}")
        p.stdin.write(cmd + "\n")
        p.stdin.flush()
        time.sleep(2)
        
    p.stdin.write("exit\n")
    p.stdin.flush()
    try:
        out, err = p.communicate(timeout=15)
        return out
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        return out

def run_integration():
    print("Test 1: Memory Persistence - Write")
    run_tars([
        '{"name": "remember", "arguments": "{\\"category\\": \\"preference\\", \\"key\\": \\"programming_language\\", \\"content\\": \\"Python\\"}"}'
    ])
    
    print("Test 1: Memory Persistence - Read")
    out = run_tars([
        '{"name": "recall", "arguments": "{\\"query\\": \\"programming\\"}"}'
    ])
    if "Python" not in out:
        print("FAIL: Memory did not persist!")
        sys.exit(1)
        
    print("Test 2: Memory Forget")
    run_tars([
        '{"name": "forget", "arguments": "{\\"category\\": \\"preference\\", \\"key\\": \\"programming_language\\"}"}'
    ])
    out = run_tars([
        '{"name": "recall", "arguments": "{\\"query\\": \\"programming\\"}"}'
    ])
    if "Python" in out:
        print("FAIL: Memory was not forgotten!")
        sys.exit(1)
        
    print("Test 3: Personality Persistence")
    run_tars([
        '{"name": "set_personality", "arguments": "{\\"humor\\": 80, \\"honesty\\": 100, \\"emotional_expression\\": 70, \\"verbosity\\": 40, \\"formality\\": 20, \\"proactivity\\": 70}"}'
    ])
    out = run_tars([
        '{"name": "get_personality", "arguments": "{}"}'
    ])
    if "Humor: 80" not in out or "Honesty: 100" not in out:
        print("FAIL: Personality did not persist!")
        sys.exit(1)
        
    print("PASS ALL")
    
if __name__ == "__main__":
    run_integration()
