import sys
from core.webcam_recog import start_webcam

def main() -> int:
    try:
        print("Iniciando Aplicativo de Visão Computacional...")
        start_webcam()
        return 0
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        return 0
    except ImportError as e:
        print(f"Erro de importação: {e}")
        return 1
    except Exception as e:
        print(f"Erro ao iniciar o aplicativo: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
