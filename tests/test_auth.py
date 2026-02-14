"""
Tests for authentication module
"""

import unittest
from auth import login

class TestAuth(unittest.TestCase):
    
    def test_admin_login(self):
        """Test admin login"""
        role = login("admin", "admin123")
        self.assertEqual(role, "admin")
    
    def test_security_login(self):
        """Test security login"""
        role = login("security", "sec123")
        self.assertEqual(role, "security")
    
    def test_viewer_login(self):
        """Test viewer login"""
        role = login("viewer", "view123")
        self.assertEqual(role, "viewer")
    
    def test_invalid_username(self):
        """Test login with invalid username"""
        role = login("invalid", "password")
        self.assertIsNone(role)
    
    def test_invalid_password(self):
        """Test login with invalid password"""
        role = login("admin", "wrongpassword")
        self.assertIsNone(role)
    
    def test_empty_credentials(self):
        """Test login with empty credentials"""
        role = login("", "")
        self.assertIsNone(role)

if __name__ == '__main__':
    unittest.main()
