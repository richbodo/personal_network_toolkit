#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""Self-tests for PNT's deterministic lints (Tier A of the conformance suite).

Why this exists: a lint with no test silently rots. PR #18 review found the
exceptions.md `Reversible:`/`Reversal:` check had been *fully dead* (it matched
nothing, and its coupling test was satisfied by unrelated prose) — green the
whole time, enforcing nothing. This harness pins each lint's behavior so that
can't recur: it asserts the clean tree passes, then applies a catalog of named
fault injections and asserts each one makes the right lint fail with the
expected message.

Mechanism: copy the repo to a tempdir, mutate one file in the copy, run the
lint *from the copy* (the lints resolve their repo root from their own __file__
location), and check the exit code + message. Stdlib only — no pytest, no `just`,
so CI runs it with a bare `python3`.

Run:  python3 tools/tests/lint_selftest.py   (or `just test`)
Exit: 0 if every case behaves as expected, 1 otherwise.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".pytest_cache")


def _run(root: Path, rel_script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(root / rel_script), *args],
        capture_output=True, text=True, cwd=str(root),
    )


# --- Fault-injection cases against lint-spec-ids.py ----------------------------
# Each: a unique substring to find-and-replace in one file, and a fragment of the
# message the lint MUST emit in response. `old` is asserted present first, so a
# case that goes stale (because the spec wording moved) fails loudly instead of
# silently passing.
SPEC_ID_FAULTS = [
    dict(
        name="constraints: registry-table Detectability cell is garbage",
        file="spec/constraints.md",
        old="| AC-1, Goal-4 | Open | feature-detect |",
        new="| AC-1, Goal-4 | Open | totally-made-up |",
        expect="Detectability",
    ),
    dict(
        name="constraints: cross-axis Triggered-by (opfs pick under comms axis)",
        file="spec/constraints.md",
        old="**Triggered-by:** storage:opfs-sqlite-wasm",
        new="**Triggered-by:** comms:opfs-sqlite-wasm",
        expect="not a pick of the named axis",
    ),
    dict(
        name="constraints: detail block with no registry-table row (typo'd heading)",
        file="spec/constraints.md",
        old="### CST-PWA-NO-SYNC ",
        new="### CST-PWA-NO-SYNCC ",
        expect="no registry-table row",
    ),
    dict(
        name="constraints: Bounds names a nonexistent AC",
        file="spec/constraints.md",
        old="**Bounds:** AC-1, Goal-4, AC-MCP-A",
        new="**Bounds:** AC-1, Goal-4, AC-999",
        expect="not a known AC",
    ),
    dict(
        name="exceptions: Reversible: yes but no Reversal: field (the rot from PR #18)",
        file="spec/exceptions.md",
        old="**Reversal:**",
        new="**Reversalx:**",
        expect="no 'Reversal:' field",
    ),
    dict(
        name="exceptions: malformed Reversible value",
        file="spec/exceptions.md",
        old="**Reversible:** yes",
        new="**Reversible:** maybe",
        expect="malformed 'Reversible:",
    ),
    dict(
        name="contract: Realizes names an AC the spec doesn't define",
        file="contracts/private-db.schema.sql",
        old="Realizes: AC-1, AC-9",
        new="Realizes: AC-1, AC-999",
        expect="AC-999",
    ),
    dict(
        name="version: an artifact's Toolkit-Version drifts from /VERSION",
        file="spec/constraints.md",
        old="**Toolkit-Version:** 0.1 (draft)",
        new="**Toolkit-Version:** 0.2 (draft)",
        expect="Toolkit-Version",
    ),
    dict(
        name="manifest: [flavor] names a pick the axis doesn't define",
        file="reference_designs/fellows_local_db/design.toml",
        old='storage = "opfs-sqlite-wasm"',
        new='storage = "bogus-pick"',
        expect="not a pick of that axis",
    ),
    dict(
        name="manifest: [flavor] names an unknown axis",
        file="reference_designs/fellows_local_db/design.toml",
        old='distribution = "web-bundle-with-magic-link"',
        new='dist = "web-bundle-with-magic-link"',
        expect="unknown axis",
    ),
    dict(
        name="manifest: status outside the fixed vocabulary",
        file="reference_designs/fellows_local_db/design.toml",
        old='status = "active"',
        new='status = "live"',
        expect="status 'live' not one of",
    ),
    dict(
        name="manifest: archived design without its SWHID pin (honest-deferral)",
        file="reference_designs/fellows_local_db/design.toml",
        old='archival = "pending"',
        new='archival = "archived"',
        expect="requires 'commit'",
    ),
    dict(
        name="manifest: malformed SWHID value",
        file="reference_designs/fellows_local_db/design.toml",
        old='swhid_dir = ""     # TODO(maintainer): swh:1:dir:<tree>',
        new='swhid_dir = "swh:1:dir:not-a-real-hash"',
        expect="malformed",
    ),
]


