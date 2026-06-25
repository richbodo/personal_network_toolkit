#!/usr/bin/env python3
# Toolkit-Version: 0.2
"""`just validate <candidate>` — one command that produces a deterministic-baseline
evaluate-report.json for a candidate PNA.

This is the assembly layer described in
docs/design-notes/2026-06-validate-command-and-strength-tiers.md: it runs the
existing deterministic lints (Tier S) against a candidate and folds their output
into a single typed report (tools/evaluate-report.schema.json), the same artifact
the Visual Validator renders and a contribution commits. The LLM architectural
review (Tier L, the skill's evaluate flow) and a cooperating design's executable
`[verify]` entrypoint (Tier F) enrich the *same* report afterwards; this tool fills
the deterministic spine.

Honesty is the load-bearing property (see the design note's "lite-as-full risk"):

  * A deterministic check that FINDS a violation is a confident call → the bearing
    AC is reported `non-conformant`, with the tool's citations.
  * A deterministic check that is CLEAN is necessary, not sufficient → the bearing
    AC is reported `unable-to-determine` (NEVER `conformant`), with the clean scan
    folded in as `source: deterministic` evidence and a rationale saying so.

So this command never emits a green `conformant` verdict on its own; a clean run is
an honest triage baseline ("here is what it demonstrably does and does not do"), not
a trust certificate. The summary posture is therefore `non-conformant` (a violation
was found on a Goal 1-5 AC) or `indeterminate` (nothing found, but undecided) — never
`conformant`.

Stdlib only: it shells out to the sibling lints (egress-lint, attestation-evidence-
lint, export-readable-lint) with their existing `--json` mode and assembles the
result. No third-party deps; runs under bare python3 like the rest of tools/.

Usage:
    validate.py <candidate-dir> [--out PATH] [--export PATH]
    just validate <candidate-dir> [args]

    --out PATH    Where to write the report (default: ./evaluate-report.json;
                  use '-' to write the JSON to stdout instead of a file).
    --export PATH Also run the PR-6 export-readability check against this export
                  dir/file (it needs an export artifact, not the repo root).

Exit: 1 if any finding is non-conformant, else 0; 2 on usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
AC_ID_RE = re.compile(r"^AC-[A-Z0-9-]+$")

# Short requirement text for the ACs a deterministic check can call non-conformant,
# kept in sync with spec/PNA_Spec.md (the schema wants a self-explaining `requirement`
# on a non-conformant finding). A generic fallback keeps the report schema-valid for
# any other AC the egress lint's `--ac` is pointed at.
AC_REQUIREMENT = {
    "AC-1": ("Shared data MUST be read-only and externally managed; private data MUST be "
             "read-write and locally owned, in separate storage namespaces — and private "
             "data MUST NOT leave the device on its own."),
    "AC-2": "Servers are delivery-only; no server may persist or sync private data.",
}


def toolkit_spec_version() -> str:
    """The MAJOR.MINOR the candidate is being validated against (the toolkit's /VERSION)."""
    vf = REPO / "VERSION"
    if vf.is_file():
        m = re.match(r"\s*(\d+\.\d+)", vf.read_text())
        if m:
            return m.group(1)
    return "0.1"


def git_short(path: Path) -> str | None:
    """Best-effort short commit of the candidate, if it is a git checkout."""
    try:
        cp = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True)
        out = cp.stdout.strip()
        return out if cp.returncode == 0 and out else None
    except (OSError, ValueError):
        return None


def parse_design_toml(path: Path) -> dict:
    """The same deliberately-tiny TOML subset the manifest lint parses: top-level
    `key = "val"` plus `[section]` tables. Returns a nested dict."""
    root: dict = {}
    section: dict = root
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = root.setdefault(line[1:-1].strip(), {})
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip()
        if val.startswith('"'):
            end = val.find('"', 1)
            val = val[1:end] if end != -1 else val[1:]
        else:
            val = val.split("#", 1)[0].strip()
        section[key] = val
    return root


