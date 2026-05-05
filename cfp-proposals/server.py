#!/usr/bin/env python3
"""Local CFP dashboard server. Run: python3 server.py"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "submissions.json")
HTML_FILE = os.path.join(HERE, "dashboard.html")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/dashboard.html"):
            self._serve_file(HTML_FILE, "text/html; charset=utf-8")
        elif self.path == "/data":
            self._serve_file(DATA_FILE, "application/json")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                parsed = json.loads(body)
                with open(DATA_FILE, "w") as f:
                    json.dump(parsed, f, indent=2, ensure_ascii=False)
                self._json_response(200, {"ok": True})
            except Exception as e:
                self._json_response(400, {"error": str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def _json_response(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # silence request logs


if __name__ == "__main__":
    port = 8765
    server = HTTPServer(("localhost", port), Handler)
    print(f"CFP Dashboard → http://localhost:{port}")
    print("Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
