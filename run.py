import cv2
import time
from ultralytics import solutions
import numpy as np

cap = cv2.VideoCapture("demo.mp4") 
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

processing_times = []  # List to store processing times for each frame

# Define region points
# region_points = [(0, 150), (400, 150)]  # For line counting
region_points = [(0, 180), (400, 180), (400, 150), (0, 150)]  # For rectangle region counting

# Video writer
video_writer = cv2.VideoWriter("demo_out.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init ObjectCounter
counter = solutions.ObjectCounter(
    show=True,  # Display the output
    region=region_points,  # Pass region points
    model="yolo11n.pt",  # model
    classes=[0],  # i.e person class with COCO pretrained model.
    show_in=True,  # Display in counts
    show_out=True,  # Display out counts
    # line_width=2,  # Adjust the line width for bounding boxes and text display
)

# Process video
while cap.isOpened():

    start_frame_time = time.time()  # Start time for the frame

    success, im0 = cap.read()

    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    im0 = counter.count(im0)

    end_frame_time = time.time()     # End time for the frame
    frame_processing_time = end_frame_time - start_frame_time
    processing_times.append(frame_processing_time)  # Save the time for this frame

    video_writer.write(im0)


# Calculate the average processing time after the loop
avg_processing_time = np.mean(processing_times)
print(f"Average processing time per frame: {avg_processing_time:.4f} seconds")

print("Program Stopped")


cap.release()
video_writer.release()
cv2.destroyAllWindows()