import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_STREAM
import urllib.parse as urlparse

HOST = '0.0.0.0'
PORT = 3000

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        elif self.path == '/message':
            self.path = '/templates/message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path
        else:
            self.path = '/templates/error.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = urlparse.parse_qs(post_data.decode('utf-8'))

            message = {
                "username": form_data['username'][0],
                "message": form_data['message'][0]
            }

            # Send data to the socket server
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect(('localhost', 5000))
                s.sendall(str(message).encode('utf-8'))
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Message sent successfully!")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer((HOST, PORT), CustomHandler)
    print(f"HTTP Server running on http://{HOST}:{PORT}")
    server.serve_forever()
