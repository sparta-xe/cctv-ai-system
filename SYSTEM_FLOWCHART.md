# AI CCTV System - Visual Flowchart

## 🎬 Complete System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Upload     │  │    Search    │  │   Results    │             │
│  │   Section    │  │   Section    │  │    Grid      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                     │
│         │                  │                  │                     │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   /upload/   │  │   /query/    │  │ /annotated_  │             │
│  │   endpoint   │  │   endpoint   │  │   image/     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  VIDEO PROCESSING                                            │ │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │ │
│  │  │ Frame  │→ │ Object │→ │ Color  │→ │ Store  │            │ │
│  │  │Extract │  │ Detect │  │ Detect │  │  Data  │            │ │
│  │  └────────┘  └────────┘  └────────┘  └────────┘            │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  SEARCH PROCESSING                                           │ │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │ │
│  │  │ Parse  │→ │ Hybrid │→ │ Filter │→ │ Rank & │            │ │
│  │  │ Query  │  │ Search │  │ Match  │  │ Return │            │ │
│  │  └────────┘  └────────┘  └────────┘  └────────┘            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Database   │  │     FAISS    │  │     CLIP     │             │
│  │  (Frames)    │  │   (Text)     │  │   (Visual)   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📹 Video Upload Flow

```
START: User selects video file
  │
  ├─→ [Validate file]
  │    ├─ Check format (MP4, AVI, MOV, etc.)
  │    ├─ Check size (< 500MB)
  │    └─ Check not empty
  │
  ├─→ [Auto-clear previous data]
  │    ├─ Clear database
  │    ├─ Clear FAISS index
  │    └─ Clear CLIP index
  │
  ├─→ [Save video to storage/videos/]
  │
  ├─→ [Open video with OpenCV]
  │
  ├─→ [FOR EACH FRAME (every 5th)]
  │    │
  │    ├─→ [Extract frame]
  │    │    └─ Resize to 640px width
  │    │
  │    ├─→ [Save frame as JPG]
  │    │    └─ storage/frames/frame_X.jpg
  │    │
  │    ├─→ [YOLOv8 Detection]
  │    │    ├─ Detect objects
  │    │    ├─ Get bounding boxes
  │    │    └─ Get confidence scores
  │    │
  │    ├─→ [Color Detection]
  │    │    ├─ Extract object region
  │    │    ├─ Convert to HSV
  │    │    ├─ Apply color masks
  │    │    └─ Get dominant color
  │    │
  │    ├─→ [Create metadata]
  │    │    └─ {image, timestamp, detections, objects, colors}
  │    │
  │    ├─→ [Index in FAISS]
  │    │    └─ Text embedding of objects
  │    │
  │    ├─→ [Index in CLIP]
  │    │    └─ Visual embedding of image
  │    │
  │    ├─→ [Store in database]
  │    │    └─ Add to frames list
  │    │
  │    └─→ [Check for alerts]
  │         ├─ Unattended bag?
  │         └─ Crowd detected?
  │
  └─→ [Return results]
       ├─ Total frames processed
       ├─ Alerts generated
       └─ Processing time

END: Video indexed and searchable
```

---

## 🔍 Search Query Flow

```
START: User enters query "red car near entrance"
  │
  ├─→ [Parse Query]
  │    ├─ Extract objects: ["car"]
  │    ├─ Extract colors: ["red"]
  │    ├─ Extract location: "near entrance"
  │    └─ Extract time range: (if any)
  │
  ├─→ [Text Search (FAISS)]
  │    ├─ Encode query to vector
  │    ├─ Search similar vectors
  │    ├─ Get top-K matches
  │    └─ Score: 40% weight
  │
  ├─→ [Visual Search (CLIP)]
  │    ├─ Encode query to features
  │    ├─ Compare with image features
  │    ├─ Calculate similarity
  │    └─ Score: 60% weight
  │
  ├─→ [Combine Results]
  │    ├─ Merge by image path
  │    ├─ Sum weighted scores
  │    └─ Total score = text + visual
  │
  ├─→ [Filter & Match]
  │    ├─ FOR EACH FRAME:
  │    │   ├─ FOR EACH DETECTION:
  │    │   │   ├─ Check object match
  │    │   │   ├─ Check color match
  │    │   │   └─ If BOTH match:
  │    │   │       ├─ Add to matched_indices
  │    │   │       ├─ Boost score +20% (object)
  │    │   │       └─ Boost score +30% (color)
  │    │   │
  │    │   └─ Keep frame if has matches
  │    │
  │    └─ Filter out frames with no matches
  │
  ├─→ [Sort Results]
  │    ├─ Primary: Score (descending)
  │    └─ Secondary: Timestamp (ascending)
  │
  ├─→ [Return Top-10]
  │    ├─ Frame metadata
  │    ├─ Matched detection indices
  │    ├─ Search scores
  │    └─ Timeline markers
  │
  └─→ [Render Results]
       ├─ Generate annotated images
       ├─ Highlight matched objects (green)
       ├─ Show other objects (cyan)
       └─ Display in chronological order

END: Results displayed to user
```

