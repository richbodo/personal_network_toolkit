#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""realization-index — derive a cross-design *realization index* from the bundled
reference-design attestation tables. **Tier-0 spike** for the code-reuse design note
([`docs/design-notes/2026-06-harvesting-reusable-code.md`]).

The asset-dual of field notes: a field note says what an AC is easy to get *wrong*;
this index says *which accepted design realizes an AC, where in its code, and at which
archived commit* — so a builder adapting the closest design can find proven code by AC
instead of opening every Architecture.md and reading AC-by-AC.

It is **derived**, not hand-maintained: every row comes from data the toolkit already
requires and maintains — each accepted design's bundled `Architecture.md` attestation
tables (Realization + Verification + Status, keyed by AC) and its `design.toml` SWHID
pin. A generated artifact can't drift from the evidence it summarizes; `--check` is the
anti-drift gate (regenerate, diff the committed file, fail on mismatch) that would wire
into `just ci` if this graduates from spike to adopted.

WHAT IT DOES (deterministic, all inside this toolkit repo):
  1. For each reference_designs/<name>/ (skipping templates/): read design.toml for the
     repo / status / archival / SWHID pin / flavor, and read Architecture.md.
  2. Parse the commitment-bearing attestation tables (Universal + conditional ACs, the
     RZ-* realizations a pick brings, and the
     not-applicable table), tolerating both cell conventions in the wild (PRM links its
     AC cells, fellows uses plain text; fellows has a separate `| AC | Reason |` table).
  3. Extract per row: AC id + title, status, triggered-by, best-effort realization code
     pointers (backticked path-like tokens) and verification refs (test refs + declared
     review kinds).
  4. Aggregate by AC across designs and render docs/realization-index.md (or --json).

WHAT IT DOES NOT DO (honest scope of the spike):
  - It does not judge *harvest value* or portability (that is Tier 1 — a curated mark).
  - It does not parse EX-*/CST-*/UM-* tables (AC rows are the reuse-relevant subset;
    the same parser extends to them).
  - Realization-pointer extraction is best-effort over prose: it surfaces backticked
    file-path-looking tokens, not a guaranteed-complete set.

Usage:
  python3 tools/realization-index.py            # regenerate docs/realization-index.md
  python3 tools/realization-index.py --check     # exit 1 if the committed file is stale
  python3 tools/realization-index.py --json       # print the machine-readable model
  python3 tools/realization-index.py --stdout      # print the markdown, don't write

Stdlib only. Exits 0 on success, 1 on --check drift or any error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DESIGNS_PATH = REPO / "reference_designs"
OUT_PATH = REPO / "docs" / "realization-index.md"

AC_ID_RE = re.compile(r"(?:AC|RZ)-[A-Z0-9]+(?:-[A-Z0-9]+)*")  # AC-* commitments + RZ-* realizations
TITLE_RE = re.compile(r"\(([^)]+)\)")
CODE_TOKEN_RE = re.compile(r"`([^`]+)`")
# A backticked token that looks like a *code* pointer: a path (has a separator) ending
# in a code extension, or a path with an optional :symbol / :line suffix (e.g.
# `app/relationships.py:open_db()`). The caller additionally rejects HTTP routes
# (a leading `/`, e.g. `/api/groups`) and doc links (`*.md` etc.) — those are context,
# not code to harvest.
CODE_POINTER_RE = re.compile(
    r"^[\w.][\w./-]*\.(?:py|js|ts|sql|json|html|css|toml|yaml|yml|sh)\b|"
    r"^[\w.][\w./-]*/[\w./-]+(?::[\w().-]+)?$"
)
DOC_EXT = (".md", ".txt", ".rst")
# Declared review kinds (no test ref) that count as verification.
REVIEW_KINDS = [
    "by construction", "by architecture", "by bounding", "code inspection",
    "human-review", "human review", "llm rubric", "architectural",
]


def fail(msg: str) -> int:
    print(f"realization-index: error: {msg}", file=sys.stderr)
    return 1


# --- design.toml (the deliberately-simple TOML subset; same shape as the lint) -------

def parse_manifest(text: str) -> dict:
    root: dict = {}
    section = root
    for raw in text.splitlines():
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


# --- Architecture.md attestation tables ----------------------------------------------

