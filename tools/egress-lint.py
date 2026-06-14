#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""Egress lint — deterministic private-data-sovereignty check (Goal 3 / AC-1).

Scans a PNA's source tree for *egress vectors*: code or markup that can send a
request to a remote origin (and therefore could carry private data off-device).
Any remote origin that is not on the design's allow-list is a violation.

This is intentionally narrow. It is NOT a general test runner — it guards the one
violation that most destroys trust (private data leaving the device) and that an
LLM scanning a large tree might miss. It is a *complement* to the LLM
architectural review described in pna-build-eval-contrib/SKILL.md, not a
replacement; it is heuristic (regex over source) and can have false positives,
which the allow-list and per-line output let a human triage quickly.

Vectors detected:
  JS/TS  : fetch(), XMLHttpRequest.open(), navigator.sendBeacon(),
           new WebSocket(), new EventSource(), importScripts(), dynamic import(),
           axios(...), $.get/$.post/$.ajax/$.getJSON(...)
  HTML   : src= (img/script/iframe/video/audio/source/embed),
           <form action=>, <object data=>, <link ... href=> (stylesheet/preload),
           <use href=>/<use xlink:href=> (SVG)
           — <a href> is navigation, not data egress, and is NOT flagged.

What counts as local (never flagged): relative URLs, same-origin/root-relative
paths, fragments, data:/blob:/about: URIs, mailto:/tel: (comms, not data egress),
and localhost / 127.0.0.1 / [::1] / 0.0.0.0. Everything else absolute is remote
and must be on the allow-list.

Allow-list. Remote origins a design legitimately talks to (per its axis flavor —
e.g. the auth + bundle origin for distribution:web-bundle-with-magic-link) are
declared in `<target>/egress-allow.json` and/or passed with --allow. Format:

    {
      "ac": "AC-1",
      "allow": [
        {"origin": "https://fellows.example.org",
         "reason": "distribution:web-bundle-with-magic-link — shared bundle + auth origin"}
      ]
    }

("allow" entries may also be bare origin strings.)

Output. Human-readable by default (path:line: [vector] url), exit 1 on any
violation, exit 0 if clean — same CI-friendly contract as lint-spec-ids.py.
With --json, emits an object whose `evidence` field conforms to the `evidence`
$def in tools/evaluate-report.schema.json (source=deterministic, tool=egress-lint),
ready to fold into the matching AC finding of an evaluate report.

