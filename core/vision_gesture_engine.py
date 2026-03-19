import cv2
import joblib
import numpy as np
import pandas as pd
import mediapipe as mp
from core.config import MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH

class VisionGestureEngine:
    def __init__(self):
        self.gesture_classifier = joblib.load(CUSTOM_MODEL_PATH)
        self.label_encoder = joblib.load(ENCODER_PATH)
        
        # Define feature names to match training data and avoid Scikit-Learn warnings
        self.feature_columns = ['handedness']
        for landmark_id in range(21):
            self.feature_columns.extend([f'x{landmark_id}', f'y{landmark_id}', f'z{landmark_id}'])
        
        mediapipe_options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=MP_MODEL_PATH),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.hand_tracker = mp.tasks.vision.GestureRecognizer.create_from_options(mediapipe_options)
        
        self.hand_connections = mp.tasks.vision.HandLandmarksConnections
        self.drawing_utility = mp.tasks.vision.drawing_utils
        self.drawing_presets = mp.tasks.vision.drawing_styles

    def process_vision_frame(self, raw_frame, draw_landmarks=True):
        mirrored_frame = cv2.flip(raw_frame, 1)
        rgb_converted_frame = cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2RGB)
        mediapipe_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_converted_frame)
        current_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        
        detection_result = self.hand_tracker.recognize_for_video(mediapipe_image, current_timestamp_ms)
        detected_gestures_list = []

        if detection_result.hand_landmarks:
            for hand_index, hand_landmarks in enumerate(detection_result.hand_landmarks):
                # Draw visual feedback
                if draw_landmarks:
                    self.drawing_utility.draw_landmarks(
                        mirrored_frame, 
                        hand_landmarks, 
                        self.hand_connections.HAND_CONNECTIONS,
                        self.drawing_presets.get_default_hand_landmarks_style(),
                        self.drawing_presets.get_default_hand_connections_style())

                # Prepare features for the classifier
                hand_handedness = detection_result.handedness[hand_index][0].category_name
                input_features = [0 if hand_handedness == 'Left' else 1]
                for landmark in hand_landmarks:
                    input_features.extend([landmark.x, landmark.y, landmark.z])
                
                # Encapsulate in DataFrame for prediction
                features_dataframe = pd.DataFrame([input_features], columns=self.feature_columns)
                
                # Execute prediction
                predicted_index = self.gesture_classifier.predict(features_dataframe)[0]
                confidence_score = float(np.max(self.gesture_classifier.predict_proba(features_dataframe)))
                gesture_name = self.label_encoder.inverse_transform([predicted_index])[0]

                detected_gestures_list.append({
                    "hand": hand_handedness,
                    "gesture": gesture_name,
                    "score": round(confidence_score, 2)
                })
                
        return mirrored_frame, detected_gestures_list

    def release_resources(self):
        """Explicitly releases all machine learning and video processing resources."""
        if hasattr(self, 'hand_tracker') and self.hand_tracker:
            try:
                self.hand_tracker.close()
            except Exception:
                pass
