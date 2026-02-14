# 🎬 Complete Video Playback Guide - How It Works

## 🎯 Overview

The CCTV AI System now includes **interactive video playback** with **timeline markers** that show exactly where your query matches appear in the video.

## ✨ Key Features

### 1. Video Player
- Plays the original uploaded video
- Standard HTML5 video controls
- Fullscreen support
- Responsive design

### 2. Timeline Markers
- **Green markers** → Query match locations
- **Yellow marker** → Current playback position
- **Clickable** → Jump to any match
- **Tooltips** → Show timestamp and detected objects

### 3. Interactive Navigation
- **Click timeline markers** → Jump to that moment
- **Click timestamps** → Jump to exact time
- **Click result images** → Jump to that frame
- **Auto-play** → Video starts playing after jump
- **Auto-scroll** → Page scrolls to video player

## 📊 Visual Layout

```
┌─────────────────────────────────────────────────────────┐
│  🎬 Video Playback with Timeline                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │              VIDEO PLAYER                          │ │
│  │          (Original Uploaded Video)                 │ │
│  │                                                    │ │
│  │  [Play] [Pause] [Volume] [Fullscreen]            │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Timeline:                                               │
│  ├──────|────────|──────────|─────────────────────────┤ │
│  0:00   ↑        ↑          ↑                      1:30 │
│       Match1   Match2    Match3                         │
│      (Green)  (Green)   (Green)                         │
│         ↑                                                │
│    Current Position (Yellow)                            │
│                                                          │
│  Legend: 🟢 Query Match  🟡 Current Position            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  📊 Results                                              │
│                                                          │
│  🎯 Result 1                                            │
│  [Image] | ⏱️ 0:05 (5.00s) ← Click to jump             │
│           | 🔍 person, car                              │
│           | 👤 P1                                        │
│                                                          │
│  🎯 Result 2                                            │
│  [Image] | ⏱️ 0:12 (12.00s) ← Click to jump            │
│           | 🔍 person, backpack                         │
│           | 👤 P2                                        │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Step-by-Step Usage

### Step 1: Upload Video
```
1. Click "Choose File"
2. Select your video (MP4, AVI, MOV, etc.)
3. Click "Upload & Process"
4. Wait for processing to complete
   ✅ "Processed - X frames extracted"
```

### Step 2: Search for Objects
```
1. Enter credentials:
   - Username: admin
   - Password: admin123

2. Enter query:
   - "person"
   - "car"
   - "person with backpack"
   - etc.

3. Click "Search"
```

### Step 3: Video Player Appears
```
After search completes, you'll see:

✅ Video player with your uploaded video
✅ Timeline with green markers at match locations
✅ Results grid below with images and details
```

### Step 4: Navigate Using Timeline
```
Click any green marker:
  ↓
Video jumps to that timestamp
  ↓
Video starts playing automatically
  ↓
See the detected object in the video
```

### Step 5: Navigate Using Results
```
Option A: Click timestamp badge
  ↓
Video jumps to that exact time
  ↓
Video starts playing

Option B: Click result image
  ↓
Video jumps to that frame
  ↓
Page scrolls to video player
  ↓
Video starts playing
```

### Step 6: Watch Current Position
```
As video plays:
  ↓
Yellow marker moves along timeline
  ↓
Shows current playback position
  ↓
Updates in real-time
```

## 🎯 Example Scenarios

### Scenario 1: Finding a Person

**Query:** "person"

**What Happens:**
1. Video player loads with your video
2. Timeline shows 5 green markers (5 matches found)
3. Markers at: 0:05, 0:12, 0:18, 0:25, 0:32

**Actions:**
- Click marker at 0:12
- Video jumps to 12 seconds
- See person in frame with green bounding box
- Person ID shows "P1"

**Timeline View:**
```
├──|──|──|──|──────────────────────────────────────┤
  5s 12s 18s 25s 32s                            60s
  ↑  ↑  ↑  ↑  ↑
  All show "person" detections
```

### Scenario 2: Tracking Unattended Bag

**Query:** "backpack"

**What Happens:**
1. Video player loads
2. Timeline shows 2 green markers
3. First marker (0:08): Person with backpack
4. Second marker (0:15): Unattended backpack (ALERT!)

**Actions:**
- Click first marker → See person carrying bag
- Click second marker → See bag alone (no person)
- Alert shows: "⚠ ALERT: Unattended bag detected at 15.00s!"

**Timeline View:**
```
├────|──────|──────────────────────────────────────┤
     8s     15s                                  45s
     ↑      ↑
  Person+Bag  Bag alone (ALERT!)
```

### Scenario 3: Following a Person Through Video

**Query:** "person"

**What Happens:**
1. Video player loads
2. Multiple markers for same person (P1)
3. Markers at: 0:05, 0:10, 0:15, 0:20

**Actions:**
- Click through markers chronologically
- Watch person's movement through scene
- Same Person ID (P1) confirms it's the same individual

**Timeline View:**
```
├──|────|────|────|────────────────────────────────┤
  5s   10s  15s  20s                            60s
  ↑    ↑    ↑    ↑
  P1   P1   P1   P1
  
