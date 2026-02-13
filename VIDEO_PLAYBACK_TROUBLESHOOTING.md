# 🔧 Video Playback Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Video Player Not Appearing

**Symptoms:**
- Search returns results but no video player shows
- Timeline section is hidden

**Possible Causes:**
1. No video was uploaded
2. Video filename not stored in metadata
3. No search results found

**Solutions:**

#### Check 1: Verify Video Upload
```bash
# Check if video was saved
ls storage/videos/

# Should see: video_yourfilename.mp4
```

#### Check 2: Check Browser Console
```javascript
// Open browser console (F12)
// Look for errors like:
// - "video_filename is undefined"
// - "timeline_markers is empty"
```

#### Check 3: Verify Search Results
```javascript
// In browser console after search:
console.log(data.video_filename);  // Should show filename
console.log(data.timeline_markers); // Should show array
```

**Fix:**
- Re-upload the video
- Make sure video processing completes
- Search again after upload

---

### Issue 2: Timeline Markers Not Showing

**Symptoms:**
- Video player appears
- Timeline is empty (no green markers)

**Possible Causes:**
1. No matches found for query
2. Timeline markers array is empty
3. Video duration is 0

**Solutions:**

#### Check 1: Verify Matches
```javascript
// Check if query found matches
console.log(data.count);  // Should be > 0
console.log(data.timeline_markers.length);  // Should be > 0
```

#### Check 2: Try Different Query
```
Instead of: "person with backpack"
Try: "person"  (more general)
```

#### Check 3: Check Video Info
```javascript
// In browser console:
fetch('/video_info/video_yourfile.mp4')
  .then(r => r.json())
  .then(d => console.log(d));

// Should show:
// { duration: 30.5, fps: 30, ... }
```

**Fix:**
- Use broader search terms
- Verify objects were detected during upload
- Check upload status for frame count

---

### Issue 3: Click Markers Not Working

**Symptoms:**
- Markers appear on timeline
- Clicking markers does nothing
- Video doesn't jump

**Possible Causes:**
1. Video not loaded yet
2. JavaScript error
3. Timestamp out of range

**Solutions:**

#### Check 1: Wait for Video Load
```javascript
// Video must be loaded first
videoPlayer.addEventListener('loadedmetadata', () => {
    console.log('Video ready!');
});
```

#### Check 2: Check Console for Errors
```
F12 → Console tab
Look for JavaScript errors
```

#### Check 3: Manually Test
```javascript
// In browser console:
const video = document.getElementById('videoPlayer');
video.currentTime = 5;  // Jump to 5 seconds
video.play();
```

**Fix:**
- Wait a few seconds for video to load
- Refresh the page
- Check browser compatibility

---

### Issue 4: Click Timestamps Not Working

**Symptoms:**
- Clicking timestamp badges does nothing
- Video doesn't jump

**Possible Causes:**
1. Video player not initialized
2. onclick handler not attached
3. Video not loaded

**Solutions:**

#### Check 1: Verify Video Player Exists
```javascript
// In browser console:
const video = document.getElementById('videoPlayer');
console.log(video);  // Should show <video> element
console.log(video.src);  // Should show video URL
```

#### Check 2: Test Click Handler
```javascript
// Click timestamp and check console
// Should see video.currentTime change
```

#### Check 3: Check Video Source
```javascript
// Verify video URL is correct
console.log(document.getElementById('videoPlayer').src);
// Should be: http://localhost:8000/video/video_yourfile.mp4
```

**Fix:**
- Ensure video player section is visible
- Check that video loaded successfully
- Try clicking after video starts playing

---

### Issue 5: Click Images Not Jumping to Video

**Symptoms:**
- Clicking result images doesn't jump to video
- No scroll to video player

**Possible Causes:**
1. Video player not visible
2. onclick handler not working
3. Timestamp not passed correctly

**Solutions:**

#### Check 1: Verify Video Player Visible
```javascript
const section = document.getElementById('videoPlayerSection');
console.log(section.style.display);  // Should be 'block'
```

#### Check 2: Check Image onclick
```html
<!-- Image should have onclick attribute -->
<img onclick="..." />
```

#### Check 3: Test Manually
```javascript
// Click image and check:
const video = document.getElementById('videoPlayer');
console.log(video.currentTime);  // Should change
```

**Fix:**
- Make sure search returned results with video
- Verify video player section is displayed
- Check browser console for errors

---

### Issue 6: Video Won't Play

**Symptoms:**
- Video player shows
- Video won't play when clicked
- Black screen

**Possible Causes:**
1. Video format not supported
2. Video file corrupted
3. Browser codec issue

