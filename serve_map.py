import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Change to the script's directory
os.chdir(Path(__file__).parent)

# Port to serve on
PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # If accessing root, serve stadiums_map.html
        if self.path == '/':
            self.path = '/stadiums_map.html'
        return super().do_GET()

# Create the server
Handler = MyHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    print("Opening map in browser...")
    webbrowser.open(f'http://localhost:{PORT}/')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
