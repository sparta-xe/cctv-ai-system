# ⚡ VIDEO PROCESSING PERFORMANCE OPTIMIZATION GUIDE

## Current Bottlenecks

### Processing Pipeline
1. **Frame Extraction** - Reading video frames (I/O bound)
2. **Object Detection** - YOLOv8 inference (CPU/GPU bound)
3. **Color Detection** - HSV analysis (CPU bound)
4. **CLIP Embedding** - Visual encoding (CPU/GPU bound)
5. **Frame Annotation** - Drawing boxes (CPU bound)
6. **Storage** - Writing files (I/O bound)

## Quick Wins (Immediate Improvements)

### 1. Skip Frames (Fastest Method)
Process every Nth frame instead of every frame.

**Current**: Process every frame (30 FPS = 30 frames/sec)
**Optimized**: Process every 5th frame (6 frames/sec)

```python
# In main.py, modify upload endpoint
FRAME_SKIP = 5  # Process every 5th frame

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Skip frames
    if frame_count % FRAME_SKIP != 0:
        frame_count += 1
        continue
    
    # Process this frame
    # ... detection code ...
    frame_count += 1
```

**Speed Improvement**: 5x faster (for FRAME_SKIP=5)
**Trade-off**: May miss fast-moving objects

### 2. Lower Resolution
Resize frames before processing.

```python
# Resize frame before detection
def resize_frame(frame, max_width=640):
    h, w = frame.shape[:2]
    if w > max_width:
        scale = max_width / w
        new_w = int(w * scale)
        new_h = int(h * scale)
        frame = cv2.resize(frame, (new_w, new_h))
    return frame

# In processing loop
frame = resize_frame(frame, max_width=640)
```

**Speed Improvement**: 2-3x faster
**Trade-off**: Lower detection accuracy for small objects

### 3. Reduce Detection Confidence
Lower the confidence threshold to skip uncertain detections.

```python
# In detector.py
detections = detect(image_path, confidence_threshold=0.6)  # Increase from 0.5
```

**Speed Improvement**: 10-20% faster
**Trade-off**: May miss some objects

### 4. Disable Color Detection (Optional)
Skip color detection if not needed.

```python
# In detector.py
detections = detect(image_path, detect_colors=False)
```

**Speed Improvement**: 20-30% faster
**Trade-off**: No color information

## Medium Optimizations (Requires Code Changes)

### 5. Parallel Processing with Multiprocessing

```python
# Create optimized_processor.py
from multiprocessing import Pool, cpu_count
import cv2
from detector import detect

def process_frame_batch(args):
    """Process a batch of frames in parallel"""
    frame_paths, frame_indices = args
    results = []
    
    for frame_path, idx in zip(frame_paths, frame_indices):
        detections = detect(frame_path, confidence_threshold=0.5)
        results.append({
            "frame_index": idx,
            "detections": detections,
            "image": frame_path
        })
    
    return results

def process_video_parallel(video_path, num_workers=None):
    """Process video using multiple CPU cores"""
    if num_workers is None:
        num_workers = cpu_count() - 1  # Leave one core free
    
    # Extract frames
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save frame
        frame_path = f"temp_frame_{frame_idx}.jpg"
        cv2.imwrite(frame_path, frame)
        frames.append((frame_path, frame_idx))
        frame_idx += 1
    
    cap.release()
    
    # Split into batches
    batch_size = len(frames) // num_workers
    batches = [frames[i:i+batch_size] for i in range(0, len(frames), batch_size)]
    
    # Process in parallel
    with Pool(num_workers) as pool:
        results = pool.map(process_frame_batch, batches)
    
    # Flatten results
    all_results = [item for batch in results for item in batch]
    
    return all_results
```

**Speed Improvement**: 3-4x faster (on 4-core CPU)
**Trade-off**: Higher memory usage

### 6. Use GPU Acceleration

```python
# Install CUDA-enabled PyTorch
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# In detector.py
from ultralytics import YOLO

# Load model with GPU
model = YOLO("yolov8n.pt")
model.to('cuda')  # Move to GPU

# In clip_engine.py
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
```

**Speed Improvement**: 5-10x faster
**Requirements**: NVIDIA GPU with CUDA

### 7. Batch Processing for CLIP

```python
# In clip_engine.py
def index_images_batch(image_paths, batch_size=32):
    """Process images in batches for faster encoding"""
    all_embeddings = []
    
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        images = [Image.open(path) for path in batch]
        
        # Process batch
        inputs = processor(images=images, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            embeddings = model.get_image_features(**inputs)
        
        all_embeddings.append(embeddings.cpu().numpy())
    
    return np.vstack(all_embeddings)
```

**Speed Improvement**: 2-3x faster for CLIP
**Trade-off**: Higher memory usage

## Advanced Optimizations

### 8. Async Processing with Background Tasks

```python
# In main.py
from fastapi import BackgroundTasks
import asyncio

async def process_video_async(video_path, user_id):
    """Process video in background"""
    # Update status
    processing_status[user_id] = {"status": "processing", "progress": 0}
    
    # Process video
    results = await asyncio.to_thread(process_video, video_path)
    
    # Update status
    processing_status[user_id] = {"status": "complete", "progress": 100}
    
    return results

@app.post("/upload/")
async def upload(file: UploadFile, background_tasks: BackgroundTasks):
    # Save file
    video_path = save_uploaded_file(file)
    
    # Start background processing
    background_tasks.add_task(process_video_async, video_path, user_id)
    
    return {"message": "Processing started", "status": "processing"}

@app.get("/status/{user_id}")
async def get_status(user_id: str):
    return processing_status.get(user_id, {"status": "not_found"})
```