def find_arch(root: Path) -> Path | None:
    for cand in ("Architecture.md", "docs/Architecture.md"):
        p = root / cand
        if p.is_file():
            return p
    return None


def run_lint_json(script: str, *args: str) -> dict:
    """Run a sibling lint with --json; return its parsed object, or a {_error} marker
    if it failed to produce JSON (e.g. a usage error to stderr)."""
    try:
        cp = subprocess.run([sys.executable, str(TOOLS / script), *map(str, args), "--json"],
                            capture_output=True, text=True)
    except OSError as e:
        return {"_error": str(e), "_returncode": -1}
    try:
        return json.loads(cp.stdout)
    except (json.JSONDecodeError, ValueError):
        return {"_error": (cp.stderr or cp.stdout or "no output").strip() or "no JSON output",
                "_returncode": cp.returncode}


def describe_candidate(path: Path) -> dict:
    """The report's `candidate` block: enough to know which design+revision this is."""
    cand: dict = {"pna_spec_version": "", "picks_source": "inferred"}
    dt = path / "design.toml"
    if dt.is_file():
        root = parse_design_toml(dt)
        if root.get("name"):
            cand["name"] = root["name"]
        if root.get("repo"):
            cand["repo_url"] = root["repo"]
        if root.get("toolkit_version"):
            cand["pna_spec_version"] = root["toolkit_version"]
        flavor = root.get("flavor")
        if isinstance(flavor, dict) and flavor:
            cand["axis_picks"] = flavor
            cand["picks_source"] = "declared"
    cand.setdefault("name", path.resolve().name)
    commit = git_short(path)
    if commit:
        cand["commit"] = commit
    if not cand["pna_spec_version"]:
        cand["pna_spec_version"] = toolkit_spec_version()
    return cand


def finding_or_signal(res: dict) -> tuple[str, dict]:
    """Map one lint's --json result to either an AC `finding` (when its `ac` is a real
    AC id) or a summary-level `signal` (when it isn't — export's PR-6, attestation's
    'attestation-integrity'; those live in the headline, not as AC findings, since the
    report is AC-keyed). The clean→unable-to-determine downgrade is the honesty layer."""
    tool = res.get("tool", "?")
    if "_error" in res:
        return ("signal", {"tool": tool, "ok": None,
                            "detail": f"could not run: {res['_error']}"})
    ac = res.get("ac", "")
    ev = res.get("evidence")
    clean = bool(res.get("clean"))
    detail = (ev or {}).get("detail", "")

    if not (isinstance(ac, str) and AC_ID_RE.match(ac)):
        return ("signal", {"tool": tool, "ok": clean, "ac": ac, "detail": detail})

    finding: dict = {"ac_id": ac, "ac_source": "universal"}
    if ev:
        finding["evidence"] = [ev]
    if clean:
        # Necessary, not sufficient: a clean static scan is NOT proof of conformance.
        finding["status"] = "unable-to-determine"
        finding["rationale"] = (
            f"The deterministic {tool} check is clean, but a passing static scan is "
            f"necessary, not sufficient, for {ac}; the LLM architectural review (the "
            f"evaluate flow) and human review are still pending.")
        finding["needs_human_review"] = True
    else:
        finding["status"] = "non-conformant"
        finding["requirement"] = AC_REQUIREMENT.get(
            ac, f"MUST satisfy {ac} — see spec/PNA_Spec.md.")
        cites = (ev or {}).get("citations") or []
        finding["citations"] = cites or [
            {"path": str(ac), "note": f"{tool} flagged a violation; see deterministic evidence"}]
    return ("finding", finding)


