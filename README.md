# 🎥 CCTV AI System - Hackathon Ready

A complete, runnable, hackathon-ready CCTV surveillance system with object detection, person tracking, vector search, and real-time alerts.

## ✨ Features

✅ **YOLO Detection** - Fast object detection with YOLOv8  
✅ **Frame Extraction** - Automatic video processing  
✅ **Vector Search** - Semantic search with FAISS  
✅ **Person Tracking** - Basic Re-ID simulation  
✅ **Alert System** - Unattended object & crowd detection  
✅ **Role-Based Auth** - Admin, security, and viewer roles  
✅ **Web Dashboard** - Beautiful, responsive HTML interface  
✅ **Error Handling** - Robust error handling throughout  
✅ **Image Display** - Visual results with bounding boxes and timestamps  
✅ **Annotated Images** - Color-coded boxes around detected objects  
✅ **Video Playback** - Watch original video with timeline markers  
✅ **Interactive Timeline** - Click markers to jump to query matches  

## 📦 Installation

```bash
# Clone or download the project
cd cctv_ai_system

# Install dependencies
pip install -r requirements.txt

# Test the system (optional but recommended)
python test_system.py
```

## 🚀 Quick Start

### 1. Start the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

### 2. Open the dashboard:
```
http://127.0.0.1:8000
```

### 3. Use the system:
- **Upload Video**: Select a video file and click upload
- **Search**: Login and query with natural language

## 🔐 Default Credentials

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | admin | upload, query, delete |
| security | sec123 | security | query |
| viewer | view123 | viewer | query |

## 🎯 Example Queries

- `person` - Find all frames with people
- `car` - Find all frames with cars
- `person with backpack` - Find people carrying backpacks
- `bag` - Find all bags/backpacks
- `person walking` - Semantic search for walking people

## 🏗 Project Structure

```
cctv_ai_system/
│
├── main.py                 # FastAPI server + video processing
├── detector.py             # YOLOv8 object detection
├── embedder.py             # Sentence transformer embeddings
├── tracker.py              # Person Re-ID simulation
├── database.py             # In-memory frame database
├── auth.py                 # Role-based authentication
├── config.py               # Configuration settings
├── test_system.py          # System test script
├── requirements.txt        # Dependencies
├── QUICKSTART.md           # Quick start guide
│
├── templates/
│   └── dashboard.html     # Web interface
│
└── storage/
    └── frames/            # Extracted frames
```

## 🔥 Key Features Explained

### Object Detection
Uses YOLOv8n for fast, accurate detection of 80+ object classes including:
- People, cars, trucks, buses
- Backpacks, handbags, suitcases
- Bicycles, motorcycles
- And many more...

### Person Tracking
Simple Re-ID simulation using sentence transformers to assign consistent IDs to people across frames. Uses cosine similarity with configurable threshold.

### Alert System
Automatically detects:
- **Unattended bags**: Backpack detected without nearby person
- **Crowd detection**: More than 5 people in a single frame
- Extensible for custom alerts

### Vector Search
Semantic search using FAISS for natural language queries. Understands context and meaning, not just keywords.

## 📊 API Endpoints

### `GET /`
Web dashboard interface

### `POST /upload/`
Upload and process video
- **Input**: Video file (MP4, AVI, MOV, MKV, FLV, WMV)
- **Output**: Processing status, frame count, alerts, total frames

### `POST /query/`
Search for frames
- **Input**: username, password, query text
- **Output**: Matching frames with metadata, count

### `GET /stats/`
Get system statistics
- **Output**: Total frames, people detected, object counts

## 🛠 Configuration

Edit `config.py` to customize:
- Frame extraction rate
- Detection confidence threshold
- Person tracking similarity threshold
- Alert settings
- Model selection

## 🧪 Testing

Run the test script to verify all components:
```bash
python test_system.py
```

This will check:
- ✅ All packages installed
- ✅ Custom modules loading
- ✅ Directories created
- ✅ Authentication working
- ✅ Embedder functioning

## 🚀 Next Steps for Production

To upgrade this system:

1. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Real Re-ID**: Implement proper person re-identification models (OSNet, FastReID)
3. **WebSocket**: Add real-time streaming and live alerts
4. **Better UI**: React/Vue dashboard with live video feed and charts
5. **Redis Queue**: Handle multiple concurrent video uploads
6. **JWT Auth**: Secure token-based authentication with refresh tokens
7. **Docker**: Containerize for easy deployment
8. **GPU**: Optimize for GPU acceleration (10x faster)
9. **Cloud Storage**: S3/Azure Blob for frame storage
10. **Monitoring**: Add Prometheus/Grafana for system monitoring

## 🎓 Perfect For

- 🏆 Hackathons (impressive demo, works immediately)
- 📚 Final year projects (extensible, well-documented)
- 🧪 Proof of concepts (production-ready architecture)
- 🎯 Demos and presentations (beautiful UI)

## 💡 Tips

- Use short videos (30-60 seconds) for faster testing
- First run downloads YOLOv8 model (~6MB, takes 1-2 minutes)
- System extracts 1 frame per second by default
- Queries are semantic - be descriptive
- Check console for real-time alert messages
- For GPU acceleration, install `torch` with CUDA support

## 🐛 Troubleshooting

**Issue**: YOLOv8 model not found  
**Solution**: First run downloads automatically. Check internet connection.

**Issue**: Video processing is slow  
**Solution**: Normal for CPU. For faster processing, use GPU-enabled PyTorch.

**Issue**: Search returns no results  
**Solution**: Upload and process a video first.

**Issue**: Import errors  
**Solution**: Run `pip install -r requirements.txt` again.

## 📝 Notes

This is a **hackathon-ready** system designed to:
- ✅ Run immediately out of the box
- ✅ Look impressive in demos
- ✅ Be easy to understand and extend
- ✅ Have production-ready architecture
- ❌ Not production-grade (yet) - needs scaling, security hardening

## 🤝 Contributing

Feel free to extend this system with:
- Additional alert types
- Better Re-ID models
- Real-time video streaming
- Mobile app integration
- Advanced analytics

## 📄 License

MIT

---

**Made with ❤️ for hackathons and learning**
