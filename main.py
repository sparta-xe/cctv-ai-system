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

app = FastAPI(title="CCTV AI System")
templates = Jinja2Templates(directory="templates")

FRAME_FOLDER = "storage/frames"
STORAGE_FOLDER = "storage"
VIDEO_FOLDER = "storage/videos"
os.makedirs(FRAME_FOLDER, exist_ok=True)
os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Serve static files (frames)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/upload/")
async def upload_video(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid video format")
    
    # Save to videos folder
    video_filename = f"video_{file.filename}"
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
                
                objects, boxes = detect(img_path)
                person_id = None
                if "person" in objects:
                    person_id = assign_id(img_path)
                
                meta = {
                    "image": img_path,
                    "timestamp": timestamp,
                    "objects": objects,
                    "person_id": person_id,
                    "boxes": boxes,
                    "video_path": path,
                    "video_filename": video_filename
                }
                
                add(" ".join(objects), meta)
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
    
    return {
        "status": "Processed",
        "frames": processed_frames,
        "alerts": alerts,
        "total_frames": frame_count,
        "video_filename": video_filename
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
    
    results = search(text)
    
    # Add timeline data for video playback
    timeline_markers = []
    video_filename = None
    
    for result in results:
        timeline_markers.append({
            "timestamp": result.get("timestamp", 0),
            "objects": result.get("objects", []),
            "person_id": result.get("person_id")
        })
        if not video_filename and "video_filename" in result:
            video_filename = result.get("video_filename")
    
    return {
        "role": role,
        "query": text,
        "results": results,
        "count": len(results),
        "timeline_markers": timeline_markers,
        "video_filename": video_filename
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
def get_annotated_image(frame_name: str, query: str = ""):
    """
    Serve an annotated image with bounding boxes drawn on detected objects
    If query is provided, highlight only matching objects
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
    
    # Parse query to extract object names
    query_objects = []
    if query:
        query_lower = query.lower()
        # Extract common object names from query
        common_objects = ["person", "car", "truck", "bus", "motorcycle", "bicycle", 
                         "backpack", "handbag", "suitcase", "bag", "bottle", "cup",
                         "chair", "couch", "bed", "table", "laptop", "phone", "book"]
        for obj in common_objects:
            if obj in query_lower:
                query_objects.append(obj)
    
    # Draw bounding boxes if we have them
    if frame_data and "boxes" in frame_data:
        boxes = frame_data["boxes"]
        objects = frame_data.get("objects", [])
        
        for i, box in enumerate(boxes):
            if box and len(box) > 0:
                # Extract coordinates
                x1, y1, x2, y2 = map(int, box[0][:4])
                
                # Get object label
                label = objects[i] if i < len(objects) else "object"
                
                # Check if this object matches the query
                is_query_match = False
                if query_objects:
                    for query_obj in query_objects:
                        if query_obj in label.lower():
                            is_query_match = True
                            break
                else:
                    # If no query, show all objects
                    is_query_match = True
                
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
                    label_text = f">>> {label.upper()} <<<"
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
                    label_text = label
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
