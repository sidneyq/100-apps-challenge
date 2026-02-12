import http.server
import socketserver
import os

PORT = 5000
HOST = "0.0.0.0"
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps", "003-move-countdown")

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer((HOST, PORT), NoCacheHandler) as httpd:
    print(f"Serving {DIRECTORY} on http://{HOST}:{PORT}")
    httpd.serve_forever()
