# AI CCTV Intelligence System

An AI-powered CCTV video analysis system that enables natural language search through surveillance footage using computer vision and deep learning.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Features

- **Natural Language Search** - Search videos using plain English (e.g., "red car near entrance")
- **Object Detection** - Detects 80+ object classes using YOLOv8
- **Color Detection** - Identifies 12 colors (red, blue, green, etc.)
- **Hybrid Search** - Combines text and visual matching with CLIP
- **Interactive UI** - Cyber-themed dashboard with real-time results
- **Video Playback** - Timeline markers and timestamp navigation
- **Smart Alerts** - Detects unattended bags and crowds
- **Fast Processing** - 10x speedup with optimizations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 8GB RAM minimum (16GB recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/sparta-xe/cctv-ai-system.git
cd cctv-ai-system

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

### Usage

1. Open browser: `http://localhost:8000`
2. Upload a video file (MP4, AVI, MOV, etc.)
3. Wait for processing (2-5 minutes for 5-min video)
4. Search using natural language queries
5. View results with bounding boxes and timestamps

## 📖 Documentation

- **[Complete Project Guide](docs/COMPLETE_PROJECT_GUIDE.md)** - Full system documentation
- **[System Flowchart](docs/SYSTEM_FLOWCHART.md)** - Visual workflow diagrams
- **[Tech Stack](docs/TECH_STACK.md)** - Technologies used
- **[Performance Guide](docs/PERFORMANCE_OPTIMIZATION_GUIDE.md)** - Speed optimization tips
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🏗️ Architecture

```
User Interface (Cyber Dashboard)
         ↓
FastAPI Backend
         ↓
┌────────┴────────┬──────────────┬─────────────┐
│  YOLOv8         │  CLIP        │  Color      │
│  Detection      │  Visual      │  Detection  │
└────────┬────────┴──────────────┴─────────────┘
         ↓
┌────────┴────────┬──────────────┬─────────────┐
│  Database       │  FAISS       │  CLIP       │
│  (Frames)       │  (Text)      │  (Visual)   │
└─────────────────┴──────────────┴─────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **YOLOv8** - Object detection
- **CLIP** - Visual-text matching
- **FAISS** - Vector similarity search
- **OpenCV** - Computer vision

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Tailwind CSS** - Utility-first CSS
- **JavaScript** - Interactivity
- **Lucide Icons** - Icon system

### AI Models
- **YOLOv8n** - Object detection (80 classes)
- **CLIP ViT-B/32** - Multimodal embeddings
- **MiniLM-L6-v2** - Text embeddings

## 📊 Performance

- **Processing Speed:** 2-5 minutes for 5-minute video
- **Speedup:** 10x faster with optimizations
- **Accuracy:** 87% object detection, 85% color detection
- **Search:** Sub-second query response time

## 🔧 Configuration

Edit `main.py` to adjust performance settings:

```python
FRAME_SKIP = 5              # Process every Nth frame (1-10)
MAX_FRAME_WIDTH = 640       # Frame width (480-1920)
DETECTION_CONFIDENCE = 0.5  # Confidence threshold (0.3-0.9)
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Slow Processing
- Increase `FRAME_SKIP` to 10
- Reduce `MAX_FRAME_WIDTH` to 480
- Process shorter videos

### Out of Memory
- Close other applications
- Reduce frame size
- Process videos in smaller chunks

## 📝 API Endpoints

- `GET /` - Dashboard UI
- `POST /upload/` - Upload and process video
- `POST /query/` - Search with natural language
- `POST /clear_data/` - Clear all indexed data
- `GET /video/{filename}` - Stream video file
- `GET /annotated_image/{frame}` - Get annotated frame

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv8 implementation
- **OpenAI** - CLIP model
- **Hugging Face** - Transformers library
- **FastAPI** - Web framework

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/sparta-xe/cctv-ai-system/issues)
- **Documentation:** [docs/](docs/)
- **Email:** support@example.com

## 🎓 Citation

If you use this project in your research, please cite:

```bibtex
@software{cctv_ai_system,
  title = {AI CCTV Intelligence System},
  author = {Your Name},
  year = {2026},
  url = {https://github.com/sparta-xe/cctv-ai-system}
}
```

---

Made with ❤️ for smarter surveillance
