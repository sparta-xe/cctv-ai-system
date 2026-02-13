"""
LLM-based structured query parsing
Extracts objects, colors, time ranges, and locations from natural language
"""

import json
import re
import os

# Try to import OpenAI (optional)
try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
except ImportError:
    OPENAI_AVAILABLE = False

def parse_query_with_llm(query):
    """
    Parse query using OpenAI GPT (requires API key)
    
    Args:
        query: Natural language query
    
    Returns:
        Dictionary with structured query components
    """
    if not OPENAI_AVAILABLE or not openai.api_key:
        return parse_query_regex(query)
    
    try:
        prompt = f"""
Extract structured information from this CCTV search query.

Query: "{query}"

Return JSON with:
- objects (list of object names)
- colors (list of colors mentioned)
- time_range (dict with start and end if mentioned)
- location (string if mentioned)
- action (string if action mentioned like "walking", "running")

Return only valid JSON, no other text.
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        result = json.loads(response["choices"][0]["message"]["content"])
        return result
        
    except Exception as e:
        print(f"LLM parsing failed, using regex fallback: {e}")
        return parse_query_regex(query)

def parse_query_regex(query):
    """
    Parse query using regex patterns (offline fallback)
    
    Args:
        query: Natural language query
    
    Returns:
        Dictionary with structured query components
    """
    query_lower = query.lower()
    
    # Common objects
    objects = []
    object_patterns = [
        "person", "people", "man", "woman", "child", "kid",
        "car", "vehicle", "truck", "bus", "motorcycle", "bicycle", "bike",
        "backpack", "bag", "handbag", "suitcase", "luggage",
        "phone", "laptop", "bottle", "cup", "book",
        "chair", "table", "couch", "bed"
    ]
    
    for obj in object_patterns:
        if obj in query_lower:
            objects.append(obj)
    
    # Colors
    colors = []
    color_patterns = [
        "red", "blue", "green", "yellow", "black", "white",
        "orange", "purple", "pink", "brown", "gray", "grey"
    ]
    
    for color in color_patterns:
        if color in query_lower:
            colors.append(color)
    
    # Time range
    time_range = None
    time_match = re.search(r'between (\d+) and (\d+)', query_lower)
    if time_match:
        time_range = {
            "start": int(time_match.group(1)),
            "end": int(time_match.group(2))
        }
    
    # Location
    location = None
    location_patterns = ["entrance", "exit", "door", "gate", "lobby", "hallway", "corridor"]
    for loc in location_patterns:
        if loc in query_lower:
            location = loc
            break
    
    # Action
    action = None
    action_patterns = ["walking", "running", "standing", "sitting", "carrying", "holding"]
    for act in action_patterns:
        if act in query_lower:
            action = act
            break
    
    return {
        "objects": objects,
        "colors": colors,
        "time_range": time_range,
        "location": location,
        "action": action,
        "original_query": query
    }

def parse_query(query):
    """
    Main query parsing function
    Tries LLM first, falls back to regex
    
    Args:
        query: Natural language query
    
    Returns:
        Dictionary with structured query components
    """
    # Try LLM if available
    if OPENAI_AVAILABLE and openai.api_key:
        return parse_query_with_llm(query)
    else:
        return parse_query_regex(query)
