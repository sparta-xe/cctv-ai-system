frames = []

def add_frame(data):
    """Add a frame entry to the database"""
    frames.append(data)

def filter_time(start, end):
    """
    Filter frames by timestamp range
    
    Args:
        start: Start timestamp in seconds
        end: End timestamp in seconds
    
    Returns:
        list: Filtered frame entries
    """
    return [f for f in frames if start <= f.get("timestamp", 0) <= end]

def get_all_frames():
    """Return all stored frames"""
    return frames

def get_frames_with_object(object_name):
    """
    Get all frames containing a specific object
    
    Args:
        object_name: Name of the object to search for
    
    Returns:
        list: Frames containing the object
    """
    return [f for f in frames if object_name in f.get("objects", [])]

def get_frame_count():
    """Return the total number of frames"""
    return len(frames)

def clear_database():
    """Clear all stored frames"""
    global frames
    frames = []
