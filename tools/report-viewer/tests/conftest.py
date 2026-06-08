"""Pytest fixtures for the Visual Validator viewer's browser-render tests.

OPT-IN, browser-based suite — **not** part of `just ci` (which stays stdlib-only
`python3`). See plans/viewer-e2e-testing-plan.md and CLAUDE.md § Conventions.

Serves `tools/report-viewer/` with a stdlib `http.server` on a dedicated port
(8791 — distinct from fellows 8765 / PRM 8770, so all three can run on one host)
so `index.html` can `fetch()` its sibling `sample-reports/*.json`; tests then drive
it with Playwright (the `page` fixture from pytest-playwright).

Set `VIEWER_BASE_URL=https://…` to test a deployed copy instead of the local server.
"""
from __future__ import annotations

import functools
import http.server
import os
import subprocess
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

VIEWER_DIR = Path(__file__).resolve().parents[1]  # tools/report-viewer/
PORT = int(os.environ.get("VIEWER_TEST_PORT", "8791"))


def _free_port(port: int) -> None:
    """Best-effort: kill whatever holds the port (clean re-runs; mirrors fellows)."""
    try:
        out = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True, timeout=2)
    except (FileNotFoundError, subprocess.SubprocessError):
        return
    for pid in (out.stdout or "").split():
        if pid.isdigit():
            subprocess.run(["kill", "-9", pid], capture_output=True, timeout=2)
            time.sleep(0.2)


def _wait_for_server(port: int, attempts: int = 30) -> bool:
    for _ in range(attempts):
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=1)
            conn.request("GET", "/index.html")
            resp = conn.getresponse()
            resp.read()
            conn.close()
            if resp.status == 200:
                return True
        except OSError:
            pass
        time.sleep(0.2)
    return False


@pytest.fixture(scope="session", autouse=True)
def static_server():
    if (os.environ.get("VIEWER_BASE_URL") or "").strip():
        yield  # testing a remote/served origin — don't start a local server
        return
    _free_port(PORT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(VIEWER_DIR))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    if not _wait_for_server(PORT):
        httpd.shutdown()
        raise RuntimeError(f"viewer test server did not come up on port {PORT}")
    yield
    httpd.shutdown()


@pytest.fixture(scope="session")
def viewer_url() -> str:
    env = (os.environ.get("VIEWER_BASE_URL") or "").strip().rstrip("/")
    return env or f"http://127.0.0.1:{PORT}"
