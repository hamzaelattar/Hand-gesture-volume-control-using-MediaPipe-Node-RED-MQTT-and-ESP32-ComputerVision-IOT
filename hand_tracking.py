
import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import time
import paho.mqtt.client as mqtt

# Charger le modèle
base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect("localhost", 1883, 60)
client.loop_start()

last_publish = 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Camera inaccessible")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]

        h, w, _ = frame.shape

        # Point 4 = pouce
        x1 = int(landmarks[4].x * w)
        y1 = int(landmarks[4].y * h)

        # Point 8 = index
        x2 = int(landmarks[8].x * w)
        y2 = int(landmarks[8].y * h)

        distance = math.hypot(x2 - x1, y2 - y1)

        if time.monotonic() - last_publish >= 0.1:
                client.publish("hand/distance", round(distance, 2))
                print(f"Distance envoyee : {distance:.2f} px")
                last_publish = time.monotonic()
   

        cv2.circle(frame, (x1, y1), 10, (0, 255, 0), -1)
        cv2.circle(frame, (x2, y2), 10, (0, 255, 0), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

        cv2.putText(
            frame,
            f"Distance: {distance:.1f} px",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Hand Tracking - MediaPipe", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
detector.close()
cv2.destroyAllWindows()
client.disconnect()
client.loop_stop()