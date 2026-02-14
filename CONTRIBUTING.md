# Contributing to AI CCTV Intelligence System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/sparta-xe/cctv-ai-system/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Error messages and logs

### Suggesting Features

1. Check existing [Issues](https://github.com/sparta-xe/cctv-ai-system/issues) for similar suggestions
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach
   - Any relevant examples

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Git
- 8GB RAM minimum

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cctv-ai-system.git
cd cctv-ai-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Start development server
python start.py
```

## 📝 Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def process_video(video_path: str, frame_skip: int = 5) -> dict:
    """
    Process video and extract frames.
    
    Args:
        video_path: Path to video file
        frame_skip: Process every Nth frame
    
    Returns:
        Dictionary with processing results
    """
    pass

# Bad
def processVideo(videoPath,frameSkip=5):
    pass
```

### Code Formatting

Use `black` for automatic formatting:

```bash
# Format all Python files
black .

# Check formatting
black --check .
```

### Linting

Use `flake8` for linting:

```bash
# Run linter
flake8 .

# Ignore specific errors
flake8 --ignore=E501,W503 .
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import List, Dict, Optional

def search_frames(
    query: str,
    top_k: int = 10,
    filters: Optional[Dict[str, str]] = None
) -> List[Dict]:
    pass
```

## 🧪 Testing

### Writing Tests

Create tests in `tests/` directory:

```python
# tests/test_detector.py
import pytest
from detector import detect

def test_detect_objects():
    """Test object detection on sample image"""
    results = detect("tests/fixtures/sample.jpg")
    assert len(results) > 0
    assert "label" in results[0]
    assert "confidence" in results[0]

def test_detect_invalid_image():
    """Test detection with invalid image"""
    with pytest.raises(FileNotFoundError):
        detect("nonexistent.jpg")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_detector.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v
```

## 📚 Documentation

### Code Comments

- Use docstrings for functions and classes
- Comment complex logic
- Keep comments up-to-date

```python
def hybrid_search(query: str, top_k: int = 10) -> List[Dict]:
    """
    Perform hybrid search combining text and visual matching.
    
    This function combines FAISS text search with CLIP visual search,
    applies score weighting, and filters results based on query parameters.
    
    Args:
        query: Natural language search query
        top_k: Number of results to return
    
    Returns:
        List of matching frames with metadata and scores
    
    Example:
        >>> results = hybrid_search("red car near entrance", top_k=5)
        >>> print(len(results))
        5
    """
    pass
```

### Documentation Files

- Update README.md for major changes
- Add guides to docs/ folder
- Include examples and screenshots

## 🔀 Git Workflow

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

Examples:
- `feature/add-face-recognition`
- `fix/memory-leak-in-detector`
- `docs/update-deployment-guide`

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

Examples:
```
feat(detector): add GPU acceleration support

Implemented CUDA support for YOLOv8 detection to improve
processing speed by 5x on compatible hardware.

Closes #123
```

```
fix(search): resolve color filtering bug

Fixed issue where color filters were not being applied
correctly in hybrid search, causing incorrect results.

Fixes #456
```

## 🎯 Areas for Contribution

### High Priority

- [ ] Multi-camera support
- [ ] Real-time streaming
- [ ] Face recognition
- [ ] License plate detection
- [ ] Mobile app

### Medium Priority

- [ ] Advanced alerts (email/SMS)
- [ ] Export reports (PDF/Excel)
- [ ] Cloud storage integration
- [ ] API documentation (OpenAPI)
- [ ] Performance benchmarks

### Low Priority

- [ ] Dark/light theme toggle
- [ ] Keyboard shortcuts
- [ ] Batch processing
- [ ] Video trimming
- [ ] Custom model training

## 🐛 Bug Fixes

### Before Fixing

1. Reproduce the bug
2. Write a failing test
3. Fix the bug
4. Ensure test passes
5. Check for side effects

### Testing Bug Fixes

```python
# tests/test_bug_fixes.py
def test_color_filter_bug_456():
    """Test that color filters are applied correctly"""
    results = hybrid_search("red car", top_k=10)
    
    # All results should have red color
    for result in results:
        detections = result.get("detections", [])
        has_red = any(d.get("color") == "red" for d in detections)
        assert has_red, "Result should contain red objects"
```

## 📊 Performance Improvements

### Benchmarking

```python
import time

def benchmark_function(func, *args, iterations=100):
    """Benchmark function execution time"""
    start = time.time()
    for _ in range(iterations):
        func(*args)
    end = time.time()
    avg_time = (end - start) / iterations
    print(f"{func.__name__}: {avg_time:.4f}s average")
```

### Profiling

```bash
# Profile with cProfile
python -m cProfile -o profile.stats main.py

# Analyze with snakeviz
pip install snakeviz
snakeviz profile.stats
```

## 🔒 Security

### Security Guidelines

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize file uploads
- Use parameterized queries
- Keep dependencies updated

### Reporting Security Issues

Email security issues to: security@example.com

Do not create public issues for security vulnerabilities.

## 📞 Getting Help

- **Documentation:** Check [docs/](docs/) folder
- **Issues:** Search existing issues
- **Discussions:** GitHub Discussions
- **Email:** support@example.com

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI CCTV Intelligence System! 🚀
