# AI Gesture & Vision Recognition System 👁️🖐️

A comprehensive computer vision workspace build with Python, integrating state-of-the-art AI models for image analysis, object detection, and real-time gesture recognition.

## 🚀 Key Features

- **Real-time Gesture Recognition:** Custom-trained Random Forest model using MediaPipe landmarks.
- **AI Vision Suite:** 
  - **Gemini API:** Structured image analysis and JSON metadata extraction.
  - **CLIPSeg:** Zero-shot text-based image segmentation.
  - **YOLOS & MobileNetV3:** Efficient object detection and image classification.
- **Data Collection:** Integrated tools to record hand landmarks and build custom gesture datasets (CSV).
- **Webcam Integration:** High-performance real-time processing using OpenCV and MediaPipe.

## 📂 Project Structure

- `notebooks/`: Interactive Jupyter notebooks for training, recording, and inference.
- `storage/`: 
  - `nn_models/`: Local AI models and trained classifiers (.tflite, .task, .pkl).
  - `csv/`: Recorded gesture datasets.
- `images/`: Sample imagery for testing classification and segmentation.
- `.venv/`: Managed environment using `uv`.

## 🛠️ Quick Start

This project uses `uv` for lightning-fast dependency management.

1. **Install Dependencies:**
   ```bash
   uv sync
   ```

2. **Run Notebooks:**
   Open any file in the `notebooks/` folder and select the `.venv` kernel to start exploring vision tasks or recording your own gestures.

3. **Custom Gestures:**
   - Record data with `gesture_data_recorder.ipynb`.
   - Train your model with `gesture_model_training.ipynb`.
   - Run inference with `webcam_object_detection.ipynb`.

## ⚙️ Environment
Requires a `.env` file in the root with your `GEMINI_API_KEY` for vision-language tasks.
