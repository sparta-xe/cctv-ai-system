from ultralytics import YOLO
import os

# Initialize model with error handling
try:
    model = YOLO("yolov8n.pt")
except Exception as e:
    print(f"Warning: Failed to load YOLOv8 model: {e}")
    model = None

def detect(image_path, confidence_threshold=0.5):
    """
    Detect objects in an image using YOLOv8
    
    Args:
        image_path: Path to the image file
        confidence_threshold: Minimum confidence score for detections
    
    Returns:
        list: List of detection dictionaries with label, box, and confidence
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
        
        return detections
    except Exception as e:
        print(f"Error during detection: {e}")
        return []
