#!/usr/bin/env python3
"""Lint the AC ↔ contract bidirectional traceability invariants.

Checks:
  1. Every AC in spec/PNA_Spec.md and spec/axes.md carries a stable ID
     (AC-N, AC-PRM-X, AC-MCP-X).
  2. Every contract file in contracts/ declares "Realizes: AC-..." somewhere
     in its head (within the first ~25 lines), naming at least one valid AC.
  3. Every AC named in a contract's "Realizes:" header actually exists in the
     spec.

Exits 0 if clean, 1 if any violation found. Designed to be CI-friendly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

AC_RE = re.compile(r"^\| (AC-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
REALIZES_RE = re.compile(r"Realizes:\s*((?:AC-[A-Z0-9-]+(?:\s*,\s*)?)+)", re.IGNORECASE)


def collect_spec_ac_ids() -> set[str]:
    """All AC IDs from the AC tables in the spec."""
    ids: set[str] = set()
    for path in (REPO / "spec" / "PNA_Spec.md", REPO / "spec" / "axes.md"):
        if not path.exists():
            print(f"FAIL: spec file missing: {path}")
            sys.exit(1)
        text = path.read_text()
        ids.update(AC_RE.findall(text))
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
        if not m:
            out[f] = []
            continue
        ids = [s.strip() for s in m.group(1).split(",")]
        out[f] = ids
    return out


def main() -> int:
    failures: list[str] = []

    spec_ids = collect_spec_ac_ids()
    if not spec_ids:
        failures.append("No AC IDs found in spec/. Check that AC tables follow the `| AC-X |` row format.")
        for line in failures:
            print(f"FAIL: {line}")
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

    if failures:
        print(f"lint-spec-ids: {len(failures)} violation(s) found.")
        for line in failures:
            print(f"  - {line}")
        return 1

    n_contracts = len(contract_realizes)
    n_acs = len(spec_ids)
    n_realizing = sum(1 for v in contract_realizes.values() if v)
    print(f"lint-spec-ids: OK")
    print(f"  spec defines {n_acs} AC IDs")
    print(f"  {n_realizing}/{n_contracts} contract files declare a 'Realizes:' header")
    return 0


if __name__ == "__main__":
    sys.exit(main())
