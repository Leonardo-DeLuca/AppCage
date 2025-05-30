from werkzeug.serving import make_server
import threading

class HTTPServerThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.server = make_server("0.0.0.0", 5000, app)
        self.server.timeout = 1  
        self.ctx = app.app_context()
        self.ctx.push()
        self._shutdown_requested = False
        self.daemon = True  

    def run(self):
        while not self._shutdown_requested:
            self.server.handle_request()

    def shutdown(self):
        self._shutdown_requested = True
