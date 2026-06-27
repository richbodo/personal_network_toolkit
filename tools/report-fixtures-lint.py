#!/usr/bin/env python3
# Toolkit-Version: 0.2
"""Render-contract lint for evaluate-report.json instances.

The Visual Validator (plans/visual-validator-plan.md; tools/report-viewer/) renders
instances of tools/evaluate-report.schema.json. This lint is the deterministic guard
that the sample reports it ships with — and any report a developer drops in a reports
directory (e.g. a cron job that runs the evaluate flow) — actually satisfy the load-
bearing fields the viewer reads, so a schema change or a malformed report fails loudly
instead of rendering blank.

Stdlib only (no jsonschema): it checks the *render contract* — the required top-level
keys, the summary posture/headline, and per-finding ac_id/status plus the schema's
status-conditional requirements (citations for (non-)conformant; requirement for
non-conformant; rationale for not-applicable/unable-to-determine). It is intentionally
NOT a full JSON Schema validator; tools/evaluate-report.schema.json remains the source
of truth (and the only place EX-*/CST-* live — as references inside the AC findings they
bear on, since ac_id matches ^AC-...$).

Usage:  python3 tools/report-fixtures-lint.py <file-or-dir>
Exit:   0 if every report satisfies the render contract, 1 otherwise, 2 on usage error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

AC_ID = re.compile(r"^AC-[A-Z0-9-]+$")
POSTURES = {"conformant", "not-pna-active", "non-conformant", "mixed", "indeterminate"}
STATUSES = {"conformant", "non-conformant", "not-applicable", "unable-to-determine"}
TOP_REQUIRED = ("report_schema_version", "candidate", "summary", "findings")


def check_report(obj: object) -> list[str]:
    """Return a list of render-contract violations for one parsed report (empty == ok)."""
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["top level is not a JSON object"]

    for k in TOP_REQUIRED:
        if k not in obj:
            errs.append(f"missing required top-level key {k!r}")
    if obj.get("report_schema_version") not in (None, "0.1"):
        errs.append(f'report_schema_version must be "0.1", got {obj.get("report_schema_version")!r}')

    cand = obj.get("candidate")
    if isinstance(cand, dict):
        for k in ("pna_spec_version", "picks_source"):
            if k not in cand:
                errs.append(f"candidate is missing required key {k!r}")
    elif "candidate" in obj:
        errs.append("candidate is not an object")

    summ = obj.get("summary")
    if isinstance(summ, dict):
        if summ.get("posture") not in POSTURES:
            errs.append(f"summary.posture {summ.get('posture')!r} not one of {sorted(POSTURES)}")
        if not isinstance(summ.get("headline"), str) or not summ.get("headline"):
            errs.append("summary.headline must be a non-empty string")
    elif "summary" in obj:
        errs.append("summary is not an object")

    findings = obj.get("findings")
    if not isinstance(findings, list) or not findings:
        errs.append("findings must be a non-empty array")
        return errs

    for i, f in enumerate(findings):
        where = f"findings[{i}]"
        if not isinstance(f, dict):
            errs.append(f"{where} is not an object")
            continue
        ac = f.get("ac_id")
        if isinstance(ac, str) and AC_ID.match(ac):
            where = f"findings[{i}]({ac})"
        else:
            errs.append(f"{where}.ac_id {ac!r} does not match ^AC-[A-Z0-9-]+$")
        st = f.get("status")
        if st not in STATUSES:
            errs.append(f"{where}.status {st!r} not one of {sorted(STATUSES)}")
            continue
        has_cites = isinstance(f.get("citations"), list) and len(f["citations"]) > 0
        if st in ("conformant", "non-conformant") and not has_cites:
            errs.append(f"{where}: status {st} requires a non-empty 'citations' array")
        if st == "non-conformant" and not f.get("requirement"):
            errs.append(f"{where}: status non-conformant requires 'requirement'")
        if st in ("not-applicable", "unable-to-determine") and not f.get("rationale"):
            errs.append(f"{where}: status {st} requires 'rationale'")
    return errs


def iter_reports(path: Path):
    if path.is_dir():
        yield from sorted(path.glob("*.json"))
    else:
        yield path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: report-fixtures-lint.py <file-or-dir>", file=sys.stderr)
        return 2
    target = Path(argv[1])
    if not target.exists():
        print(f"error: {target} does not exist", file=sys.stderr)
        return 2
    files = list(iter_reports(target))
    if not files:
        print(f"error: no .json reports found under {target}", file=sys.stderr)
        return 2

    bad = 0
    for fp in files:
        try:
            obj = json.loads(fp.read_text())
        except json.JSONDecodeError as e:
            print(f"FAIL  {fp}: not valid JSON ({e})")
            bad += 1
            continue
        errs = check_report(obj)
        if errs:
            bad += 1
            print(f"FAIL  {fp}")
            for e in errs:
                print(f"        - {e}")
        else:
            print(f"ok    {fp}")

    print(f"\nreport-fixtures-lint: {len(files) - bad}/{len(files)} reports satisfy the render contract")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
