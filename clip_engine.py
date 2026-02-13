"""
CLIP-based visual + text matching for better query accuracy
Multimodal search using OpenAI's CLIP model
"""

import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🎯 CLIP Engine using: {device.upper()}")

# Initialize CLIP model
try:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("✅ CLIP model loaded successfully")
except Exception as e:
    print(f"⚠️  CLIP model loading failed: {e}")
    model = None
    processor = None

# Storage for embeddings
image_embeddings = []
image_metadata = []

def add_image_embedding(image_path, meta):
    """
    Add image embedding to CLIP index
    
    Args:
        image_path: Path to image file
        meta: Metadata dictionary
    """
    if model is None or processor is None:
        return
    
    try:
        if not os.path.exists(image_path):
            return
        
        # Load and process image
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt").to(device)
        
        # Get image features
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        
        # Normalize features
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        
        # Store
        image_embeddings.append(image_features.cpu().numpy())
        image_metadata.append(meta)
        
    except Exception as e:
        print(f"Error adding image embedding: {e}")

def search_clip(query, top_k=5):
    """
    Search images using CLIP text-to-image matching
    
    Args:
        query: Text query
        top_k: Number of results to return
    
    Returns:
        List of metadata dictionaries for matching images
    """
    if model is None or processor is None or len(image_embeddings) == 0:
        return []
    
    try:
        # Process text query
        inputs = processor(text=[query], return_tensors="pt").to(device)
        
        # Get text features
        with torch.no_grad():
            text_features = model.get_text_features(**inputs)
        
        # Normalize features
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
        text_features = text_features.cpu().numpy()
        
        # Calculate similarities
        similarities = []
        for i, img_emb in enumerate(image_embeddings):
            sim = np.dot(text_features, img_emb.T)[0][0]
            similarities.append((float(sim), image_metadata[i]))
        
        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top-k results with scores
        results = []
        for score, meta in similarities[:top_k]:
            result = meta.copy()
            result['clip_score'] = score
            results.append(result)
        
        return results
        
    except Exception as e:
        print(f"Error in CLIP search: {e}")
        return []

def get_clip_status():
    """Return CLIP engine status"""
    return {
        "available": model is not None,
        "device": device,
        "indexed_images": len(image_embeddings)
    }

def clear_clip_index():
    """Clear all CLIP embeddings"""
    global image_embeddings, image_metadata
    image_embeddings = []
    image_metadata = []
