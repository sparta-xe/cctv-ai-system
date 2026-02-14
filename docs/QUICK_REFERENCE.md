# 🚀 Quick Reference Card

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Access
```
http://127.0.0.1:8000
```

## Credentials
| User | Password | Role |
|------|----------|------|
| admin | admin123 | admin |
| security | sec123 | security |
| viewer | view123 | viewer |

## API Endpoints

### Dashboard
```
GET /
```

### Upload Video
```
POST /upload/
Body: multipart/form-data with "file"
```

### Search
```
POST /query/
Body: username, password, text
```

### Statistics
```
GET /stats/
```

## Example Queries
- `person`
- `car`
- `person with backpack`
- `bag`
- `person walking`

## File Structure
```
main.py          - Server
detector.py      - YOLO detection
embedder.py      - Vector search
tracker.py       - Person tracking
database.py      - Storage
auth.py          - Authentication
config.py        - Settings
test_system.py   - Tests
```

## Configuration (config.py)
```python
FRAME_EXTRACTION_RATE = 1
CONFIDENCE_THRESHOLD = 0.5
SIMILARITY_THRESHOLD = 0.85
ALERT_CROWD_THRESHOLD = 5
```

## Testing
```bash
python test_system.py
```

## Common Commands
```bash
# Install
pip install -r requirements.txt

# Test
python test_system.py

# Run
python main.py

# Run with reload
uvicorn main:app --reload

# Run on different port
uvicorn main:app --port 8080
```

## Troubleshooting

### Model not found
First run downloads YOLOv8 (~6MB)

### Slow processing
Normal for CPU. Use GPU for 10x speed.

### No results
Upload a video first.

### Import errors
Run: `pip install -r requirements.txt`

## Quick Test
1. Start server: `python main.py`
2. Open: http://127.0.0.1:8000
3. Upload any video
4. Login: admin/admin123
5. Query: "person"

## Features
✅ Object detection (80+ classes)
✅ Person tracking
✅ Semantic search
✅ Alerts (bag, crowd)
✅ Web dashboard
✅ Role-based auth

## Supported Formats
- MP4, AVI, MOV, MKV, FLV, WMV

## Alerts
- Unattended bag (backpack without person)
- Crowd (>5 people)

## Performance
- Extraction: 1 frame/second
- Detection: ~30ms/frame (CPU)
- Search: <10ms/query

## Next Steps
1. Test with sample video
2. Try different queries
3. Check alerts in console
4. Explore API docs: /docs
5. Extend with custom features

---
**Ready to demo!** 🎉
