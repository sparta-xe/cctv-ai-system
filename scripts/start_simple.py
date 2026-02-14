"""
Simple startup script that handles common issues
"""

import os
import sys
import time

print("=" * 60)
print("🎥 CCTV AI System - Simple Startup")
print("=" * 60)

# Step 1: Create directories
print("\n📁 Creating directories...")
os.makedirs("storage/frames", exist_ok=True)
os.makedirs("storage/videos", exist_ok=True)
os.makedirs("templates", exist_ok=True)
print("✅ Directories ready")

# Step 2: Pre-load models (with timeout handling)
print("\n📥 Loading AI models (this may take a moment)...")
print("   If this hangs, it's downloading models from internet...")

try:
    # Load YOLO
    print("   - Loading YOLOv8...")
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    print("   ✅ YOLOv8 ready")
    
    # Load Sentence Transformer (may timeout on first run)
    print("   - Loading Sentence Transformer...")
    print("     (This may take 1-2 minutes on first run)")
    from sentence_transformers import SentenceTransformer
    
    # Set longer timeout
    import socket
    socket.setdefaulttimeout(60)
    
    st_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("   ✅ Sentence Transformer ready")
    
except Exception as e:
    print(f"   ⚠️  Warning: {e}")
    print("   Models will load when needed (may be slower)")

# Step 3: Start server
print("\n🚀 Starting server...")
print("\n📍 Server will be available at:")
print("   http://127.0.0.1:8080")
print("   http://localhost:8080")
print("\n📚 API Documentation:")
print("   http://127.0.0.1:8080/docs")
print("\n⏹️  Press Ctrl+C to stop")
print("=" * 60)
print()

# Import and start
try:
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False, log_level="info")
except KeyboardInterrupt:
    print("\n\n✅ Server stopped gracefully")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure no other server is running")
    print("2. Check if port 8080 is available")
    print("3. Try: python -m uvicorn main:app --port 8081")
