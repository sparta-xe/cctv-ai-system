# 🚀 GitHub Setup Guide

## Quick Setup (5 Steps)

### Step 1: Initialize Git Repository
```bash
git init
```

### Step 2: Add All Files
```bash
git add .
```

### Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: Complete CCTV AI System with video playback and query highlighting"
```

### Step 4: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `cctv-ai-system`
3. Description: `AI-powered CCTV surveillance system with object detection, video playback, and smart highlighting`
4. Choose: Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 5: Push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/cctv-ai-system.git
git branch -M main
git push -u origin main
```

---

## Detailed Instructions

### Option A: Using GitHub CLI (Easiest)

If you have GitHub CLI installed:

```bash
# Login to GitHub
gh auth login

# Create repository and push
gh repo create cctv-ai-system --public --source=. --remote=origin --push
```

### Option B: Using Git Commands (Manual)

```bash
# 1. Initialize repository
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Complete CCTV AI System

Features:
- YOLOv8 object detection
- Semantic search with FAISS
- Person tracking with Re-ID
- Video playback with timeline markers
- Query highlighting (only searched objects highlighted)
- Smart alerts (unattended bags, crowds)
- Beautiful web dashboard
- Role-based authentication
- Comprehensive documentation"

# 4. Create repository on GitHub (via web browser)
# Go to: https://github.com/new

# 5. Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/cctv-ai-system.git
git branch -M main
git push -u origin main
```

---

## Repository Details

### Recommended Settings

**Repository Name:** `cctv-ai-system`

**Description:**
```
AI-powered CCTV surveillance system with YOLOv8 detection, semantic search, video playback with timeline markers, and intelligent query highlighting. Perfect for hackathons and security applications.
```

**Topics (Tags):**
```
computer-vision
object-detection
yolov8
fastapi
video-analysis
cctv
surveillance
ai
machine-learning
python
faiss
semantic-search
person-tracking
hackathon
```

**Features to Enable:**
- ✅ Issues
- ✅ Projects
- ✅ Wiki
- ✅ Discussions (optional)

---

## What Gets Pushed

### Included Files (✅)
- All Python source code
- HTML templates
- Documentation (15+ markdown files)
- Configuration files
- Test scripts
- Requirements.txt
- LICENSE
- .gitignore

### Excluded Files (❌)
- storage/ folder (videos and frames)
- __pycache__/ folders
- Downloaded models (*.pt files)
- Temporary files
- IDE settings

---

## After Pushing

### 1. Add Repository Description
On GitHub, click "Edit" and add:
```
🎥 AI-powered CCTV surveillance system with object detection, video playback, and smart highlighting
```

### 2. Add Topics
Click "⚙️ Settings" → "Topics" and add:
- computer-vision
- object-detection
- yolov8
- fastapi
- video-analysis

### 3. Create README Badge
Add to top of README.md:
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-latest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

### 4. Add Screenshots
Create a `screenshots/` folder and add:
- Dashboard screenshot
- Video playback screenshot
- Query highlighting screenshot
- Timeline markers screenshot

### 5. Enable GitHub Pages (Optional)
For documentation hosting:
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Save

---

## Commit Message Guidelines

### For Future Commits

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat: add real-time video streaming"
git commit -m "fix: resolve port binding issue"
git commit -m "docs: update installation guide"
```

---

## Branching Strategy

### Main Branch
- Production-ready code
- Always stable
- Protected

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push feature branch
git push origin feature/new-feature

# Create Pull Request on GitHub
# Merge after review
```

---

## Useful Git Commands

### Check Status
```bash
git status
```

### View Changes
```bash
git diff
```

### View Commit History
```bash
git log --oneline
```

### Update from Remote
```bash
git pull origin main
```

### Create New Branch
```bash
git checkout -b feature-name
```

### Switch Branch
```bash
git checkout main
```

### Push Changes
```bash
git add .
git commit -m "Your message"
git push origin main
```

---

## Troubleshooting

### Issue: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/cctv-ai-system.git
```

### Issue: "failed to push"
```bash
git pull origin main --rebase
git push origin main
```

### Issue: "large files"
```bash
# Remove large files from git
git rm --cached storage/videos/*
git commit -m "Remove large files"
```

### Issue: "authentication failed"
```bash
# Use personal access token instead of password
# Generate at: https://github.com/settings/tokens
```

---

## GitHub Repository Structure

```
cctv-ai-system/
├── .github/
│   └── workflows/          # CI/CD (optional)
├── docs/                   # Documentation
├── templates/              # HTML templates
├── tests/                  # Test files (optional)
├── main.py                 # Main application
├── detector.py             # Object detection
├── embedder.py             # Vector search
├── tracker.py              # Person tracking
├── database.py             # Data storage
├── auth.py                 # Authentication
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── README.md               # Main documentation
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
└── GITHUB_SETUP.md         # This file
```

---

## Next Steps After Push

1. ✅ Verify all files are on GitHub
2. ✅ Add repository description and topics
3. ✅ Create releases/tags for versions
4. ✅ Add screenshots to README
5. ✅ Enable GitHub Actions (optional)
6. ✅ Add contributors (if team project)
7. ✅ Star your own repository 😊

---

## Quick Commands Summary

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/cctv-ai-system.git
git push -u origin main

# Regular updates
git add .
git commit -m "Your message"
git push

# Check status
git status
git log --oneline
```

---

**Your CCTV AI System is ready to be shared with the world!** 🚀🌟