Track person's journey through the video!
```

## 🎨 Interactive Elements

### 1. Timeline Markers (Green)
```
Appearance: Green vertical line with dot
Position: Based on timestamp percentage
Hover: Shows tooltip with details
Click: Jumps video to that timestamp

Tooltip shows:
- Timestamp (e.g., "5.00s")
- Detected objects (e.g., "person, car")
- Person ID if applicable (e.g., "P1")
```

### 2. Current Position Marker (Yellow)
```
Appearance: Yellow vertical line
Position: Tracks current playback
Updates: Real-time (60fps)
Purpose: Shows where you are in video

Moves automatically as video plays
```

### 3. Timestamp Badges
```
Appearance: Gray badge with time
Format: "MM:SS (seconds)"
Example: "0:05 (5.00s)"
Click: Jumps video to that time
Hover: Cursor changes to pointer
```

### 4. Result Images
```
Appearance: Annotated frame with boxes
Size: 300px wide
Click: Jumps video to that frame
Hover: Cursor changes to pointer
Title: "Click to view full size or jump to video"
```

## 🔧 Technical Details

### How Timeline Markers Are Positioned

```javascript
// Calculate marker position
const position = (timestamp / videoDuration) * 100;
marker.style.left = position + '%';

// Example:
// Video duration: 60 seconds
// Match at: 12 seconds
// Position: (12 / 60) * 100 = 20%
// Marker appears at 20% from left
```

### How Video Jumping Works

```javascript
// When marker clicked:
videoPlayer.currentTime = markerTimestamp;
videoPlayer.play();

// Example:
// Marker at 12 seconds
// Sets video.currentTime = 12
// Starts playing from 12 seconds
```

### How Current Position Updates

```javascript
// Video timeupdate event fires continuously
videoPlayer.addEventListener('timeupdate', () => {
    const position = (videoPlayer.currentTime / duration) * 100;
    currentMarker.style.left = position + '%';
});

// Updates 60 times per second
// Smooth, real-time tracking
```

## 📊 Data Flow

### Upload Phase
```
1. User uploads video
   ↓
2. Server saves to storage/videos/
   ↓
3. Extract frames (1 per second)
   ↓
4. Detect objects in each frame
   ↓
5. Store metadata with video_filename
   ↓
6. Return success with frame count
```

### Search Phase
```
1. User enters query
   ↓
2. Search vector database
   ↓
3. Find matching frames
   ↓
4. Collect timeline markers
   ↓
5. Get video_filename from first result
   ↓
6. Return results + markers + filename
```

### Display Phase
```
1. Receive search results
   ↓
2. Check if video_filename exists
   ↓
3. Load video: /video/{filename}
   ↓
4. Get video info (duration, fps)
   ↓
5. Calculate marker positions
   ↓
6. Render markers on timeline
   ↓
7. Attach click handlers
   ↓
8. Setup current position tracking
```

## 🎯 Best Practices

### For Best Results

1. **Use Short Videos**
   - 30-60 seconds ideal for testing
   - Faster processing
   - Quicker navigation

2. **Use Clear Queries**
   - Start broad: "person"
   - Then specific: "person with backpack"
   - Check what objects were detected

3. **Wait for Video Load**
   - Give video 2-3 seconds to load
   - Then click markers
   - Smoother experience

4. **Use Timeline for Overview**
   - See all matches at once
   - Identify patterns
   - Find clusters of activity

5. **Use Results for Details**
   - See exact frames
   - Verify detections
   - Check bounding boxes

## 🎉 What Makes This Special

### 1. Complete Integration
- Not just detection
- Full video context
- Interactive navigation
- Visual verification

### 2. Intuitive Interface
- Click anywhere to jump
- Visual timeline
- Real-time feedback
- Smooth animations

### 3. Professional Quality
- Production-ready code
- Error handling
- Responsive design
- Browser compatible

### 4. Demo-Ready
- Impressive visuals
- Easy to explain
- Interactive features
- Wow factor

## 🚀 Quick Start

```bash
# 1. Start server
python main.py

# 2. Open browser
http://127.0.0.1:8000

# 3. Upload video
Choose file → Upload & Process

# 4. Search
admin / admin123
Query: "person"

# 5. Enjoy!
Click markers, timestamps, images
Watch video with timeline markers
Navigate through matches
```

## ✅ Success Checklist

Your video playback is working if:

✅ Video player appears after search
✅ Timeline shows green markers
✅ Clicking markers jumps video
✅ Clicking timestamps jumps video  
✅ Clicking images jumps video
✅ Yellow marker tracks playback
✅ Tooltips show on hover
✅ Video plays smoothly
✅ Auto-scroll works
✅ Auto-play works

## 🎓 Summary

The video playback feature provides:

- **Visual Context** - See what was detected
- **Easy Navigation** - Jump to any match
- **Timeline Overview** - See all matches at once
- **Interactive Experience** - Click anywhere to navigate
- **Professional Look** - Impressive for demos

**Perfect for security monitoring, event analysis, and impressive demonstrations!** 🎬✨

---

**Start using it now and experience the magic of interactive video analysis!** 🚀