def split_row(line: str) -> list[str]:
    """Split a markdown table row `| a | b |` into stripped cell strings."""
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def iter_tables(md: str):
    """Yield (header_cells, [data_row_cells, ...]) for each markdown table — a run of
    `|`-led lines whose second line is the `|---|` separator."""
    lines = md.splitlines()
    i, n = 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|") and i + 1 < n and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]
        ):
            header = split_row(lines[i])
            rows = []
            j = i + 2
            while j < n and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def extract_pointers(cell: str) -> list[str]:
    """Best-effort *code* pointers from a Realization cell: backticked tokens that look
    like source paths. Excludes HTTP routes (a leading `/`, e.g. `/api/groups`) and doc
    links (`*.md`/`*.txt`/`*.rst`) — those are context for a reader, not code to lift."""
    out: list[str] = []
    for tok in CODE_TOKEN_RE.findall(cell):
        t = tok.strip()
        if t.startswith("/") or t.lower().endswith(DOC_EXT):
            continue
        if "/" in t and CODE_POINTER_RE.match(t) and t not in out:
            out.append(t)
    return out


def extract_verifications(cell: str) -> list[str]:
    """Verification refs from a Verification cell: test/code refs + any declared review
    kinds. A bare `::name` continuation (the attestation shorthand for "another test in
    the file named just before it") is stitched back onto that file so every ref
    resolves on its own. Doc links are kept here — a `*.md` can be human-review
    evidence, unlike in a Realization cell."""
    out: list[str] = []
    last_file = None
    for tok in CODE_TOKEN_RE.findall(cell):
        t = tok.strip()
        ref = None
        if t.startswith("::"):
            ref = (last_file + t) if last_file else t
        elif "::" in t:
            last_file = t.split("::", 1)[0]
            ref = t
        elif "/" in t or t.endswith(".py"):
            last_file = t
            ref = t
        if ref and ref not in out:
            out.append(ref)
    low = cell.lower()
    for kind in REVIEW_KINDS:
        if kind in low and kind not in out:
            out.append(kind)
    return out


def normalize_status(raw: str) -> str:
    low = raw.lower()
    if low.startswith("conformant"):
        return "conformant"
    if low.startswith("partial"):
        return "partial"
    if "not-applicable" in low or "not applicable" in low:
        return "not-applicable"
    return raw.strip() or "unspecified"


def parse_attestations(md: str, design: str) -> list[dict]:
    """Return AC attestation rows from a design's Architecture.md. Handles the
    Universal/Flavor AC tables (Realization+Verification+Status) and the dedicated
    `| AC | Reason |` not-applicable table."""
    rows: list[dict] = []
    for header, data in iter_tables(md):
        hl = [h.lower() for h in header]
        if not hl or hl[0] != "ac":
            continue
        # Dedicated not-applicable table: | AC | Reason |
        if hl == ["ac", "reason"]:
            for cells in data:
                if len(cells) < 2:
                    continue
                m = AC_ID_RE.search(cells[0])
                if not m:
                    continue
                rows.append({
                    "ac": m.group(0).rstrip("-"),
                    "title": _title(cells[0]),
                    "design": design,
                    "status": "not-applicable",
                    "triggered_by": "",
                    "realization": [],
                    "verification": [],
                    "reason": cells[1],
                })
            continue
        # AC attestation tables: need Realization + Verification + Status columns.
        try:
            i_real = hl.index("realization")
            i_ver = hl.index("verification")
            i_stat = hl.index("status")
        except ValueError:
            continue
        i_trig = hl.index("triggered by") if "triggered by" in hl else -1
        for cells in data:
            if len(cells) <= max(i_real, i_ver, i_stat):
                continue
            m = AC_ID_RE.search(cells[0])
            if not m:
                continue
            rows.append({
                "ac": m.group(0).rstrip("-"),
                "title": _title(cells[0]),
                "design": design,
                "status": normalize_status(cells[i_stat]),
                "status_raw": cells[i_stat],
                "triggered_by": cells[i_trig].replace("`", "").strip() if i_trig >= 0 else "",
                "realization": extract_pointers(cells[i_real]),
                "verification": extract_verifications(cells[i_ver]),
            })
    return rows


def _title(ac_cell: str) -> str:
    m = TITLE_RE.search(ac_cell)
    return m.group(1).strip() if m else ""


