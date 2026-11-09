"""Mide ms por cuadro con reloj real a 1920x1080 (px=4). Uso: python medir.py [shot ...]
Necesita el server del juego en el 5331 (abrir.cmd o preview)."""
import http.server, subprocess, sys, threading
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 5332
got = []
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        got.append(self.rfile.read(int(self.headers['Content-Length'])).decode())
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Headers', '*'); self.end_headers()
    def log_message(self, *a): pass
srv = http.server.HTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
for n in sys.argv[1:] or ['1', '2', '3']:
    got.clear()
    p = subprocess.Popen([CHROME, '--headless=new', '--enable-gpu', '--use-angle=d3d11', '--ignore-gpu-blocklist',
        '--window-size=1920,1080', f'http://localhost:5331/?shot={n}&ui=0&px=4&bench={PORT}'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time; t = time.time()
    while not got and time.time() - t < 90: time.sleep(.2)
    subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
    print(f'cuadro {n}:', got[0] if got else 'sin respuesta')
