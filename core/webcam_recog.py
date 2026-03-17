import cv2
import os
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from core.processor import GestureProcessor, VideoProcessor
from core.config import (
    MP_MODEL_PATH, 
    CUSTOM_MODEL_PATH, 
    ENCODER_PATH,
    WINDOW_NAME,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    RTC_CONFIGURATION
)

class WebCamRecog():
    @classmethod
    def run(cls, option: str = 'TERMINAL'):
        if not cls.check_models():
            raise Exception("Modelos não encontrados.")
        if option not in ['STREAMLIT', 'TERMINAL']:
            raise ValueError("Opção inválida. Escolha entre 'STREAMLIT' ou 'TERMINAL'.")
        match (option):
            case 'TERMINAL':
                cls.start_webcam()
            case 'STREAMLIT':
                cls.start_streamlit()

    @staticmethod
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

    @classmethod
    def start_webcam(cls):
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

    @classmethod
    def start_streamlit(cls):
        st.set_page_config(
            page_title="Gesture Recognition WebApp",
            page_icon="🖐️",
            layout="wide"
        )
        
        st.title("Real-time Gesture Recognition")
        st.markdown("""
        Este WebApp utiliza **MediaPipe** e um modelo customizado treinado com **Scikit-Learn** 
        para reconhecer gestos manuais em tempo real através do navegador.
        """)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Webcam Feed")
            ctx = webrtc_streamer(
                key="gesture-recognition",
                video_processor_factory=VideoProcessor,
                rtc_configuration=RTC_CONFIGURATION,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )

        with col2:
            st.subheader("Informações do Modelo")
            st.info("O modelo está rodando no servidor via WebRTC.")
            
            st.write("### Gestos Suportados")
            # List common gestures if known, or just a general description
            st.write("- joinha")
            st.write("- paz")
            st.write("- rock")
            st.write("- coracao")
            st.write("- hangloose")
            st.write("- spock")
            st.write("- ola")

            if st.button("Reiniciar Processador"):
                st.cache_resource.clear()
                st.rerun()