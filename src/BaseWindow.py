from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys, os

def resource_path(relative_path):
    """Retorna o caminho absoluto correto, considerando que tudo está em src/"""
    try:
        # Modo PyInstaller (executável empacotado)
        base_path = sys._MEIPASS
    except AttributeError:
        # Modo desenvolvimento (python main.py)
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    
    # Debug: Verifique se o arquivo existe
    if not os.path.exists(full_path):
        print(f"AVISO: Arquivo não encontrado em {full_path}")
    
    return full_path

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Define o ícone para todas as janelas
        icon_path = resource_path("AppCage.png")
        self.setWindowIcon(QIcon(icon_path))

        # Aplica o cursor de mão aos botões
        self.set_button_cursor()

    def set_button_cursor(self):
        """Define o cursor de mão para todos os botões"""
        # Encontra todos os botões filhos da janela
        for button in self.findChildren(QPushButton):
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            # Adiciona hover para o botão
            button.setStyleSheet("""
                QPushButton:hover {
                    background-color: #e0b7f2;  /* Cor de fundo ao passar o mouse */
                    color: #fff;  /* Cor do texto no hover */
                }
                QPushButton:pressed {
                    background-color: #d091f1;  /* Cor quando pressionado */
                    transform: scale(0.95);  /* Efeito de redução de tamanho ao pressionar */
                }
            """)
