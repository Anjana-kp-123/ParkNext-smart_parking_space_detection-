import cv2
import pickle
import cvzone
import numpy as np
import os

# File paths
VIDEO_PATH = r'C:\Users\NEW DELL\Downloads\PartNxts\Parking-Space-Counter-using-Machine-learning-main\carPark.mp4'
POS_FILE = r'C:\Users\NEW DELL\Downloads\PartNxts\Parking-Space-Counter-using-Machine-learning-main\CarParkPos'

# Check if files exist
if not os.path.exists(VIDEO_PATH):
    print(f"Error: Video file not found at {VIDEO_PATH}")
    exit()

# Video feed
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Error: Could not open video file")
    exit()

# Load positions file
try:
    with open(POS_FILE, 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print(f"Error: Positions file not found at {POS_FILE}")
    print("Please run ParkingSpacePicker.py first")
    exit()

width, height = 107, 48

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # Draw rectangle only (no spot number label)
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

        # Optional: comment out the next line if you don’t want to display pixel count
        # cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    # Show total available spots
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                      thickness=5, offset=20, colorR=(0, 200, 0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    success, img = cap.read()
    if not success:
        print("Error: Failed to read video frame")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)

    # Break loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
