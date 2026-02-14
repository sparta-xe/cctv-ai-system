#!/usr/bin/env python3
"""
AI CCTV Intelligence System - Startup Script
Handles initialization and server startup
"""

import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def kill_port_process(port=8000):
    """Kill any process using the specified port"""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    print(f"⚠️  Port {port} is in use by process {pid}")
                    print(f"   Killing process {pid}...")
                    subprocess.run(["taskkill", "/PID", pid, "/F"], 
                                 capture_output=True)
                    print(f"✅ Process killed successfully")
                    return True
        else:
            # Linux/Mac
            result = subprocess.run(
                ["lsof", f"-ti:{port}"],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                pid = result.stdout.strip()
                print(f"⚠️  Port {port} is in use by process {pid}")
                print(f"   Killing process {pid}...")
                subprocess.run(["kill", "-9", pid])
                print(f"✅ Process killed successfully")
                return True
    except Exception as e:
        print(f"⚠️  Could not check/kill port process: {e}")
    
    return False

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "storage",
        "storage/frames",
        "storage/videos",
        "storage/marked",
        "storage/highlights",
        "templates",
        "static",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "cv2",
        "ultralytics",
        "sentence_transformers",
        "faiss",
        "transformers",
        "torch"
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == "cv2":
                __import__("cv2")
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ All dependencies installed")

def main():
    """Main startup function"""
    print("=" * 60)
    print("AI CCTV Intelligence System v2.0")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    check_dependencies()
    
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    workers = int(os.getenv("WORKERS", 1))
    
    # Check and kill any process using the port
    kill_port_process(port)
    
    print(f"\n🚀 Starting server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Workers: {workers}")
    print(f"   Reload: {reload}")
    print(f"\n📱 Open browser: http://localhost:{port}")
    print(f"   Press Ctrl+C to stop\n")
    print("=" * 60)
    
    # Start server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
