# 🛠️ TECH STACK - AI CCTV Intelligence System

## Backend Technologies

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
  - Async/await support
  - Automatic API documentation
  - Type hints and validation
  - WebSocket support

### AI/ML Models

#### Computer Vision
- **YOLOv8** (Ultralytics) - Object detection
  - Real-time object detection
  - 80+ object classes
  - High accuracy and speed
  - Pre-trained on COCO dataset

- **CLIP** (OpenAI) - Visual-semantic search
  - Vision-language model
  - Natural language queries
  - Zero-shot classification
  - Multimodal embeddings

#### Image Processing
- **OpenCV (cv2)** - Computer vision library
  - Image manipulation
  - Video processing
  - Bounding box annotation
  - Color space conversion (BGR, HSV)
  - Gaussian blur and filtering

#### Color Detection
- **Custom HSV-based algorithm**
  - 12 color categories
  - Gaussian blur for noise reduction
  - Adaptive thresholding
  - Multi-color detection

### Vector Search & Embeddings
- **FAISS** (Facebook AI Similarity Search)
  - Fast similarity search
  - Vector indexing
  - Efficient nearest neighbor search
  - CPU/GPU support

- **Sentence Transformers**
  - Text embeddings
  - Semantic search
  - Pre-trained models
  - Multi-language support

### Data Processing
- **NumPy** - Numerical computing
  - Array operations
  - Mathematical functions
  - Image data manipulation

- **Pillow (PIL)** - Image processing
  - Image loading/saving
  - Format conversion
  - Basic transformations

### Video Processing
- **MoviePy** - Video editing
  - Video concatenation
  - Clip extraction
  - Frame manipulation
  - Audio handling

### Authentication & Security
- **Custom auth system**
  - Role-based access control (RBAC)
  - User/Admin roles
  - Session management
  - Password validation

### Database
- **JSON-based storage**
  - Frame metadata
  - Detection results
  - User data
  - Configuration

## Frontend Technologies

### UI Framework
- **Tailwind CSS** - Utility-first CSS framework
  - Responsive design
  - Custom color schemes
  - Rapid prototyping
  - Minimal CSS

### Icons
- **Lucide Icons** - Modern icon library
  - 1000+ icons
  - Lightweight
  - Customizable
  - SVG-based

### JavaScript (Vanilla)
- **ES6+ Features**
  - Async/await
  - Arrow functions
  - Template literals
  - Destructuring
  - Modules

### UI Components
- **Custom Modal/Lightbox**
  - Full-screen image viewer
  - Keyboard shortcuts
  - Smooth animations
  - Touch support

- **Drag & Drop API**
  - Native HTML5 drag-and-drop
  - File upload
  - Visual feedback
  - Event handling

### Animations
- **CSS Animations**
  - Keyframe animations
  - Transitions
  - Transform effects
  - Parallax scrolling

- **Custom Effects**
  - Twinkling stars (200 particles)
  - Neon glow effects
  - Glassmorphism
  - Hover animations

## Development Tools

### Version Control
- **Git** - Source control
- **GitHub** - Code hosting
  - Repository: sparta-xe/cctv-ai-system
  - Commit history
  - Issue tracking

### Package Management
- **pip** - Python package manager
- **requirements.txt** - Dependency management

### Testing
- **pytest** - Testing framework
- **unittest** - Built-in testing

### Containerization
- **Docker** - Containerization
  - Dockerfile included
  - docker-compose.yml
  - Isolated environment
  - Easy deployment

## Server & Deployment

### Web Server
- **Uvicorn** - ASGI server
  - High performance
  - WebSocket support
  - Auto-reload
  - Production-ready

### Static Files
- **FastAPI StaticFiles**
  - CSS/JS serving
  - Image serving
  - Video streaming
  - Favicon support

### CORS
- **FastAPI CORS Middleware**
  - Cross-origin requests
  - API access control
  - Security headers

## File Formats

### Video Formats Supported
- MP4
- AVI
- MOV
- MKV
- WebM

