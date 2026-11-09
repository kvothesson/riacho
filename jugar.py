"""Juega Riacho de punta a punta con el piloto automático y muestra los eventos.
Uso: python jugar.py [lento]   (lento: avanza a los tirones, para que lo alcancen las luces malas)"""
import http.server, json, random, subprocess, sys, threading, time
RUN = str(random.randrange(10**9))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 5333
evs = []
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        e = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if e.pop('run', None) != RUN: return self._ok()
        if not (e['ev'] == 'fin' and any(x['ev'] == 'fin' for x in evs)):
            evs.append(e); print(e, flush=True)
        self._ok()
    def _ok(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
    def log_message(self, *a): pass
srv = http.server.HTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
extra = '&lento=1' if 'lento' in sys.argv else ''
p = subprocess.Popen([CHROME, '--headless=new', '--enable-gpu', '--use-angle=d3d11', '--ignore-gpu-blocklist', '--window-size=1280,720',
    f'http://localhost:5331/?bot={PORT}&run={RUN}&mute=1{extra}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t = time.time()
while time.time() - t < 420 and not any(e['ev'] == 'fin' for e in evs): time.sleep(.5)
subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
print('TERMINÓ' if any(e['ev'] == 'fin' for e in evs) else 'NO LLEGÓ AL FINAL', f'({time.time()-t:.0f} s)')
