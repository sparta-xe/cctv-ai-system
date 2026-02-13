import numpy as np
from sentence_transformers import SentenceTransformer
import cv2

model = SentenceTransformer('all-MiniLM-L6-v2')

tracked = []

def assign_id(image_path, similarity_threshold=0.85):
    """
    Assign a person ID based on image similarity (basic Re-ID simulation)
    
    Args:
        image_path: Path to the person image
        similarity_threshold: Minimum similarity to match existing person
    
    Returns:
        str: Person ID (e.g., "P1", "P2")
    """
    try:
        # Read and encode image
        img = cv2.imread(image_path)
        if img is None:
            return f"P{len(tracked)+1}"
        
        # Use image path as simple feature (in production, use proper Re-ID model)
        vector = model.encode(image_path)
        
        # Normalize vector for cosine similarity
        vector_norm = vector / np.linalg.norm(vector)
        
        # Check against existing tracked persons
        for person in tracked:
            person_vector_norm = person["embedding"] / np.linalg.norm(person["embedding"])
            similarity = np.dot(person_vector_norm, vector_norm)
            
            if similarity > similarity_threshold:
                person["last_seen"] = image_path
                return person["id"]
        
        # New person detected
        new_id = f"P{len(tracked)+1}"
        tracked.append({
            "id": new_id,
            "embedding": vector,
            "first_seen": image_path,
            "last_seen": image_path
        })
        return new_id
    except Exception as e:
        print(f"Error in person tracking: {e}")
        return f"P{len(tracked)+1}"

def get_tracked_count():
    """Return the number of unique persons tracked"""
    return len(tracked)

def reset_tracking():
    """Clear all tracked persons"""
    global tracked
    tracked = []