# --- model ---------------------------------------------------------------------------

def ac_sort_key(ac: str):
    m = re.fullmatch(r"AC-(\d+)", ac)
    return (0, int(m.group(1)), "") if m else (1, 0, ac)


def build_model() -> dict:
    designs: list[dict] = []
    all_rows: list[dict] = []
    if not DESIGNS_PATH.exists():
        return {"designs": [], "acs": {}}
    for sub in sorted(p for p in DESIGNS_PATH.iterdir() if p.is_dir()):
        if sub.name == "templates":
            continue
        manifest_f, arch_f = sub / "design.toml", sub / "Architecture.md"
        if not (manifest_f.exists() and arch_f.exists()):
            continue
        man = parse_manifest(manifest_f.read_text(encoding="utf-8"))
        flavor = man.get("flavor", {})
        designs.append({
            "name": man.get("name", sub.name),
            "repo": man.get("repo", ""),
            "status": man.get("status", ""),
            "archival": man.get("archival", ""),
            "commit": man.get("commit", ""),
            "swhid_dir": man.get("swhid_dir", ""),
            "flavor": flavor,
        })
        all_rows.extend(parse_attestations(arch_f.read_text(encoding="utf-8"), man.get("name", sub.name)))
    acs: dict[str, list[dict]] = {}
    for r in all_rows:
        acs.setdefault(r["ac"], []).append(r)
    for rs in acs.values():
        rs.sort(key=lambda r: r["design"])
    # Per-design realization-pointer coverage — the progress metric toward the
    # "full coverage" goal (every non-N/A row should resolve to a code pointer).
    coverage: dict[str, dict] = {}
    for d in designs:
        rows = [r for r in all_rows
                if r["design"] == d["name"] and r["status"] != "not-applicable"]
        with_ptr = sum(1 for r in rows if r["realization"])
        coverage[d["name"]] = {
            "non_na_rows": len(rows),
            "with_pointer": with_ptr,
            "pct": round(100 * with_ptr / len(rows)) if rows else 0,
        }
    return {"designs": designs, "acs": acs, "coverage": coverage}


# --- rendering -----------------------------------------------------------------------

def _cell(s: str) -> str:
    return s.replace("|", r"\|")


def _short(commit: str) -> str:
    return commit[:7] if commit else "—"


def _join_code(items: list[str], cap: int = 4) -> str:
    if not items:
        return "—"
    shown = items[:cap]
    extra = len(items) - len(shown)
    out = ", ".join(f"`{_cell(i)}`" for i in shown)
    return out + (f" (+{extra})" if extra else "")


def _na_reason(reason: str, cap: int = 90) -> str:
    r = reason.replace("`", "").strip()
    if len(r) > cap:
        r = r[:cap].rsplit(" ", 1)[0] + "…"
    return r