def case_clean(results: list) -> None:
    """The clean tree must pass lint-spec-ids."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "repo"
        shutil.copytree(REPO, root, ignore=IGNORE)
        cp = _run(root, "tools/lint-spec-ids.py")
        ok = cp.returncode == 0
        _record(results, "clean tree passes lint-spec-ids", ok,
                "" if ok else cp.stdout + cp.stderr)


def case_fault(results: list, fault: dict) -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "repo"
        shutil.copytree(REPO, root, ignore=IGNORE)
        target = root / fault["file"]
        text = target.read_text()
        if fault["old"] not in text:
            _record(results, fault["name"], False,
                    f"STALE TEST: {fault['old']!r} not found in {fault['file']}")
            return
        target.write_text(text.replace(fault["old"], fault["new"]))
        cp = _run(root, "tools/lint-spec-ids.py")
        out = cp.stdout + cp.stderr
        ok = cp.returncode != 0 and fault["expect"] in out
        detail = ("" if ok else
                  f"exit={cp.returncode}, expected message {fault['expect']!r} in:\n{out}")
        _record(results, fault["name"], ok, detail)


def case_fixture_lint(results: list, script: str, clean: str, dirty: str) -> None:
    """A fixture-based lint (egress / export-readable): clean → 0, dirty → 1."""
    c = _run(REPO, script, clean)
    _record(results, f"{script}: clean fixture passes", c.returncode == 0,
            "" if c.returncode == 0 else c.stdout + c.stderr)
    d = _run(REPO, script, dirty)
    _record(results, f"{script}: dirty fixture fails", d.returncode != 0,
            "" if d.returncode != 0 else "dirty fixture was not flagged")


def case_attestation_marker_message(results: list) -> None:
    """Pin the marker-state behavior specifically: the dirty fixture must fail
    *because* a conformant row cites an xfail test (not just exit non-zero for
    some other reason). This is the seam the lint exists to close, so its
    message is asserted, not just the exit code."""
    d = _run(REPO, "tools/attestation-evidence-lint.py",
             "tools/attestation-evidence-lint-fixtures/dirty")
    out = d.stdout + d.stderr
    ok = d.returncode != 0 and "xfail" in out and "not evidence" in out
    _record(results, "attestation-evidence-lint: flags xfail test as non-evidence",
            ok, "" if ok else f"exit={d.returncode}, missing xfail message in:\n{out}")


def _record(results: list, name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok and detail:
        print("        " + detail.replace("\n", "\n        "))


def main() -> int:
    print("lint self-tests (Tier A):")
    results: list = []

    case_clean(results)
    for fault in SPEC_ID_FAULTS:
        case_fault(results, fault)
    case_fixture_lint(results, "tools/egress-lint.py",
                      "tools/egress-lint-fixtures/clean",
                      "tools/egress-lint-fixtures/dirty")
    case_fixture_lint(results, "tools/export-readable-lint.py",
                      "tools/export-readable-lint-fixtures/clean",
                      "tools/export-readable-lint-fixtures/dirty")
    case_fixture_lint(results, "tools/attestation-evidence-lint.py",
                      "tools/attestation-evidence-lint-fixtures/clean",
                      "tools/attestation-evidence-lint-fixtures/dirty")
    case_attestation_marker_message(results)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"\nlint-selftest: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
