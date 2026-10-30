"""
Local Web Server for Routing Protocol Simulator
Serves index.html on http://localhost:8000 and automatically opens the browser.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 65)
        print("  ROUTING PROTOCOL SIMULATOR - INTERACTIVE WEB DASHBOARD")
        print("=" * 65)
        print(f"\n[+] Serving interactive web app at: {url}")
        print("[+] Press Ctrl+C in this terminal to stop the web server.\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Web server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    run()

