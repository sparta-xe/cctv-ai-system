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
            color_name = det.get("color", "")
            
            if len(box) < 4:
                continue
            
            x1, y1, x2, y2 = map(int, box[:4])
            
            # Check if this detection should be highlighted
            is_highlighted = highlight_indices is not None and idx in highlight_indices
            
            # Always draw boxes - highlighted ones are bright, others are subtle
            if is_highlighted:
                # Highlighted style - bright neon green for query matches
                color = (0, 255, 0)  # Bright green
                thickness = 2
                font_scale = 0.5
                font_thickness = 1
            else:
                # Normal style - cyan outline for all detected objects
                color = (56, 189, 248)  # Cyan (matches UI theme)
                thickness = 2
                font_scale = 0.4
                font_thickness = 1
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
            
            # Create label with color if available
            if color_name and color_name not in ["unknown", "mixed"]:
                label_text = f"{color_name} {label} {int(confidence * 100)}%"
            else:
                label_text = f"{label} {int(confidence * 100)}%"
            (text_width, text_height), baseline = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
            )
            
            # Label background with padding
            padding = 4
            label_y = y1 - text_height - padding * 2 - 2
            if label_y < 0:
                label_y = y1 + 2
                label_bg_y2 = label_y + text_height + padding * 2
            else:
                label_bg_y2 = y1 - 2
            
            # Draw label background
            if is_highlighted:
                # Bright green background for matches
                bg_color = (0, 255, 0)
                text_color = (0, 0, 0)  # Black text
            else:
                # Dark semi-transparent background for normal
                bg_color = (30, 30, 30)
                text_color = (56, 189, 248)  # Cyan text
            
            cv2.rectangle(
                image,
                (x1, label_y),
                (x1 + text_width + padding * 2, label_bg_y2),
                bg_color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                image, label_text,
                (x1 + padding, label_bg_y2 - padding - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                text_color,
                font_thickness,
                cv2.LINE_AA
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
