import http.server, os, sys, urllib.parse
DEST = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def _h(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
    def do_OPTIONS(self):
        self.send_response(204); self._h(); self.end_headers()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = os.path.basename(q.get("name", ["sans_nom"])[0])
        n = int(self.headers.get("Content-Length", 0)); data = self.rfile.read(n)
        open(os.path.join(DEST, name), "wb").write(data)
        self.send_response(200); self._h(); self.end_headers(); self.wfile.write(str(len(data)).encode())
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", 8765), H).serve_forever()
