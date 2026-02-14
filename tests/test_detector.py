"""
Tests for detector module
"""

import unittest
import os
import cv2
import numpy as np
from detector import detect

class TestDetector(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Create a test image"""
        cls.test_image_path = "test_image.jpg"
        # Create a simple test image
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.imwrite(cls.test_image_path, img)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test image"""
        if os.path.exists(cls.test_image_path):
            os.remove(cls.test_image_path)
    
    def test_detect_returns_list(self):
        """Test that detect returns a list"""
        result = detect(self.test_image_path)
        self.assertIsInstance(result, list)
    
    def test_detect_with_invalid_path(self):
        """Test detect with invalid image path"""
        result = detect("nonexistent.jpg")
        self.assertEqual(result, [])
    
    def test_detect_with_confidence_threshold(self):
        """Test detect with custom confidence threshold"""
        result = detect(self.test_image_path, confidence_threshold=0.7)
        self.assertIsInstance(result, list)
    
    def test_detection_format(self):
        """Test that detections have correct format"""
        result = detect(self.test_image_path)
        if result:  # If any detections
            detection = result[0]
            self.assertIn("label", detection)
            self.assertIn("box", detection)
            self.assertIn("confidence", detection)
            self.assertIsInstance(detection["box"], list)
            self.assertEqual(len(detection["box"]), 4)

if __name__ == '__main__':
    unittest.main()