def render_markdown(model: dict) -> str:
    designs, acs = model["designs"], model["acs"]
    L: list[str] = []
    L.append("# Realization index (derived — Tier-0 spike)")
    L.append("")
    L.append("> **GENERATED FILE — do not edit by hand.** Regenerate with "
             "`python3 tools/realization-index.py`; `--check` fails on drift.")
    L.append(">")
    L.append("> A cross-design map of *which accepted reference design realizes each "
             "AC, where in its code, and at which archived commit* — the asset-dual of "
             "[field notes](field-notes/), derived from each design's bundled "
             "`Architecture.md` attestation table + `design.toml` SWHID pin. Spike for "
             "[`design-notes/2026-06-harvesting-reusable-code.md`](design-notes/2026-06-harvesting-reusable-code.md). "
             "Realization pointers are best-effort over prose; the design's own "
             "Architecture.md is authoritative. Fetch the pinned `swhid_dir` (not "
             "`main`) to study a realization at the archived commit.")
    L.append("")

    # Designs indexed
    L.append("## Designs indexed")
    L.append("")
    L.append("| Design | Status | Archival | Pin | swhid_dir | Flavor |")
    L.append("|---|---|---|---|---|---|")
    for d in designs:
        flav = ", ".join(f"{k}:{v}" for k, v in d["flavor"].items())
        L.append(f"| [{_cell(d['name'])}]({_cell(d['repo'])}) | {_cell(d['status'])} | "
                 f"{_cell(d['archival'])} | `{_short(d['commit'])}` | "
                 f"`{_cell(d['swhid_dir']) or '—'}` | {_cell(flav)} |")
    L.append("")

    # Coverage summary
    realized_multi = sorted(
        (ac for ac, rs in acs.items()
         if len({r['design'] for r in rs if r['status'] != 'not-applicable'}) > 1),
        key=ac_sort_key)
    n_acs = len(acs)
    n_realized = sum(1 for rs in acs.values()
                     if any(r['status'] != 'not-applicable' for r in rs))
    cov = model["coverage"]
    L.append("## Coverage summary")
    L.append("")
    L.append(f"- **{n_acs}** distinct ACs indexed across **{len(designs)}** designs; "
             f"**{n_realized}** have at least one non-N/A realization.")
    L.append(f"- **{len(realized_multi)}** ACs are realized by **more than one** design "
             f"(the prime harvest candidates — two realizations to compare): "
             + (", ".join(realized_multi) if realized_multi else "none") + ".")
    L.append("- **Realization-pointer coverage** — the standing goal is **100%** for "
             "every accepted design (each non-N/A row's realization should resolve to a "
             "`path:symbol` code pointer; see the design note). A number below 100% "
             "marks attestation prose that names a symbol without its file:")
    for d in designs:
        c = cov[d["name"]]
        L.append(f"    - {d['name']}: **{c['with_pointer']}/{c['non_na_rows']}** "
                 f"non-N/A rows carry a code pointer (**{c['pct']}%**).")
    L.append("")

    # Realization matrix
    L.append("## Realization matrix")
    L.append("")
    L.append("One row per (commitment-or-realization, design) — `AC-*` architectural "
             "commitments and the `RZ-*` realizations a pick brings. `Realization` and "
             "`Verification` are the code/test pointers harvested from the attestation; "
             "`Pin` is the design's archived commit (study the realization there, via "
             "`swhid_dir` above).")
    L.append("")
    L.append("| AC / RZ | Title | Design | Status | Realization | Verification | Pin |")
    L.append("|---|---|---|---|---|---|---|")
    pin_by_design = {d["name"]: _short(d["commit"]) for d in designs}
    for ac in sorted(acs, key=ac_sort_key):
        rows = acs[ac]
        title = next((r["title"] for r in rows if r["title"]), "")
        for r in rows:
            real = _join_code(r["realization"])
            if not r["realization"] and r.get("reason"):
                real = f"_n/a: {_cell(_na_reason(r['reason']))}_"
            ver = _join_code(r["verification"])
            L.append(f"| {ac} | {_cell(title)} | {_cell(r['design'])} | "
                     f"{_cell(r['status'])} | {real} | {ver} | "
                     f"`{pin_by_design.get(r['design'], '—')}` |")
    L.append("")
    return "\n".join(L) + "\n"


def render_json(model: dict) -> str:
    return json.dumps(model, indent=2, sort_keys=True) + "\n"


# --- main ----------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Derive the cross-design realization index.")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed docs/realization-index.md is stale")
    ap.add_argument("--json", action="store_true", help="print the JSON model to stdout")
    ap.add_argument("--stdout", action="store_true", help="print markdown, do not write")
    args = ap.parse_args(argv)

    model = build_model()
    if not model["designs"]:
        return fail(f"no accepted designs found under {DESIGNS_PATH}")

    if args.json:
        sys.stdout.write(render_json(model))
        return 0

    md = render_markdown(model)
    if args.stdout:
        sys.stdout.write(md)
        return 0
    if args.check:
        current = OUT_PATH.read_text(encoding="utf-8") if OUT_PATH.exists() else ""
        if current != md:
            return fail(f"{OUT_PATH.relative_to(REPO)} is stale — "
                        f"regenerate with `python3 tools/realization-index.py`")
        print(f"realization-index: {OUT_PATH.relative_to(REPO)} is up to date.")
        return 0
    OUT_PATH.write_text(md, encoding="utf-8")
    n_rows = sum(len(v) for v in model["acs"].values())
    print(f"realization-index: wrote {OUT_PATH.relative_to(REPO)} "
          f"({len(model['acs'])} ACs, {n_rows} rows, {len(model['designs'])} designs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
