#!/usr/bin/env python3
"""Lint the AC/EX ↔ contract bidirectional traceability invariants.

Checks:
  1. Every AC in spec/PNA_Spec.md and spec/axes.md carries a stable ID
     (AC-N, AC-PRM-X, AC-MCP-X).
  2. Every contract file in contracts/ declares "Realizes: AC-..." somewhere
     in its head (within the first ~25 lines), naming at least one valid AC.
  3. Every AC named in a contract's "Realizes:" header actually exists in the
     spec.
  4. Every Exception in spec/exceptions.md carries a stable ID (EX-*) in a
     registry table row.
  5. Every "Relaxes:" header (in exceptions.md) names only valid AC IDs, EX
     IDs, or the PNA-DEFINITION sentinel.
  6. Every "Reversible:" field is well-formed (yes|no); a "yes" requires a
     "Reversal:" field. Every value in a strength-profile column is one of the
     fixed strength classes (EX-H8).

The lint validates the *shape* of declarations (presence + ID/vocabulary
resolution), not their behavioral correctness — that is the LLM evaluate
flow's job (see pna-build-eval-contrib/SKILL.md § Evaluate flow).

Exits 0 if clean, 1 if any violation found. Designed to be CI-friendly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

AC_RE = re.compile(r"^\| (AC-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
REALIZES_RE = re.compile(r"Realizes:\s*((?:AC-[A-Z0-9-]+(?:\s*,\s*)?)+)", re.IGNORECASE)

# Exception registry IDs live in `| EX-... |` table rows (mirrors AC_RE). The
# handler-clause IDs (EX-H1..EX-H8) are list items, not table rows, so they are
# deliberately NOT collected here as registry exceptions.
EX_RE = re.compile(r"^\| (EX-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
# Inverse of REALIZES_RE. Tokens may be AC-*, EX-*, or the PNA-DEFINITION
# sentinel (the PNA definition is prose in vocab-pna, not an `| AC-X |` row).
RELAXES_RE = re.compile(
    r"Relaxes:\s*((?:(?:AC-[A-Z0-9-]+|EX-[A-Z0-9-]+|PNA-DEFINITION)(?:\s*,\s*)?)+)",
    re.IGNORECASE,
)
REVERSIBLE_RE = re.compile(r"Reversible:\s*([A-Za-z]+)", re.IGNORECASE)
STRENGTH_CLASSES = {
    "enforced", "verifiable", "best-effort",
    "provider-asserted", "recoverable-only", "none",
}

EXCEPTIONS_PATH = REPO / "spec" / "exceptions.md"


def collect_spec_ac_ids() -> set[str]:
    """All AC IDs from the AC tables in the spec."""
    ids: set[str] = set()
    for path in (REPO / "spec" / "PNA_Spec.md", REPO / "spec" / "axes.md"):
        if not path.exists():
            print(f"FAIL: spec file missing: {path}")
            sys.exit(1)
        ids.update(AC_RE.findall(path.read_text()))
    return ids


def collect_contract_realizes() -> dict[Path, list[str]]:
    """For each contract file, the list of AC IDs in its 'Realizes:' header."""
    contracts_dir = REPO / "contracts"
    out: dict[Path, list[str]] = {}
    for f in sorted(contracts_dir.iterdir()):
        if not f.is_file() or f.name.startswith(".") or f.name == "README.md":
            continue
        head = "\n".join(f.read_text().splitlines()[:25])
        m = REALIZES_RE.search(head)
        out[f] = [s.strip() for s in m.group(1).split(",")] if m else []
    return out


def collect_exception_ids() -> set[str]:
    """EX-* registry IDs from spec/exceptions.md. Empty if the file is absent
    (so the lint stays green on toolkit versions that predate Exceptions)."""
    if not EXCEPTIONS_PATH.exists():
        return set()
    return set(EX_RE.findall(EXCEPTIONS_PATH.read_text()))


def collect_relaxes() -> list[str]:
    """All tokens from every 'Relaxes:' header in exceptions.md (flattened)."""
    if not EXCEPTIONS_PATH.exists():
        return []
    tokens: list[str] = []
    for m in RELAXES_RE.finditer(EXCEPTIONS_PATH.read_text()):
        tokens.extend(t.strip() for t in m.group(1).split(","))
    return tokens


def collect_strength_violations(text: str) -> list[str]:
    """Validate strength-profile tables: any markdown table with a column
    headed 'Strength' must carry only fixed strength-class values in that
    column. Keyed on the header name so unrelated tables are untouched."""
    violations: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and "strength" in line.lower():
            cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
            if "strength" in cells:
                col = cells.index("strength")
                j = i + 2  # skip header + |---| separator
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    row = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    if len(row) > col and row[col]:
                        val = row[col]
                        if val not in STRENGTH_CLASSES:
                            violations.append(
                                f"strength-profile names unknown class '{val}' "
                                f"(allowed: {', '.join(sorted(STRENGTH_CLASSES))})"
                            )
                    j += 1
                i = j
                continue
        i += 1
    return violations


def main() -> int:
    failures: list[str] = []

    spec_ids = collect_spec_ac_ids()
    if not spec_ids:
        print("FAIL: No AC IDs found in spec/. Check the `| AC-X |` row format.")
        return 1

    contract_realizes = collect_contract_realizes()
    if not contract_realizes:
        failures.append("No contract files found under contracts/.")

    for path, ac_list in contract_realizes.items():
        rel = path.relative_to(REPO)
        if not ac_list:
            failures.append(f"{rel}: no 'Realizes: AC-...' header found in head of file.")
            continue
        for ac in ac_list:
            if ac not in spec_ids:
                failures.append(f"{rel}: claims to realize {ac}, but {ac} is not defined in spec/.")

    # --- Exceptions (spec/exceptions.md) ---
    exception_ids = collect_exception_ids()
    known = spec_ids | exception_ids | {"PNA-DEFINITION"}
    for tok in collect_relaxes():
        if tok not in known:
            failures.append(
                f"exceptions.md: Relaxes names {tok}, which is not a known AC, EX, "
                "or PNA-DEFINITION."
            )

    if EXCEPTIONS_PATH.exists():
        ex_text = EXCEPTIONS_PATH.read_text()
        rev_values = [m.group(1).lower() for m in REVERSIBLE_RE.finditer(ex_text)]
        for v in rev_values:
            if v not in ("yes", "no"):
                failures.append(f"exceptions.md: malformed 'Reversible: {v}' (want yes|no).")
        if "yes" in rev_values and "Reversal:" not in ex_text:
            failures.append("exceptions.md: 'Reversible: yes' present but no 'Reversal:' field.")
        failures.extend(f"exceptions.md: {v}" for v in collect_strength_violations(ex_text))

    if failures:
        print(f"lint-spec-ids: {len(failures)} violation(s) found.")
        for line in failures:
            print(f"  - {line}")
        return 1

    n_realizing = sum(1 for v in contract_realizes.values() if v)
    print("lint-spec-ids: OK")
    print(f"  spec defines {len(spec_ids)} AC IDs")
    print(f"  {n_realizing}/{len(contract_realizes)} contract files declare a 'Realizes:' header")
    print(f"  exceptions.md defines {len(exception_ids)} exception ID(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
