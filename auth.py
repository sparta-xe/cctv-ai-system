import hashlib

users = {
    "admin": {"password": "admin123", "role": "admin", "permissions": ["upload", "query", "delete"]},
    "security": {"password": "sec123", "role": "security", "permissions": ["query"]},
    "viewer": {"password": "view123", "role": "viewer", "permissions": ["query"]},
}

def login(username, password):
    """
    Authenticate user with username and password
    
    Args:
        username: Username string
        password: Password string
    
    Returns:
        str: User role if authenticated, None otherwise
    """
    if not username or not password:
        return None
    
    user = users.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

def get_user_permissions(username):
    """
    Get permissions for a user
    
    Args:
        username: Username string
    
    Returns:
        list: List of permission strings
    """
    user = users.get(username)
    if user:
        return user.get("permissions", [])
    return []

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role, permissions):
    """
    Add a new user (for future expansion)
    
    Args:
        username: Username string
        password: Plain text password
        role: User role
        permissions: List of permissions
    """
    users[username] = {
        "password": password,
        "role": role,
        "permissions": permissions
    }