---

## 🎨 Object Detection Flow

```
INPUT: Video frame (image)
  │
  ├─→ [Preprocess]
  │    ├─ Resize to model input size
  │    ├─ Normalize pixel values
  │    └─ Convert to tensor
  │
  ├─→ [YOLOv8 Inference]
  │    ├─ Forward pass through network
  │    ├─ Get predictions
  │    └─ Apply NMS (Non-Max Suppression)
  │
  ├─→ [Filter by confidence]
  │    └─ Keep only > 0.5 confidence
  │
  ├─→ [FOR EACH DETECTION]
  │    │
  │    ├─→ [Extract info]
  │    │    ├─ Bounding box [x1, y1, x2, y2]
  │    │    ├─ Class label (person, car, etc.)
  │    │    └─ Confidence score
  │    │
  │    ├─→ [Color Detection]
  │    │    ├─ Crop object region
  │    │    ├─ Convert BGR → HSV
  │    │    ├─ Apply 12 color masks
  │    │    ├─ Count pixels per color
  │    │    ├─ Get dominant (>15%)
  │    │    └─ Get top 3 colors
  │    │
  │    └─→ [Create detection dict]
  │         └─ {label, box, confidence, color, colors}
  │
  └─→ [Return detections list]

OUTPUT: List of detected objects with metadata
```

---

## 🌈 Color Detection Flow

```
INPUT: Image region (bounding box)
  │
  ├─→ [Validate region]
  │    ├─ Check bounds
  │    └─ Ensure not empty
  │
  ├─→ [Extract ROI]
  │    └─ Crop image[y1:y2, x1:x2]
  │
  ├─→ [Resize if large]
  │    └─ Max 100x100 for speed
  │
  ├─→ [Convert to HSV]
  │    └─ Better for color detection
  │
  ├─→ [Apply Gaussian blur]
  │    └─ Reduce noise
  │
  ├─→ [FOR EACH COLOR (12 colors)]
  │    │
  │    ├─→ [Create mask]
  │    │    ├─ Red: [0-10, 170-180] hue
  │    │    ├─ Blue: [95-130] hue
  │    │    ├─ Green: [35-85] hue
  │    │    └─ ... (9 more colors)
  │    │
  │    ├─→ [Count pixels]
  │    │    └─ cv2.countNonZero(mask)
  │    │
  │    └─→ [Calculate percentage]
  │         └─ pixel_count / total_pixels
  │
  ├─→ [Get dominant color]
  │    ├─ Find max percentage
  │    └─ Return if > 15%
  │
  └─→ [Get top 3 colors]
       └─ Sort by percentage

OUTPUT: Dominant color + list of colors
```

---

## 🔄 Data Clear Flow

```
TRIGGER: New video upload OR manual clear button
  │
  ├─→ [User confirmation]
  │    └─ "Clear all data?" dialog
  │
  ├─→ [Clear Database]
  │    └─ frames = []
  │
  ├─→ [Clear FAISS Index]
  │    ├─ metadata = []
  │    └─ index = new IndexFlatL2()
  │
  ├─→ [Clear CLIP Index]
  │    ├─ image_embeddings = []
  │    └─ image_metadata = []
  │
  ├─→ [Reset UI Stats]
  │    ├─ Total Frames = 0
  │    ├─ Detections = 0
  │    └─ Alerts = 0
  │
  └─→ [Show success message]
       └─ "All data cleared successfully!"

RESULT: Clean state, ready for new video
```

---

## 🎯 Bounding Box Annotation Flow

