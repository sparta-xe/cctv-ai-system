# Contributing to CCTV AI System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/cctv-ai-system.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 📋 Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py

# Start development server
python main.py
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Real-time video streaming
- [ ] WebSocket support for live alerts
- [ ] PostgreSQL/MongoDB integration
- [ ] Proper person Re-ID models (OSNet, FastReID)
- [ ] GPU optimization
- [ ] Docker deployment improvements
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit tests and integration tests

### Medium Priority
- [ ] React/Vue frontend
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] Export reports (PDF/CSV)
- [ ] Multi-camera support
- [ ] Cloud storage integration (S3, Azure Blob)
- [ ] Redis caching
- [ ] JWT authentication

### Low Priority
- [ ] Dark mode toggle
- [ ] Internationalization (i18n)
- [ ] Email/SMS alerts
- [ ] Webhook integrations
- [ ] Custom alert rules
- [ ] Video compression
- [ ] Thumbnail generation

## 🧪 Testing Guidelines

- Write tests for new features
- Ensure existing tests pass
- Test on multiple Python versions (3.8+)
- Test with different video formats
- Check performance with large videos

## 📝 Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions
- Keep functions small and focused
- Comment complex logic

### Example
```python
def process_frame(image_path: str, confidence: float = 0.5) -> list:
    """
    Process a single frame for object detection.
    
    Args:
        image_path: Path to the image file
        confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        list: Detected objects with bounding boxes
    """
    # Implementation
    pass
```

## 🐛 Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Screenshots (if applicable)

## ✨ Feature Requests

When requesting features, include:
- Clear description
- Use case/motivation
- Proposed implementation (optional)
- Examples from other systems (optional)

## 📦 Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Update documentation if needed
- Add tests for new features
- Ensure all tests pass
- Follow the existing code style
- Write clear commit messages

### Commit Message Format
```
Type: Brief description

Detailed explanation (optional)

Fixes #issue_number (if applicable)
```

Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`, `Test`

## 🔍 Code Review Process

1. Automated checks run on PR
2. Maintainer reviews code
3. Feedback provided
4. Changes requested (if needed)
5. Approval and merge

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Help others learn
- Share knowledge
- Provide constructive feedback
- Have fun!

## 📞 Contact

- GitHub Issues: For bugs and features
- Discussions: For questions and ideas
- Email: your.email@example.com

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🚀
