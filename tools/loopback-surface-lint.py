#!/usr/bin/env python3
# Toolkit-Version: 0.2
"""Loopback-surface lint — the static half of "checked, not asserted" for the one
surface a PNA opens over its *own* data: an app-stood-up HTTP server / local daemon —
candidate AC-PRM-H (RFC; the loopback-surface design note and the AC itself land with their
demonstrator, PRM). This is "Surface 1" of the ways a PNA's private data is reachable on a host.

A local-first PNA that serves its workspace over an HTTP daemon must keep that
surface the app's *own transport*, not an ungoverned tap any other local process
can read. This lint flags two statically-checkable ways that breaks, at two
severities — and the severity split is deliberate (see "Bounded claim" below):

  L1  NON-LOOPBACK BIND  (error — gates) — a server constructed (or a host-ish
      parameter defaulting) to a hardcoded non-loopback literal (`0.0.0.0`, `""`,
      `::`, a public host). The surface is reachable off-device. High confidence:
      a literal bind address is unambiguous. A host passed as a *variable* is NOT
      flagged (it may be pinned at runtime).

  L2  UNAUTHENTICATED HANDLER  (advisory — does not gate by default) — a module
      that defines an HTTP request handler (a `BaseHTTPRequestHandler` subclass, or
      a `do_GET`/`do_POST`/… method) but shows *no* auth guard at all (a
      constant-time token check, a Host allowlist, a session/cookie check). That is
      an app-opened surface any same-host process can dial.

Bounded claim (honest — the soft spot this severity split addresses). L1 is a
high-confidence literal; it gates. L2 is a *heuristic*: it flags the ABSENCE of any
recognized auth signal in a handler module — it can neither prove a present guard
is sufficient (false negative) nor prove an unrecognized guard is missing (false
positive). So L2 is **advisory** by default — it is reported for a human/evaluator
to triage, but does not fail the run, precisely so a heuristic can't rot into
alarm-fatigued noise. A design that wants L2 as a self-regression-guard (its own
gate, where it knows its auth shape) opts in with `--strict`, which promotes L2 to
an error. This is the same posture as the grep-style egress lint: a tripwire, not a
proof of enforcement (that is for the design's tests and LLM/human review).

Scope. Scans Python (`.py`) source — the demonstrated daemon case (PRM). Detecting
non-Python servers (a Node/Go loopback daemon) is a future extension; their absence
from a scan is not a clean bill of health. Vendored / generated / test trees are
skipped.

Output. Human-readable by default (path:line: [L1|L2] message); exit 1 if any L1
(or, with --strict, any L2), else 0 — the CI-friendly contract egress-lint uses.
With --json, emits an object whose `evidence` field conforms to the `evidence`
$def in tools/evaluate-report.schema.json (source=deterministic,
tool=loopback-surface-lint), ready to fold into the matching AC finding of an
evaluate report. suggested_status: non-conformant on any L1; unable-to-determine
when only L2 advisories remain (a heuristic absence, not a proven violation);
conformant when clean.

Usage:
    loopback-surface-lint.py <target-dir> [--strict] [--ext .py,...]
                             [--exclude DIR]... [--ac AC-ID] [--json]
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

DEFAULT_EXTS = {".py"}
DEFAULT_EXCLUDES = {
    ".git", ".venv", "venv", "site-packages", "node_modules", "__pycache__",
    "build", "dist", ".tox", ".mypy_cache", ".pytest_cache", ".eggs", "vendor",
}
DEFAULT_AC = "AC-PRM-H"  # candidate (RFC); a label for the evidence, not a live-table claim.

# "" / "0.0.0.0" / "::" bind every interface — NOT loopback. Anything else that is
# not one of these literals is treated as a non-loopback host and flagged (L1).
LOOPBACK = {"127.0.0.1", "localhost", "::1"}
SERVER_CTORS = {
    "HTTPServer", "ThreadingHTTPServer", "TCPServer", "ThreadingTCPServer",
    "ForkingTCPServer", "UDPServer", "WSGIServer",
}
HANDLER_METHODS = {"do_GET", "do_POST", "do_PUT", "do_DELETE", "do_PATCH", "do_HEAD", "do_OPTIONS"}
HOST_PARAMS = {"host", "bind", "address", "interface", "bind_host", "hostname"}
# A substring whose presence in a handler module is taken as "an auth guard exists".
# Deliberately broad (a tripwire suppressor): the goal is to catch a surface with
# *no* guard at all, not to grade the guard. Broad here ⇒ fewer false positives.
AUTH_SIGNALS = (
    "compare_digest", "host_is_loopback", "origin_is_loopback", "token_ok",
    "auth_token", "x-prm-token", "x-auth", "authorization", "authenticate",
    "samesite", "csrf", "bearer", "verify_token", "_request_token", "session",
    "allowed_hosts", "allowlist", "host allowlist",
)


class Finding:
    __slots__ = ("path", "line", "code", "message")

    def __init__(self, path: str, line: int, code: str, message: str) -> None:
        self.path, self.line, self.code, self.message = path, line, code, message


def _name(func: ast.AST) -> str:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _host_literal(arg: ast.AST) -> str | None:
    """The host string of a ``(host, port)`` bind tuple, when literal; else None."""
    if isinstance(arg, ast.Tuple) and arg.elts:
        head = arg.elts[0]
        if isinstance(head, ast.Constant) and isinstance(head.value, str):
            return head.value
    return None


def _flag_default(arg: ast.arg, default: ast.AST | None, line: int, rel: str, out: list[Finding]) -> None:
    if (default is not None and arg.arg in HOST_PARAMS
            and isinstance(default, ast.Constant) and isinstance(default.value, str)
            and default.value not in LOOPBACK):
        out.append(Finding(rel, line, "L1",
                           f"parameter {arg.arg!r} defaults to non-loopback {default.value!r} — "
                           "a surface bound here is reachable off-device"))


def _check_defaults(node: ast.AST, rel: str, out: list[Finding]) -> None:
    args = node.args
    positional = args.posonlyargs + args.args
    for a, d in zip(positional[len(positional) - len(args.defaults):], args.defaults):
        _flag_default(a, d, node.lineno, rel, out)
    for a, d in zip(args.kwonlyargs, args.kw_defaults):
        _flag_default(a, d, node.lineno, rel, out)


def lint_text(source: str, rel: str) -> list[Finding]:
    """Lint one module's source. Returns its findings (L1 errors, L2 advisories)."""
    out: list[Finding] = []
    try:
        tree = ast.parse(source, filename=rel)
    except SyntaxError as exc:
        return [Finding(rel, exc.lineno or 0, "L0", f"syntax error: {exc.msg}")]

    handlers: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = _name(node.func)
            if (fname in SERVER_CTORS or fname == "bind") and node.args:
                host = _host_literal(node.args[0])
                if host is not None and host not in LOOPBACK:
                    out.append(Finding(rel, node.lineno, "L1",
                        f"{fname} bound to non-loopback host {host!r} — exposes the surface "
                        "off-device (bind 127.0.0.1, or gate a non-loopback host behind an "
                        "explicit, documented opt-out)"))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_defaults(node, rel, out)
        elif isinstance(node, ast.ClassDef):
            base_handler = any(_name(b).endswith("BaseHTTPRequestHandler") for b in node.bases)
            method_handler = any(isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                                 and m.name in HANDLER_METHODS for m in node.body)
            if base_handler or method_handler:
                handlers.append((node.name, node.lineno))

    if handlers and not any(sig in source.lower() for sig in AUTH_SIGNALS):
        name, line = handlers[0]
        out.append(Finding(rel, line, "L2",
            f"HTTP request handler {name!r}, but the module shows no auth guard (token check / "
            "Host allowlist / session) — an unauthenticated app-opened surface other local "
            "processes can read"))
    return out


