from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QSequentialAnimationGroup
from login import LoginScreen

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("welcomeScreen")  # Para aplicar estilos específicos definidos no style.qss
        self.setWindowTitle("Bem-vindo")
        self.resize(500, 400)
        self.setMinimumSize(500, 400)
        self.setStyleSheet("background-color: #a16ef5;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Bem-vindo!")
        self.label.setObjectName("welcomeLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(self.label)

        self.access_btn = QPushButton("Acessar o Sistema")
        self.access_btn.setObjectName("accessButton")
        self.access_btn.setStyleSheet("background-color: white; color: #a16ef5; border-radius: 10px; padding: 10px; font-weight: bold;")
        self.access_btn.clicked.connect(self.animateButton)
        layout.addWidget(self.access_btn)

        self.setLayout(layout)

    def animateButton(self):
        original_geometry = self.access_btn.geometry()
        deslocamento = 10  # Pixels de deslocamento

        # Cria um grupo de animações sequenciais para garantir a execução ordenada
        anim_group = QSequentialAnimationGroup(self)

        # Primeira animação: desloca o botão para a direita
        anim1 = QPropertyAnimation(self.access_btn, b"geometry")
        anim1.setDuration(150)
        anim1.setStartValue(original_geometry)
        anim1.setEndValue(QRect(original_geometry.x() + deslocamento,
                                 original_geometry.y(),
                                 original_geometry.width(),
                                 original_geometry.height()))
        
        # Segunda animação: retorna o botão à posição original
        anim2 = QPropertyAnimation(self.access_btn, b"geometry")
        anim2.setDuration(150)
        anim2.setStartValue(QRect(original_geometry.x() + deslocamento,
                                 original_geometry.y(),
                                 original_geometry.width(),
                                 original_geometry.height()))
        anim2.setEndValue(original_geometry)

        anim_group.addAnimation(anim1)
        anim_group.addAnimation(anim2)
        anim_group.finished.connect(self.goToLogin)
        anim_group.start()

    def goToLogin(self):
        self.login_screen = LoginScreen()
        self.login_screen.show()
        self.close()
