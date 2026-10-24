"""Servidor de la interfaz de demostracion.
Sirve interfaz.html en http://127.0.0.1:5500 y reenvia /api/... a la API (127.0.0.1:8000).
Asi el navegador no bloquea las peticiones (sin CORS) y no se toca el codigo del proyecto.
Solo usa la biblioteca estandar de Python."""
import urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

API = "http://127.0.0.1:8000"
HTML = Path(__file__).with_name("interfaz.html")

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _proxy(self):
        if not self.path.startswith("/api/"):
            if self.path in ("/", "/index.html"):
                return self._send(200, HTML.read_bytes(), "text/html; charset=utf-8")
            return self._send(404, b'{"detail":"No encontrado"}')
        n = int(self.headers.get("Content-Length") or 0)
        data = self.rfile.read(n) if n else None
        req = urllib.request.Request(API + self.path[4:], data=data, method=self.command)
        for h in ("Content-Type", "Authorization"):
            if self.headers.get(h):
                req.add_header(h, self.headers[h])
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                self._send(r.status, r.read())
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read())
        except Exception:
            self._send(502, '{"detail":"La API no responde en el puerto 8000. Inicia la aplicacion primero."}'.encode())

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _proxy
    def log_message(self, *a): pass

print("Interfaz lista en http://127.0.0.1:5500  (Ctrl+C para detener)")
ThreadingHTTPServer(("127.0.0.1", 5500), H).serve_forever()
