import os
import cv2
import base64
import numpy as np
from core.config import MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH

def check_models():
    """Verifies if all necessary model files exist."""
    models = [MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH]
    missing = [p for p in models if not os.path.exists(p)]
    if missing:
        print("Erro: Os seguintes modelos não foram encontrados:")
        for m in missing:
            print(f" - {m}")
        return False
    return True

def decode_image(data_url: str):
    """Decodes a base64 Data URL to an OpenCV frame."""
    if not data_url or ',' not in data_url:
        return None
    encoded_data = data_url.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame

def encode_image(image):
    """Encodes an OpenCV frame to a base64 Data URL."""
    _, buffer = cv2.imencode('.jpg', image)
    b64_encoded = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_encoded}"
