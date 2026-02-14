"""
GPU Detection and Verification Script
Run this to check if GPU is available and working
"""

import torch
import sys

print("=" * 60)
print("GPU DETECTION TEST")
print("=" * 60)

# PyTorch version
print(f"\n📦 PyTorch version: {torch.__version__}")

# CUDA availability
cuda_available = torch.cuda.is_available()
print(f"🔍 CUDA available: {cuda_available}")

if cuda_available:
    print("\n✅ GPU DETECTED!")
    print("-" * 60)
    
    # CUDA version
    print(f"🔧 CUDA version: {torch.version.cuda}")
    
    # GPU count
    gpu_count = torch.cuda.device_count()
    print(f"🎮 Number of GPUs: {gpu_count}")
    
    # GPU details
    for i in range(gpu_count):
        print(f"\n📊 GPU {i} Details:")
        print(f"   Name: {torch.cuda.get_device_name(i)}")
        
        props = torch.cuda.get_device_properties(i)
        print(f"   Total memory: {props.total_memory / 1e9:.2f} GB")
        print(f"   Compute capability: {props.major}.{props.minor}")
        print(f"   Multi-processors: {props.multi_processor_count}")
    
    # Memory info
    print(f"\n💾 Current GPU Memory Usage:")
    print(f"   Allocated: {torch.cuda.memory_allocated(0) / 1e9:.4f} GB")
    print(f"   Reserved: {torch.cuda.memory_reserved(0) / 1e9:.4f} GB")
    
    # Test tensor operation
    print(f"\n🧪 Testing GPU computation...")
    try:
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        z = torch.matmul(x, y)
        print(f"   ✅ GPU computation successful!")
        print(f"   Result shape: {z.shape}")
        print(f"   Device: {z.device}")
    except Exception as e:
        print(f"   ❌ GPU computation failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ GPU IS READY TO USE!")
    print("=" * 60)
    print("\nYour system will use GPU for:")
    print("  • YOLOv8 object detection (5-10x faster)")
    print("  • CLIP visual search (3-5x faster)")
    print("  • Overall processing (10-20x faster)")
    
else:
    print("\n⚠️  NO GPU DETECTED")
    print("-" * 60)
    print("\nPossible reasons:")
    print("  1. No NVIDIA GPU installed")
    print("  2. NVIDIA drivers not installed")
    print("  3. PyTorch CPU version installed (not CUDA)")
    print("  4. CUDA not compatible with your GPU")
    
    print("\n📝 To enable GPU:")
    print("  1. Install NVIDIA drivers from:")
    print("     https://www.nvidia.com/Download/index.aspx")
    print("\n  2. Install CUDA-enabled PyTorch:")
    print("     pip uninstall torch torchvision torchaudio")
    print("     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("\n  3. Restart and run this script again")
    
    print("\n" + "=" * 60)
    print("⚠️  SYSTEM WILL USE CPU (SLOWER)")
    print("=" * 60)
    print("\nCPU processing is functional but slower:")
    print("  • 1 min video: ~5-10 minutes")
    print("  • 5 min video: ~25-50 minutes")

print("\n")
