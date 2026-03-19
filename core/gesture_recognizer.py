import cv2
import joblib
import numpy as np
import pandas as pd
import mediapipe as mp
from core.config import MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH

class GestureRecognizer:
    def __init__(self):
        self.clf = joblib.load(CUSTOM_MODEL_PATH)
        self.label_encoder = joblib.load(ENCODER_PATH)
        
        # Define feature names to match training data and avoid Scikit-Learn warnings
        self.feature_names = ['handedness']
        for i in range(21):
            self.feature_names.extend([f'x{i}', f'y{i}', f'z{i}'])
        
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=MP_MODEL_PATH),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        
        self.mp_hands = mp.tasks.vision.HandLandmarksConnections
        self.mp_drawing = mp.tasks.vision.drawing_utils
        self.mp_drawing_styles = mp.tasks.vision.drawing_styles

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        
        result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks:
            for i, hand_landmarks in enumerate(result.hand_landmarks):
                # Draw landmarks
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

                # Prepare features
                hand_label = result.handedness[i][0].category_name
                landmarks_data = [0 if hand_label == 'Left' else 1]
                for lm in hand_landmarks:
                    landmarks_data.extend([lm.x, lm.y, lm.z])
                
                # Create DataFrame with feature names (avoids UserWarning)
                features_df = pd.DataFrame([landmarks_data], columns=self.feature_names)
                
                # Predict gesture
                prediction_idx = self.clf.predict(features_df)[0]
                prediction_prob = np.max(self.clf.predict_proba(features_df))
                gesture_name = self.label_encoder.inverse_transform([prediction_idx])[0]

                text = f"{hand_label}: {gesture_name} ({prediction_prob:.2f})"
                cv2.putText(frame, text, (20, 50 + (i * 40)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return frame

    def close(self):
        """Explicitly releases MediaPipe resources."""
        if hasattr(self, 'recognizer') and self.recognizer:
            try:
                self.recognizer.close()
            except Exception:
                pass
