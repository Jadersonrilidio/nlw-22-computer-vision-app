import os, time
from fasthtml.common import fast_app, serve, Video, Canvas, Script, Div, H1, H3, Input, Label, Span, Link, Title
from starlette.responses import FileResponse
from core.detector import GestureDetector
from core.io_utils import validate_model_files, convert_base64_to_frame, convert_frame_to_base64

# 1. Basic Setup & Model Verification
if not validate_model_files():
    raise Exception("Critical component failure: unable to locate required ML model files.")

# Initialize the FastHTML app and our custom detection engine
# 'rt' is the route decorator for building pages
app, rt = fast_app()
vision_engine = GestureDetector()

# 2. Asset Serving Route
@rt("/assets/{fname:path}")
async def get_static_assets(fname:str):
    """Serve any file from the /assets folder (CSS, JS, images, etc.)"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "assets", fname)
    return FileResponse(file_path)

# 3. Main Dashboard Page
@rt("/")
def render_dashboard():
    """Renders the single-page application UI."""
    return (
        Title("Vision Gesture Pro"),
        Link(rel="stylesheet", href="/assets/css/style.css"),
        Div(
            Div(H1("Vision Gesture Pro"), cls="header"),
            Div(
                # Left Panel: Live Visuals
                Div(
                    Video(id="v", autoplay=True, cls="hidden-video", playsinline=True),
                    Canvas(id="c", width=640, height=480),
                    cls="video-section"
                ),
                # Right Panel: Interactive Controls and Data
                Div(
                    # Settings (40% height)
                    Div(
                        H3("Settings & Analysis", Span(id="fps", cls="fps-badge")),
                        Div(
                            Label("Stream Quality", cls="field-label"),
                            Input(id="quality", type="range", min="0.1", max="1.0", step="0.1", value="0.5", cls="field-range"),
                        ),
                        Div(
                            Label(
                                Input(id="show_landmarks", type="checkbox", checked="true", cls="checkbox-input"),
                                "Draw Hand Landmarks",
                                cls="field-label-flex"
                            )
                        ),
                        # Live gesture list is populated dynamically here
                        Div(id="gestures"),
                        cls="panel-box settings-panel"
                    ),
                    # Gesture Result (60% height)
                    Div(
                        H3("Detected Gesture"),
                        Div(id="match-container"),
                        cls="panel-box gesture-panel"
                    ),
                    cls="info-panel"
                ),
                cls="app-grid"
            ),
            cls="main-container"
        ),
        Script(src=f"/assets/js/script.js?v={os.urandom(4).hex()}")
    )

# 4. WebSocket Data Processing Entrypoint
@app.ws('/ws')
async def handle_vision_feed(image:str, show_landmarks:bool, ws):
    """Bridge between client-side frames and the backend detection engine."""
    start_time = time.time()
    try:
        if not image: return
        
        # Process the raw base64 frame from the browser
        current_frame = convert_base64_to_frame(image)
        
        if current_frame is not None:
            # Perform detection and classification
            processed_image, detected_gestures = vision_engine.detect_gestures(
                current_frame, draw_landmarks=show_landmarks
            )
            
            # Simplified match rule: if multiple hands, we look for consensus (matching gestures)
            consensus_gesture = None
            if len(detected_gestures) >= 2:
                g1, g2 = detected_gestures[0]['gesture'], detected_gestures[1]['gesture']
                if g1 == g2: consensus_gesture = g1

            # Performance metric calculation
            runtime = time.time() - start_time
            current_fps = 1.0 / runtime if runtime > 0 else 0

            # Send back the processed JPG frame and JSON metadata
            await ws.send_json({
                "image": convert_frame_to_base64(processed_image),
                "gestures": detected_gestures,
                "match": consensus_gesture,
                "fps": round(current_fps, 1)
            })
    except Exception as e:
        print(f"Vision Stream Error: {e}")


# 5. Application Execution Entrypoint
if __name__ == "__main__":
    try:
        serve()
    finally:
        # Crucial for memory management in MediaPipe
        print("\nShutting down vision engine...")
        vision_engine.release_resources()
