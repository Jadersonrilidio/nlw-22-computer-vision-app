import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Models directory
MODELS_DIR = os.path.join(BASE_DIR, "models")
# The .task file was found in .notes/storage/nn_models/ during search
# but often it might be in assets or models. Let's provide a way to set it.
MP_MODELS_DIR = os.path.join(BASE_DIR, ".notes", "storage", "nn_models")

# Model Paths
MP_MODEL_PATH = os.path.join(MP_MODELS_DIR, "gesture_recognizer.task")
CUSTOM_MODEL_PATH = os.path.join(MODELS_DIR, "gesture_model.joblib")
ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.joblib")

# Window settings
WINDOW_NAME = 'Custom Gesture Recognition'
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
