"""
Hybrid search combining CLIP visual matching + text embeddings
Provides national-level accuracy with smart scoring
"""

from embedder import search as text_search
from clip_engine import search_clip, get_clip_status
from query_parser import parse_query

def hybrid_search(query, top_k=10):
    """
    Hybrid search combining multiple methods
    
    Args:
        query: Natural language query
        top_k: Number of results to return
    
    Returns:
        List of ranked results with scores
    """
    # Parse query for structured information
    parsed = parse_query(query)
    
    # Get results from text search
    text_results = text_search(query, k=top_k)
    
    # Get results from CLIP if available
    clip_status = get_clip_status()
    clip_results = []
    if clip_status['available']:
        clip_results = search_clip(query, top_k=top_k)
    
    # Combine results with scoring
    combined = {}
    
    # Add text search results (weight: 0.4)
    for item in text_results:
        image_key = item.get("image", "")
        if image_key:
            combined[image_key] = {
                "meta": item,
                "text_score": 0.4,
                "clip_score": 0.0,
                "total_score": 0.4
            }
    
    # Add CLIP results (weight: 0.6 - visual matching is more accurate)
    for item in clip_results:
        image_key = item.get("image", "")
        if image_key:
            clip_score = item.get('clip_score', 0) * 0.6
            
            if image_key in combined:
                # Boost score if found in both
                combined[image_key]["clip_score"] = clip_score
                combined[image_key]["total_score"] += clip_score
            else:
                combined[image_key] = {
                    "meta": item,
                    "text_score": 0.0,
                    "clip_score": clip_score,
                    "total_score": clip_score
                }
    
    # Apply query filters
    filtered = []
    for image_key, data in combined.items():
        meta = data["meta"]
        
        # Time range filter
        if parsed.get("time_range"):
            timestamp = meta.get("timestamp", 0)
            if not (parsed["time_range"]["start"] <= timestamp <= parsed["time_range"]["end"]):
                continue
        
        # Object filter
        if parsed.get("objects"):
            detected_objects = meta.get("objects", [])
            has_match = any(
                obj in " ".join(detected_objects).lower()
                for obj in parsed["objects"]
            )
            if has_match:
                data["total_score"] += 0.2  # Boost for object match
        
        filtered.append(data)
    
    # Sort by total score
    filtered.sort(key=lambda x: x["total_score"], reverse=True)
    
    # Return top-k results with scores
    results = []
    for item in filtered[:top_k]:
        result = item["meta"].copy()
        result["search_score"] = round(item["total_score"], 3)
        result["text_score"] = round(item["text_score"], 3)
        result["clip_score"] = round(item["clip_score"], 3)
        results.append(result)
    
    return results

def get_search_stats():
    """Get statistics about search engines"""
    clip_status = get_clip_status()
    
    return {
        "clip_available": clip_status['available'],
        "clip_device": clip_status['device'],
        "clip_indexed": clip_status['indexed_images'],
        "hybrid_search": "enabled" if clip_status['available'] else "text-only"
    }
