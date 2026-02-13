"""
Startup script for CCTV AI System
Handles model downloads and starts the server
"""

import os
import sys

print("=" * 60)
print("🎥 CCTV AI System - Starting Server")
print("=" * 60)

# Pre-download models if needed
print("\n📥 Checking models...")

try:
    print("  - Loading YOLOv8 model...")
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    print("  ✅ YOLOv8 ready")
except Exception as e:
    print(f"  ⚠️  YOLOv8 warning: {e}")

try:
    print("  - Loading Sentence Transformer model...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("  ✅ Sentence Transformer ready")
except Exception as e:
    print(f"  ⚠️  Sentence Transformer warning: {e}")
    print("  ℹ️  Model will download on first use (may take a few minutes)")

print("\n🚀 Starting FastAPI server...")
print("=" * 60)
print("\n📍 Server will be available at:")
print("   http://127.0.0.1:8000")
print("   http://localhost:8000")
print("\n📚 API Documentation:")
print("   http://127.0.0.1:8000/docs")
print("\n🔐 Default Credentials:")
print("   Username: admin")
print("   Password: admin123")
print("\n⏹️  Press Ctrl+C to stop the server")
print("=" * 60)
print()

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
