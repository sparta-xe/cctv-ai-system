# 🚀 QUICK REFERENCE CARD

## ⚡ Start System (Choose One)

```bash
# Option 1: Direct Python
python main.py

# Option 2: Uvicorn
uvicorn main:app --reload

# Option 3: Docker
docker-compose up

# Option 4: Package
pip install -e .
cctv-ai
```

## 🌐 Access Dashboard

```
http://localhost:8000
```

## 🔐 Default Credentials

| User | Password | Role |
|------|----------|------|
| admin | admin123 | Full access |
| security | sec123 | Query only |
| viewer | view123 | Query only |

## 📁 Key Files

| File | Purpose |
|------|---------|
| main.py | FastAPI server |
| detector.py | Object detection |
| hybrid_search.py | AI search |
| templates/dashboard.html | UI |
| config.py | Settings |
| requirements.txt | Dependencies |

## 🧪 Run Tests

```bash
# All tests
python -m pytest tests/

# Specific test
python -m pytest tests/test_detector.py

# Integration test
python test_system.py
```

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| / | GET | Dashboard |
| /upload/ | POST | Upload video |
| /query/ | POST | Search |
| /stats/ | GET | Statistics |
| /health | GET | Health check |
| /video/{name} | GET | Video file |
| /annotated_image/{name} | GET | Annotated frame |

## 🎯 Example Queries

```
person
car
person with backpack
bag
person walking
car at night
```

## 🔧 Configuration

Edit `config.py`:
```python
FRAME_EXTRACTION_RATE = 1  # FPS
CONFIDENCE_THRESHOLD = 0.5  # Detection
ALERT_CROWD_THRESHOLD = 5   # People
```

## 📦 Storage Structure

```
storage/
├── frames/      # Extracted frames
├── videos/      # Uploaded videos
├── marked/      # Annotated frames
└── highlights/  # Highlight videos
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Change PORT in config.py |
| Model not found | First run downloads automatically |
| Slow processing | Normal for CPU, use GPU for speed |
| No results | Upload video first |
| Import errors | pip install -r requirements.txt |

## 📚 Documentation

| Doc | Purpose |
|-----|---------|
| README.md | Overview |
| QUICKSTART.md | Quick start |
| PROJECT_STATUS.md | System status |
| FINAL_AUDIT_REPORT.md | Audit results |
| CONTRIBUTING.md | How to contribute |

## 🎨 UI Features

- 🌌 Parallax stars (200)
- 💎 Neon icons (20+)
- ✨ Smooth animations (60fps)
- 🎯 Cyber defense theme
- 📱 Responsive design

## 🔥 Hot Keys

| Action | Command |
|--------|---------|
| Start server | python main.py |
| Run tests | pytest |
| Check health | curl localhost:8000/health |
| View logs | tail -f logs/*.log |
| Stop server | Ctrl+C |

## 📈 Performance

| Metric | Value |
|--------|-------|
| Frame extraction | 1 FPS |
| Detection speed | 0.1s/frame |
| Search speed | <1s |
| UI load time | <1s |
| Animation FPS | 60 |

## 🚀 Deployment

```bash
# Local
python main.py

# Docker
docker-compose up -d

# Production
export HOST=0.0.0.0
export PORT=8000
python main.py
```

## 🔒 Security

- ✅ Role-based auth
- ✅ Input validation
- ✅ File validation
- ⚠️ Use .env for secrets
- ⚠️ Enable HTTPS in production

## 📞 Support

- 📖 Docs: Check documentation folder
- 🐛 Bugs: GitHub Issues
- 💡 Questions: Discussions
- 📧 Email: Direct support

## ✅ Quick Checklist

- [ ] Dependencies installed
- [ ] Server started
- [ ] Dashboard accessible
- [ ] Video uploaded
- [ ] Search working
- [ ] Results displaying
- [ ] Timeline working
- [ ] Bounding boxes showing

## 🎯 Next Steps

1. Upload test video
2. Try search queries
3. Check timeline markers
4. View annotated images
5. Explore features
6. Read documentation
7. Customize settings
8. Deploy to production

---

**Quick Help:** `python main.py --help`  
**Version:** 2.0.0  
**Status:** ✅ Production Ready

**Keep this card handy!** 📌
