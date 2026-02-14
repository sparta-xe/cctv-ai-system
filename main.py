from fastapi import FastAPI, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os
import cv2
import numpy as np

from detector import detect
from embedder import add, search
from database import add_frame, get_all_frames
from tracker import assign_id
from auth import login
from clip_engine import add_image_embedding, get_clip_status
from hybrid_search import hybrid_search, get_search_stats
from video_builder import create_highlight_video

app = FastAPI(title="CCTV AI System")
templates = Jinja2Templates(directory="templates")

FRAME_FOLDER = "storage/frames"
STORAGE_FOLDER = "storage"
VIDEO_FOLDER = "storage/videos"
MARKED_FOLDER = "storage/marked"
HIGHLIGHTS_FOLDER = "storage/highlights"

# Create all necessary directories
os.makedirs(FRAME_FOLDER, exist_ok=True)
os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(MARKED_FOLDER, exist_ok=True)
os.makedirs(HIGHLIGHTS_FOLDER, exist_ok=True)

# Serve static files (frames)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    response = templates.TemplateResponse("dashboard.html", {"request": request})
    # Add cache-busting headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    clip_status = get_clip_status()
    all_frames = get_all_frames()
    
    return {
        "status": "healthy",
        "version": "2.0",
        "clip_available": clip_status.get('available', False),
        "clip_device": clip_status.get('device', 'unknown'),
        "frames_indexed": len(all_frames),
        "search_engine": "hybrid" if clip_status.get('available') else "text-only",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

@app.post("/upload/")
async def upload_video(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Invalid video format. Allowed: {', '.join(allowed_extensions)}")
    
    # Validate file size (max 500MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    max_size = 500 * 1024 * 1024  # 500MB
    if file_size > max_size:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: 500MB")
    
    # Sanitize filename
    import re
    safe_filename = re.sub(r'[^\w\s.-]', '', file.filename)
    video_filename = f"video_{safe_filename}"
    path = f"{VIDEO_FOLDER}/{video_filename}"
    
    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    cap = cv2.VideoCapture(path)
    
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Failed to open video file")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # Default fallback
    
    frame_count = 0
    processed_frames = 0
    alerts = []
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % int(fps) == 0:
                timestamp = frame_count / fps
                img_path = f"{FRAME_FOLDER}/frame_{int(timestamp)}.jpg"
                cv2.imwrite(img_path, frame)
                
                detections = detect(img_path)
                
                # Extract objects list for backward compatibility
                objects = [d["label"] for d in detections]
                
                person_id = None
                if "person" in objects:
                    person_id = assign_id(img_path)
                
                meta = {
                    "image": img_path,
                    "timestamp": timestamp,
                    "detections": detections,  # Full detection data with boxes and confidence
                    "objects": objects,  # For backward compatibility
                    "person_id": person_id,
                    "video_path": path,
                    "video_filename": video_filename
                }
                
                # Add to text search index
                add(" ".join(objects), meta)
                
                # Add to CLIP visual search index
                add_image_embedding(img_path, meta)
                
                # Add to database
                add_frame(meta)
                processed_frames += 1
                
                # ALERT: bag without person
                if "backpack" in objects and "person" not in objects:
                    alert_msg = f"⚠ ALERT: Unattended bag detected at {timestamp:.2f}s!"
                    print(alert_msg)
                    alerts.append(alert_msg)
                
                # ALERT: multiple people
                person_count = objects.count("person")
                if person_count > 5:
                    alert_msg = f"⚠ ALERT: Crowd detected ({person_count} people) at {timestamp:.2f}s!"
                    print(alert_msg)
                    alerts.append(alert_msg)
            
            frame_count += 1
    finally:
        cap.release()
    
    # Get search engine status
    search_stats = get_search_stats()
    
    return {
        "status": "Processed",
        "frames": processed_frames,
        "alerts": alerts,
        "total_frames": frame_count,
        "video_filename": video_filename,
        "search_engine": search_stats
    }

@app.post("/query/")
def query(
    username: str = Form(...),
    password: str = Form(...),
    text: str = Form(...)
):
    role = login(username, password)
    if not role:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
    
    # Use hybrid search for better accuracy
    results = hybrid_search(text, top_k=10)
    
    # Handle empty results
    if not results:
        return {
            "role": role,
            "query": text,
            "results": [],
            "count": 0,
            "timeline_markers": [],
            "video_filename": None,
            "highlight_video": None,
            "search_method": "hybrid" if get_clip_status()['available'] else "text-only",
            "message": "No results found. Try a different query."
        }
    
    # Add timeline data for video playback with matched detections
    timeline_markers = []
    video_filename = None
    
    for result in results:
        timeline_markers.append({
            "timestamp": int(result.get("timestamp", 0)),  # Ensure integer seconds
            "objects": result.get("objects", []),
            "person_id": result.get("person_id"),
            "search_score": result.get("search_score", 0),
            "matched_detection_indices": result.get("matched_detection_indices", [])
        })
        if not video_filename and "video_filename" in result:
            video_filename = result.get("video_filename")
    
    # Sort timeline markers by timestamp (ascending order)
    timeline_markers.sort(key=lambda x: x["timestamp"])
    
    # Create highlight video if results found
    highlight_video = None
    if results and len(results) > 0:
        try:
            highlight_path = f"{STORAGE_FOLDER}/highlight_{video_filename}"
            if create_highlight_video(results, highlight_path, fps=2):
                highlight_video = highlight_path
        except Exception as e:
            print(f"Could not create highlight video: {e}")
    
    return {
        "role": role,
        "query": text,
        "results": results,
        "count": len(results),
        "timeline_markers": timeline_markers,
        "video_filename": video_filename,
        "highlight_video": highlight_video,
        "search_method": "hybrid" if get_clip_status()['available'] else "text-only"
    }

@app.get("/stats/")
def get_stats():
    all_frames = get_all_frames()
    
    total_objects = {}
    total_people = 0
    
    for frame in all_frames:
        for obj in frame.get("objects", []):
            total_objects[obj] = total_objects.get(obj, 0) + 1
            if obj == "person":
                total_people += 1
    
    return {
        "total_frames": len(all_frames),
        "total_people_detected": total_people,
        "object_counts": total_objects,
        "unique_objects": len(total_objects)
    }

@app.get("/annotated_image/{frame_name}")
def get_annotated_image(frame_name: str, query: str = "", matched_indices: str = ""):
    """
    Serve an annotated image with bounding boxes drawn on detected objects
    If query is provided, highlight only matching objects
    matched_indices: comma-separated list of detection indices to highlight
    """
    image_path = f"{FRAME_FOLDER}/{frame_name}"
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise HTTPException(status_code=500, detail="Failed to read image")
    
    # Get detection results for this frame
    all_frames = get_all_frames()
    frame_data = None
    for frame in all_frames:
        if frame_name in frame.get("image", ""):
            frame_data = frame
            break
    
    # Parse matched indices
    highlight_indices = set()
    if matched_indices:
        try:
            highlight_indices = set(int(idx) for idx in matched_indices.split(",") if idx.strip())
        except ValueError:
            pass
    
    # Parse query to extract object names (fallback if no indices provided)
    query_objects = []
    if query and not highlight_indices:
        query_lower = query.lower()
        common_objects = ["person", "car", "truck", "bus", "motorcycle", "bicycle", 
                         "backpack", "handbag", "suitcase", "bag", "bottle", "cup",
                         "chair", "couch", "bed", "table", "laptop", "phone", "book"]
        for obj in common_objects:
            if obj in query_lower:
                query_objects.append(obj)
    
    # Draw bounding boxes if we have them
    if frame_data and "detections" in frame_data:
        detections = frame_data["detections"]
        
        for idx, det in enumerate(detections):
            box = det.get("box", [])
            label = det.get("label", "object")
            confidence = det.get("confidence", 0)
            
            if len(box) >= 4:
                x1, y1, x2, y2 = map(int, box[:4])
                
                # Check if this detection should be highlighted
                is_query_match = False
                
                if highlight_indices:
                    # Use matched indices if provided
                    is_query_match = idx in highlight_indices
                elif query_objects:
                    # Fallback to query object matching
                    for query_obj in query_objects:
                        if query_obj in label.lower():
                            is_query_match = True
                            break
                else:
                    # No query - show all objects normally
                    is_query_match = False
                
                # Choose color and thickness based on match
                if is_query_match:
                    # Highlighted - thick, bright color
                    thickness = 4
                    if label == "person":
                        color = (0, 255, 0)  # Bright Green
                    elif label == "car":
                        color = (255, 0, 0)  # Bright Blue
                    elif "backpack" in label or "bag" in label:
                        color = (0, 165, 255)  # Bright Orange
                    else:
                        color = (255, 255, 0)  # Bright Cyan
                    
                    # Draw thick rectangle for query matches
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
                    
                    # Draw label background with highlight
                    label_text = f">>> {label.upper()} ({confidence:.2f}) <<<"
                    font_scale = 0.8
                    font_thickness = 2
                    (text_width, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                    
                    # Yellow background for highlight
                    cv2.rectangle(img, (x1, y1 - text_height - 15), (x1 + text_width + 10, y1), (0, 255, 255), -1)
                    
                    # Black text for contrast
                    cv2.putText(img, label_text, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)
                else:
                    # Non-matching objects - thin, gray
                    thickness = 1
                    color = (128, 128, 128)  # Gray
                    
                    # Draw thin rectangle
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
                    
                    # Small gray label
                    label_text = f"{label} ({confidence:.2f})"
                    font_scale = 0.4
                    font_thickness = 1
                    (text_width, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                    
                    # Gray background
                    cv2.rectangle(img, (x1, y1 - text_height - 8), (x1 + text_width, y1), (128, 128, 128), -1)
                    
                    # White text
                    cv2.putText(img, label_text, (x1, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
    
    # Save annotated image temporarily
    annotated_path = f"{FRAME_FOLDER}/annotated_{frame_name}"
    cv2.imwrite(annotated_path, img)
    
    return FileResponse(annotated_path, media_type="image/jpeg")

@app.get("/video/{video_filename}")
def get_video(video_filename: str):
    """
    Serve video file for playback
    """
    video_path = f"{VIDEO_FOLDER}/{video_filename}"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(video_path, media_type="video/mp4")

@app.get("/video_info/{video_filename}")
def get_video_info(video_filename: str):
    """
    Get video metadata (duration, fps, etc.)
    """
    video_path = f"{VIDEO_FOLDER}/{video_filename}"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    return {
        "duration": duration,
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height
    }

if __name__ == "__main__":
    import uvicorn
    os.makedirs("storage/frames", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
