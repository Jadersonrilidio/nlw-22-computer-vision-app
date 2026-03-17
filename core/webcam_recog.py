import cv2
import os
from core.processor import GestureProcessor
from core.config import (
    MP_MODEL_PATH, 
    CUSTOM_MODEL_PATH, 
    ENCODER_PATH,
    WINDOW_NAME,
    FRAME_WIDTH,
    FRAME_HEIGHT
)

def check_models():
    """Verifies if all necessary model files exist."""
    models = [MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH]
    missing = [p for p in models if not os.path.exists(p)]
    if missing:
        print("Erro: Os seguintes modelos não foram encontrados:")
        for m in missing:
            print(f" - {m}")
        return False
    return True

def start_webcam():
    if not check_models():
        return

    print("--- Carregando modelos customizados ---")
    
    # Instance tracking the capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print(f"\nIniciando reconhecimento CUSTOMIZADO... Pressione 'q' para sair.")

    # Use the processor in a context manager
    try:
        with GestureProcessor(MP_MODEL_PATH, CUSTOM_MODEL_PATH, ENCODER_PATH) as processor:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    print("Falha ao capturar imagem da webcam.")
                    break

                # Process the frame (image_in -> image_out)
                processed_frame = processor.process_frame(frame)

                # Show result
                cv2.imshow(WINDOW_NAME, processed_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