### Image Formats
- JPEG/JPG
- PNG
- BMP
- TIFF

### Data Formats
- JSON (metadata storage)
- CSV (export capability)
- Markdown (documentation)

## Architecture Patterns

### Design Patterns
- **MVC-like Architecture**
  - Models: Data structures
  - Views: HTML templates
  - Controllers: API endpoints

- **Modular Design**
  - Separate modules for each feature
  - Loose coupling
  - High cohesion

### API Design
- **RESTful API**
  - GET, POST endpoints
  - JSON responses
  - Status codes
  - Error handling

### Search Architecture
- **Hybrid Search**
  - Text-based search (embeddings)
  - Visual search (CLIP)
  - Combined scoring
  - Relevance ranking

## Color Scheme

### UI Colors (Cyber Theme)
- **Primary**: Cyan (#38bdf8)
- **Secondary**: Blue (#3b82f6)
- **Accent**: Purple (#8b5cf6)
- **Success**: Green (#22c55e)
- **Warning**: Yellow (#eab308)
- **Error**: Red (#ef4444)
- **Background**: Dark slate (#0f172a)

## Performance Optimizations

### Backend
- Async/await for I/O operations
- FAISS indexing for fast search
- Image resizing for faster processing
- Caching mechanisms
- Batch processing

### Frontend
- Lazy loading
- Image optimization
- CSS animations (GPU-accelerated)
- Debouncing/throttling
- Cache-busting headers

## Browser Compatibility

### Supported Browsers
- Chrome/Edge (Chromium) - Full support
- Firefox - Full support
- Safari - Full support
- Opera - Full support
- Mobile browsers - Touch support

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- 2GB disk space
- CPU (no GPU required)

### Recommended
- Python 3.10+
- 8GB RAM
- 5GB disk space
- GPU (CUDA) for faster processing

## Dependencies (Key Packages)

### Core
```
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
```

### AI/ML
```
ultralytics>=8.0.0
torch>=2.0.0
transformers>=4.35.0
sentence-transformers>=2.2.2
faiss-cpu>=1.7.4
```

### Image/Video
```
opencv-python>=4.8.0
Pillow>=10.0.0
moviepy>=1.0.3
numpy>=1.24.0
```

## Development Environment

### IDE/Editor Support
- VS Code (recommended)
- PyCharm
- Sublime Text
- Vim/Neovim

### Operating Systems
- Windows (tested)
- Linux (supported)
- macOS (supported)

## API Endpoints

### Main Endpoints
- `POST /upload/` - Video upload
- `POST /query/` - Search query
- `GET /video/{filename}` - Video streaming
- `GET /annotated_image/{filename}` - Annotated frames
- `GET /stats/` - System statistics
- `GET /clip_status/` - CLIP engine status

## Security Features

### Implemented
- Authentication system
- Role-based access control
- Input validation
- CORS configuration
- Secure file handling

### Best Practices
- No hardcoded credentials
- Environment variables
- Input sanitization
- Error handling
- Logging system

## Monitoring & Logging

### Logging
- Custom logger module
- Console output
- Error tracking
- Performance metrics

### Status Monitoring
- System health checks
- CLIP engine status
- Detection statistics
- Frame processing metrics

## Documentation

### Types
- README.md - Project overview
- API documentation (auto-generated)
- Feature documentation (40+ MD files)
- Code comments
- Inline documentation

## Future Tech Stack Additions

### Potential Enhancements
- PostgreSQL/MongoDB for scalable storage
- Redis for caching
- Celery for task queuing
- Prometheus for monitoring
- Grafana for dashboards
- Kubernetes for orchestration
- CI/CD pipelines (GitHub Actions)

---

## Quick Reference

**Language**: Python 3.8+  
**Framework**: FastAPI  
**AI Models**: YOLOv8 + CLIP  
**Frontend**: Vanilla JS + Tailwind CSS  
**Server**: Uvicorn  
**Deployment**: Docker  
**Repository**: https://github.com/sparta-xe/cctv-ai-system
