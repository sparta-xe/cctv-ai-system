# Test Video Isolation Feature

## Quick Test Steps

### Test 1: Auto-Clear on Upload
1. Start the server: `python main.py`
2. Upload first video (e.g., traffic.mp4)
3. Wait for processing to complete
4. Note the frame count (e.g., 150 frames)
5. Upload second video (e.g., parking.mp4)
6. Watch for "🗑️ Clearing previous data..." message
7. Check frame count resets and shows new video's count
8. Search for objects - should only show results from second video ✅

### Test 2: Manual Clear Button
1. Upload a video and let it process
2. Click "Clear All Data" button (red button next to title)
3. Confirm the dialog
4. Verify:
   - Total Frames shows 0
   - Total Detections shows 0
   - Total Alerts shows 0
   - Results section disappears
   - Video player disappears
   - Alerts reset to "No alerts"
5. Upload new video - should work normally ✅

### Test 3: Multiple Videos in Sequence
1. Upload video1.mp4 → Process → Search "person"
2. Note results (e.g., 5 matches)
3. Upload video2.mp4 → Auto-clear → Process → Search "person"
4. Note results (e.g., 3 matches)
5. Results should be different and only from video2 ✅

## Expected Behavior

### Upload Status Messages
```
1. "🗑️ Clearing previous data..."
2. "⏳ Processing video..."
3. "✅ Processed X frames"
```

### Clear Data Messages
```
1. "🗑️ Clearing all data..."
2. "✅ All data cleared successfully!"
```

### Error Cases
- If clear fails: "❌ Error: [error message]"
- If no file selected: "⚠ Please select a video file first"

## Browser Console Checks

Open browser console (F12) and look for:
- `console.log('Upload response:', data)` - Shows upload results
- `console.warn('Could not clear previous data:', error)` - If clear fails (non-critical)
- No JavaScript errors related to undefined properties

## API Testing

You can also test the clear endpoint directly:

```bash
# Clear all data
curl -X POST http://localhost:8000/clear_data/

# Expected response:
{
    "status": "success",
    "message": "All data cleared successfully",
    "frames_cleared": true,
    "embeddings_cleared": true,
    "clip_cleared": true
}
```

## Troubleshooting

### Issue: Data not clearing
- Check browser console for errors
- Verify server is running
- Check server logs for clear_data endpoint calls

### Issue: Old results still showing
- Hard refresh browser: Ctrl + Shift + R
- Manually click "Clear All Data" button
- Restart server

### Issue: Clear button not visible
- Hard refresh browser
- Check if Lucide icons are loading
- Verify dashboard.html has the latest changes

## Success Criteria

✅ Auto-clear works on every upload
✅ Manual clear button visible and functional
✅ Confirmation dialog appears before clearing
✅ Stats reset to 0 after clearing
✅ No data mixing between videos
✅ Search results only from current video
✅ No JavaScript errors in console

All tests passing = Feature working correctly! 🎉
