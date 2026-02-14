from ultralytics import YOLO
import os
from color_detector import add_colors_to_detections

# Initialize model with error handling
try:
    model = YOLO("yolov8n.pt")
except Exception as e:
    print(f"Warning: Failed to load YOLOv8 model: {e}")
    model = None

def detect(image_path, confidence_threshold=0.5, detect_colors=True):
    """
    Detect objects in an image using YOLOv8 with color detection
    
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
        results = model(image_path, conf=confidence_threshold, verbose=False)
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
