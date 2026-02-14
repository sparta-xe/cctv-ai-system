from ultralytics import YOLO
import os
import torch
from color_detector import add_colors_to_detections

# Check for GPU availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🎯 YOLOv8 using device: {device.upper()}")

# Initialize model with GPU support
try:
    model = YOLO("yolov8n.pt")
    if device == 'cuda':
        model.to(device)
        print(f"✅ YOLOv8 loaded on GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  GPU not available, using CPU (slower)")
except Exception as e:
    print(f"Warning: Failed to load YOLOv8 model: {e}")
    model = None

def detect(image_path, confidence_threshold=0.5, detect_colors=True):
    """
    Detect objects in an image using YOLOv8 with GPU acceleration
    
    Args:
        image_path: Path to the image file
        confidence_threshold: Minimum confidence score for detections
        detect_colors: Whether to detect colors for each object
    
    Returns:
        list: List of detection dictionaries with label, box, confidence, color, and colors
    """
    if model is None:
        return []
    
    if not os.path.exists(image_path):
        print(f"Warning: Image not found: {image_path}")
        return []
    
    try:
        # Run inference with device specification
        results = model(image_path, conf=confidence_threshold, verbose=False, device=device)
        detections = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                
                detections.append({
                    "label": label,
                    "box": [x1, y1, x2, y2],
                    "confidence": conf
                })
        
        # Add color detection
        if detect_colors and detections:
            detections = add_colors_to_detections(image_path, detections)
        
        return detections
    except Exception as e:
        print(f"Error during detection: {e}")
        return []
