from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
import requests
import math
import datetime

class LiveViewScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título da página
        self.label_title = QLabel("Live View")
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)
        
        layout.addStretch()
        info_layout = QVBoxLayout()
        
        # Nome da Gaiola
        self.label_nome_gaiola = QLabel("Nome da Gaiola:")
        self.value_nome_gaiola = QLabel("Aguardando...")
        self.label_nome_gaiola.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_nome_gaiola.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_nome_gaiola, self.value_nome_gaiola))
        
        # Número de Voltas
        self.label_numero_voltas = QLabel("Número de Voltas:")
        self.value_numero_voltas = QLabel("0")
        self.label_numero_voltas.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_numero_voltas.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_numero_voltas, self.value_numero_voltas))
        
        # Tempo de Atividade
        self.label_tempo_atividade = QLabel("Tempo de Atividade:")
        self.value_tempo_atividade = QLabel("0 s")
        self.label_tempo_atividade.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_tempo_atividade.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_tempo_atividade, self.value_tempo_atividade))
        
        # Diâmetro da Gaiola
        self.label_diametro_gaiola = QLabel("Diâmetro da Gaiola:")
        self.value_diametro_gaiola = QLabel("0 m")
        self.label_diametro_gaiola.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_diametro_gaiola.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_diametro_gaiola, self.value_diametro_gaiola))
        
        # Distância
        self.label_distancia = QLabel("Distância:")
        self.value_distancia = QLabel("0 m")
        self.label_distancia.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_distancia.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_distancia, self.value_distancia))

        # Velocidade Média
        self.label_velocidade = QLabel("Velocidade Média:")
        self.value_velocidade = QLabel("0 m/s")
        self.label_velocidade.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_velocidade.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_velocidade, self.value_velocidade))

        # Início da Atividade
        self.label_inicio = QLabel("Início da Atividade:")
        self.value_inicio = QLabel("--:--:--")
        self.label_inicio.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_inicio.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_inicio, self.value_inicio))

        # Fim da Atividade
        self.label_fim = QLabel("Fim da Atividade:")
        self.value_fim = QLabel("--:--:--")
        self.label_fim.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        self.value_fim.setStyleSheet("font-size: 18px; color: #333;")
        info_layout.addLayout(self.create_info_row(self.label_fim, self.value_fim))
        
        layout.addLayout(info_layout)

        layout.addStretch()
        self.setLayout(layout)
        
        # Timer para atualização periódica
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_status)
        self.timer.start(10000)

    def create_info_row(self, label, value_label):
        row_layout = QHBoxLayout()
        row_layout.addWidget(label)
        row_layout.addWidget(value_label)
        row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return row_layout

    def fetch_status(self):
        try:
            response = requests.get("http://localhost:5000/dados", timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                numero_voltas      = data.get("NumeroVoltas", 0)
                nome_gaiola        = data.get("NomeGaiola", "N/A")
                tempo_atividade     = data.get("TempoAtividade", 0)
                diametro_gaiola_cm = data.get("DiametroGaiola", 0.0)
                inicio_epoch       = data.get("InicioAtividade", 0)
                fim_epoch          = data.get("FimAtividade", 0)

                # Conversões
                diametro_m = diametro_gaiola_cm / 100.0
                distancia  = numero_voltas * math.pi * diametro_m
                vel_media  = distancia / tempo_atividade if tempo_atividade > 0 else 0

                # Formatação de datas
                inicio_str = datetime.datetime.fromtimestamp(inicio_epoch).strftime("%d/%m/%Y %H:%M:%S") if inicio_epoch > 0 else "--:--:--"
                fim_str    = datetime.datetime.fromtimestamp(fim_epoch).strftime("%d/%m/%Y %H:%M:%S") if fim_epoch > 0 else "--:--:--"

                # Atualiza labels
                self.value_nome_gaiola.setText(nome_gaiola)
                self.value_numero_voltas.setText(str(numero_voltas))
                self.value_tempo_atividade.setText(f"{tempo_atividade} s")
                self.value_diametro_gaiola.setText(f"{diametro_m:.2f} m")
                self.value_distancia.setText(f"{distancia:.2f} m")
                self.value_velocidade.setText(f"{vel_media:.2f} m/s")
                self.value_inicio.setText(inicio_str)
                self.value_fim.setText(fim_str)
        except Exception:
            pass
