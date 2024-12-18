import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import ctypes
import sys
import cv2
import base64
import requests

cccd_base64 = "E:\anh.jpeg"  # Đảm bảo đường dẫn tệp là chính xác

if len(cccd_base64) == 0:
    ctypes.windll.user32.MessageBoxW(0, "Citizen image data length must be > 0", "ERROR", 0)
    sys.exit()

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return len(faces) > 0

def frame_to_base64(frame):
    success, buffer = cv2.imencode('.jpg', frame)
    if success:
        base64_string = base64.b64encode(buffer).decode('utf-8')
        return base64_string
    else:
        return None

# Mở camera tích hợp và webcam cắm ngoài
rgb_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Sử dụng backend DSHOW
webcam = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Sử dụng backend DSHOW

detected = False
delay = 0
while True:
    ret_rgb, frame_rgb = rgb_cam.read()
    ret_webcam, frame_webcam = webcam.read()
    if not ret_rgb or not ret_webcam:
        break

    faces_rgb = detect_bounding_box(frame_rgb)
    faces_webcam = detect_bounding_box(frame_webcam)
    print(f"RGB: {faces_rgb}, Webcam: {faces_webcam}")
    if faces_rgb and faces_webcam:
        if delay < 50:
            delay += 1
        else:
            form_data = {
                "image1": frame_to_base64(frame_rgb),  # Ảnh từ camera RGB tích hợp
                "image2": frame_to_base64(frame_webcam)    # Ảnh từ webcam cắm ngoài
            }
            returned = requests.post("http://localhost:5001/analyze_image", data=form_data)
            detected = returned.text
            break

    cv2.imshow("RGB Camera", frame_rgb)
    cv2.imshow("Webcam", frame_webcam)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

rgb_cam.release()
webcam.release()
cv2.destroyAllWindows()

ctypes.windll.user32.MessageBoxW(0, str(detected), "Is the same person", 0)
