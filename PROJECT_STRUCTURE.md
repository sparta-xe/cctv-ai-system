# Project Structure

```
cctv_ai_system/
│
├── 📁 Core Application Files
│   ├── main.py                    # FastAPI server & endpoints
│   ├── config.py                  # Configuration settings
│   ├── start.py                   # Startup script
│   └── requirements.txt           # Python dependencies
│
├── 📁 AI & Detection Modules
│   ├── detector.py                # YOLOv8 object detection
│   ├── color_detector.py          # HSV-based color detection
│   ├── clip_engine.py             # CLIP visual-text matching
│   ├── embedder.py                # Text embeddings (FAISS)
│   ├── hybrid_search.py           # Combined search logic
│   ├── query_parser.py            # Natural language parsing
│   └── annotator.py               # Bounding box drawing
│
├── 📁 Data & Storage
│   ├── database.py                # In-memory frame storage
│   ├── tracker.py                 # Person tracking
│   └── video_builder.py           # Highlight video creation
│
├── 📁 Utilities
│   ├── auth.py                    # Authentication
│   ├── logger.py                  # Logging configuration
│   └── utils.py                   # Helper functions
│
├── 📁 Frontend
│   ├── templates/
│   │   └── dashboard.html         # Main UI (Cyber theme)
│   └── static/
│       └── favicon.svg            # Cyber-themed favicon
│
├── 📁 Storage (Runtime)
│   ├── storage/
│   │   ├── frames/                # Extracted video frames
│   │   ├── videos/                # Uploaded videos
│   │   ├── marked/                # Annotated frames
│   │   └── highlights/            # Generated highlight videos
│   └── logs/                      # Application logs
│
├── 📁 Scripts
│   ├── scripts/
│   │   ├── test_gpu.py            # GPU testing
│   │   ├── test_system.py         # System testing
│   │   ├── start_server.py        # Alternative startup
│   │   └── *.bat                  # Windows batch scripts
│
├── 📁 Documentation
│   ├── docs/
│   │   ├── COMPLETE_PROJECT_GUIDE.md
│   │   ├── SYSTEM_FLOWCHART.md
│   │   ├── TECH_STACK.md
│   │   ├── PERFORMANCE_OPTIMIZATION_GUIDE.md
│   │   └── [70+ other documentation files]
│   │
│   ├── README.md                  # Main documentation
│   ├── DEPLOYMENT.md              # Deployment guide
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   └── LICENSE                    # MIT License
│
├── 📁 Configuration
│   ├── .env.example               # Environment variables template
│   ├── .gitignore                 # Git ignore rules
│   └── setup.py                   # Package setup
│
└── 📁 Development
    ├── tests/                     # Test files
    ├── __pycache__/               # Python cache (ignored)
    └── .vscode/                   # VS Code settings (ignored)
```

## 📋 File Descriptions

### Core Application

**main.py**
- FastAPI application setup
- API endpoints (upload, query, video, etc.)
- Request/response handling
- Server configuration

**config.py**
- Performance settings (frame skip, resize, confidence)
- Path configurations
- Model settings

**start.py**
- Startup script with dependency checks
- Directory creation
- Server initialization

### AI Modules

**detector.py**
- YOLOv8 model loading
- Object detection inference
- Bounding box extraction
- Confidence filtering

**color_detector.py**
- HSV color space conversion
- 12-color detection
- Dominant color extraction
- Multi-color analysis

**clip_engine.py**
- CLIP model initialization
- Image embedding generation
- Text-to-image matching
- Similarity scoring

**embedder.py**
- Sentence transformer model
- FAISS index management
- Text embedding generation
- Vector similarity search

**hybrid_search.py**
- Combined text + visual search
- Score weighting and boosting
- Result filtering and ranking
- Detection-level matching

**query_parser.py**
- Natural language parsing
- Object/color extraction
- Time range parsing
- Location parsing

**annotator.py**
- Bounding box drawing
- Label rendering
- Color-coded highlighting
- Image annotation

### Data Management

**database.py**
- In-memory frame storage
- CRUD operations
- Video-specific queries
- Data clearing functions

**tracker.py**
- Person ID assignment
- Object tracking
- Trajectory analysis

**video_builder.py**
- Highlight video creation
- Frame compilation
- Video encoding

### Frontend

**templates/dashboard.html**
- Cyber-themed UI
- Parallax star background
- Neon glow effects
- Interactive components
- Drag & drop upload
- Search interface
- Results grid
- Video player
- Timeline markers

**static/favicon.svg**
- Cyber-themed icon
- SVG format

### Storage Structure

```
storage/
├── frames/              # frame_0.jpg, frame_5.jpg, ...
├── videos/              # video_filename.mp4
├── marked/              # annotated_frame_0.jpg
└── highlights/          # highlight_video.mp4
```

### Scripts

**test_gpu.py**
- GPU availability check
- CUDA/DirectML testing
- Performance benchmarking

**test_system.py**
- End-to-end testing
- API endpoint testing
- Model loading verification

### Documentation

**docs/** folder contains:
- Complete project guide
- System flowcharts
- Technology stack details
- Performance optimization
- Feature documentation
- Bug fix history
- Development notes

## 🔧 Key Configuration Files

### .env (Create from .env.example)
```bash
HOST=0.0.0.0
PORT=8000
FRAME_SKIP=5
MAX_FRAME_WIDTH=640
DETECTION_CONFIDENCE=0.5
```

### requirements.txt
All Python dependencies with versions

## 📊 Data Flow

```
User Upload → main.py → detector.py → color_detector.py
                ↓
         database.py ← embedder.py ← clip_engine.py
                ↓
User Search → hybrid_search.py → query_parser.py
                ↓
         annotator.py → Results Display
```

## 🚀 Startup Sequence

1. **start.py** - Initialize
2. **main.py** - Load FastAPI
3. **detector.py** - Load YOLOv8
4. **clip_engine.py** - Load CLIP
5. **embedder.py** - Load Sentence Transformer
6. **Server Ready** - Accept requests

## 📝 Important Notes

- **storage/** folder is created automatically
- **logs/** folder is created on first run
- **yolov8n.pt** downloads automatically (~6MB)
- **CLIP model** downloads on first use (~350MB)
- **Sentence Transformer** downloads on first use (~80MB)

## 🔒 Security

- Sensitive files in `.gitignore`
- Environment variables in `.env`
- Authentication in `auth.py`
- Input validation in `main.py`

## 📦 Deployment Files

- **DEPLOYMENT.md** - Deployment guide
- **start.py** - Production startup

---

This structure is optimized for:
✅ Development
✅ Testing
✅ Deployment
✅ Maintenance
✅ Scalability
