"""
Start CCTV AI System on port 8080 (alternative port)
Use this if port 8000 is already in use
"""

import uvicorn
import os

if __name__ == "__main__":
    print("=" * 60)
    print("🎥 CCTV AI System - Starting on Port 8080")
    print("=" * 60)
    print("\n📍 Server will be available at:")
    print("   http://127.0.0.1:8080")
    print("   http://localhost:8080")
    print("\n📚 API Documentation:")
    print("   http://127.0.0.1:8080/docs")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Ensure directories exist
    os.makedirs("storage/frames", exist_ok=True)
    os.makedirs("storage/videos", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    # Start server on port 8080
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
