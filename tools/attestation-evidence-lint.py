#!/usr/bin/env python3
# Toolkit-Version: 0.2
"""Attestation-evidence lint — the AC/CST attestation table is a Security Target,
and a `conformant` claim with no executable evidence is a finding.

This is the portable reference implementation the
`reference_designs/templates/ARCHITECTURE_TEMPLATE.md` "Mechanical check" note
points at. A design copies it into its own repo and runs it against its own
Architecture document + test tree (the toolkit runs it here only against fixtures —
it hosts no application code). It is the deterministic half of the evaluate
flow's "confirm the named test exists **and passes**" step: a static lint can
prove the cited test *exists and is a live, non-deferred assertion*; whether it
actually *passes* is the runtime/CI layer this lint cannot see (run the suite).

For every attestation row whose Status is `conformant` (and not `partial`), it
requires either:
  - a resolvable test ref `path/to/test.py[::name]` — the file exists (relative
    to the design root, or by unique basename), and if `::name` is given a
    `def`/`class name` exists — that is NOT decorated `xfail` or an
    unconditional `skip`; or
  - an explicitly declared non-test verification kind (human-review / LLM rubric
    / code inspection / by architecture / by bounding / by construction).

Two failure modes it catches that a bare existence check does not:
  1. **Doc-only evidence.** A `*.md` pointer asserts a property; it does not
     prove it. A `conformant` row whose only Verification is a doc fails.
  2. **Known-false / unrun evidence.** A `conformant` row may not cite an
     `xfail` test (a *declared-false* invariant) or an unconditional `skip`
     (a *declared-never-run* one). This closes the exact seam where a reference
     design cited an `xfail(strict=True)` test as proof of conformance and every
     gate stayed green. A conditional `skipif(cond)` is deliberately exempt —
     it's a legitimate environment guard that runs in real CI; whether it ran is
     a runtime fact, not a static one.

Marker detection covers per-test and per-class decorators and a module-level
`pytestmark = …` global (so a deferred test can't dodge the rule by hoisting its
marker out of the decorator). Per-parameter `parametrize(marks=…)` is not
separately resolved — cite the specific deferred test, not a parametrized
umbrella. `partial` / `Open` / `not-applicable` rows are exempt from resolution
— they carry an honest, non-conformant status by design.

Output: human-readable (row: reason), exit 1 on any finding, exit 0 if clean —
the same CI contract as egress-lint.py / export-readable-lint.py. With --json,
emits an evaluate-report-compatible `evidence` object (source=deterministic,
tool=attestation-evidence-lint).

Usage:
    attestation-evidence-lint.py [design-root]        # default: cwd
    attestation-evidence-lint.py . --arch docs/Architecture.md
    attestation-evidence-lint.py <root> --json
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Declared non-test verification kinds (case-insensitive substring match).
REVIEW_KINDS = (
    "human-review", "human review", "llm rubric", "code inspection",
    "by architecture", "by bounding", "by construction", "architectural",
)

# A path-like Python ref, optionally `::name`. The leading boundary stops it
# matching mid-token (e.g. the `deploy` inside `test_deploy_*`).
TEST_REF = re.compile(r"(?<![\w./-])[\w./-]+\.py(?:::\w+)?")

# Markers that *statically* disqualify a cited test as evidence: `xfail` is a
# declared-false invariant; an unconditional `skip` is a declared-never-run one.
# `skipif` is intentionally absent (exact attr compare below), so a conditional
# environment guard is left alone.
DISQUALIFYING_MARKERS = ("xfail", "skip")

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv"}

DEFAULT_ARCH_CANDIDATES = ("Architecture.md", "docs/Architecture.md")


@dataclass
class Finding:
    row: str
    reason: str


# --- markdown attestation parsing --------------------------------------------

def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", line)) and "-" in line


def parse_attestation_rows(md_text: str):
    """Yield (row_id, verification_cell, status_cell) for every data row of every
    table that has both a 'Verification' and a 'Status' column header."""
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            header = [h.lower() for h in split_row(line)]
            if "verification" in header and "status" in header:
                v_idx, s_idx = header.index("verification"), header.index("status")
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|") and not is_separator(lines[j]):
                    cells = split_row(lines[j])
                    if len(cells) > max(v_idx, s_idx):
                        yield cells[0], cells[v_idx], cells[s_idx]
                    j += 1
                i = j
                continue
        i += 1


def is_full_conformant(status_cell: str) -> bool:
    # "non-conformant" / "not conformant" both *contain* "conformant" — exclude
    # them explicitly so a genuinely non-conformant row isn't treated as a
    # conformant claim and dunned for missing evidence.
    s = status_cell.lower()
    return ("conformant" in s and "partial" not in s
            and "non-conformant" not in s and "not conformant" not in s)


# --- test-ref resolution + marker detection ----------------------------------

def build_py_index(root: Path) -> dict:
    """basename -> [absolute paths] for every .py under root (built once)."""
    index: dict = {}
    for p in root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
            continue
        index.setdefault(p.name, []).append(p)
    return index


def resolve_candidates(ref_path: str, root: Path, py_index: dict) -> list[Path]:
    if "/" in ref_path:
        cand = root / ref_path
        return [cand] if cand.is_file() else []
    return list(py_index.get(Path(ref_path).name, []))


def _marker_names(decorator: ast.AST):
    for node in ast.walk(decorator):
        if isinstance(node, ast.Attribute):
            yield node.attr
        elif isinstance(node, ast.Name):
            yield node.id


def _module_marker_hits(tree: ast.Module) -> set:
    """Disqualifying markers applied to *every* test in a file via a module-level
    `pytestmark = …` global — the common way to xfail/skip a whole file without a
    per-def decorator, and an easy way to slip a deferred test past a
    decorator-only check. Same exact-name match as `_marker_names`, so a
    conditional `skipif` global stays exempt."""
    hits: set = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
            hits |= set(_marker_names(node.value)) & set(DISQUALIFYING_MARKERS)
    return hits


def _named_nodes(tree: ast.Module, name: str):
    """Yield (enclosing_class_or_None, node) for every top-level or one-level-
    nested def/class named `name`."""
    defs = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    for node in tree.body:
        if isinstance(node, defs) and node.name == name:
            yield None, node
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, defs) and child.name == name:
                    yield node, child


def classify_ref(ref: str, root: Path, py_index: dict):
    """Return (status, detail) where status is 'live' | 'xfail' | 'skip' |
    'dangling'. 'live' = resolves and carries no disqualifying static marker."""
    ref_path, _, name = ref.partition("::")
    cands = resolve_candidates(ref_path, root, py_index)
    if not cands:
        return "dangling", f"file {ref_path!r} not found under the design root"
    if not name:
        return "live", ""
    found_def = False
    for c in cands:
        try:
            tree = ast.parse(c.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        module_hits = _module_marker_hits(tree)  # pytestmark applies file-wide
        for class_node, fn in _named_nodes(tree, name):
            found_def = True
            decos = list(fn.decorator_list)
            if class_node is not None:
                decos += list(class_node.decorator_list)
            hits = set(module_hits)
            for d in decos:
                hits |= set(_marker_names(d)) & set(DISQUALIFYING_MARKERS)
            if hits:
                return sorted(hits)[0], ""
    if not found_def:
        return "dangling", f"no `def {name}` / `class {name}` in {ref_path!r}"
    return "live", ""


# --- the check ---------------------------------------------------------------

def find_arch(root: Path, override: str | None) -> Path | None:
    if override:
        p = (root / override) if not Path(override).is_absolute() else Path(override)
        return p if p.is_file() else None
    for cand in DEFAULT_ARCH_CANDIDATES:
        p = root / cand
        if p.is_file():
            return p
    return None


def check(arch_md: Path, root: Path) -> list[Finding]:
    py_index = build_py_index(root)
    findings: list[Finding] = []
    rows = list(parse_attestation_rows(arch_md.read_text(encoding="utf-8")))
    if not rows:
        return [Finding("(table)", "no attestation table found (no table with "
                                   "both 'Verification' and 'Status' columns)")]
    for row_id, verification, status in rows:
        if not is_full_conformant(status):
            continue
        haystack = (verification + " " + status).lower()
        refs = TEST_REF.findall(verification + " " + status)
        if refs:
            for ref in refs:
                st, detail = classify_ref(ref, root, py_index)
                if st == "dangling":
                    findings.append(Finding(row_id, f"dangling evidence — {detail}"))
                elif st in DISQUALIFYING_MARKERS:
                    findings.append(Finding(
                        row_id,
                        f"cites `{ref}` as conformant evidence, but that test is "
                        f"`@pytest.mark.{st}` — a declared-false/unrun invariant is "
                        f"not evidence. Drop the citation or fix the test and remove "
                        f"the marker."))
        elif any(k in haystack for k in REVIEW_KINDS):
            continue
        else:
            findings.append(Finding(
                row_id,
                f"claims `conformant` with no executable test and no declared "
                f"verification kind (a doc pointer is not evidence) — "
                f"verification={verification!r}"))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Attestation-evidence lint — every `conformant` row needs live evidence.")
    ap.add_argument("root", type=Path, nargs="?", default=Path("."),
                    help="The design repo root (default: cwd).")
    ap.add_argument("--arch", metavar="PATH", default=None,
                    help="Architecture document path (default: Architecture.md or docs/Architecture.md under root).")
    ap.add_argument("--json", action="store_true", help="Emit evaluate-report-compatible evidence JSON.")
    args = ap.parse_args()

    root: Path = args.root
    if not root.is_dir():
        print(f"attestation-evidence-lint: not a directory: {root}", file=sys.stderr)
        return 2
    arch = find_arch(root, args.arch)
    if arch is None:
        print(f"attestation-evidence-lint: no Architecture document found under {root} "
              f"(looked for {', '.join(DEFAULT_ARCH_CANDIDATES)} or --arch)", file=sys.stderr)
        return 2

    findings = check(arch, root)
    clean = not findings

    if args.json:
        detail = ("every `conformant` row cites a live, non-deferred test or a "
                  "declared review kind." if clean
                  else f"{len(findings)} conformant row(s) lack executable evidence.")
        citations = [{"path": str(arch), "lines": "", "note": f"{f.row}: {f.reason}"}
                     for f in findings]
        print(json.dumps({
            "tool": "attestation-evidence-lint",
            "ac": "attestation-integrity",
            "clean": clean,
            "suggested_status": "conformant" if clean else "non-conformant",
            "evidence": {"source": "deterministic", "tool": "attestation-evidence-lint",
                         "detail": detail, "citations": citations},
        }, indent=2))
        return 0 if clean else 1

    if clean:
        print("attestation-evidence-lint: OK")
        print(f"  {arch}: every `conformant` row cites live, non-deferred evidence")
        return 0

    print(f"attestation-evidence-lint: {len(findings)} conformant row(s) without "
          f"executable evidence in {arch}:")
    for f in sorted(findings, key=lambda f: f.row):
        print(f"  - {f.row}: {f.reason}")
    print("\nA `conformant` attestation row is a Security-Target claim; it needs a "
          "resolvable, non-xfail/skip test or a declared verification kind. See "
          "reference_designs/templates/ARCHITECTURE_TEMPLATE.md (the \"Mechanical check\" note).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
