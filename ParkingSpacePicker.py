import cv2
import pickle
import os

# Constants
width, height = 107, 48

# File paths
IMG_PATH = r'C:\Users\NEW DELL\Downloads\PartNxts\Parking-Space-Counter-using-Machine-learning-main\carParkImg.png'
POS_FILE = r'C:\Users\NEW DELL\Downloads\PartNxts\Parking-Space-Counter-using-Machine-learning-main\CarParkPos'

# Initialize positions list
try:
    with open(POS_FILE, 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open(POS_FILE, 'wb') as f:
        pickle.dump(posList, f)

def main():
    if not os.path.exists(IMG_PATH):
        print(f"Error: Image not found at {IMG_PATH}")
        return

    while True:
        img = cv2.imread(IMG_PATH)
        if img is None:
            print(f"Error: Could not load image {IMG_PATH}")
            break

        # Draw rectangles for each parking space
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        
        # Break loop if ESC is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()