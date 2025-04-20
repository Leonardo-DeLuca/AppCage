from flask import Flask
from werkzeug.serving import make_server
import threading

class HTTPServerThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.server = make_server("0.0.0.0", 5000, app)
        # Define um timeout para permitir que handle_request() retorne periodicamente
        self.server.timeout = 1  
        self.ctx = app.app_context()
        self.ctx.push()
        self._shutdown_requested = False
        self.daemon = True  # Garante que a thread seja encerrada com o app

    def run(self):
        # Loop que chama handle_request() de forma periódica,
        # verificando se há solicitação de shutdown
        while not self._shutdown_requested:
            self.server.handle_request()

    def shutdown(self):
        # Solicita o encerramento
        self._shutdown_requested = True
