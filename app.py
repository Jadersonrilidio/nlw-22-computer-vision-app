import sys
from core.webcam_recog import WebCamRecog

# run on terminal: `uv run streamlit run app.py`
# options: ['STREAMLIT', 'TERMINAL']
def main() -> int:
    try:
        print("Iniciando Aplicativo de Visão Computacional...")

        WebCamRecog.run(option='STREAMLIT')

        return 0
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        return 0
    except ImportError as e:
        print(f"Erro de importação: {e}")
        return 1
    except ValueError as e:
        print(f"Erro: {e}")
        return 1
    except Exception as e:
        print(f"Erro ao iniciar o aplicativo: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