**Solutions:**

#### Check 1: Verify Video Format
```bash
# Check video file
file storage/videos/video_yourfile.mp4

# Should show: MP4, H.264, etc.
```

#### Check 2: Test Video Directly
```
Open in browser:
http://localhost:8000/video/video_yourfile.mp4

Should play directly
```

#### Check 3: Try Different Browser
```
Chrome: Best support
Firefox: Good support
Safari: May have issues with some codecs
Edge: Good support
```

**Fix:**
- Convert video to MP4 H.264
- Try different browser
- Re-upload video

---

### Issue 7: Timeline Position Not Updating

**Symptoms:**
- Yellow marker doesn't move
- Current position stuck

**Possible Causes:**
1. timeupdate event not firing
2. Duration is 0
3. JavaScript error

**Solutions:**

#### Check 1: Verify Event Listener
```javascript
const video = document.getElementById('videoPlayer');
video.addEventListener('timeupdate', () => {
    console.log('Current time:', video.currentTime);
});
```

#### Check 2: Check Duration
```javascript
const video = document.getElementById('videoPlayer');
console.log('Duration:', video.duration);  // Should be > 0
```

#### Check 3: Check Marker Element
```javascript
const marker = document.getElementById('currentTimeMarker');
console.log(marker);  // Should exist
console.log(marker.style.left);  // Should update
```

**Fix:**
- Wait for video to load metadata
- Refresh page
- Check console for errors

---

## Quick Diagnostic Checklist

Run these checks in browser console (F12):

```javascript
// 1. Check video player
const video = document.getElementById('videoPlayer');
console.log('Video exists:', !!video);
console.log('Video src:', video.src);
console.log('Video duration:', video.duration);

// 2. Check video section
const section = document.getElementById('videoPlayerSection');
console.log('Section visible:', section.style.display === 'block');

// 3. Check timeline
const timeline = document.getElementById('timelineMarkers');
console.log('Timeline exists:', !!timeline);
console.log('Markers count:', timeline.children.length);

// 4. Check current marker
const current = document.getElementById('currentTimeMarker');
console.log('Current marker exists:', !!current);

// 5. Test video control
video.currentTime = 5;
video.play();
console.log('Video playing:', !video.paused);
```

---

## Browser Compatibility

### Supported Browsers
✅ Chrome 90+
✅ Firefox 88+
✅ Edge 90+
✅ Safari 14+

### Known Issues
⚠️ Safari: May require user interaction before autoplay
⚠️ Firefox: Some codecs may not work
⚠️ Mobile: Fullscreen may behave differently

---

## Debug Mode

Add this to your dashboard to enable debug logging:

```javascript
// Add after search form submit
console.log('=== DEBUG INFO ===');
console.log('Video filename:', data.video_filename);
console.log('Timeline markers:', data.timeline_markers);
console.log('Results count:', data.count);
console.log('Video player src:', videoPlayer.src);
console.log('Video section display:', videoSection.style.display);
```

---

## Still Not Working?

### Step 1: Clear Everything
```bash
# Stop server
# Delete storage
rm -rf storage/

# Restart server
python main.py
```

### Step 2: Test with Simple Video
```bash
# Use a short, simple MP4 video
# 10-30 seconds, H.264 codec
# Upload and test
```

### Step 3: Check Server Logs
```bash
# Look for errors in terminal
# Check for:
# - Video upload errors
# - Detection errors
# - File not found errors
```

### Step 4: Verify Endpoints
```bash
# Test video endpoint
curl http://localhost:8000/video/video_test.mp4

# Test video info endpoint
curl http://localhost:8000/video_info/video_test.mp4
```

---

## Common Error Messages

### "Video not found"
**Cause:** Video file doesn't exist
**Fix:** Re-upload video

### "Failed to load video"
**Cause:** Unsupported format or corrupted file
**Fix:** Convert to MP4 H.264

### "Timeline markers undefined"
**Cause:** No search results
**Fix:** Use broader search terms

### "Cannot read property 'currentTime'"
**Cause:** Video player not initialized
**Fix:** Wait for video to load

---

## Performance Tips

1. **Use Short Videos** - 30-60 seconds for testing
2. **Compress Videos** - Smaller files load faster
3. **Use MP4 H.264** - Best browser support
4. **Wait for Load** - Let video load before clicking
5. **Clear Cache** - Refresh browser if issues persist

---

## Contact & Support

If issues persist:
1. Check browser console for errors
2. Check server terminal for errors
3. Verify video file is valid MP4
4. Try different browser
5. Re-upload video

**The video playback feature should work smoothly once the video is properly uploaded and processed!** 🎬✨
