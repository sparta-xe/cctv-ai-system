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
    
    # Apply query filters and match specific detections
    filtered = []
    for image_key, data in combined.items():
        meta = data["meta"]
        
        # Time range filter
        if parsed.get("time_range"):
            timestamp = meta.get("timestamp", 0)
            if not (parsed["time_range"]["start"] <= timestamp <= parsed["time_range"]["end"]):
                continue
        
        # Match specific detections to query
        matched_detection_indices = []
        detections = meta.get("detections", [])
        
        if parsed.get("objects") or parsed.get("colors"):
            # Match query objects and colors to specific detections
            for idx, det in enumerate(detections):
                det_label = det.get("label", "").lower()
                det_color = det.get("color", "").lower()
                det_colors = [c.lower() for c in det.get("colors", [])]
                
                object_matched = False
                color_matched = False
                
                # Check object match
                if parsed.get("objects"):
                    for query_obj in parsed["objects"]:
                        if query_obj.lower() in det_label:
                            object_matched = True
                            break
                else:
                    # No object filter specified, so any object matches
                    object_matched = True
                
                # Check color match
                if parsed.get("colors"):
                    for query_color in parsed["colors"]:
                        query_color_lower = query_color.lower()
                        if query_color_lower == det_color or query_color_lower in det_colors:
                            color_matched = True
                            break
                else:
                    # No color filter specified, so any color matches
                    color_matched = True
                
                # BOTH conditions must be true (AND logic)
                if object_matched and color_matched:
                    matched_detection_indices.append(idx)
                    
                    # Boost score for matches
                    if parsed.get("objects") and object_matched:
                        data["total_score"] += 0.2
                    if parsed.get("colors") and color_matched:
                        data["total_score"] += 0.3
        else:
            # No specific object/color filter - all detections are matches
            matched_detection_indices = list(range(len(detections)))
        
        # Store matched detection indices
        data["matched_detection_indices"] = matched_detection_indices
        
        # Only include frames that have at least one matched detection
        if len(matched_detection_indices) > 0:
            filtered.append(data)
    
    # Sort by total score (primary) and timestamp (secondary - ascending)
    filtered.sort(key=lambda x: (-x["total_score"], x["meta"].get("timestamp", 0)))
    
    # Return top-k results with scores and matched detection indices
    results = []
    for item in filtered[:top_k]:
        result = item["meta"].copy()
        result["search_score"] = round(item["total_score"], 3)
        result["text_score"] = round(item["text_score"], 3)
        result["clip_score"] = round(item["clip_score"], 3)
        result["matched_detection_indices"] = item["matched_detection_indices"]
        results.append(result)
    
    # Final sort by timestamp in ascending order (chronological)
    results.sort(key=lambda x: x.get("timestamp", 0))
    
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
