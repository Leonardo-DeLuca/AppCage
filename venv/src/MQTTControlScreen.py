import subprocess
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class MQTTControlScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.mqtt_process = None
        self.is_on = False  # Estado inicial do botão
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza tudo na tela

        # Título no topo
        title = QLabel("Controle MQTT")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()  # Adiciona espaço antes do botão para centralizar na tela

        # Botão toggle estilizado como um switch
        self.toggle_button = QPushButton("OFF")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFixedSize(120, 45)
        self.update_button_style()
        self.toggle_button.clicked.connect(self.toggle_mqtt)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Mensagem de status centralizada
        self.status_label = QLabel("Desligado")
        self.status_label.setStyleSheet("font-size: 18px; color: #333;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()  # Adiciona espaço depois do botão para centralizar

        self.setLayout(layout)

    def update_button_style(self):
        """ Atualiza o estilo do botão para parecer um switch """
        if self.is_on:
            self.toggle_button.setText("ON")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9cc659, stop:1 #b9d78a);
                    color: #2E7D32;
                    border-radius: 22px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                    border: 2px solid #81C784;
                }
            """)
        else:
            self.toggle_button.setText("OFF")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E0E0E0, stop:1 #BDBDBD);
                    color: #424242;
                    border-radius: 22px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                    border: 2px solid #9E9E9E;
                }
            """)

    def toggle_mqtt(self):
        self.is_on = not self.is_on  # Alterna o estado do botão
        self.update_button_style()
        if self.is_on:
            self.start_mqtt()
        else:
            self.stop_mqtt()

    def start_mqtt(self):
        if self.mqtt_process is None:
            try:
                self.mqtt_process = subprocess.Popen(["mosquitto"])
                self.status_label.setText("Ligado")
            except Exception as e:
                self.status_label.setText("Erro ao ligar")
                print("Erro ao iniciar o mosquitto:", e)

    def stop_mqtt(self):
        if self.mqtt_process is not None:
            try:
                self.mqtt_process.terminate()
                self.mqtt_process = None
                self.status_label.setText("Desligado")
            except Exception as e:
                self.status_label.setText("Erro ao desligar")
                print("Erro ao parar o mosquitto:", e)
