"""
Tests for utility functions
"""

import unittest
import os
from utils import (
    format_timestamp,
    format_file_size,
    sanitize_filename,
    ensure_directories
)

class TestUtils(unittest.TestCase):
    
    def test_format_timestamp(self):
        """Test timestamp formatting"""
        self.assertEqual(format_timestamp(0), "00:00")
        self.assertEqual(format_timestamp(65), "01:05")
        self.assertEqual(format_timestamp(3661), "61:01")
    
    def test_format_file_size(self):
        """Test file size formatting"""
        self.assertEqual(format_file_size(0), "0.00 B")
        self.assertEqual(format_file_size(1024), "1.00 KB")
        self.assertEqual(format_file_size(1048576), "1.00 MB")
        self.assertEqual(format_file_size(1073741824), "1.00 GB")
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        self.assertEqual(sanitize_filename("test file.mp4"), "test_file.mp4")
        self.assertEqual(sanitize_filename("test@#$file.mp4"), "testfile.mp4")
        self.assertEqual(sanitize_filename("test-file_2.mp4"), "test-file_2.mp4")
    
    def test_ensure_directories(self):
        """Test directory creation"""
        ensure_directories()
        self.assertTrue(os.path.exists("storage"))
        self.assertTrue(os.path.exists("storage/frames"))
        self.assertTrue(os.path.exists("storage/videos"))
        self.assertTrue(os.path.exists("logs"))

if __name__ == '__main__':
    unittest.main()
