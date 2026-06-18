"""Clean fixture: a loopback-bound, authenticated app daemon — zero findings.

- bind host is a *variable* (pinned at runtime; default 127.0.0.1) → no L1.
- the handler module shows a constant-time token check + a Host allowlist → no L2.
"""
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer

_TOKEN = "set-at-launch-from-the-workspace-url"
_ALLOWED = ("127.0.0.1", "localhost")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if not hmac.compare_digest(self.headers.get("X-PRM-Token", ""), _TOKEN):
            self.send_response(401)
            self.end_headers()
            return
        if self.headers.get("Host", "").split(":")[0] not in _ALLOWED:
            self.send_response(403)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()


def serve(host: str = "127.0.0.1", port: int = 8770) -> None:
    HTTPServer((host, port), Handler).serve_forever()
