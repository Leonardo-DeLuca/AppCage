import os, requests
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor

class ImportDataScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Importar Histórico BIN")
        self.resize(500, 250)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.status_label = QLabel("Pronto para solicitar.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Botão solicitar
        self.btn_request = QPushButton("📤 Solicitar Histórico")
        self.btn_request.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_request.clicked.connect(self.request_upload)
        layout.addWidget(self.btn_request, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão salvar (inicialmente desabilitado)
        self.btn_save = QPushButton("💾 Salvar Arquivo")
        self.btn_save.setEnabled(False)
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.clicked.connect(self.save_file)
        layout.addWidget(self.btn_save, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def request_upload(self):
        try:
            resp = requests.post("http://localhost:5000/request-upload", timeout=1)
            resp.raise_for_status()
            self.status_label.setText("Solicitação enviada. Aguardando ESP...")
            self.btn_request.setEnabled(False)
            self.timer.start(2000)  # checa status a cada 1s
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível solicitar: {e}")

    def check_status(self):
        try:
            resp = requests.get("http://localhost:5000/upload-status", timeout=0.5)
            data = resp.json()
            if data.get("uploaded"):
                self.timer.stop()
                self.status_label.setText("Histórico recebido! Salve o arquivo.")
                self.btn_save.setEnabled(True)
        except:
            pass  # ignora erros até o arquivo chegar

    def save_file(self):
        src = "esp_history.txt"
        if not os.path.exists(src):
            QMessageBox.warning(self, "Atenção", "Arquivo não encontrado no servidor.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Histórico Como", "esp_history.txt", "TXT Files (*.txt)"
        )
        if not path:
            return

        try:
            # Salva o arquivo localmente
            with open(src, "rb") as fsrc, open(path, "wb") as fdst:
                fdst.write(fsrc.read())
            self.status_label.setText(f"Salvo em:\n{path}")

            # CHANGED: notificar o servidor para resetar as flags de upload
            try:
                import requests
                requests.post("http://localhost:5000/reset-upload", timeout=1)
            except Exception:
                # opcional: logar ou ignorar erro
                pass

            # CHANGED: ajustar UI para permitir nova solicitação
            self.btn_save.setEnabled(False)
            self.btn_request.setEnabled(True)
            self.status_label.setText("Pronto para solicitar novo histórico.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar: {e}")

