import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from welcome import WelcomeScreen

def resource_path(relative_path):
    """Retorna o caminho absoluto correto, considerando que tudo está em src/"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    
    if not os.path.exists(full_path):
        print(f"AVISO: Arquivo não encontrado em {full_path}")
    
    return full_path

if __name__ == '__main__':
    app = QApplication(sys.argv)

    style_path = resource_path("style.qss")
    try:
        with open(style_path, "r") as style_file:
            app.setStyleSheet(style_file.read())
    except Exception as e:
        print("Erro ao carregar style.qss:", e)

    icon_path = resource_path("AppCage.png")
    app.setWindowIcon(QIcon(icon_path))

    window = WelcomeScreen()
    window.show()

    sys.exit(app.exec())
