"""
Fix port 8000 already in use issue
Run this to start the server on a different port or kill existing process
"""

import subprocess
import sys
import os

def find_process_on_port(port=8000):
    """Find process using the specified port"""
    try:
        # Windows command to find process on port
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(f"Process found on port {port}:")
            print(result.stdout)
            
            # Extract PID
            lines = result.stdout.strip().split('\n')
            if lines:
                parts = lines[0].split()
                if parts:
                    pid = parts[-1]
                    print(f"\nProcess ID (PID): {pid}")
                    return pid
        else:
            print(f"No process found on port {port}")
            return None
    except Exception as e:
        print(f"Error finding process: {e}")
        return None

def kill_process(pid):
    """Kill process by PID"""
    try:
        subprocess.run(f'taskkill /F /PID {pid}', shell=True, check=True)
        print(f"✅ Process {pid} killed successfully")
        return True
    except Exception as e:
        print(f"❌ Error killing process: {e}")
        return False

def start_server_on_different_port(port=8080):
    """Start server on different port"""
    print(f"\n🚀 Starting server on port {port}...")
    print(f"Open: http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop\n")
    
    try:
        subprocess.run(
            f'python -m uvicorn main:app --host 0.0.0.0 --port {port}',
            shell=True
        )
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")

def main():
    print("=" * 60)
    print("🔧 Port 8000 Issue Fixer")
    print("=" * 60)
    
    print("\nOptions:")
    print("1. Kill process on port 8000 and start server")
    print("2. Start server on different port (8080)")
    print("3. Just show what's using port 8000")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🔍 Finding process on port 8000...")
        pid = find_process_on_port(8000)
        
        if pid:
            confirm = input(f"\nKill process {pid}? (y/n): ").strip().lower()
            if confirm == 'y':
                if kill_process(pid):
                    print("\n✅ Port 8000 is now free!")
                    print("Starting server on port 8000...")
                    start_server_on_different_port(8000)
        else:
            print("\n✅ Port 8000 is already free!")
            print("Starting server on port 8000...")
            start_server_on_different_port(8000)
    
    elif choice == "2":
        print("\n🚀 Starting server on port 8080...")
        start_server_on_different_port(8080)
    
    elif choice == "3":
        print("\n🔍 Checking port 8000...")
        find_process_on_port(8000)
    
    elif choice == "4":
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    main()
