import requests
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QFont

class ImportDataScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Importar Histórico do ESP")
        self.resize(600, 450)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("Importar Histórico do ESP")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)

        # Botão Solicitar
        self.btn_request = QPushButton("📤 Solicitar Histórico")
        self.btn_request.setFixedSize(350, 70)
        self.btn_request.setFont(QFont("Segoe UI", 18))
        self.btn_request.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_request.clicked.connect(self.request_upload)
        layout.addWidget(self.btn_request, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        # Botão Salvar TXT
        self.btn_save_txt = QPushButton("💾 Salvar como TXT")
        self.btn_save_txt.setFixedSize(350, 70)
        self.btn_save_txt.setFont(QFont("Segoe UI", 18))
        self.btn_save_txt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save_txt.setEnabled(False)
        self.btn_save_txt.clicked.connect(self.save_txt)
        layout.addWidget(self.btn_save_txt, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        # Botão Salvar Excel
        self.btn_save_excel = QPushButton("📊 Salvar como Excel")
        self.btn_save_excel.setFixedSize(350, 70)
        self.btn_save_excel.setFont(QFont("Segoe UI", 18))
        self.btn_save_excel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save_excel.setEnabled(False)
        self.btn_save_excel.clicked.connect(self.save_excel)
        layout.addWidget(self.btn_save_excel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        # Label de status
        self.status_label = QLabel("Pronto para solicitação")
        self.status_label.setFont(QFont("Segoe UI", 16))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Timer para checar status de upload
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_status)

    def _fetch_records_and_meta(self):
        try:
            # Busca o conteúdo do arquivo TXT (texto formatado)
            resp = requests.get("http://localhost:5000/download", timeout=5)
            resp.raise_for_status()
            content = resp.text.strip().splitlines()

            nome = ""
            diametro_cm = 0.0
            registros = []

            for line in content:
                if line.startswith("Nome da Gaiola:"):
                    nome = line.split(":", 1)[1].strip()
                elif line.startswith("Diâmetro da Gaiola:"):
                    diametro_cm = float(line.split(":")[1].strip().split()[0])
                elif line.startswith("Início:"):
                    partes = line.split("|")
                    dados = {}
                    for p in partes:
                        chave, valor = p.strip().split(":", 1)
                        dados[chave.strip()] = valor.strip()
                    
                    inicio = dados.get("Início", "")
                    voltas = int(dados.get("Voltas", 0))
                    duracao = int(dados.get("Duração(s)", 0))
                    distancia = float(dados.get("Distância(m)", 0))
                    velocidade = float(dados.get("Vel.Média(m/s)", 0))

                    registros.append({
                        "Início": inicio,
                        "Voltas": voltas,
                        "Duração(s)": duracao,
                        "Distância(m)": distancia,
                        "Vel.Média(m/s)": velocidade,
                        "NomeGaiola": nome,
                        "Diâmetro (cm)": diametro_cm
                    })

            return registros

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar dados:\n{e}")
            return []


    def request_upload(self):
        try:
            resp = requests.post("http://localhost:5000/request-upload", timeout=2)
            resp.raise_for_status()
            self.status_label.setText("Solicitação enviada. Aguardando ESP...")
            self.btn_request.setEnabled(False)
            self.timer.start(1000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao solicitar histórico:\n{e}")

    def check_status(self):
        try:
            resp = requests.get("http://localhost:5000/upload-status", timeout=1)
            data = resp.json()
            if data.get("uploaded"):
                self.timer.stop()
                self.status_label.setText("Histórico recebido! Escolha o formato:")
                self.btn_save_txt.setEnabled(True)
                self.btn_save_excel.setEnabled(True)
        except:
            pass

    def save_txt(self):
        try:
            resp = requests.get("http://localhost:5000/download", timeout=5)
            resp.raise_for_status()
            path, _ = QFileDialog.getSaveFileName(
                self, "Salvar como TXT", "esp_history.txt", "TXT Files (*.txt)"
            )
            if path:
                with open(path, "wb") as f:
                    f.write(resp.content)
                self.status_label.setText(f"Arquivo TXT salvo em:\n{path}")
                # Reseta flags no servidor
                requests.post("http://localhost:5000/reset-upload", timeout=1)
                self.reset_buttons()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar TXT:\n{e}")

    def save_excel(self):
        try:
            # Busca registros e metadados
            recs = self._fetch_records_and_meta()
            df = pd.DataFrame(recs) 

            # Remove as colunas redundantes que já estão no cabeçalho
            df = df.drop(columns=["NomeGaiola", "Diâmetro (cm)"], errors="ignore")


            path, _ = QFileDialog.getSaveFileName(
                self, "Salvar como Excel", "esp_history.xlsx", "Excel Files (*.xlsx)"
            )
            if not path:
                return

            # Cria o Excel
            with pd.ExcelWriter(path, engine='openpyxl') as writer:
                # Escreve o DataFrame a partir da linha 4 (índice startrow=3)
                df.to_excel(writer, index=False, startrow=3, sheet_name='Histórico')
                
                # Acessa a planilha gerada
                worksheet = writer.sheets['Histórico']
                
                # Escreve cabeçalho nas duas primeiras linhas
                # Usamos os mesmos valores do primeiro registro
                if recs:
                    primeiro = recs[0]
                    nome = primeiro["NomeGaiola"]
                    diam_cm = primeiro["Diâmetro (cm)"]
                else:
                    nome = ""
                    diam_cm = 0.0

                worksheet['A1'] = f"Nome da Gaiola: {nome}"
                worksheet['A2'] = f"Diâmetro da Gaiola: {diam_cm:.2f} cm"
                
                # (Opcional) ajusta largura de colunas para melhor visualização
                for idx, col in enumerate(df.columns, start=1):
                    worksheet.column_dimensions[worksheet.cell(row=4, column=idx).column_letter].width = 20

            self.status_label.setText(f"Excel salvo em:\n{path}")
            # Reseta flags no servidor
            requests.post("http://localhost:5000/reset-upload", timeout=1)
            self.reset_buttons()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar Excel:\n{e}")


    def reset_buttons(self):
        self.btn_request.setEnabled(True)
        self.btn_save_txt.setEnabled(False)
        self.btn_save_excel.setEnabled(False)
        self.status_label.setText("Pronto para solicitação")
