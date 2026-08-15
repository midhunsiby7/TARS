import subprocess
import time
import socket
import os
import sys

def check_process_running(proc_name):
    # Use tasklist on Windows
    out = subprocess.check_output('tasklist', shell=True).decode('utf-8', errors='ignore')
    return proc_name.lower() in out.lower()

def test_orphan_process():
    print("Running orphan process test...")
    # Ensure not running initially
    if check_process_running("llama-server.exe"):
        os.system("taskkill /f /im llama-server.exe >nul 2>&1")
        time.sleep(1)
        
    # Start TARS
    print("Starting TARS...")
    tars_proc = subprocess.Popen([sys.executable, "tars/main.py", "--fallback"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for it to start up
    time.sleep(10)
    
    # Verify running
    if not check_process_running("llama-server.exe"):
        print("FAIL: llama-server.exe did not start.")
        tars_proc.kill()
        return False
        
    print("llama-server is running. Sending exit command...")
    
    # Send exit
    tars_proc.stdin.write("exit\n")
    tars_proc.stdin.flush()
    
    # Wait for shutdown
    try:
        tars_proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        print("FAIL: TARS did not shut down gracefully.")
        tars_proc.kill()
        return False
        
    time.sleep(2)
    
    if check_process_running("llama-server.exe"):
        print("FAIL: llama-server.exe was orphaned!")
        os.system("taskkill /f /im llama-server.exe >nul 2>&1")
        return False
        
    print("PASS: Clean shutdown verified. No orphan process.")
    return True

def test_port_conflict():
    print("\nRunning port conflict test...")
    # Bind to port 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', 8080))
        sock.listen(1)
    except Exception as e:
        print(f"Failed to bind mock socket: {e}")
        return False
        
    print("Mock socket bound on 8080. Starting TARS...")
    tars_proc = subprocess.Popen([sys.executable, "tars/main.py", "--fallback"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Since port is blocked, it should fail to start backend and exit quickly.
    try:
        tars_proc.wait(timeout=15)
        # Should exit with code 0 (clean graceful abort) or 1.
        out, err = tars_proc.communicate()
        if "Backend failed to start" in out or "Backend failed to start" in err:
            print("PASS: Port conflict detected and aborted gracefully.")
            sock.close()
            return True
        else:
            print("FAIL: Did not see expected abort message.")
            sock.close()
            return False
    except subprocess.TimeoutExpired:
        print("FAIL: TARS hung during port conflict.")
        tars_proc.kill()
        sock.close()
        return False

if __name__ == "__main__":
    success = True
    if not test_orphan_process():
        success = False
    if not test_port_conflict():
        success = False
        
    if not success:
        sys.exit(1)
    sys.exit(0)
