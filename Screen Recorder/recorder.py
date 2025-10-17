import cv2                   
import pyautogui              
import numpy as np           
import time                  
from win32api import GetSystemMetrics 

# Get screen width and height
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
dim = (width, height)

# Define the codec and create VideoWriter object
f = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("test.mp4", f, 20.0, dim)

# Get recording duration from user
start_time = time.time()
dur = int(input("Enter duration (in seconds): "))
end_time = start_time + dur

print("🎥 Recording...")
print("🛑 Press Ctrl+C to stop recording.")

# Start screen recording loop
while True:
    image = pyautogui.screenshot()             # Capture current screen
    frame_1 = np.array(image)                  # Convert screenshot to numpy array
    
    frame = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)  # Convert color format to RGB
    
    output.write(frame)       # Write frame to video file
    curr_time = time.time()   # Get current time

    if curr_time > end_time:                   # Stop if duration is reached
        break

# Release video writer and save file
output.release()
print("Video Recorded Successfully✅")