**Speed Improvement**: Better UX (non-blocking)
**Trade-off**: Requires status polling

### 9. Use Smaller YOLO Model

```python
# Instead of yolov8n.pt, use even smaller model
model = YOLO("yolov8n.pt")  # Nano (current)
# or
model = YOLO("yolov8s.pt")  # Small (more accurate, slower)
# or
model = YOLO("yolov8m.pt")  # Medium (even more accurate, much slower)

# For fastest processing, stick with yolov8n.pt
```

**Current**: YOLOv8n (nano) - Already the fastest!

### 10. Optimize OpenCV Settings

```python
# In video processing
cap = cv2.VideoCapture(video_path)

# Set buffer size to 1 (reduce memory)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Use hardware acceleration if available
cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)
```

**Speed Improvement**: 10-15% faster

## Configuration File

Create `config.py` with optimization settings:

```python
# config.py - Performance Configuration

# Frame Processing
FRAME_SKIP = 5              # Process every Nth frame (1 = all frames)
MAX_FRAME_WIDTH = 640       # Resize frames to this width
MAX_FRAME_HEIGHT = 480      # Maximum height

# Detection Settings
DETECTION_CONFIDENCE = 0.6  # Higher = faster but less detections
ENABLE_COLOR_DETECTION = True  # Set False to skip color detection

# Parallel Processing
ENABLE_MULTIPROCESSING = True
NUM_WORKERS = 4             # Number of CPU cores to use

# GPU Settings
USE_GPU = False             # Set True if CUDA available
GPU_BATCH_SIZE = 32         # Batch size for GPU processing

# CLIP Settings
CLIP_BATCH_SIZE = 16        # Batch size for CLIP encoding
ENABLE_CLIP = True          # Set False to disable CLIP search

# Storage
SAVE_ANNOTATED_FRAMES = True  # Set False to skip saving annotated images
COMPRESSION_QUALITY = 85    # JPEG quality (0-100, lower = faster)
```

## Implementation Priority

### Phase 1: Quick Wins (1 hour)
1. ✅ Add frame skipping (FRAME_SKIP = 5)
2. ✅ Resize frames (max_width = 640)
3. ✅ Increase confidence threshold (0.6)

**Expected**: 5-7x faster

### Phase 2: Medium Optimizations (4 hours)
1. ✅ Implement multiprocessing
2. ✅ Add batch processing for CLIP
3. ✅ Optimize OpenCV settings

**Expected**: 10-15x faster total

### Phase 3: Advanced (1 day)
1. ✅ GPU acceleration setup
2. ✅ Async background processing
3. ✅ Progress tracking UI

**Expected**: 20-30x faster with GPU

## Benchmarks

### Current Performance (CPU only)
- 1 minute video (30 FPS): ~5-10 minutes processing
- 5 minute video: ~25-50 minutes processing

### With Quick Wins (Frame Skip + Resize)
- 1 minute video: ~1-2 minutes processing
- 5 minute video: ~5-10 minutes processing

### With Multiprocessing (4 cores)
- 1 minute video: ~30-60 seconds processing
- 5 minute video: ~2-5 minutes processing

### With GPU (NVIDIA RTX 3060)
- 1 minute video: ~10-20 seconds processing
- 5 minute video: ~1-2 minutes processing

## Hardware Recommendations

### Budget Option
- CPU: Intel i5 or AMD Ryzen 5 (4+ cores)
- RAM: 8GB minimum
- Storage: SSD (faster I/O)
- **Cost**: $500-800
- **Speed**: 5-10x faster than current

### Recommended Option
- CPU: Intel i7 or AMD Ryzen 7 (8+ cores)
- RAM: 16GB
- GPU: NVIDIA GTX 1660 or better
- Storage: NVMe SSD
- **Cost**: $1000-1500
- **Speed**: 15-25x faster than current

### Professional Option
- CPU: Intel i9 or AMD Ryzen 9 (12+ cores)
- RAM: 32GB
- GPU: NVIDIA RTX 3060 or better
- Storage: NVMe SSD
- **Cost**: $2000-3000
- **Speed**: 30-50x faster than current

## Monitoring Performance

Add timing to see bottlenecks:

```python
import time

def process_video_with_timing(video_path):
    timings = {}
    
    # Frame extraction
    start = time.time()
    frames = extract_frames(video_path)
    timings['frame_extraction'] = time.time() - start
    
    # Detection
    start = time.time()
    detections = detect_objects(frames)
    timings['detection'] = time.time() - start
    
    # Color detection
    start = time.time()
    add_colors(detections)
    timings['color_detection'] = time.time() - start
    
    # CLIP encoding
    start = time.time()
    encode_with_clip(frames)
    timings['clip_encoding'] = time.time() - start
    
    print("Performance Breakdown:")
    for task, duration in timings.items():
        print(f"  {task}: {duration:.2f}s")
    
    return detections
```

## Next Steps

1. **Immediate**: Implement frame skipping (5 minutes)
2. **Short-term**: Add configuration file (30 minutes)
3. **Medium-term**: Implement multiprocessing (2-4 hours)
4. **Long-term**: Set up GPU acceleration (1 day)

Choose based on your needs and available hardware!
