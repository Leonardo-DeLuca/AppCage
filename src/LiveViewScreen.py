from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
import requests
import math

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
        
        # Label para exibir os dados recebidos
        self.label_dados = QLabel("Aguardando dados...")
        self.label_dados.setStyleSheet("font-size: 18px; color: #333;")
        self.label_dados.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_dados)
        
        # Label para velocidade média e distância
        self.label_velocidade = QLabel("Velocidade Média: 0 m/s")
        self.label_velocidade.setStyleSheet("font-size: 18px; color: #333;")
        self.label_velocidade.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_velocidade)

        self.label_distancia = QLabel("Distância: 0 m")
        self.label_distancia.setStyleSheet("font-size: 18px; color: #333;")
        self.label_distancia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_distancia)
        
        self.setLayout(layout)
        
        # Timer para atualizar os dados a cada 1 segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_status)
        self.timer.start(1000)

    def fetch_status(self):
        try:
            response = requests.get("http://localhost:5000/status", timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                numero_voltas = data.get("NumeroVoltas", 0)
                nome_gaiola = data.get("NomeGaiola", "N/A")
                tempo_atividade = data.get("TempoAtividade", 0)
                diametro_gaiola = data.get("DiametroGaiola", 0.0)

                
                
                # Converte para metros
                diametro_gaiola_cm = data.get("DiametroGaiola", 0.0)
                diametro_gaiola = diametro_gaiola_cm / 100.0  # cm → m

                # Distância = NúmeroVoltas * (π * Diâmetro)
                distancia = numero_voltas * math.pi * diametro_gaiola

                # Velocidade média = Distância / Tempo (se tempo > 0)
                velocidade_media = distancia / tempo_atividade if tempo_atividade > 0 else 0

                texto = (
                    f"Nome da Gaiola: {nome_gaiola}\n"
                    f"Número de Voltas: {numero_voltas}\n"
                    f"Tempo de Atividade: {tempo_atividade} s\n"
                    f"Diâmetro da Gaiola: {diametro_gaiola} m"
                )
                self.label_dados.setText(texto)
                
                self.label_distancia.setText(f"Distância: {distancia:.2f} m")
                self.label_velocidade.setText(f"Velocidade Média: {velocidade_media:.2f} m/s")
        except Exception as e:
            # Se não conseguir obter os dados, não atualiza
            pass
