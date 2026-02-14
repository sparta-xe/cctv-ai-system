# ⚡ QUICK TEST - 2 MINUTES

## 🚀 Start Fresh

```bash
# Delete old data (important!)
rmdir /s /q storage

# Start server
python main.py
```

## 📤 Upload Test Video

1. Open browser: `http://localhost:8000`
2. Upload any video with people/cars
3. Wait for processing

## 🔍 Test Query

```bash
# In browser or Postman
POST http://localhost:8000/query/
{
    "username": "admin",
    "password": "admin123",
    "text": "person"
}
```

## ✅ Check Response

Look for these NEW fields:

```json
{
    "results": [
        {
            "detections": [
                {"label": "person", "box": [x,y,x,y], "confidence": 0.95}
            ],
            "matched_detection_indices": [0]  // ← NEW!
        }
    ],
    "timeline_markers": [
        {
            "timestamp": 5,  // ← Integer, not float
            "matched_detection_indices": [0]  // ← NEW!
        }
    ]
}
```

## 🎨 Test Annotated Image

```bash
# Open in browser
http://localhost:8000/annotated_image/frame_5.jpg?matched_indices=0

# Should show:
# - Detection 0: THICK GREEN box, yellow label ">>> PERSON (0.95) <<<"
# - Other detections: thin gray boxes
```

## ✅ Success Criteria

1. ✅ Response includes `matched_detection_indices`
2. ✅ Timestamps are integers (5, not 5.0)
3. ✅ Annotated image highlights ONLY matched boxes
4. ✅ Confidence scores shown on boxes
5. ✅ Non-matched boxes shown in gray

## 🐛 If Something's Wrong

### No matched_detection_indices in response
→ Old data format. Delete storage and re-upload.

### All boxes highlighted
→ Frontend not passing `matched_indices` parameter.

### No boxes shown
→ Check console for detection errors.

### Timeline jumps wrong
→ Check timestamps are integers in response.

## 🎯 Quick Debug

```python
# Check detection format
from database import get_all_frames
frames = get_all_frames()
print(frames[0].get("detections"))
# Should show: [{"label": ..., "box": [...], "confidence": ...}]

# Check query results
from hybrid_search import hybrid_search
results = hybrid_search("person", top_k=5)
print(results[0].get("matched_detection_indices"))
# Should show: [0, 2] or similar
```

## 🏆 If All Pass

**FIX IS WORKING!** 🎉

Your system now:
- Stores full detection data with confidence
- Matches queries to specific detections
- Highlights ONLY matched bounding boxes
- Timeline markers work correctly
- Shows non-matched objects in gray for context

**Detection-precise, not just frame-precise!**
