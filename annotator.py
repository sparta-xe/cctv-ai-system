"""
Frame annotation with highlighted bounding boxes
Marks query-matched objects with special highlighting
"""

import cv2
import numpy as np

def annotate_frame(image_path, detections, output_path, highlight_indices=None):
    """
    Annotate frame with bounding boxes from detection data
    
    Args:
        image_path: Path to input image
        detections: List of detection dicts with 'label', 'box', 'confidence'
        output_path: Path to save annotated image
        highlight_indices: List of detection indices to highlight (optional)
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        for idx, det in enumerate(detections):
            box = det.get("box", [])
            label = det.get("label", "object")
            confidence = det.get("confidence", 0)
            
            if len(box) < 4:
                continue
            
            x1, y1, x2, y2 = map(int, box[:4])
            
            # Check if this detection should be highlighted
            is_highlighted = highlight_indices is not None and idx in highlight_indices
            
            if is_highlighted:
                # Highlighted style - thick, bright
                color = (0, 255, 0)  # Bright green
                thickness = 4
                font_scale = 0.8
                font_thickness = 2
                
                # Draw thick rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                
                # Yellow background for label
                label_text = f">>> {label.upper()} ({confidence:.2f}) <<<"
                (text_width, text_height), _ = cv2.getTextSize(
                    label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
                )
                
                cv2.rectangle(
                    image,
                    (x1, y1 - text_height - 15),
                    (x1 + text_width + 10, y1),
                    (0, 255, 255),  # Yellow
                    -1
                )
                
                # Black text
                cv2.putText(
                    image, label_text,
                    (x1 + 5, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (0, 0, 0),  # Black
                    font_thickness
                )
            else:
                # Normal style - thin, gray
                color = (128, 128, 128)  # Gray
                thickness = 1
                font_scale = 0.4
                font_thickness = 1
                
                # Draw thin rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                
                # Gray background for label
                label_text = f"{label} ({confidence:.2f})"
                (text_width, text_height), _ = cv2.getTextSize(
                    label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
                )
                
                cv2.rectangle(
                    image,
                    (x1, y1 - text_height - 8),
                    (x1 + text_width, y1),
                    (128, 128, 128),  # Gray
                    -1
                )
                
                # White text
                cv2.putText(
                    image, label_text,
                    (x1, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),  # White
                    font_thickness
                )
        
        # Save annotated image
        cv2.imwrite(output_path, image)
        return True
        
    except Exception as e:
        print(f"Error annotating frame: {e}")
        return False

def add_query_overlay(image_path, query_text, output_path):
    """
    Add query text overlay to image
    
    Args:
        image_path: Path to input image
        query_text: Query text to display
        output_path: Path to save image with overlay
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        # Add semi-transparent overlay at top
        overlay = image.copy()
        height, width = image.shape[:2]
        
        cv2.rectangle(overlay, (0, 0), (width, 60), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
        
        # Add query text
        cv2.putText(
            image,
            f"Query: {query_text}",
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
        
        cv2.imwrite(output_path, image)
        return True
        
    except Exception as e:
        print(f"Error adding overlay: {e}")
        return False
