import cv2
import mediapipe as mp
import numpy as np
import joblib

class GestureProcessor:
    """
    Class responsible for processing images to detect hands and recognize gestures.
    """
    def __init__(self, mp_model_path, custom_model_path, encoder_path):
        """
        Initializes the MediaPipe Gesture Recognizer and the Custom Model.
        """
        # Load custom models
        self.clf = joblib.load(custom_model_path)
        self.label_encoder = joblib.load(encoder_path)
        
        # Initialize MediaPipe Task
        base_options = mp.tasks.BaseOptions(model_asset_path=mp_model_path)
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        
        # Drawing utilities
        self.mp_hands = mp.tasks.vision.HandLandmarksConnections
        self.mp_drawing = mp.tasks.vision.drawing_utils
        self.mp_drawing_styles = mp.tasks.vision.drawing_styles

    def process_frame(self, frame):
        """
        Receives an image (OpenCV frame), processes it and returns a new image with landmarks and predictions.
        
        Args:
            frame: Input OpenCV image (BGR).
            
        Returns:
            processed_frame: Image with hand landmarks and gesture prediction (BGR).
        """
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Calculate timestamp for video mode
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        
        # Run recognition
        recognition_result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)

        # Draw results if hands are detected
        if recognition_result.hand_landmarks:
            for i, hand_landmarks in enumerate(recognition_result.hand_landmarks):
                # 1. Draw landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

                # 2. Extract features for custom model
                hand_label = recognition_result.handedness[i][0].category_name
                handedness_val = 0 if hand_label == 'Left' else 1
                
                landmarks_array = [handedness_val]
                for lm in hand_landmarks:
                    landmarks_array.extend([lm.x, lm.y, lm.z])
                
                # Reshape for prediction
                features = np.array(landmarks_array).reshape(1, -1)
                
                # Make prediction
                prediction_idx = self.clf.predict(features)[0]
                prediction_prob = np.max(self.clf.predict_proba(features))
                gesture_name = self.label_encoder.inverse_transform([prediction_idx])[0]

                # 3. Put text on image
                color = (0, 255, 0) # Green
                display_text = f"Custom {hand_label}: {gesture_name} ({prediction_prob:.2f})"
                cv2.putText(frame, display_text, (20, 50 + (i * 40)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Releases resources."""
        if self.recognizer:
            self.recognizer.close()
