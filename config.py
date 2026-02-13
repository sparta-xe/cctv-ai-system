"""
Configuration file for CCTV AI System
"""

# Video Processing
FRAME_EXTRACTION_RATE = 1  # Extract 1 frame per second
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for object detection

# Person Tracking
SIMILARITY_THRESHOLD = 0.85  # Threshold for person re-identification

# Search
DEFAULT_SEARCH_RESULTS = 5  # Default number of search results

# Storage
FRAME_FOLDER = "storage/frames"
STORAGE_FOLDER = "storage"
TEMPLATES_FOLDER = "templates"

# Server
HOST = "0.0.0.0"
PORT = 8000

# Alerts
ALERT_UNATTENDED_BAG = True
ALERT_CROWD_THRESHOLD = 5  # Alert when more than N people detected

# Supported video formats
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

# Model Settings
YOLO_MODEL = "yolov8n.pt"  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
