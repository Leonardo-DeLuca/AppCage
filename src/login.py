from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QSequentialAnimationGroup
from home import HomeScreen
from BaseWindow import BaseWindow


class LoginScreen(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(500, 400)
        self.setMinimumSize(500, 400)
        self.setStyleSheet("background-color: #f4f4f8;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Faça o Login")
        self.title_label.setObjectName("loginLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        layout.addWidget(self.title_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        self.user_input.setObjectName("inputField")
        self.user_input.setFixedWidth(250)
        self.user_input.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("inputField")
        self.password_input.setFixedWidth(250)
        self.password_input.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")
        layout.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setFixedWidth(250)
        self.error_label.setFixedHeight(20)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.login_button = QPushButton("Entrar")
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedWidth(250)
        self.login_button.setStyleSheet("background-color: #a16ef5; color: white; font-weight: bold; padding: 10px; border-radius: 8px;")
        self.login_button.clicked.connect(self.validate_login)
        layout.addWidget(self.login_button)

        self.user_input.textChanged.connect(self.clear_error)
        self.password_input.textChanged.connect(self.clear_error)

        self.setLayout(layout)

    def validate_login(self):
        username = self.user_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.animateSuccess()
        else:
            self.animateFailure()

    def clear_error(self):
        self.error_label.setText("")

    def animateSuccess(self):
        original_geometry = self.login_button.geometry()
        deslocamento = 10

        anim1 = QPropertyAnimation(self.login_button, b"geometry")
        anim1.setDuration(300)
        anim1.setStartValue(original_geometry)
        anim1.setEndValue(QRect(original_geometry.x() + deslocamento,
                                  original_geometry.y(),
                                  original_geometry.width(),
                                  original_geometry.height()))

        anim2 = QPropertyAnimation(self.login_button, b"geometry")
        anim2.setDuration(300)
        anim2.setStartValue(QRect(original_geometry.x() + deslocamento,
                                  original_geometry.y(),
                                  original_geometry.width(),
                                  original_geometry.height()))
        anim2.setEndValue(original_geometry)

        self.success_group = QSequentialAnimationGroup()
        self.success_group.addAnimation(anim1)
        self.success_group.addAnimation(anim2)
        self.success_group.finished.connect(self.on_success)
        self.success_group.start()

    def on_success(self):
        print("Login bem-sucedido!")
        geometry = self.geometry()
        is_maximized = self.isMaximized()

        self.home_screen = HomeScreen()
        self.home_screen.setGeometry(geometry)
        if is_maximized:
            self.home_screen.showMaximized()
        else:
            self.home_screen.show()

        self.close()


    def animateFailure(self):
        original_geometry = self.login_button.geometry()
        shake_offset = 5
        duration_per_move = 80

        self.failure_group = QSequentialAnimationGroup()
        for offset in [-shake_offset, shake_offset, -shake_offset, shake_offset, 0]:
            anim = QPropertyAnimation(self.login_button, b"geometry")
            anim.setDuration(duration_per_move)
            anim.setStartValue(self.login_button.geometry())
            new_x = original_geometry.x() + offset
            anim.setEndValue(QRect(new_x, original_geometry.y(), original_geometry.width(), original_geometry.height()))
            self.failure_group.addAnimation(anim)

        self.failure_group.start()
        self.error_label.setText("Login inválido!")