Usage:
    egress-lint.py <target-dir> [--allow ORIGIN]... [--config PATH]
                    [--ac AC-ID] [--ext .js,.html,...] [--exclude DIR]... [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_EXTS = {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".html", ".htm", ".vue", ".svelte"}
DEFAULT_EXCLUDES = {".git", "node_modules", "dist", "build", "out", "vendor", ".next", "coverage", "__pycache__"}
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"}
NON_EGRESS_SCHEMES = {"data", "blob", "about", "mailto", "tel", "javascript", "#"}
DEFAULT_AC = "AC-1"

# (name, regex). The URL is capture group 1.
VECTORS: list[tuple[str, re.Pattern[str]]] = [
    ("fetch",         re.compile(r"""\bfetch\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("xhr.open",      re.compile(r"""\.open\s*\(\s*['"][A-Za-z]+['"]\s*,\s*['"`]([^'"`]+)['"`]""")),
    ("sendBeacon",    re.compile(r"""sendBeacon\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("WebSocket",     re.compile(r"""new\s+WebSocket\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("EventSource",   re.compile(r"""new\s+EventSource\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("importScripts", re.compile(r"""importScripts\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("import()",      re.compile(r"""(?<![.\w])import\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("axios",         re.compile(r"""\baxios\s*(?:\.\w+)?\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("jquery.ajax",   re.compile(r"""\$\.(?:get|post|ajax|getJSON)\s*\(\s*['"`]([^'"`]+)['"`]""")),
    ("html.src",      re.compile(r"""<(?:img|script|iframe|video|audio|source|embed)\b[^>]*?\bsrc\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE | re.DOTALL)),
    ("html.action",   re.compile(r"""<form\b[^>]*?\baction\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE | re.DOTALL)),
    ("html.object",   re.compile(r"""<object\b[^>]*?\bdata\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE | re.DOTALL)),
    ("html.link",     re.compile(r"""<link\b[^>]*?\bhref\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE | re.DOTALL)),
    ("svg.use",       re.compile(r"""<use\b[^>]*?\b(?:xlink:)?href\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE | re.DOTALL)),
]


class Violation:
    __slots__ = ("path", "line", "vector", "url")

    def __init__(self, path: str, line: int, vector: str, url: str) -> None:
        self.path, self.line, self.vector, self.url = path, line, vector, url


def normalize_origin(value: str) -> str:
    """Reduce an allow entry or URL to a comparable scheme://host[:port] origin."""
    p = urlparse(value if "//" in value else "//" + value, scheme="https")
    host = (p.hostname or "").lower()
    if not host:
        return value.lower().rstrip("/")
    origin = f"{p.scheme}://{host}"
    if p.port:
        origin += f":{p.port}"
    return origin


def classify(url: str, allow: set[str]) -> str:
    """Return 'local', 'allowed', or 'remote' for a URL string."""
    u = url.strip()
    if not u:
        return "local"
    scheme = u.split(":", 1)[0].lower() if ":" in u.split("/", 1)[0] else ""
    if u.startswith("#") or scheme in NON_EGRESS_SCHEMES:
        return "local"
    # Protocol-relative (//host/..) is remote; root-relative (/path) and bare
    # relative paths are local.
    if not u.startswith("//") and "://" not in u:
        return "local"
    p = urlparse(u if "://" in u else "https:" + u)
    host = (p.hostname or "").lower()
    if not host or host in LOCAL_HOSTS:
        return "local"
    origin = normalize_origin(u)
    if origin in allow or host in allow:
        return "allowed"
    return "remote"


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def scan_text(text: str, rel: str, allow: set[str]) -> list[Violation]:
    out: list[Violation] = []
    for name, rx in VECTORS:
        for m in rx.finditer(text):
            url = m.group(1)
            if classify(url, allow) == "remote":
                out.append(Violation(rel, line_of(text, m.start(1)), name, url))
    return out


def load_allow(target: Path, config: Path | None, cli_allows: list[str], cli_ac: str | None) -> tuple[set[str], str]:
    allow: set[str] = set()
    ac = cli_ac or DEFAULT_AC
    cfg_path = config or (target / "egress-allow.json")
    if cfg_path.exists():
        data = json.loads(cfg_path.read_text())
        if not cli_ac and isinstance(data.get("ac"), str):
            ac = data["ac"]
        for entry in data.get("allow", []):
            origin = entry["origin"] if isinstance(entry, dict) else entry
            allow.add(normalize_origin(origin))
    for a in cli_allows:
        allow.add(normalize_origin(a))
    return allow, ac


def iter_files(target: Path, exts: set[str], excludes: set[str]):
    for p in sorted(target.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if any(part in excludes for part in p.relative_to(target).parts):
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser(description="Egress lint — private-data-sovereignty check (AC-1).")
    ap.add_argument("target", type=Path, help="Root of the PNA source tree to scan.")
    ap.add_argument("--allow", action="append", default=[], metavar="ORIGIN", help="Allow a remote origin (repeatable).")
    ap.add_argument("--config", type=Path, default=None, help="Allow-list JSON (default: <target>/egress-allow.json).")
    ap.add_argument("--ac", default=None, help=f"AC this check bears on (default: config's ac, else {DEFAULT_AC}).")
    ap.add_argument("--ext", default=None, help="Comma-separated extensions to scan (overrides defaults).")
    ap.add_argument("--exclude", action="append", default=[], metavar="DIR", help="Extra directory name to skip (repeatable).")
    ap.add_argument("--json", action="store_true", help="Emit evaluate-report-compatible evidence JSON.")
    args = ap.parse_args()

    target: Path = args.target
    if not target.is_dir():
        print(f"egress-lint: target is not a directory: {target}", file=sys.stderr)
        return 2

    exts = {e if e.startswith(".") else "." + e for e in args.ext.split(",")} if args.ext else set(DEFAULT_EXTS)
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
    allow, ac = load_allow(target, args.config, args.allow, args.ac)

    violations: list[Violation] = []
    for f in iter_files(target, exts, excludes):
        rel = str(f.relative_to(target))
        try:
            violations.extend(scan_text(f.read_text(encoding="utf-8", errors="replace"), rel, allow))
        except OSError as e:
            print(f"egress-lint: could not read {rel}: {e}", file=sys.stderr)

    if args.json:
        citations = [{"path": v.path, "lines": str(v.line), "note": f"{v.vector} -> {v.url}"} for v in violations]
        clean = not violations
        detail = (
            "No unsanctioned egress vectors found; all remote origins are allow-listed."
            if clean else
            f"{len(violations)} unsanctioned egress vector(s) to non-allow-listed remote origin(s)."
        )
        print(json.dumps({
            "tool": "egress-lint",
            "ac": ac,
            "clean": clean,
            "suggested_status": "conformant" if clean else "non-conformant",
            "evidence": {"source": "deterministic", "tool": "egress-lint", "detail": detail, "citations": citations},
        }, indent=2))
        return 0 if clean else 1

    if not violations:
        print("egress-lint: OK")
        print(f"  scanned {target} (no unsanctioned egress; {len(allow)} allow-listed origin(s))")
        return 0

    print(f"egress-lint: {len(violations)} unsanctioned egress vector(s) found (bears on {ac}):")
    for v in sorted(violations, key=lambda v: (v.path, v.line)):
        print(f"  - {v.path}:{v.line}: [{v.vector}] {v.url}")
    print("\nIf an origin above is legitimate for this design's flavor, add it to")
    print("egress-allow.json (with a reason naming the axis pick that justifies it).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