def iter_files(target: Path, exts: set[str], excludes: set[str]):
    for p in sorted(target.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        parts = set(p.relative_to(target).parts)
        if parts & excludes:
            continue
        if "tests" in parts or p.name.startswith("test_"):
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser(description="Loopback-surface lint — app-opened-transport check (candidate AC-PRM-H).")
    ap.add_argument("target", type=Path, help="Root of the PNA source tree to scan.")
    ap.add_argument("--strict", action="store_true",
                    help="Promote L2 advisories to gating errors (a design's own self-regression guard).")
    ap.add_argument("--ext", default=None, help="Comma-separated extensions to scan (default: .py).")
    ap.add_argument("--exclude", action="append", default=[], metavar="DIR", help="Extra directory name to skip (repeatable).")
    ap.add_argument("--ac", default=DEFAULT_AC, help=f"AC this check bears on (default: {DEFAULT_AC}, candidate).")
    ap.add_argument("--json", action="store_true", help="Emit evaluate-report-compatible evidence JSON.")
    args = ap.parse_args()

    target: Path = args.target
    if not target.is_dir():
        print(f"loopback-surface-lint: target is not a directory: {target}", file=sys.stderr)
        return 2

    exts = {e if e.startswith(".") else "." + e for e in args.ext.split(",")} if args.ext else set(DEFAULT_EXTS)
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)

    findings: list[Finding] = []
    for f in iter_files(target, exts, excludes):
        rel = str(f.relative_to(target))
        try:
            findings.extend(lint_text(f.read_text(encoding="utf-8", errors="replace"), rel))
        except OSError as e:
            print(f"loopback-surface-lint: could not read {rel}: {e}", file=sys.stderr)

    errors = [f for f in findings if f.code in ("L1", "L0")]
    advisories = [f for f in findings if f.code == "L2"]
    gating = errors + (advisories if args.strict else [])

    if args.json:
        if errors:
            status = "non-conformant"
        elif advisories:
            status = "unable-to-determine"  # heuristic absence, not a proven violation
        else:
            status = "conformant"
        detail = (
            "No app-opened loopback surface left unbound/unauthenticated."
            if not findings else
            f"{len(errors)} non-loopback bind(s); {len(advisories)} unauthenticated-handler advisory(ies)."
        )
        citations = [{"path": f.path, "lines": str(f.line), "note": f"[{f.code}] {f.message}"} for f in findings]
        print(json.dumps({
            "tool": "loopback-surface-lint",
            "ac": args.ac,
            "clean": not gating,
            "suggested_status": status,
            "evidence": {"source": "deterministic", "tool": "loopback-surface-lint",
                         "detail": detail, "citations": citations},
        }, indent=2))
        return 1 if gating else 0

    if not findings:
        print("loopback-surface-lint: OK")
        print(f"  scanned {target} (no non-loopback binds; no unauthenticated app-opened handlers)")
        return 0

    if errors:
        print(f"loopback-surface-lint: {len(errors)} error(s) — non-loopback bind (bears on {args.ac}):")
        for f in sorted(errors, key=lambda f: (f.path, f.line)):
            print(f"  - {f.path}:{f.line}: [{f.code}] {f.message}")
    if advisories:
        label = "error(s)" if args.strict else "advisory(ies)"
        print(f"loopback-surface-lint: {len(advisories)} {label} — unauthenticated handler"
              f"{' (--strict: gating)' if args.strict else ' (advisory — triage; not gating without --strict)'}:")
        for f in sorted(advisories, key=lambda f: (f.path, f.line)):
            print(f"  - {f.path}:{f.line}: [{f.code}] {f.message}")

    return 1 if gating else 0


if __name__ == "__main__":
    sys.exit(main())
