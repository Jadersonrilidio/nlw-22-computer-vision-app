import cv2, joblib, numpy as np, pandas as pd, mediapipe as mp
from core.settings import MEDIAPIPE_TASK_FILE, CLASSIFIER_MODEL_FILE, LABEL_ENCODER_FILE

class GestureDetector:
    """Handles hand detection and custom gesture classification via MediaPipe and Random Forest."""
    
    def __init__(self):
        # Load custom classifier and its label encoder
        self.classification_model = joblib.load(CLASSIFIER_MODEL_FILE)
        self.label_encoder = joblib.load(LABEL_ENCODER_FILE)
        
        # Consistent feature column names for Pandas
        self.feature_columns = ['handedness']
        for i in range(21):
            self.feature_columns.extend([f'x{i}', f'y{i}', f'z{i}'])
        
        # Initialize MediaPipe's Gesture Recognizer task
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=MEDIAPIPE_TASK_FILE),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.mp_engine = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        
        # Standard drawing utilities
        self.mp_conn = mp.tasks.vision.HandLandmarksConnections
        self.mp_draw = mp.tasks.vision.drawing_utils
        self.mp_styles = mp.tasks.vision.drawing_styles

    def detect_gestures(self, frame, draw_landmarks=True):
        """Processes a frame, draws landmarks, and returns list of recognized gestures."""
        # Flip frame to match webcam (mirror mode)
        frame = cv2.flip(frame, 1)
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_data = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
        ms_ts = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        
        results = self.mp_engine.recognize_for_video(mp_data, ms_ts)
        gestures_data = []

        if results.hand_landmarks:
            for i, landmarks in enumerate(results.hand_landmarks):
                # 1. Visualize landmarks if enabled
                if draw_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, landmarks, self.mp_conn.HAND_CONNECTIONS,
                        self.mp_styles.get_default_hand_landmarks_style(),
                        self.mp_styles.get_default_hand_connections_style())

                # 2. Extract features: [handedness, x0, y0, z0, ..., x20, y20, z20]
                hand_label = results.handedness[i][0].category_name
                features_data = [0 if hand_label == 'Left' else 1]
                for lm in landmarks:
                    features_data.extend([lm.x, lm.y, lm.z])
                
                # 3. Classify custom gesture
                df_row = pd.DataFrame([features_data], columns=self.feature_columns)
                pred_idx = self.classification_model.predict(df_row)[0]
                pred_prob = float(np.max(self.classification_model.predict_proba(df_row)))
                name = self.label_encoder.inverse_transform([pred_idx])[0]

                gestures_data.append({
                    "hand": hand_label,
                    "gesture": name,
                    "score": round(pred_prob, 2)
                })
                
        return frame, gestures_data

    def release_resources(self):
        """Must be called on shutdown to clean up memory."""
        if hasattr(self, 'mp_engine'):
            self.mp_engine.close()