```
INPUT: Frame + Detections + Query + Matched Indices
  │
  ├─→ [Load image]
  │    └─ cv2.imread(frame_path)
  │
  ├─→ [FOR EACH DETECTION]
  │    │
  │    ├─→ [Check if matched]
  │    │    └─ Is index in matched_indices?
  │    │
  │    ├─→ [IF MATCHED (query result)]
  │    │    ├─ Color: Bright Green (0, 255, 0)
  │    │    ├─ Thickness: 2px
  │    │    ├─ Label: "color object 95%"
  │    │    └─ Background: Green
  │    │
  │    ├─→ [ELSE (other objects)]
  │    │    ├─ Color: Cyan (56, 189, 248)
  │    │    ├─ Thickness: 2px
  │    │    ├─ Label: "object 95%"
  │    │    └─ Background: Dark gray
  │    │
  │    ├─→ [Draw rectangle]
  │    │    └─ cv2.rectangle(img, pt1, pt2, color, thickness)
  │    │
  │    └─→ [Draw label]
  │         ├─ Calculate text size
  │         ├─ Draw background rectangle
  │         └─ Draw text
  │
  ├─→ [Save annotated image]
  │    └─ cv2.imwrite(output_path, img)
  │
  └─→ [Return image path]

OUTPUT: Annotated image with colored boxes
```

---

## 📊 Score Calculation Flow

```
INPUT: Query + Frame detections
  │
  ├─→ [Text Search Score]
  │    ├─ FAISS similarity
  │    └─ Weight: 0.4 (40%)
  │
  ├─→ [Visual Search Score]
  │    ├─ CLIP similarity
  │    └─ Weight: 0.6 (60%)
  │
  ├─→ [Base Score]
  │    └─ text_score + clip_score
  │
  ├─→ [Object Match Boost]
  │    ├─ IF query object in detection
  │    └─ +0.2 (20% boost)
  │
  ├─→ [Color Match Boost]
  │    ├─ IF query color in detection
  │    └─ +0.3 (30% boost)
  │
  └─→ [Final Score]
       └─ base + object_boost + color_boost

OUTPUT: Total score (0.0 - 2.0 range)

EXAMPLE:
  Query: "red car"
  Frame: Has red car detection
  
  Calculation:
  - Text score: 0.35 × 0.4 = 0.14
  - CLIP score: 0.85 × 0.6 = 0.51
  - Base: 0.65
  - Object match: +0.20
  - Color match: +0.30
  - Final: 1.15 (115%)
```

---

## 🎬 Timeline Marker Flow

```
INPUT: Search results
  │
  ├─→ [FOR EACH RESULT]
  │    │
  │    ├─→ [Extract data]
  │    │    ├─ Timestamp (seconds)
  │    │    ├─ Objects detected
  │    │    ├─ Search score
  │    │    └─ Matched indices
  │    │
  │    └─→ [Create marker]
  │         └─ {timestamp, objects, score, indices}
  │
  ├─→ [Sort by timestamp]
  │    └─ Ascending order (chronological)
  │
  ├─→ [Send to frontend]
  │    └─ timeline_markers array
  │
  └─→ [Frontend renders]
       ├─ Calculate position on timeline
       ├─ Draw marker dot
       └─ Enable click to jump

RESULT: Interactive timeline with markers
```

---

## 🔄 Complete User Journey

```
1. USER OPENS APP
   └─→ Dashboard loads with cyber theme

2. USER UPLOADS VIDEO
   ├─→ Drag & drop or click to select
   ├─→ System validates file
   ├─→ Auto-clears previous data
   ├─→ Processes video (2-5 min)
   └─→ Shows stats and alerts

3. USER SEARCHES
   ├─→ Types: "red car near entrance"
   ├─→ System processes query
   ├─→ Returns top 10 results
   └─→ Displays keyframes in grid

4. USER INTERACTS
   ├─→ Single-click: Opens modal
   ├─→ Double-click: Jumps to video
   ├─→ ESC: Closes modal
   └─→ Plays video at timestamp

5. USER CLEARS DATA
   ├─→ Clicks "Clear All Data"
   ├─→ Confirms action
   └─→ System resets

6. USER UPLOADS NEW VIDEO
   └─→ Cycle repeats from step 2
```

---

This flowchart provides a complete visual understanding of how every component works together! 🚀
