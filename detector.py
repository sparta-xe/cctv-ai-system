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
        tuple: (list of object labels, list of bounding boxes)
    """
    if model is None:
        return [], []
    
    if not os.path.exists(image_path):
        print(f"Warning: Image not found: {image_path}")
        return [], []
    
    try:
        results = model(image_path, conf=confidence_threshold, verbose=False)
        objects = []
        boxes = []
        
        for r in results:
            for box in r.boxes:
                cls = int(box.cls)
                label = model.names[cls]
                objects.append(label)
                boxes.append(box.xyxy.tolist())
        
        return objects, boxes
    except Exception as e:
        print(f"Error during detection: {e}")
        return [], []
