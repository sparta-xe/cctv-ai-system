"""
Utility functions for CCTV AI System
"""

import os
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "storage",
        "storage/frames",
        "storage/videos",
        "storage/marked",
        "storage/highlights",
        "templates",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def get_file_hash(file_path: str) -> str:
    """
    Calculate MD5 hash of a file
    
    Args:
        file_path: Path to the file
    
    Returns:
        str: MD5 hash
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def format_timestamp(seconds: float) -> str:
    """
    Format timestamp in MM:SS format
    
    Args:
        seconds: Timestamp in seconds
    
    Returns:
        str: Formatted timestamp
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def format_file_size(bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        bytes: File size in bytes
    
    Returns:
        str: Formatted file size
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing special characters
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    import re
    # Remove special characters except dots, dashes, and underscores
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def get_video_info(video_path: str) -> Optional[Dict[str, Any]]:
    """
    Get video metadata
    
    Args:
        video_path: Path to video file
    
    Returns:
        dict: Video metadata or None if error
    """
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return None
        
        info = {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0,
            "file_size": os.path.getsize(video_path)
        }
        
        cap.release()
        return info
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None

def save_json(data: Any, file_path: str):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to JSON file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(file_path: str) -> Optional[Any]:
    """
    Load data from JSON file
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Loaded data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def cleanup_old_files(directory: str, days: int = 7):
    """
    Delete files older than specified days
    
    Args:
        directory: Directory to clean
        days: Number of days to keep files
    """
    import time
    
    if not os.path.exists(directory):
        return
    
    current_time = time.time()
    cutoff_time = current_time - (days * 86400)  # 86400 seconds in a day
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            if file_time < cutoff_time:
                try:
                    os.remove(file_path)
                    print(f"Deleted old file: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

def get_system_stats() -> Dict[str, Any]:
    """
    Get system resource usage statistics
    
    Returns:
        dict: System statistics
    """
    import psutil
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "timestamp": datetime.now().isoformat()
    }

def validate_video_file(file_path: str, max_size_mb: int = 500) -> tuple[bool, str]:
    """
    Validate video file
    
    Args:
        file_path: Path to video file
        max_size_mb: Maximum file size in MB
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File too large ({file_size_mb:.2f}MB). Max: {max_size_mb}MB"
    
    # Check file extension
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in allowed_extensions:
        return False, f"Invalid format. Allowed: {', '.join(allowed_extensions)}"
    
    # Try to open with OpenCV
    try:
        import cv2
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return False, "Cannot open video file"
        cap.release()
    except Exception as e:
        return False, f"Video validation error: {str(e)}"
    
    return True, "Valid"
