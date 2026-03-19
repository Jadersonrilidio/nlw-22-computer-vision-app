from fasthtml.common import fast_app, serve, Titled, Video, Canvas, Script
from starlette.responses import FileResponse
from core.gesture_recognizer import GestureRecognizer
from core.utils import check_models, decode_image, encode_image

# Pre-startup model check
if not check_models():
    raise Exception("Critical models missing.")

app, rt = fast_app()
recognizer = GestureRecognizer()

@rt("/assets/{fname:path}")
async def get_assets(fname:str):
    return FileResponse(f"assets/{fname}")

@rt("/")
def get():
    return Titled("Hand Gesture Recognition (FastHTML)",
        Video(id="v", autoplay=True, style="display:none"),
        Canvas(id="c", width=640, height=480),
        Script(src="/assets/script.js")
    )

@app.ws('/ws')
async def ws(image:str, send):
    try:
        frame = decode_image(image)
        if frame is not None:
            processed_image = recognizer.process_frame(frame)
            await send(encode_image(processed_image))
    except Exception as e:
        print(f"WS Error: {e}")

if __name__ == "__main__":
    try:
        serve()
    finally:
        # Graceful shutdown of MediaPipe resources
        print("\nShutting down resources...")
        recognizer.close()
