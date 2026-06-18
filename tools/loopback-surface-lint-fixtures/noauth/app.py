"""Advisory fixture (L2, non-gating by default): loopback-bound, but the handler
has no guard of any kind — any other local process can read it. This is the
heuristic the lint reports for triage but does NOT fail CI on, unless --strict."""
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # no guard of any kind — any local process can dial this and read everything
        self.send_response(200)
        self.end_headers()


def serve() -> None:
    HTTPServer(("127.0.0.1", 8770), Handler).serve_forever()
