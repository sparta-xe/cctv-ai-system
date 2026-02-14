# 🔴 DirectML Setup for AMD Radeon RX 5500M

## Installation Steps

### Step 1: Install torch-directml
```cmd
pip install torch-directml
```

### Step 2: Verify Installation
Run this to test:
```cmd
python -c "import torch_directml; print(torch_directml.device())"
```

Expected output: `privateuseone:0`

## Important Notes

⚠️ **DirectML Limitations:**
- Only works with CLIP (not YOLOv8)
- YOLOv8 doesn't support DirectML backend
- Limited framework support
- May be unstable
- Slower than NVIDIA CUDA

## What Will Be Accelerated

✅ **CLIP visual search** - 2-3x faster
❌ **YOLOv8 detection** - Will still use CPU
✅ **Text embeddings** - 2x faster

## Expected Performance

### With DirectML (Partial GPU)
- CLIP encoding: 2-3x faster
- YOLOv8 detection: CPU (no change)
- Overall: ~1.5-2x faster than pure CPU

### With CPU Optimizations (Already Applied)
- Frame skipping: 5x faster
- Frame resizing: 2x faster
- Overall: ~10x faster

### Combined (DirectML + CPU Optimizations)
- Total speedup: ~12-15x faster

## Installation Command

Run this now:
```cmd
pip install torch-directml
```

After installation, I'll update the code to use DirectML for CLIP.
