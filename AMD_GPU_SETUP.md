# 🔴 AMD RADEON GPU SETUP GUIDE

## Your Hardware
- **CPU**: AMD Ryzen 5
- **GPU**: AMD Radeon RX series
- **Platform**: ROCm (AMD's alternative to CUDA)

## Important Note

⚠️ **AMD GPU support for PyTorch is LIMITED on Windows**

- PyTorch with ROCm officially supports **Linux only**
- Windows support for AMD GPUs is experimental and limited
- Most deep learning frameworks prioritize NVIDIA CUDA

## Options for AMD GPU Users

### Option 1: Use CPU (Current - Recommended for Windows)

**Pros:**
- ✅ Works out of the box
- ✅ No setup required
- ✅ Stable and reliable

**Cons:**
- ❌ Slower (5-10x slower than GPU)

**Current Performance:**
- 1 min video: 5-10 minutes
- 5 min video: 25-50 minutes

### Option 2: DirectML (Windows - Experimental)

DirectML is Microsoft's machine learning acceleration that works with AMD GPUs on Windows.

**Installation:**
```bash
pip install torch-directml
```

**Modify detector.py:**
```python
import torch_directml

# Use DirectML device
device = torch_directml.device()
model = YOLO("yolov8n.pt")
# Note: YOLOv8 may not fully support DirectML
```

**Pros:**
- ✅ Works on Windows
- ✅ Supports AMD GPUs
- ✅ Some acceleration possible

**Cons:**
- ❌ Limited framework support
- ❌ Slower than CUDA
- ❌ May not work with all models
- ❌ Experimental/unstable

**Expected Performance:**
- 2-3x faster than CPU (not 10x like NVIDIA)

### Option 3: ROCm on Linux (Best Performance)

If you can dual-boot or use Linux:

**Supported Linux Distributions:**
- Ubuntu 20.04/22.04
- RHEL 8/9
- SLES 15

**Installation (Ubuntu):**
```bash
# Install ROCm
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/focal/amdgpu-install_5.7.50700-1_all.deb
sudo apt install ./amdgpu-install_5.7.50700-1_all.deb
sudo amdgpu-install --usecase=rocm

# Install PyTorch with ROCm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

**Pros:**
- ✅ Full AMD GPU support
- ✅ Good performance (5-8x faster than CPU)
- ✅ Official PyTorch support

**Cons:**
- ❌ Requires Linux
- ❌ Complex setup
- ❌ Still slower than NVIDIA

### Option 4: Quick CPU Optimizations (Recommended)

Since GPU acceleration is limited for AMD on Windows, let's optimize CPU performance instead:

**Implement these for 5-7x speedup:**

1. **Frame Skipping** (Fastest improvement)
2. **Lower Resolution**
3. **Multiprocessing**
4. **Disable Color Detection** (optional)

See `PERFORMANCE_OPTIMIZATION_GUIDE.md` for details.

## Recommended Solution for You

### Best Option: CPU Optimizations

Since you're on Windows with AMD GPU, I recommend implementing CPU optimizations instead of trying GPU acceleration:

**Step 1: Add Frame Skipping**
```python
# In main.py
FRAME_SKIP = 5  # Process every 5th frame
```

**Step 2: Lower Resolution**
```python
# Resize frames to 640px
frame = cv2.resize(frame, (640, 360))
```

**Step 3: Use Multiprocessing**
```python
# Use all CPU cores (Ryzen 5 has 6 cores)
from multiprocessing import Pool
```

**Expected Result:**
- 1 min video: 1-2 minutes (5x faster)
- 5 min video: 5-10 minutes (5x faster)

This is more practical than trying to get AMD GPU working on Windows.

## Why NVIDIA is Preferred for AI/ML

### CUDA Ecosystem
- ✅ Mature and stable (15+ years)
- ✅ Supported by all major frameworks
- ✅ Extensive documentation
- ✅ Better performance

### ROCm (AMD)
- ⚠️ Newer (5+ years)
- ⚠️ Limited framework support
- ⚠️ Linux-only for most features
- ⚠️ Smaller community

### Market Share
- NVIDIA: ~90% of AI/ML workloads
- AMD: ~5% of AI/ML workloads
- Others: ~5%

## Performance Comparison

### NVIDIA RTX 3060 (CUDA)
- 1 min video: 30-60 seconds
- 5 min video: 2-5 minutes
- **Speed: 10-20x faster than CPU**

### AMD Radeon RX (ROCm on Linux)
- 1 min video: 1-2 minutes
- 5 min video: 5-10 minutes
- **Speed: 5-8x faster than CPU**

### AMD Radeon RX (DirectML on Windows)
- 1 min video: 2-4 minutes
- 5 min video: 10-20 minutes
- **Speed: 2-3x faster than CPU**

### CPU Only (Your Current Setup)
- 1 min video: 5-10 minutes
- 5 min video: 25-50 minutes
- **Baseline**

### CPU Optimized (Recommended)
- 1 min video: 1-2 minutes
- 5 min video: 5-10 minutes
- **Speed: 5-7x faster than unoptimized CPU**

## My Recommendation

**For your AMD Ryzen 5 + Radeon RX on Windows:**

1. ✅ **Stick with CPU processing**
2. ✅ **Implement CPU optimizations** (frame skip, multiprocessing)
3. ✅ **Get 5-7x speedup** without GPU hassle
4. ❌ **Don't try DirectML** (unstable, limited support)
5. ❌ **Don't try ROCm on Windows** (not supported)

**If you want GPU acceleration:**
- Consider dual-booting Linux for ROCm
- Or consider getting an NVIDIA GPU (GTX 1660 ~$200)

## Implementation Steps

### Quick CPU Optimization (30 minutes)

Create `config.py`:
```python
# Performance Configuration
FRAME_SKIP = 5              # Process every 5th frame
MAX_FRAME_WIDTH = 640       # Resize to 640px
DETECTION_CONFIDENCE = 0.6  # Higher threshold
ENABLE_COLOR_DETECTION = True
NUM_WORKERS = 6             # Ryzen 5 has 6 cores
```

Update `main.py`:
```python
from config import *

# In video processing loop
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Skip frames
    if frame_count % FRAME_SKIP != 0:
        frame_count += 1
        continue
    
    # Resize frame
    if frame.shape[1] > MAX_FRAME_WIDTH:
        scale = MAX_FRAME_WIDTH / frame.shape[1]
        frame = cv2.resize(frame, None, fx=scale, fy=scale)
    
    # Process frame
    # ... rest of code ...
```

**Expected Result: 5-7x faster processing!**

## Summary

| Option | Speed | Difficulty | Recommended |
|--------|-------|------------|-------------|
| CPU Only | 1x | Easy | ❌ Current |
| CPU Optimized | 5-7x | Easy | ✅ **Best** |
| DirectML | 2-3x | Hard | ❌ Unstable |
| ROCm Linux | 5-8x | Very Hard | ⚠️ If Linux |
| NVIDIA GPU | 10-20x | Medium | ⚠️ Requires new GPU |

## Next Steps

1. ✅ Accept that AMD GPU won't help much on Windows
2. ✅ Implement CPU optimizations (see PERFORMANCE_OPTIMIZATION_GUIDE.md)
3. ✅ Get 5-7x speedup without GPU
4. ⚠️ Consider Linux dual-boot if you really want GPU
5. ⚠️ Consider NVIDIA GPU upgrade in future

Your Ryzen 5 CPU is actually quite capable! With optimizations, you'll get good performance without needing GPU acceleration.
