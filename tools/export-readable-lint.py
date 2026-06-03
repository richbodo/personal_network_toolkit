#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""Export-readability lint — deterministic PR-6 check (Goal 4 / PR-6).

Verifies that a PNA's human-readable Private-DB export is actually readable
*without any PNA tooling*. PR-6 (see spec/PNA_Spec.md § Sub-contracts per slot →
Private schema) says implementations SHOULD ship a flat, human-readable export
of the Private DB *in addition to* the canonical SQLite file, and that the
export MUST be readable with a generic CSV / JSON / Markdown reader.

The "Long Now" gap this guards: owning the bytes is not the same as being able
to read them. "Your data is in a SQLite file" fails for any user without a
SQLite-capable tool on hand. This lint operationalizes "readable without PNA
tooling" mechanically: every file in the export must parse with a Python
*standard-library* reader (csv / json) or be plain UTF-8 text (Markdown / txt),
and require no project code. A canonical `.sqlite` binary in the export dir is
the textbook failure — it is exactly the tooling-dependent form PR-6 exists to
complement.

This is intentionally narrow, like egress-lint.py: it checks tool-free
readability, not schema correctness or completeness (whether the export
contains every row is the reference design's own test). It is the deterministic
half of PR-6's verification; an LLM/human can judge whether the export is
*useful*, but this proves it is *openable*.

Recognized tool-free formats (by extension, all parsed with stdlib only):
  .csv, .tsv   -> csv.reader must consume it as UTF-8
  .json        -> json.loads must succeed
  .md, .markdown, .txt -> must decode as UTF-8 text

Anything else in the export tree is a violation. A binary file (fails UTF-8
decode) is a violation regardless of extension. An empty file is a violation.
An export with no recognized, non-empty file at all is a violation (PR-6 wants
an actual export, not an empty directory).

Output. Human-readable by default (path: reason), exit 1 on any violation,
exit 0 if clean — the same CI-friendly contract as egress-lint.py and
lint-spec-ids.py. With --json, emits an object whose `evidence` field conforms
to the `evidence` $def in tools/evaluate-report.schema.json
(source=deterministic, tool=export-readable-lint), ready to fold into the PR-6
finding of an evaluate report.

Usage:
    export-readable-lint.py <export-dir-or-file> [--exclude DIR]... [--json]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

AC = "PR-6"

# Extensions we accept as tool-free human-readable, grouped by how we validate.
JSON_EXTS = {".json"}
CSV_EXTS = {".csv", ".tsv"}
TEXT_EXTS = {".md", ".markdown", ".txt"}
RECOGNIZED = JSON_EXTS | CSV_EXTS | TEXT_EXTS

# Canonical-store extensions worth a pointed message when found in an export.
SQLITE_EXTS = {".sqlite", ".sqlite3", ".db", ".sqlite-wal", ".sqlite-shm", ".db-wal", ".db-shm"}

DEFAULT_EXCLUDES = {".git", "node_modules", "__pycache__", ".DS_Store"}


@dataclass
class Violation:
    path: str
    reason: str


def iter_files(target: Path, excludes: set[str]):
    if target.is_file():
        yield target
        return
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        if any(part in excludes for part in p.relative_to(target).parts):
            continue
        if p.name in excludes:
            continue
        yield p


def check_file(path: Path, rel: str) -> Violation | None:
    """Return a Violation if `path` is not tool-free human-readable, else None."""
    suffix = path.suffix.lower()

    if suffix not in RECOGNIZED:
        if suffix in SQLITE_EXTS:
            return Violation(rel, "canonical SQLite store, not a tool-free export — "
                                  "PR-6 wants a human-readable export *in addition to* it")
        return Violation(rel, f"unrecognized format '{suffix or '(none)'}' — "
                              f"not a generic CSV/JSON/Markdown reader can open it")

    try:
        raw = path.read_bytes()
    except OSError as e:
        return Violation(rel, f"could not read: {e}")

    if not raw.strip():
        return Violation(rel, "empty file — no exported data")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return Violation(rel, "not valid UTF-8 text — requires non-text tooling to read")

    if suffix in JSON_EXTS:
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            return Violation(rel, f"does not parse as JSON with the stdlib reader: {e}")
    elif suffix in CSV_EXTS:
        delimiter = "\t" if suffix == ".tsv" else ","
        try:
            rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
        except csv.Error as e:
            return Violation(rel, f"does not parse as CSV with the stdlib reader: {e}")
        if not any(any(cell.strip() for cell in row) for row in rows):
            return Violation(rel, "no rows — empty CSV export")
    # TEXT_EXTS: a successful UTF-8 decode is the whole check.
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Export-readability lint — PR-6 tool-free-export check (Goal 4).")
    ap.add_argument("target", type=Path, help="The human-readable export directory (or a single export file).")
    ap.add_argument("--exclude", action="append", default=[], metavar="DIR",
                    help="Extra directory or file name to skip (repeatable).")
    ap.add_argument("--json", action="store_true", help="Emit evaluate-report-compatible evidence JSON.")
    args = ap.parse_args()

    target: Path = args.target
    if not target.exists():
        print(f"export-readable-lint: target does not exist: {target}", file=sys.stderr)
        return 2

    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)

    violations: list[Violation] = []
    recognized_nonempty = 0
    for f in iter_files(target, excludes):
        rel = str(f.relative_to(target)) if target.is_dir() else f.name
        v = check_file(f, rel)
        if v is not None:
            violations.append(v)
        elif f.suffix.lower() in RECOGNIZED:
            recognized_nonempty += 1

    if recognized_nonempty == 0 and not violations:
        violations.append(Violation(str(target), "no human-readable export found "
                                                  "(no non-empty CSV/JSON/Markdown file)"))

    clean = not violations

    if args.json:
        detail = (
            f"every exported file parses with a stdlib reader; {recognized_nonempty} readable file(s)."
            if clean else
            f"{len(violations)} file(s) not readable without PNA tooling."
        )
        citations = [{"path": v.path, "lines": "", "note": v.reason} for v in violations]
        print(json.dumps({
            "tool": "export-readable-lint",
            "ac": AC,
            "clean": clean,
            "suggested_status": "conformant" if clean else "non-conformant",
            "evidence": {"source": "deterministic", "tool": "export-readable-lint",
                         "detail": detail, "citations": citations},
        }, indent=2))
        return 0 if clean else 1

    if clean:
        print("export-readable-lint: OK")
        print(f"  {target}: {recognized_nonempty} tool-free file(s); export is readable without PNA tooling")
        return 0

    print(f"export-readable-lint: {len(violations)} file(s) not readable without PNA tooling (bears on {AC}):")
    for v in sorted(violations, key=lambda v: v.path):
        print(f"  - {v.path}: {v.reason}")
    print("\nPR-6 wants a flat, human-readable export (CSV per table, schema-embedded JSON,")
    print("or a Markdown vault) *in addition to* the canonical SQLite file — openable with")
    print("no PNA tooling. See spec/PNA_Spec.md § Private schema (PR-6).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