def build_report(candidate: Path, export: Path | None) -> tuple[dict, int]:
    """Assemble the deterministic-baseline report. Returns (report, exit_code)."""
    results: list[dict] = []
    # Tier S, check 1 — egress (AC-1). Always runs; the headline sovereignty check.
    results.append(run_lint_json("egress-lint.py", candidate))
    # Tier S, check 2 — attestation evidence, only if the candidate self-attests.
    if find_arch(candidate) is not None:
        results.append(run_lint_json("attestation-evidence-lint.py", candidate))
    # Tier S, check 3 — PR-6 export readability, only against a given export artifact.
    if export is not None:
        results.append(run_lint_json("export-readable-lint.py", export))

    findings: list[dict] = []
    signals: list[dict] = []
    for res in results:
        kind, payload = finding_or_signal(res)
        (findings if kind == "finding" else signals).append(payload)

    if not findings:  # defensive: the schema needs >=1 finding
        findings.append({
            "ac_id": "AC-1", "status": "unable-to-determine",
            "rationale": "No deterministic check produced an AC finding; run the evaluate flow.",
            "needs_human_review": True})

    nonconf = [f for f in findings if f["status"] == "non-conformant"]

    # Tier F availability (a cooperating design's executable entrypoint) — reported, not run.
    verify_note = ""
    dt = candidate / "design.toml"
    if dt.is_file():
        entry = (parse_design_toml(dt).get("verify") or {}).get("entrypoint")
        if entry:
            verify_note = (f" Tier F available: run `{entry}` in the candidate to add "
                           f"executable evidence.")

    sig_notes = []
    for s in signals:
        if s.get("ok") is False:
            sig_notes.append(f"{s['tool']} flagged: {s['detail']}")
        elif s.get("ok") is None:
            sig_notes.append(f"{s['tool']} {s['detail']}")
    sig_txt = (" " + " ".join(sig_notes)) if sig_notes else ""

    if nonconf:
        posture = "non-conformant"
        names = ", ".join(f["ac_id"] for f in nonconf)
        headline = (f"Deterministic baseline: {names} NON-CONFORMANT (a static check found a "
                    f"violation).{sig_txt} The LLM architectural review and human review are "
                    f"still pending.{verify_note}")
    else:
        posture = "indeterminate"
        headline = (f"Deterministic baseline only: the static checks are clean, but a clean "
                    f"scan is necessary, not sufficient — no conformance verdict is conferred at "
                    f"this strength.{sig_txt} The LLM architectural review (the evaluate flow) and "
                    f"human review are pending; this is a triage baseline.{verify_note}")

    report = {
        "report_schema_version": "0.1",
        "generated_by": "tools/validate.py (deterministic baseline; Tier S)",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "candidate": describe_candidate(candidate),
        "summary": {
            "posture": posture,
            "headline": headline,
            "leading_concerns": [f["ac_id"] for f in nonconf],
        },
        "findings": findings,
    }
    return report, (1 if nonconf else 0)


def human_summary(report: dict, out_path: str | None) -> str:
    lines = [f"validate: {report['summary']['posture'].upper()} — {report['candidate']['name']}",
             f"  {report['summary']['headline']}", "  findings:"]
    for f in report["findings"]:
        extra = ""
        if f.get("evidence"):
            extra = f"  [{f['evidence'][0].get('tool', f['evidence'][0]['source'])}]"
        lines.append(f"    - {f['ac_id']}: {f['status']}{extra}")
    if out_path and out_path != "-":
        lines.append(f"  report written to {out_path}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Produce a deterministic-baseline evaluate-report.json for a candidate PNA.")
    ap.add_argument("candidate", type=Path, help="Candidate PNA source tree to validate.")
    ap.add_argument("--out", default="evaluate-report.json",
                    help="Report path (default: ./evaluate-report.json; '-' for stdout).")
    ap.add_argument("--export", type=Path, default=None, metavar="PATH",
                    help="Also run the PR-6 export-readability check against this export dir/file.")
    args = ap.parse_args()

    if not args.candidate.is_dir():
        print(f"validate: candidate is not a directory: {args.candidate}", file=sys.stderr)
        return 2

    report, code = build_report(args.candidate, args.export)
    blob = json.dumps(report, indent=2)

    if args.out == "-":
        print(blob)
        print(human_summary(report, args.out), file=sys.stderr)
    else:
        Path(args.out).write_text(blob + "\n")
        print(human_summary(report, args.out))
    return code


if __name__ == "__main__":
    sys.exit(main())
