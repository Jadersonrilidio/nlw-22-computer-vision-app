# Vision Gesture Pro 🖐️🤖

**Vision Gesture Pro** is a real-time computer vision application that detects and recognizes hand gestures through a webcam. Combining deep learning for hand landmark detection and a custom machine learning classifier for gesture identification, the project offers a low-latency, interactive experience.

This project was developed during the **NLW 22 Challenge** (Next Level Week) by Rocketseat, an intensive event focused on cutting-edge technologies.

---

## 🚀 The NLW 22 Journey

The development was structured into three major milestones:

### 1️⃣ Foundations & CNNs
We explored the fundamentals of computer vision and Convolutional Neural Networks (CNNs). We implemented the **LeNet-5 architecture** from scratch, covering convolutional layers, pooling, and padding. The model was trained on the MNIST dataset to understand how networks "see" and interpret visual patterns.

### 2️⃣ Object Detection & Gesture Training
The focus shifted to real-world tasks like classification and detection. We utilized pre-trained models like **MobileNet** and **YOLO** for real-time object detection. Finally, we collected hand landmark data and trained a custom **Random Forest** classifier to create our own gesture recognition system.

### 3️⃣ Real-Time Web Integration
The final phase involved building a full-stack application. We integrated the AI models into a Python backend using **FastHTML** (built on Starlette) and implemented **WebSockets** for real-time video processing. The result is a seamless dashboard that processes webcam frames and displays gesture metadata with minimal delay.

---

## ✨ Key Features

- **Real-Time Hand Tracking**: Uses MediaPipe to detect 21 hand landmarks.
- **Custom Gesture Recognition**: High-accuracy classification of signs like "Heart", "Spock", "Rock", and more.
- **Low-Latency Streaming**: Bidirectional communication via WebSockets.
- **Dynamic Quality Control**: Adjustable stream quality to optimize performance based on network/hardware capacity.
- **Glassmorphism UI**: A modern, premium interface designed for clear data visualization.
- **Landmark Toggle**: Option to visualize hand skeletons directly on the video feed.

---

## 🛠️ Technologies Used

- **Language**: Python 3.12+
- **Computer Vision**: OpenCV, MediaPipe
- **Machine Learning**: Scikit-Learn, Joblib, NumPy, Pandas
- **Web Framework**: FastHTML / Starlette
- **Protocols**: WebSockets
- **Environment**: [uv](https://github.com/astral-sh/uv) (Package Manager)

---

## 🧠 Developed with Agentic Code

A significant portion of this project's **frontend structure and visual features** was generated and refined through **Agentic Code** interactions. This highlights the synergy between traditional software engineering and autonomous AI agents in building complex, modern interfaces and integrating real-time data streams efficiently.

---

## ⚙️ How to Run

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd computer_vision_app
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Start the server**:
   ```bash
   uv run python app.py
   ```

4. **Access the application**:
   Open your browser at `http://localhost:5001`.

---

**Developed during the Rocketseat NLW 22 Challenge.**
