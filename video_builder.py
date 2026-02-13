"""
Generate annotated output video from marked frames
Creates highlight reel of query matches
"""

import cv2
import os
from pathlib import Path

def build_video_from_frames(frame_folder, output_path, fps=5, add_timestamps=True):
    """
    Build video from annotated frames
    
    Args:
        frame_folder: Folder containing frames
        output_path: Path to save output video
        fps: Frames per second
        add_timestamps: Whether to add timestamp overlays
    
    Returns:
        bool: Success status
    """
    try:
        # Get all image files
        frame_files = sorted([
            f for f in os.listdir(frame_folder)
            if f.endswith(('.jpg', '.jpeg', '.png'))
        ])
        
        if not frame_files:
            print("No frames found")
            return False
        
        # Read first frame to get dimensions
        first_frame_path = os.path.join(frame_folder, frame_files[0])
        first_frame = cv2.imread(first_frame_path)
        
        if first_frame is None:
            print("Could not read first frame")
            return False
        
        height, width, _ = first_frame.shape
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Write frames
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frame_folder, frame_file)
            frame = cv2.imread(frame_path)
            
            if frame is None:
                continue
            
            # Add timestamp if requested
            if add_timestamps:
                # Extract timestamp from filename if possible
                try:
                    timestamp = float(frame_file.split('_')[1].split('.')[0])
                    time_text = f"Time: {timestamp:.2f}s"
                    
                    cv2.putText(
                        frame, time_text,
                        (10, height - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2
                    )
                except:
                    pass
            
            video.write(frame)
        
        video.release()
        print(f"✅ Video created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error building video: {e}")
        return False

def create_highlight_video(results, output_path, fps=2):
    """
    Create highlight video from search results
    
    Args:
        results: List of result dictionaries with 'image' key
        output_path: Path to save highlight video
        fps: Frames per second
    
    Returns:
        bool: Success status
    """
    try:
        if not results:
            return False
        
        # Get first image to determine dimensions
        first_image = cv2.imread(results[0]['image'])
        if first_image is None:
            return False
        
        height, width, _ = first_image.shape
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Write each result frame
        for result in results:
            frame = cv2.imread(result['image'])
            if frame is not None:
                # Add result info overlay
                timestamp = result.get('timestamp', 0)
                objects = result.get('objects', [])
                
                # Add info text
                info_text = f"Time: {timestamp:.2f}s | Objects: {', '.join(objects[:3])}"
                cv2.putText(
                    frame, info_text,
                    (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 255),
                    2
                )
                
                video.write(frame)
        
        video.release()
        print(f"✅ Highlight video created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating highlight video: {e}")
        return False
