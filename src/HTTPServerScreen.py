import sys
import os
import socket
import struct
import datetime
from flask import Flask, request, jsonify, send_file
from werkzeug.serving import make_server
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from HTTPServerThread import HTTPServerThread

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_LOG_FILE      = os.path.join(BASE_DIR, "esp_data.txt")
BIN_FILE           = os.path.join(BASE_DIR, "data.bin")
TXT_CONVERTED_FILE = os.path.join(BASE_DIR, "esp_history.txt")

HEADER_NAME_LEN = 32

_request_upload = False
_uploaded       = False

dados_esp = {
    "NomeGaiola":       "",
    "DiametroGaiola":   0.0,  # cm
    "NumeroVoltas":     0,
    "TempoAtividade":   0
}


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


class HTTPServerScreen(QWidget):
    def __init__(self):
        super().__init__()

        open(DATA_LOG_FILE, "a").close()

        self.server_thread  = None
        self.app            = Flask(__name__)
        self.configure_routes()
        self.server_running = False
        self.initUI()

    def configure_routes(self):
        global _request_upload, _uploaded

        @self.app.route("/request-upload", methods=["POST"])
        def request_upload():
            global _request_upload, _uploaded
            _request_upload = True
            _uploaded = False
            return jsonify({"ok": True})

        @self.app.route("/upload-status", methods=["GET"])
        def upload_status():
            return jsonify({"request": _request_upload, "uploaded": _uploaded})

        @self.app.route("/upload-bin", methods=["POST"])
        def upload_bin():
            global _request_upload, _uploaded
            data = request.get_data()
            try:
                with open(BIN_FILE, "wb") as f:
                    f.write(data)
                print("✅ Arquivo binário salvo com sucesso.")

                self.convert_bin_to_txt()

                _request_upload = False
                _uploaded       = True
                return jsonify({"status": "received"})
            except Exception as e:
                print("❌ Erro ao salvar binário:", e)
                return jsonify({"status": "error", "message": str(e)}), 500

        @self.app.route("/reset-upload", methods=["POST"])
        def reset_upload():
            global _request_upload, _uploaded
            _request_upload = False
            _uploaded       = False
            return jsonify({"reset": True})

        @self.app.route("/dados", methods=["GET"])
        def receber_dados():
            return dados_esp

        @self.app.route("/dados", methods=["POST"])
        def enviar_dados():
            global dados_esp
            dados = request.get_json()
            if dados:
                for chave in ["NumeroVoltas", "NomeGaiola", "TempoAtividade", "DiametroGaiola"]:
                    if chave in dados:
                        dados_esp[chave] = dados[chave]
            print("📦 Dados recebidos do ESP:", dados_esp)
            return {"status": "ok"}

        @self.app.route("/download", methods=["GET"])
        def download_converted():
            try:
                if os.path.exists(TXT_CONVERTED_FILE):
                    return send_file(
                        TXT_CONVERTED_FILE,
                        as_attachment=True,
                        download_name="esp_history.txt",
                        mimetype="text/plain"
                    )
                else:
                    return "Arquivo convertido não encontrado", 404
            except Exception as e:
                print("❌ Erro no download:", e)
                return jsonify({"error": str(e)}), 500

        @self.app.route("/ping", methods=["GET"])
        def ping():
            return "ok", 200

    def convert_bin_to_txt(self):
        global dados_esp

        try:
            with open(BIN_FILE, "rb") as f:
                name_bytes = f.read(HEADER_NAME_LEN)
                name = name_bytes.split(b'\x00', 1)[0].decode('utf-8', 'ignore')
                diameter_cm = struct.unpack("<f", f.read(4))[0]

                dados_esp["NomeGaiola"]     = name
                dados_esp["DiametroGaiola"] = diameter_cm

                lines = [
                    f"Nome da Gaiola: {name}",
                    f"Diâmetro da Gaiola: {diameter_cm:.2f} cm",
                    ""
                ]

                import math
                while True:
                    chunk = f.read(8)
                    if len(chunk) < 8:
                        break

                    timestamp, laps, duration = struct.unpack("<IHH", chunk)
                    inicio = datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

                    diam_m = diameter_cm / 100.0
                    distancia = laps * math.pi * diam_m
                    velocidade = distancia / duration if duration > 0 else 0

                    lines.append(
                        f"Início: {inicio} | Voltas: {laps} | Duração(s): {duration} | "
                        f"Distância(m): {distancia:.2f} | Vel.Média(m/s): {velocidade:.2f}"
                    )

            with open(TXT_CONVERTED_FILE, "w", encoding="utf-8") as f_txt:
                f_txt.write("\n".join(lines))

            print("📝 TXT formatado gerado com sucesso!")
        except Exception as e:
            print("❌ Erro na conversão bin→txt:", e)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Servidor Local para ESP")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        self.toggle_button = QPushButton("OFF")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFixedSize(120, 45)
        self.toggle_button.clicked.connect(self.toggle_server)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Desligado")
        self.status_label.setStyleSheet("font-size: 18px; color: #333;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)
        self.update_button_style()

    def toggle_server(self):
        if not self.server_running:
            self.start_server()
        else:
            self.stop_server()
        self.update_button_style()

    def start_server(self):
        self.server_thread = HTTPServerThread(self.app)
        self.server_thread.start()
        self.server_running = True

        ip = get_local_ip()
        port = 5000
        self.status_label.setText(f"Ligado em {ip}:{port}")

    def stop_server(self):
        if self.server_thread:
            self.server_thread.shutdown()
            self.server_thread.join(timeout=1)
            self.server_thread = None
        self.server_running = False
        self.status_label.setText("Desligado")

    def update_button_style(self):
        if self.server_running:
            self.toggle_button.setText("ON")
            self.toggle_button.setStyleSheet("""
                QPushButton { background-color: #9cc659; color: #2E7D32; border-radius: 22px; font-weight: bold; }
            """)
        else:
            self.toggle_button.setText("OFF")
            self.toggle_button.setStyleSheet("""
                QPushButton { background-color: #E0E0E0; color: #424242; border-radius: 22px; font-weight: bold; }
            """)
        from PyQt6.QtGui import QCursor
        self.toggle_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
