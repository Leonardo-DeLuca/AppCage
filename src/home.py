import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap
from HTTPServerScreen import HTTPServerScreen
from LiveViewScreen import LiveViewScreen
from ImportDataScreen import ImportDataScreen
from BaseWindow import BaseWindow


class HomeScreen(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.resize(900, 600)
        self.setMinimumSize(900, 600)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # LATERAL ESQUERDA
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setStyleSheet("background-color: #a16ef5;")
        self.sidebar_frame.setFixedWidth(200)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setSpacing(20)

        logo_label = QLabel()
        try:
            pixmap = QPixmap("../AppCage.png")
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            logo_label.setPixmap(pixmap)
        except Exception:
            logo_label.setText("Logo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        self.btn_server = QPushButton("🔌 Ligar Server")
        self.btn_import = QPushButton("📥 Importar Dados")
        self.btn_live = QPushButton("📡 Live View")

        for btn in [self.btn_server, self.btn_import, self.btn_live]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                border: none;
                background-color: #fff;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            """)
            btn.clicked.connect(self.animate_button)

        sidebar_layout.addWidget(self.btn_server)
        sidebar_layout.addWidget(self.btn_import)
        sidebar_layout.addWidget(self.btn_live)
        self.sidebar_frame.setLayout(sidebar_layout)

        # CONTEÚDO PRINCIPAL
        self.stack = QStackedWidget()

        # HOME aprimorada
        self.home_content = QWidget()
        home_layout = QVBoxLayout()
        home_layout.setContentsMargins(30, 30, 30, 30)
        home_layout.setSpacing(20)

        welcome_label = QLabel("👋 Olá, bem-vindo de volta!")
        welcome_label.setStyleSheet("font-size: 28px; font-weight: 600; color: #333;")

        subtitle_label = QLabel("Use o menu à esquerda para começar.")
        subtitle_label.setStyleSheet("font-size: 18px; color: #555;")
        home_layout.addWidget(welcome_label)
        home_layout.addWidget(subtitle_label)
        self.home_content.setLayout(home_layout)
        self.stack.addWidget(self.home_content)

        # OUTRAS TELAS
        self.server_control = HTTPServerScreen()
        self.stack.addWidget(self.server_control)

        self.live_view_screen = LiveViewScreen()
        self.stack.addWidget(self.live_view_screen)

        self.import_screen = ImportDataScreen()
        self.stack.addWidget(self.import_screen)

        # Troca de telas
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

        anim = QPropertyAnimation(sender, b"geometry")
        anim.setDuration(150)
        anim.setStartValue(original_geometry)
        anim.setEndValue(QRect(original_geometry.x() + deslocamento,
                                original_geometry.y(),
                                original_geometry.width(),
                                original_geometry.height()))

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