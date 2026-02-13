from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

dimension = 384
index = faiss.IndexFlatL2(dimension)
metadata = []

def add(text, meta):
    """
    Add a text embedding to the FAISS index
    
    Args:
        text: Text to encode
        meta: Metadata dictionary to store
    """
    if not text or not text.strip():
        text = "unknown"
    
    vector = model.encode([text])
    index.add(np.array(vector).astype('float32'))
    metadata.append(meta)

def search(query, k=5):
    """
    Search for similar embeddings in the index
    
    Args:
        query: Query text
        k: Number of results to return
    
    Returns:
        list: List of metadata dictionaries for matching results
    """
    if not metadata:
        return []
    
    if not query or not query.strip():
        return []
    
    # Limit k to available items
    k = min(k, len(metadata))
    
    vector = model.encode([query])
    D, I = index.search(np.array(vector).astype('float32'), k)
    
    results = []
    for i in I[0]:
        if i < len(metadata) and i >= 0:
            results.append(metadata[i])
    
    return results

def get_index_size():
    """Return the number of items in the index"""
    return len(metadata)
