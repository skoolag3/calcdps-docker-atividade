from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

HOST = "0.0.0.0"
PORT = 8000

class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        damage = float(params.get("damage", ["100"])[0])
        attacks = float(params.get("attacks", ["1"])[0])
        crit = float(params.get("crit", ["0"])[0])
        dps = damage * attacks * (1 + crit / 100)

        payload = {
            "damage": damage,
            "attacks_per_second": attacks,
            "critical_bonus_percent": crit,
            "dps": round(dps, 2),
        }
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args), flush=True)

if __name__ == "__main__":
    print(f"Calculadora DPS disponível em http://{HOST}:{PORT}", flush=True)
    HTTPServer((HOST, PORT), CalculatorHandler).serve_forever()
