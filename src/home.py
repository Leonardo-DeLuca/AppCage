import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap
from HTTPServerScreen import HTTPServerScreen
from LiveViewScreen import LiveViewScreen
from ImportDataScreen import ImportDataScreen

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.resize(900, 600)
        self.setMinimumSize(900, 600)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setStyleSheet("background-color: #a16ef5;")
        self.sidebar_frame.setFixedWidth(200)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setSpacing(20)
        
        # Logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap("../AppCage.png")
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            logo_label.setPixmap(pixmap)
        except Exception as e:
            logo_label.setText("Logo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        # Botões do menu lateral
        self.btn_server = QPushButton("🔌 Ligar Server")
        self.btn_import = QPushButton("📥 Importar Dados")
        self.btn_live = QPushButton("📡 Live View")
        
        for btn in [self.btn_server, self.btn_import, self.btn_live]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("border: none; background-color: #fff; padding: 10px; border-radius: 10px; font-weight: bold;")
            btn.clicked.connect(self.animate_button)
        
        sidebar_layout.addWidget(self.btn_server)
        sidebar_layout.addWidget(self.btn_import)
        sidebar_layout.addWidget(self.btn_live)
        self.sidebar_frame.setLayout(sidebar_layout)
        
        # Área de conteúdo usando QStackedWidget
        self.stack = QStackedWidget()
        
        # Página inicial ("Bem-vindo")
        self.home_content = QWidget()
        home_layout = QVBoxLayout()
        home_layout.setContentsMargins(20, 20, 20, 20)
        welcome_label = QLabel("Bem-vindo!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        home_layout.addWidget(welcome_label)
        home_layout.addStretch()
        self.home_content.setLayout(home_layout)
        self.stack.addWidget(self.home_content)
        
        # Tela de Controle do Server
        self.server_control = HTTPServerScreen()
        self.stack.addWidget(self.server_control)
        
        # Nova Tela de Live View
        self.live_view_screen = LiveViewScreen()
        self.stack.addWidget(self.live_view_screen)

        self.import_screen = ImportDataScreen()
        self.stack.addWidget(self.import_screen)
        
        # Conecta os botões para trocar a página da área de conteúdo
        self.btn_server.clicked.connect(lambda: self.stack.setCurrentWidget(self.server_control))
        self.btn_import.clicked.connect(lambda: self.stack.setCurrentWidget(self.import_screen))
        self.btn_live.clicked.connect(lambda: self.stack.setCurrentWidget(self.live_view_screen))
        
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        
        self.setLayout(main_layout)

    def animate_button(self):
        sender = self.sender()
        original_geometry = sender.geometry()
        deslocamento = 10
        
        # Animação para deslocar o botão para a direita
        anim = QPropertyAnimation(sender, b"geometry")
        anim.setDuration(150)
        anim.setStartValue(original_geometry)
        anim.setEndValue(QRect(original_geometry.x() + deslocamento,
                                original_geometry.y(),
                                original_geometry.width(),
                                original_geometry.height()))
        
        # Animação de retorno
        anim_back = QPropertyAnimation(sender, b"geometry")
        anim_back.setDuration(150)
        anim_back.setStartValue(QRect(original_geometry.x() + deslocamento,
                                      original_geometry.y(),
                                      original_geometry.width(),
                                      original_geometry.height()))
        anim_back.setEndValue(original_geometry)
        
        anim.finished.connect(anim_back.start)
        anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    home_screen = HomeScreen()
    home_screen.show()
    sys.exit(app.exec())
