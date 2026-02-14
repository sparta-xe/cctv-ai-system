# 🧪 TESTING THE BOUNDING BOX FIX

## Quick Test Steps

### 1. Start Fresh
```bash
# Delete old storage to test with new format
rmdir /s /q storage
python main.py
```

### 2. Upload Test Video
- Upload a video with multiple objects (people, cars, etc.)
- Check console output for detection data

### 3. Test Query Matching
```bash
# Query for specific object
POST /query/
{
    "username": "admin",
    "password": "admin123",
    "text": "person"
}
```

**Expected Response:**
```json
{
    "results": [
        {
            "image": "storage/frames/frame_5.jpg",
            "timestamp": 5,
            "detections": [
                {"label": "person", "box": [100, 200, 300, 400], "confidence": 0.95},
                {"label": "car", "box": [400, 100, 600, 300], "confidence": 0.87}
            ],
            "matched_detection_indices": [0],  // ← CRITICAL: Only person matched
            "search_score": 0.8
        }
    ],
    "timeline_markers": [
        {
            "timestamp": 5,
            "matched_detection_indices": [0]  // ← CRITICAL: Indices included
        }
    ]
}
```

### 4. Test Annotated Image
```bash
# Request annotated image with matched indices
GET /annotated_image/frame_5.jpg?matched_indices=0

# Should show:
# - Detection 0 (person): THICK GREEN box, yellow label ">>> PERSON (0.95) <<<"
# - Detection 1 (car): thin gray box, small label "car (0.87)"
```

### 5. Test Timeline Markers
- Click timeline marker at timestamp 5
- Video should jump to exactly 5 seconds
- Annotated image should highlight ONLY the person box

## 🔍 What to Check

### ✅ Detection Storage
```python
# In console after upload, you should see:
print(meta["detections"])
# Output: [{"label": "person", "box": [x1,y1,x2,y2], "confidence": 0.95}, ...]
```

### ✅ Query Response
```python
# Check matched_detection_indices in response
assert "matched_detection_indices" in result
assert isinstance(result["matched_detection_indices"], list)
```

### ✅ Annotated Image
- Query-matched boxes: Thick (4px), bright green, yellow label
- Non-matched boxes: Thin (1px), gray, small label
- Confidence scores shown on all boxes

### ✅ Timeline
- Timestamps are integers (not floats)
- Timeline markers include matched_detection_indices
- Video jumps to correct timestamp

## 🐛 Common Issues

### Issue: No boxes shown
**Cause:** Old data format in storage
**Fix:** Delete storage folder and re-upload video

### Issue: All boxes highlighted
**Cause:** matched_indices parameter not passed
**Fix:** Ensure frontend passes `?matched_indices=0,2,5`

### Issue: Timeline jumps to wrong time
**Cause:** Float vs integer timestamp
**Fix:** Already fixed - timestamps now integers

### Issue: Boxes in wrong position
**Cause:** Box coordinates format issue
**Fix:** Already fixed - boxes now flat [x1,y1,x2,y2]

## 🎯 Success Criteria

1. ✅ Upload video → detections stored with confidence
2. ✅ Query "person" → only person boxes highlighted
3. ✅ Query "car" → only car boxes highlighted
4. ✅ Timeline markers include detection indices
5. ✅ Clicking marker jumps to exact timestamp
6. ✅ Annotated images show correct highlighting
7. ✅ Non-matched objects shown in gray for context

## 📊 Debug Commands

### Check Detection Format
```python
from database import get_all_frames
frames = get_all_frames()
print(frames[0]["detections"])
# Should show: [{"label": ..., "box": [...], "confidence": ...}]
```

### Check Query Results
```python
from hybrid_search import hybrid_search
results = hybrid_search("person", top_k=5)
print(results[0]["matched_detection_indices"])
# Should show: [0, 2] or similar
```

### Check Timeline Data
```python
# In query endpoint response
print(timeline_markers[0])
# Should include: {"timestamp": 5, "matched_detection_indices": [0, 2]}
```

## 🚀 Performance Check

- Upload time: Should be same as before
- Query time: Slightly slower (detection matching) but < 1 second
- Image annotation: Real-time (< 100ms per image)
- Timeline generation: Instant

## ✅ Final Verification

Run this complete test:

1. Upload video with people and cars
2. Query "person" → Check only person boxes highlighted
3. Query "car" → Check only car boxes highlighted  
4. Query "person with backpack" → Check both highlighted
5. Click timeline markers → Check correct jumps
6. View multiple frames → Check consistent highlighting

If all pass → **FIX IS WORKING!** 🎉
