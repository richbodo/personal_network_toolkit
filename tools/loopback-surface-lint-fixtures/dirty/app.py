"""Dirty fixture (L1, gating): the daemon binds every interface — reachable
off-device. A literal non-loopback bind is the high-confidence error that gates."""
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()


def serve() -> None:
    # L1: 0.0.0.0 binds every interface — not loopback.
    HTTPServer(("0.0.0.0", 8770), Handler).serve_forever()
