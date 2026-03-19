import os, cv2, base64, numpy as np
from core.settings import MEDIAPIPE_TASK_FILE, CLASSIFIER_MODEL_FILE, LABEL_ENCODER_FILE

def validate_model_files():
    """Verify that all required binary models are present on the disk."""
    required_paths = [MEDIAPIPE_TASK_FILE, CLASSIFIER_MODEL_FILE, LABEL_ENCODER_FILE]
    missing_files = [p for p in required_paths if not os.path.exists(p)]
    
    if missing_files:
        print("Error: Missing critical model files:")
        for file in missing_files:
            print(f" - {file}")
        return False
    return True

def convert_base64_to_frame(data_url: str):
    """Convert a client-side base64 Data URL to an OpenCV BGR frame (numpy array)."""
    if not data_url or ',' not in data_url:
        return None
    encoded_str = data_url.split(',')[1]
    raw_buffer = np.frombuffer(base64.b64decode(encoded_str), np.uint8)
    return cv2.imdecode(raw_buffer, cv2.IMREAD_COLOR)

def convert_frame_to_base64(opencv_image):
    """Compress and encode an OpenCV BGR frame to a JPEG Data URL for the client."""
    success, encoded_buffer = cv2.imencode('.jpg', opencv_image)
    if not success:
        return None
    b64_str = base64.b64encode(encoded_buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_str}"
