# https://docs.ultralytics.com/modes/track
import cv2
import numpy as np
import os
import torch
from ultralytics import YOLO

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model', 'best.pt')
model = YOLO(model_path)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)
# https://www.youtube.com/watch?v=oWMXQkGOzho
cap = cv2.VideoCapture(os.path.join(current_dir, "test.mp4"))
# cap = cv2.VideoCapture(0)
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
while cap.isOpened():
    success, frame = cap.read()
    if success:
        red_count = 0
        blue_count = 0
        yellow_count = 0
        results = model.track(frame, persist=True, tracker="bytetrack.yaml")
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                id = int(box.id[0]) if box.id is not None else None
                roi = frame[y1:y2, x1:x2]
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                red_mask = cv2.inRange(hsv_roi, lower_red, upper_red)
                blue_mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)
                yellow_mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
                red_pixels = cv2.countNonZero(red_mask)
                blue_pixels = cv2.countNonZero(blue_mask)
                yellow_pixels = cv2.countNonZero(yellow_mask)
                max_pixels = max(red_pixels, blue_pixels, yellow_pixels)
                if max_pixels == red_pixels:
                    color = "Red"
                    color_box = (0, 0, 255)
                    background_color = (0, 0, 255)
                    red_count += 1
                elif max_pixels == blue_pixels:
                    color = "Blue"
                    color_box = (255, 0, 0)
                    background_color = (255, 0, 0)
                    blue_count += 1
                else:
                    color = "Yellow"
                    color_box = (0, 255, 255)
                    background_color = (0, 255, 255)
                    yellow_count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), color_box, 4)
                label = f"id: {id} {color}" if id is not None else color
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), background_color, -1)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)
        
        total_count = red_count + blue_count + yellow_count
        print(f"Red Count: {red_count}")
        print(f"Blue Count: {blue_count}")
        print(f"Yellow Count: {yellow_count}")
        print(f"All: {total_count}")
        print("-" * 30)
        
        cv2.imshow("YOLO11 Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()