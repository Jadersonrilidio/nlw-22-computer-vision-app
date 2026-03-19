import os

# Root directory of the project
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model storage locations
MODELS_DIR = os.path.join(ROOT_PATH, "models")

# Specific model file paths
MEDIAPIPE_TASK_FILE = os.path.join(MODELS_DIR, "gesture_recognizer.task")
CLASSIFIER_MODEL_FILE = os.path.join(MODELS_DIR, "gesture_model.joblib")
LABEL_ENCODER_FILE = os.path.join(MODELS_DIR, "label_encoder.joblib")
