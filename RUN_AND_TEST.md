# 🚀 RUN AND TEST - STEP BY STEP

## ⚡ STEP 1: Clean Start

```bash
# Delete old storage (IMPORTANT - old format won't work)
rmdir /s /q storage

# Verify it's deleted
dir storage
# Should show "File Not Found"
```

## 🎯 STEP 2: Start Server

```bash
# Start the server
python main.py

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 📤 STEP 3: Upload Video

### Option A: Browser
1. Open: `http://localhost:8000`
2. Click upload button
3. Select video file (MP4, AVI, MOV)
4. Wait for processing

### Option B: Command Line (curl)
```bash
curl -X POST "http://localhost:8000/upload/" ^
  -F "file=@your_video.mp4"
```

### Expected Output:
```json
{
    "status": "Processed",
    "frames": 30,
    "alerts": [],
    "search_engine": {
        "clip_available": true,
        "hybrid_search": "enabled"
    }
}
```

## 🔍 STEP 4: Test Query

### Option A: Browser
1. Enter username: `admin`
2. Enter password: `admin123`
3. Enter query: `person`
4. Click Search

### Option B: Command Line (curl)
```bash
curl -X POST "http://localhost:8000/query/" ^
  -F "username=admin" ^
  -F "password=admin123" ^
  -F "text=person"
```

### Expected Response:
```json
{
    "role": "admin",
    "query": "person",
    "results": [
        {
            "image": "storage/frames/frame_5.jpg",
            "timestamp": 5,
            "detections": [
                {
                    "label": "person",
                    "box": [100, 200, 300, 400],
                    "confidence": 0.95
                },
                {
                    "label": "car",
                    "box": [400, 100, 600, 300],
                    "confidence": 0.87
                }
            ],
            "objects": ["person", "car"],
            "matched_detection_indices": [0],  // ← CHECK THIS!
            "search_score": 0.8
        }
    ],
    "timeline_markers": [
        {
            "timestamp": 5,  // ← Integer, not float
            "objects": ["person", "car"],
            "matched_detection_indices": [0]  // ← CHECK THIS!
        }
    ]
}
```

## ✅ STEP 5: Verify Response

### Check 1: matched_detection_indices exists
```bash
# Should see: "matched_detection_indices": [0]
# NOT: "matched_detection_indices": null or missing
```

### Check 2: Timestamps are integers
```bash
# Should see: "timestamp": 5
# NOT: "timestamp": 5.5 or 5.0
```

### Check 3: Detections have confidence
```bash
# Should see: "confidence": 0.95
# NOT: missing confidence field
```

### Check 4: Box format is flat
```bash
# Should see: "box": [100, 200, 300, 400]
# NOT: "box": [[100, 200, 300, 400]]
```

## 🎨 STEP 6: Test Annotated Image

### Option A: Browser
```
http://localhost:8000/annotated_image/frame_5.jpg?matched_indices=0
```

### Option B: Command Line
```bash
curl "http://localhost:8000/annotated_image/frame_5.jpg?matched_indices=0" ^
  --output test_annotated.jpg

# Open test_annotated.jpg to verify
```

### Expected Visual:
- **Detection 0 (person):**
  - Thick green box (4px)
  - Yellow label background
  - Black text: ">>> PERSON (0.95) <<<"
  
- **Detection 1 (car):**
  - Thin gray box (1px)
  - Gray label background
  - White text: "car (0.87)"

## 🧪 STEP 7: Test Different Queries

### Test 1: Query "car"
```bash
curl -X POST "http://localhost:8000/query/" ^
  -F "username=admin" ^
  -F "password=admin123" ^
  -F "text=car"

# Check: matched_detection_indices should point to car detections
```

### Test 2: Query "person with backpack"
```bash
curl -X POST "http://localhost:8000/query/" ^
  -F "username=admin" ^
  -F "password=admin123" ^
  -F "text=person with backpack"

# Check: matched_detection_indices should include both person and backpack indices
```

### Test 3: Query with time range
```bash
curl -X POST "http://localhost:8000/query/" ^
  -F "username=admin" ^
  -F "password=admin123" ^
  -F "text=person between 5 and 10 seconds"

# Check: Only results with timestamp 5-10 returned
```

## 📊 STEP 8: Check Stats

```bash
curl "http://localhost:8000/stats/"
```

### Expected Output:
```json
{
    "total_frames": 30,
    "total_people_detected": 15,
    "object_counts": {
        "person": 15,
        "car": 8,
        "backpack": 3
    },
    "unique_objects": 3
}
```

## 🏥 STEP 9: Health Check

```bash
curl "http://localhost:8000/health"
```

### Expected Output:
```json
{
    "status": "healthy",
    "version": "2.0",
    "clip_available": true,
    "clip_device": "cuda",
    "frames_indexed": 30,
    "search_engine": "hybrid"
}
```

## 🐛 TROUBLESHOOTING

### Issue: No matched_detection_indices in response
**Cause:** Old data format
**Fix:**
```bash
rmdir /s /q storage
python main.py
# Re-upload video
```

### Issue: All boxes highlighted
**Cause:** matched_indices parameter not passed
**Fix:**
```bash
# Ensure URL includes: ?matched_indices=0,2
```

### Issue: No boxes shown
**Cause:** Detection error
**Fix:**
```bash
# Check console for errors
# Verify YOLOv8 model downloaded: yolov8n.pt
```

### Issue: Timeline jumps wrong
**Cause:** Timestamp format issue
**Fix:**
```bash
# Check response: "timestamp" should be integer (5, not 5.0)
# If float, old data format - delete storage and re-upload
```

## ✅ SUCCESS CHECKLIST

Run through this checklist:

- [ ] Storage deleted and recreated
- [ ] Server started successfully
- [ ] Video uploaded without errors
- [ ] Query returns results
- [ ] Response includes `matched_detection_indices`
- [ ] Timestamps are integers
- [ ] Detections include confidence scores
- [ ] Annotated image shows correct highlighting
- [ ] Only matched boxes are thick green
- [ ] Non-matched boxes are thin gray
- [ ] Timeline markers include detection indices
- [ ] Multiple queries work correctly

## 🎯 QUICK DEBUG

### Check Detection Format
```python
# In Python console
from database import get_all_frames
frames = get_all_frames()
print(frames[0])

# Should show:
# {
#     "detections": [
#         {"label": "person", "box": [x,y,x,y], "confidence": 0.95}
#     ],
#     "matched_detection_indices": [0]
# }
```

### Check Query Results
```python
from hybrid_search import hybrid_search
results = hybrid_search("person", top_k=5)
print(results[0].get("matched_detection_indices"))

# Should show: [0, 2] or similar
# NOT: None or missing
```

## 🏆 IF ALL PASS

**CONGRATULATIONS!** 🎉

Your system now has:
- ✅ Detection-precise matching
- ✅ Correct bounding box highlighting
- ✅ Working timeline markers
- ✅ Confidence scores
- ✅ Integer timestamps
- ✅ Professional-grade object detection

**Ready for production!**
