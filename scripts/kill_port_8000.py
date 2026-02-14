#!/usr/bin/env python3
"""
Kill process using port 8000
Quick utility to free up the port
"""

import os
import sys
import subprocess

def kill_port_8000():
    """Kill process using port 8000"""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if ':8000' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    print(f"Found process {pid} using port 8000")
                    
                    # Kill the process
                    subprocess.run(["taskkill", "/PID", pid, "/F"])
                    print(f"✅ Process {pid} killed successfully!")
                    return True
            
            print("ℹ️  No process found on port 8000")
            return False
            
        else:
            # Linux/Mac
            result = subprocess.run(
                ["lsof", "-ti:8000"],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                pid = result.stdout.strip()
                print(f"Found process {pid} using port 8000")
                subprocess.run(["kill", "-9", pid])
                print(f"✅ Process {pid} killed successfully!")
                return True
            else:
                print("ℹ️  No process found on port 8000")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Kill Port 8000 Utility")
    print("=" * 50)
    kill_port_8000()
    print("=" * 50)
