# 🚀 Quick Start Guide

## Installation (5 minutes)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python main.py
```

3. **Open browser:**
```
http://127.0.0.1:8000
```

## Usage

### Upload Video
1. Click "Choose File" in the Upload Video section
2. Select any video file (MP4, AVI, etc.)
3. Click "Upload & Process"
4. Wait for processing (extracts 1 frame/second)

### Search
1. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
2. Enter query: `person with backpack`
3. Click "Search"
4. View results below

## Example Queries

- `person` - Find all frames with people
- `car` - Find all frames with cars
- `person with backpack` - Find people carrying backpacks
- `bag` - Find all bags/backpacks

## Features Demo

### Alert System
Upload a video with an unattended bag - the system will automatically detect and alert you!

### Person Tracking
The system assigns consistent IDs to people across frames (basic Re-ID simulation).

### Vector Search
Natural language queries work semantically - "person with backpack" will find relevant frames even if the exact words aren't in the metadata.

## Troubleshooting

**Issue**: YOLOv8 model not found
**Solution**: First run will download the model automatically (takes 1-2 minutes)

**Issue**: Video processing is slow
**Solution**: Normal for CPU. For faster processing, use GPU-enabled PyTorch

**Issue**: Search returns no results
**Solution**: Make sure you've uploaded and processed a video first

## Next Steps

- Try different videos
- Experiment with queries
- Check the alerts for unattended objects
- View person tracking IDs in results

## Tips

- Use short videos (30-60 seconds) for faster testing
- The system extracts 1 frame per second
- Queries are semantic - be descriptive
- Check console for alert messages
