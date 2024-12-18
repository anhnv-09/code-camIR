import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import base64
import cv2
import numpy as np
from deepface import DeepFace
from flask import Flask, request

app = Flask(__name__)

def decode_base64_to_image(base64_str):
    base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
    img_data = base64.b64decode(base64_str)
    img_array = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    image1 = request.form.get('image1')
    image2 = request.form.get('image2')

    verified = DeepFace.verify(
        img1_path=decode_base64_to_image(image1), 
        img2_path=decode_base64_to_image(image2),
        model_name="VGG-Face",
        detector_backend="opencv",
        enforce_detection=False
    )
    return str(verified["verified"])

if __name__ == "__main__":
    app.run(port=5001)
