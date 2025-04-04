import cv2
import os

def extract_frames(video_path, output_folder):
    video_path="./Fortin Evo-One Thar-One-Maz3 - Remote Start Install on Mazda 2019 CX-5 GT [ ezmp3.cc ].mp3"
    # Open video file
    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(cv2.CAP_PROP_FPS)  # Get the frame rate
    frame_count = 0
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # Save a frame every 30th frame (can adjust based on your needs)
        if frame_count % int(frame_rate * 60) == 0:  # Extract frame every 5 seconds
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
        
        frame_count += 1
    
    video.release()

# Usage example
extract_frames('installation_video.mp4', 'output_frames/')
