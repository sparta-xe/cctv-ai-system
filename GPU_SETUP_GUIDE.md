# 🚀 GPU ACCELERATION SETUP GUIDE

## Current Status
✅ Code is now GPU-ready!
- YOLOv8 will automatically use GPU if available
- CLIP will automatically use GPU if available
- Falls back to CPU if no GPU detected

## Requirements

### Hardware
- **NVIDIA GPU** (GTX 1050 or better)
- **Minimum**: 4GB VRAM
- **Recommended**: 6GB+ VRAM (GTX 1660, RTX 2060, RTX 3060, etc.)

### Software
- **NVIDIA Driver** (Latest version)
- **CUDA Toolkit** (11.8 or 12.1)
- **cuDNN** (Comes with PyTorch)

## Installation Steps

### Step 1: Check if You Have an NVIDIA GPU

**Windows:**
```cmd
nvidia-smi
```

**Expected Output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.2   |
|-------------------------------+----------------------+----------------------+
| GPU  Name            TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ... WDDM  | 00000000:01:00.0  On |                  N/A |
| 30%   45C    P8    15W / 170W |    500MiB /  8192MiB |      2%      Default |
+-------------------------------+----------------------+----------------------+
```

If you see this, you have an NVIDIA GPU! ✅

If you get an error, you either:
- Don't have an NVIDIA GPU
- Need to install NVIDIA drivers

### Step 2: Install NVIDIA Drivers

**Download from:**
https://www.nvidia.com/Download/index.aspx

1. Select your GPU model
2. Download the driver
3. Install and restart

### Step 3: Install CUDA-Enabled PyTorch

**Uninstall CPU version first:**
```bash
pip uninstall torch torchvision torchaudio
```

**Install GPU version (CUDA 11.8):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Or for CUDA 12.1:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Step 4: Verify GPU Installation

Create `test_gpu.py`:
```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️  No GPU detected - using CPU")
```

Run it:
```bash
python test_gpu.py
```

**Expected Output (with GPU):**
```
PyTorch version: 2.1.0+cu118
CUDA available: True
CUDA version: 11.8
GPU device: NVIDIA GeForce RTX 3060
GPU memory: 12.00 GB
```

### Step 5: Restart Your Server

```bash
python main.py
```

**You should see:**
```
🎯 YOLOv8 using device: CUDA
✅ YOLOv8 loaded on GPU: NVIDIA GeForce RTX 3060
🎯 CLIP Engine using: CUDA
✅ CLIP model loaded successfully
```

## Performance Comparison

### CPU (Intel i7)
- 1 minute video: ~5-10 minutes
- 5 minute video: ~25-50 minutes
- Frame processing: ~2-3 seconds/frame

### GPU (RTX 3060)
- 1 minute video: ~30-60 seconds
- 5 minute video: ~2-5 minutes
- Frame processing: ~0.1-0.2 seconds/frame

**Speed Improvement: 10-20x faster!**

## Troubleshooting

### Issue 1: "CUDA out of memory"

**Solution 1: Reduce batch size**
```python
# In clip_engine.py
BATCH_SIZE = 8  # Reduce from 32
```

**Solution 2: Process fewer frames**
```python
# In main.py
FRAME_SKIP = 10  # Process every 10th frame
```

**Solution 3: Use smaller model**
```python
# In detector.py
model = YOLO("yolov8n.pt")  # Already using smallest
```

### Issue 2: "CUDA not available" after installation

**Check PyTorch installation:**
```python
import torch
print(torch.__version__)
# Should show: 2.x.x+cu118 or cu121
# If it shows: 2.x.x+cpu, reinstall with CUDA
```

**Reinstall with correct CUDA version:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue 3: "RuntimeError: CUDA error: no kernel image"

**Your GPU is too old for this CUDA version.**

**Solution: Use older CUDA version**
```bash
pip uninstall torch torchvision torchaudio
pip install torch==2.0.0+cu117 torchvision==0.15.0+cu117 --index-url https://download.pytorch.org/whl/cu117
```

### Issue 4: GPU not being used

**Check device in code:**
```python
import torch
print(f"Device: {torch.cuda.is_available()}")
```

**Force GPU usage:**
```python
# In detector.py
device = 'cuda'  # Remove the if statement
```

## GPU Memory Management

### Monitor GPU Usage

**Windows:**
```cmd
nvidia-smi -l 1
```
This updates every second.

**Check memory in Python:**
```python
import torch
print(f"Allocated: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB")
print(f"Cached: {torch.cuda.memory_reserved(0) / 1e9:.2f} GB")
```

### Clear GPU Memory

```python
import torch
torch.cuda.empty_cache()
```

## Recommended GPU Settings

### For 4GB VRAM (GTX 1050 Ti)
```python
FRAME_SKIP = 5
MAX_FRAME_WIDTH = 640
BATCH_SIZE = 4
```

### For 6GB VRAM (GTX 1660)
```python
FRAME_SKIP = 3
MAX_FRAME_WIDTH = 1280
BATCH_SIZE = 8
```

### For 8GB+ VRAM (RTX 2060, 3060)
```python
FRAME_SKIP = 2
MAX_FRAME_WIDTH = 1920
BATCH_SIZE = 16
```

### For 12GB+ VRAM (RTX 3080, 4080)
```python
FRAME_SKIP = 1  # Process all frames
MAX_FRAME_WIDTH = 1920
BATCH_SIZE = 32
```

## Cloud GPU Options

### If You Don't Have a GPU

**Google Colab (Free)**
- Free GPU access (T4)
- 12GB VRAM
- Limited to 12 hours
- https://colab.research.google.com

**Kaggle (Free)**
- Free GPU access (P100)
- 16GB VRAM
- 30 hours/week
- https://www.kaggle.com

**AWS EC2 (Paid)**
- g4dn.xlarge: $0.526/hour (T4, 16GB)
- p3.2xlarge: $3.06/hour (V100, 16GB)
- https://aws.amazon.com/ec2/instance-types/

**Google Cloud (Paid)**
- n1-standard-4 + T4: $0.35/hour
- https://cloud.google.com/compute

## Verification Checklist

After setup, verify:
- ✅ `nvidia-smi` shows your GPU
- ✅ `torch.cuda.is_available()` returns `True`
- ✅ Server logs show "CUDA" not "CPU"
- ✅ Processing is significantly faster
- ✅ GPU usage shows in `nvidia-smi`

## Expected Startup Messages

**With GPU:**
```
🎯 YOLOv8 using device: CUDA
✅ YOLOv8 loaded on GPU: NVIDIA GeForce RTX 3060
🎯 CLIP Engine using: CUDA
✅ CLIP model loaded successfully
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Without GPU (CPU fallback):**
```
🎯 YOLOv8 using device: CPU
⚠️  GPU not available, using CPU (slower)
🎯 CLIP Engine using: CPU
✅ CLIP model loaded successfully
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Next Steps

1. ✅ Install NVIDIA drivers
2. ✅ Install CUDA-enabled PyTorch
3. ✅ Run `test_gpu.py` to verify
4. ✅ Restart server
5. ✅ Upload a video and see the speed!

## Support

If you encounter issues:
1. Check `nvidia-smi` output
2. Verify PyTorch CUDA version
3. Check GPU memory usage
4. Try reducing batch size
5. Check CUDA compatibility with your GPU

Your code is now GPU-ready! Just install the drivers and CUDA-enabled PyTorch.
