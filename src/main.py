import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from welcome import WelcomeScreen

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funcionando tanto em desenvolvimento quanto em executável empacotado."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Aplica o style.qss usando o caminho absoluto
    style_path = resource_path("style.qss")
    try:
        with open(style_path, "r") as style_file:
            app.setStyleSheet(style_file.read())
    except Exception as e:
        print("Erro ao carregar style.qss:", e)

    # Configura o ícone da janela
    icon_path = resource_path("../AppCage.png")
    app.setWindowIcon(QIcon(icon_path))

    window = WelcomeScreen()
    window.show()

    sys.exit(app.exec())
