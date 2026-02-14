"""
Color detection for objects in video frames
Extracts dominant colors from bounding box regions
"""

import cv2
import numpy as np
from collections import Counter

# Improved color name mapping (HSV ranges) - more accurate ranges
COLOR_RANGES = {
    # Red (wraps around HSV hue)
    'red': [
        [(0, 50, 50), (10, 255, 255)],      # Lower red
        [(170, 50, 50), (180, 255, 255)]    # Upper red
    ],
    # Orange
    'orange': [[(10, 50, 50), (25, 255, 255)]],
    # Yellow
    'yellow': [[(25, 50, 50), (35, 255, 255)]],
    # Green
    'green': [[(35, 50, 50), (85, 255, 255)]],
    # Cyan/Turquoise
    'cyan': [[(85, 50, 50), (95, 255, 255)]],
    # Blue
    'blue': [[(95, 50, 50), (130, 255, 255)]],
    # Purple/Violet
    'purple': [[(130, 50, 50), (155, 255, 255)]],
    # Pink/Magenta
    'pink': [[(155, 50, 50), (170, 255, 255)]],
    # White (low saturation, high value)
    'white': [[(0, 0, 180), (180, 40, 255)]],
    # Gray (low saturation, medium value)
    'gray': [[(0, 0, 40), (180, 40, 180)]],
    # Black (low value)
    'black': [[(0, 0, 0), (180, 255, 40)]],
    # Brown (orange hue with lower saturation/value)
    'brown': [[(10, 40, 20), (25, 200, 150)]]
}

def get_dominant_color(image, box):
    """
    Extract dominant color from bounding box region using improved algorithm
    
    Args:
        image: OpenCV image (BGR)
        box: Bounding box [x1, y1, x2, y2]
    
    Returns:
        Color name (string)
    """
    try:
        x1, y1, x2, y2 = map(int, box[:4])
        
        # Ensure coordinates are within image bounds
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return "unknown"
        
        # Extract region of interest
        roi = image[y1:y2, x1:x2]
        
        if roi.size == 0:
            return "unknown"
        
        # Resize for faster processing (but not too small)
        roi_h, roi_w = roi.shape[:2]
        if roi_h > 100 or roi_w > 100:
            scale = min(100 / roi_h, 100 / roi_w)
            new_h, new_w = int(roi_h * scale), int(roi_w * scale)
            roi = cv2.resize(roi, (new_w, new_h))
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Apply Gaussian blur to reduce noise
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        
        # Detect colors with improved scoring
        color_scores = {}
        total_pixels = hsv.shape[0] * hsv.shape[1]
        
        for color_name, ranges in COLOR_RANGES.items():
            mask = None
            
            # Combine multiple ranges for the same color
            for color_range in ranges:
                lower, upper = np.array(color_range[0]), np.array(color_range[1])
                temp_mask = cv2.inRange(hsv, lower, upper)
                
                if mask is None:
                    mask = temp_mask
                else:
                    mask = cv2.bitwise_or(mask, temp_mask)
            
            # Count pixels in this color range
            pixel_count = cv2.countNonZero(mask)
            percentage = pixel_count / total_pixels
            
            # Store score
            color_scores[color_name] = percentage
        
        # Get dominant color (highest percentage)
        if not color_scores or max(color_scores.values()) == 0:
            return "unknown"
        
        # Sort by percentage
        sorted_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top color
        dominant_color, dominant_percentage = sorted_colors[0]
        
        # Only return if it's significant (>15% of pixels)
        if dominant_percentage > 0.15:
            return dominant_color
        
        # Check if it's a mix of colors
        if len(sorted_colors) > 1 and sorted_colors[1][1] > 0.10:
            return "mixed"
        
        return "unknown"
        
    except Exception as e:
        print(f"Error detecting color: {e}")
        return "unknown"

def get_color_histogram(image, box, top_n=3):
    """
    Get multiple dominant colors for more detailed analysis
    
    Args:
        image: OpenCV image (BGR)
        box: Bounding box [x1, y1, x2, y2]
        top_n: Number of top colors to return
    
    Returns:
        List of dominant colors
    """
    try:
        x1, y1, x2, y2 = map(int, box[:4])
        
        # Ensure coordinates are within image bounds
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return []
        
        # Extract region of interest
        roi = image[y1:y2, x1:x2]
        
        if roi.size == 0:
            return []
        
        # Resize for faster processing
        roi_h, roi_w = roi.shape[:2]
        if roi_h > 100 or roi_w > 100:
            scale = min(100 / roi_h, 100 / roi_w)
            new_h, new_w = int(roi_h * scale), int(roi_w * scale)
            roi = cv2.resize(roi, (new_w, new_h))
        
        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Apply Gaussian blur
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        
        # Detect all present colors
        detected_colors = []
        total_pixels = hsv.shape[0] * hsv.shape[1]
        
        for color_name, ranges in COLOR_RANGES.items():
            mask = None
            
            for color_range in ranges:
                lower, upper = np.array(color_range[0]), np.array(color_range[1])
                temp_mask = cv2.inRange(hsv, lower, upper)
                
                if mask is None:
                    mask = temp_mask
                else:
                    mask = cv2.bitwise_or(mask, temp_mask)
            
            pixel_count = cv2.countNonZero(mask)
            percentage = pixel_count / total_pixels
            
            # Include if >8% of pixels
            if percentage > 0.08:
                detected_colors.append((color_name, percentage))
        
        # Sort by percentage
        detected_colors.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N colors
        return [color[0] for color in detected_colors[:top_n]]
        
    except Exception as e:
        print(f"Error in color histogram: {e}")
        return []

def add_colors_to_detections(image_path, detections):
    """
    Add color information to detection metadata
    
    Args:
        image_path: Path to image file
        detections: List of detection dicts with 'box' key
    
    Returns:
        Updated detections with 'color' and 'colors' keys
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return detections
        
        for det in detections:
            box = det.get("box", [])
            if len(box) >= 4:
                # Get dominant color
                dominant = get_dominant_color(image, box)
                det["color"] = dominant
                
                # Get all significant colors
                colors = get_color_histogram(image, box, top_n=3)
                det["colors"] = colors if colors else [dominant]
        
        return detections
        
    except Exception as e:
        print(f"Error adding colors: {e}")
        return detections
