#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""Lint the AC/EX ↔ contract traceability invariants and toolkit-version stamps.

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
  6b. Every Constraint in spec/constraints.md carries a stable ID (CST-*) in a
     registry table row AND a matching '### CST-...' detail block (same set of
     IDs on both sides). On both the table and the blocks: every "Triggered-by:"
     token resolves to a pick of the *named* axis (axis prefix + pick family
     from axes.md — a cross-axis pick does not resolve); every "Bounds:" token
     is a valid AC/Goal-N/PNA-DEFINITION; every "Frontier:" is well-formed
     (Open|Mitigated|Solved-on-<platform>|Inherent), and Mitigated/Solved-* each
     require a "Workaround:"; every "Detectability:" is one of the fixed classes.
     The table and the blocks must agree on every field per entry (no drift).
  7. The toolkit is versioned as a unit: a /VERSION file is the source of
     truth, and every versioned toolkit artifact (spec, skill, lint,
     contracts, templates, CONTRIBUTING, README) carries a "Toolkit-Version:"
     header whose minor matches /VERSION.
  8. Every reference_designs/<name>/design.toml is well-formed: required keys
     present; status/archival from their fixed vocab; [flavor] picks resolve to
     the right axis in axes.md; [verify] runner known. An `archived` design must
     carry a 40-hex commit + well-formed swhid_rev/swhid_dir (swhid_rev matching
     the commit) + a verify entrypoint; a `pending` design may defer those but
     any present value must still be well-formed. A design dir with an
     Architecture.md must have a manifest.

The lint validates the *shape* of declarations (presence + ID/vocabulary/
version resolution), not their behavioral correctness — that is the LLM
evaluate flow's job (see pna-build-eval-contrib/SKILL.md § Evaluate flow).

Exits 0 if clean, 1 if any violation found. Designed to be CI-friendly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# A table-cell ID may be preceded by a stable deep-link anchor
# (`| <a id="ac-1"></a>AC-1 |`) so reference-design conformance reports can
# link to a specific row. The registry regexes tolerate that optional prefix.
_CELL_ANCHOR = r'(?:<a id="[^"]*"></a>)?'

AC_RE = re.compile(r"^\| " + _CELL_ANCHOR + r"(AC-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
REALIZES_RE = re.compile(r"Realizes:\s*((?:AC-[A-Z0-9-]+(?:\s*,\s*)?)+)", re.IGNORECASE)

# Exception registry IDs live in `| EX-... |` table rows (mirrors AC_RE). The
# handler-clause IDs (EX-H1..EX-H8) are list items, not table rows, so they are
# deliberately NOT collected here as registry exceptions.
EX_RE = re.compile(r"^\| " + _CELL_ANCHOR + r"(EX-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
# Inverse of REALIZES_RE. Tokens may be AC-*, EX-*, or the PNA-DEFINITION
# sentinel (the PNA definition is prose in vocab-pna, not an `| AC-X |` row).
RELAXES_RE = re.compile(
    r"Relaxes:\s*((?:(?:AC-[A-Z0-9-]+|EX-[A-Z0-9-]+|PNA-DEFINITION)(?:\s*,\s*)?)+)",
    re.IGNORECASE,
)
# `\**` tolerates the markdown-bold field form (`**Reversible:** yes`); without
# it this matched nothing against the bold form actually used in exceptions.md,
# leaving the well-formedness + coupling checks below dead. The backtick header-
# convention mention (`**`Reversible:`**`) is not followed by a letter, so it is
# correctly NOT captured as a value.
REVERSIBLE_RE = re.compile(r"Reversible:\**\s*([A-Za-z]+)", re.IGNORECASE)
# The actual `**Reversal:**` field (line-anchored), distinct from the literal
# "Reversal:" that also appears in the header-conventions prose — a bare
# substring test was satisfied by that prose and so never enforced the coupling.
REVERSAL_FIELD_RE = re.compile(r"^\**Reversal:", re.MULTILINE | re.IGNORECASE)
STRENGTH_CLASSES = {
    "enforced", "verifiable", "best-effort",
    "provider-asserted", "recoverable-only", "none",
}

# --- Constraints (spec/constraints.md) ---
# Constraint registry IDs live in `| CST-... |` table rows (mirrors AC_RE / EX_RE).
CST_RE = re.compile(r"^\| " + _CELL_ANCHOR + r"(CST-[A-Z0-9-]+?)(?=\s|\*|\|)", re.MULTILINE)
# Detail blocks open with a '### CST-...' heading.
CST_BLOCK_RE = re.compile(r"^### (CST-[A-Z0-9-]+)", re.MULTILINE)
# Field value extractors operate on a single source string (one registry-table
# cell, or the line that follows a '**Field:**' label in a detail block). Each
# pulls the well-formed tokens out of free text, so prose like "(build space —
# see entry)" simply yields no tokens rather than a false positive.
TRIGGERED_TOKEN_RE = re.compile(r"[a-z0-9-]+:[a-z0-9-]+", re.IGNORECASE)
BOUNDS_TOKEN_RE = re.compile(r"AC-[A-Z0-9-]+|Goal-[0-9]+|PNA-DEFINITION", re.IGNORECASE)
# Frontier: Open | Mitigated | Solved-on-<platform> | Inherent. Mitigated and
# Solved-* require a Workaround: field (cross-checked below). Anchored at the
# value's start (a registry-table cell, or the text after a '**Frontier:**'
# label) so trailing prose ("Open — no workaround …") doesn't matter and a
# malformed value can't be salvaged from mid-string.
FRONTIER_VALUE_RE = re.compile(
    r"^\s*(Open|Mitigated|Solved-on-[a-z0-9-]+|Inherent)\b", re.IGNORECASE
)
# The full hyphen-chain at the value's start, so `feature-detect-extra` is
# captured whole (and rejected) rather than truncated to a valid prefix.
DETECT_VALUE_RE = re.compile(r"^\s*([a-z]+(?:-[a-z]+)+)", re.IGNORECASE)
DETECT_CLASSES = {"feature-detect", "empirical-probe", "ua-sniff"}
# Triggered-by `<axis>:<pick>` tokens resolve against the picks of the *named
# axis only* (per-axis, not a global pool — so `comms:opfs-sqlite-wasm` is caught
# as a cross-axis error). Maps the axis-prefix token a constraint may use to the
# axes.md section heading whose '### Picks' bullets define that axis's picks.
AXIS_PREFIX_TO_HEADING = {
    "distribution": "distribution",
    "storage": "storage substrate",
    "ingestion": "ingestion shape",
    "workspace": "workspace shell",
    "comms": "comms transport set",
    "mcp-exposure": "mcp-exposure",
}
# Pick IDs in axes.md appear as the leading bolded code span of a Picks bullet:
#   - **`opfs-sqlite-wasm`** — …   (the `+` admits mcp-exposure picks like
#   `shared+private+comms`, which would otherwise be truncated at the plus).
AXES_PICK_RE = re.compile(r"^- \*\*`([a-z0-9+-]+)`", re.MULTILINE)
# Section headings in axes.md: '## Storage substrate'.
AXES_SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)

# --- Reference-design manifests (reference_designs/<name>/design.toml) ---
DESIGNS_PATH = REPO / "reference_designs"
SWHID_REV_RE = re.compile(r"^swh:1:rev:[0-9a-f]{40}$")
SWHID_DIR_RE = re.compile(r"^swh:1:dir:[0-9a-f]{40}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DESIGN_STATUS = {"active", "archived", "superseded"}
DESIGN_ARCHIVAL = {"pending", "archived"}
DESIGN_RUNNERS = {"container", "just", "make"}

# Matches the version stamp across every artifact format: markdown
# (`**Toolkit-Version:** 0.1`), comments (`# / -- / //  Toolkit-Version: 0.1`),
# and JSON `$comment` strings (`... Toolkit-Version: 0.1.`).
TOOLKIT_VERSION_RE = re.compile(r"Toolkit-Version:\**\s*(\d+\.\d+)")

EXCEPTIONS_PATH = REPO / "spec" / "exceptions.md"
CONSTRAINTS_PATH = REPO / "spec" / "constraints.md"
AXES_PATH = REPO / "spec" / "axes.md"
VERSION_PATH = REPO / "VERSION"

# Toolkit artifacts that must carry a Toolkit-Version stamp matching /VERSION.
# (contracts/* are added at runtime via glob.) Absent files are skipped so the
# lint stays usable on partial checkouts.
VERSIONED_ARTIFACTS = [
    "spec/PNA_Spec.md", "spec/axes.md", "spec/use_cases.md", "spec/exceptions.md",
    "spec/constraints.md",
    "pna-build-eval-contrib/SKILL.md", "CONTRIBUTING.md", "README.md",
    "tools/lint-spec-ids.py", "tools/egress-lint.py", "tools/export-readable-lint.py",
    "tools/attestation-evidence-lint.py",
    "tools/evaluate-report.schema.json", "tools/swh-save.sh",
    "reference_designs/templates/TEMPLATE.md",
    "reference_designs/templates/ARCHITECTURE_TEMPLATE.md",
]


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
    """EX-* registry IDs from spec/exceptions.md. Empty if the file is absent."""
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
                    if len(row) > col and row[col] and row[col] not in STRENGTH_CLASSES:
                        violations.append(
                            f"strength-profile names unknown class '{row[col]}' "
                            f"(allowed: {', '.join(sorted(STRENGTH_CLASSES))})"
                        )
                    j += 1
                i = j
                continue
        i += 1
    return violations


def collect_constraint_ids() -> set[str]:
    """CST-* registry IDs from spec/constraints.md. Empty if the file is absent
    (the lint stays green on checkouts that haven't adopted constraints)."""
    if not CONSTRAINTS_PATH.exists():
        return set()
    return set(CST_RE.findall(CONSTRAINTS_PATH.read_text()))


def collect_axis_picks_by_axis() -> dict[str, set[str]]:
    """Map each axis-prefix (the token a constraint's Triggered-by uses, e.g.
    `storage`) to the set of pick IDs catalogued under that axis's section in
    axes.md. Per-axis (not a global pool) so a Triggered-by token must name a
    pick that actually belongs to the axis it cites."""
    by_axis: dict[str, set[str]] = {}
    if not AXES_PATH.exists():
        return by_axis
    text = AXES_PATH.read_text()
    heading_to_prefix = {h: p for p, h in AXIS_PREFIX_TO_HEADING.items()}
    # re.split keeps captured headings interleaved: [pre, head1, body1, ...].
    parts = AXES_SECTION_RE.split(text)
    for i in range(1, len(parts), 2):
        heading, body = parts[i].strip().lower(), parts[i + 1]
        prefix = heading_to_prefix.get(heading)
        if prefix:
            by_axis[prefix] = set(AXES_PICK_RE.findall(body))
    return by_axis


def _triggered_by_resolves(token: str, picks_by_axis: dict[str, set[str]]) -> bool:
    """A Triggered-by token `<axis>:<pick>` resolves iff the axis prefix is known
    AND the pick belongs to *that* axis — as an exact pick ID or a family prefix
    of one (so `distribution:web-bundle` matches `web-bundle-with-magic-link`).
    A pick from a different axis (`comms:opfs-sqlite-wasm`) does not resolve."""
    axis, sep, pick = token.partition(":")
    axis = axis.lower()
    if not sep or not pick or axis not in AXIS_PREFIX_TO_HEADING:
        return False
    picks = picks_by_axis.get(axis, set())
    return any(p == pick or p.startswith(pick + "-") for p in picks)


def _constraint_fields(triggered: str, bounds: str, frontier: str, detect: str) -> dict:
    """Normalize one entry's four field sources (registry-table cells, or the
    lines after the `**Field:**` labels in a detail block) into comparable
    tokens. Free-text prose around a value simply yields no extra tokens."""
    fm = FRONTIER_VALUE_RE.search(frontier or "")
    dm = DETECT_VALUE_RE.search(detect or "")
    return {
        "triggered": [t.lower() for t in TRIGGERED_TOKEN_RE.findall(triggered or "")],
        "bounds": [b.upper() if b.upper().startswith(("AC-", "PNA")) else b
                   for b in BOUNDS_TOKEN_RE.findall(bounds or "")],
        "frontier": fm.group(1).lower() if fm else None,
        "detect": dm.group(1).lower() if dm else None,
    }


def parse_constraint_table(text: str) -> dict[str, dict]:
    """The summary registry table, keyed by CST id → normalized fields. Columns:
    CST | Name | Triggered-by | Bounds | Frontier | Detectability."""
    out: dict[str, dict] = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("| CST-"):
            continue
        cells = [c.strip() for c in line.split("|")]  # ['', id, name, trig, bounds, front, detect, '']
        if len(cells) < 8:
            continue
        cid, _name, trig, bounds, front, detect = cells[1:7]
        out[cid] = _constraint_fields(trig, bounds, front, detect)
    return out


def parse_constraint_blocks(text: str) -> dict[str, dict]:
    """The per-constraint detail blocks (each opening with '### CST-...'), keyed
    by CST id → normalized fields plus `has_workaround`."""
    out: dict[str, dict] = {}
    parts = CST_BLOCK_RE.split(text)  # [pre, id1, body1, id2, body2, ...]

    def field_line(body: str, name: str) -> str:
        m = re.search(rf"(?mi)^\**{re.escape(name)}:\**[ \t]*(.*)$", body)
        return m.group(1).strip() if m else ""

    for i in range(1, len(parts), 2):
        cid, body = parts[i], parts[i + 1]
        fields = _constraint_fields(
            field_line(body, "Triggered-by"), field_line(body, "Bounds"),
            field_line(body, "Frontier"), field_line(body, "Detectability"),
        )
        fields["has_workaround"] = bool(re.search(r"(?mi)^\**Workaround:", body))
        out[cid] = fields
    return out


def _validate_constraint_fields(label: str, f: dict, picks_by_axis: dict,
                                known_bounds: set[str]) -> list[str]:
    """Shape-validate one entry's normalized fields (table row or detail block)."""
    v: list[str] = []
    for tok in f["triggered"]:
        if not _triggered_by_resolves(tok, picks_by_axis):
            v.append(f"{label}: Triggered-by names {tok!r}, not a pick of the named "
                     "axis in axes.md.")
    for tok in f["bounds"]:
        if tok == "PNA-DEFINITION" or re.fullmatch(r"Goal-[0-9]+", tok, re.IGNORECASE):
            continue
        if tok not in known_bounds:
            v.append(f"{label}: Bounds names {tok}, not a known AC, Goal-N, or PNA-DEFINITION.")
    if f["frontier"] is None:
        v.append(f"{label}: no well-formed 'Frontier:' "
                 "(Open|Mitigated|Solved-on-<platform>|Inherent).")
    elif (f["frontier"] == "mitigated" or f["frontier"].startswith("solved-on")) \
            and f.get("has_workaround") is False:
        v.append(f"{label}: Frontier '{f['frontier']}' requires a 'Workaround:' field.")
    if f["detect"] is None:
        v.append(f"{label}: no 'Detectability:' field.")
    elif f["detect"] not in DETECT_CLASSES:
        v.append(f"{label}: Detectability '{f['detect']}' is not one of "
                 f"{', '.join(sorted(DETECT_CLASSES))}.")
    return v


def collect_constraint_violations(spec_ids: set[str]) -> list[str]:
    """Shape-validate spec/constraints.md and keep its human-facing summary table
    honest against the authoritative detail blocks:
      - Triggered-by resolves to a pick of the *named* axis; Bounds tokens are
        valid; Frontier is well-formed (Mitigated/Solved-* need a Workaround);
        Detectability is a known class — checked on BOTH the table and the blocks.
      - the table and the blocks declare the same set of CST IDs, and agree on
        every field per entry (no silent table-vs-block drift).
    Absent file → no violations (the lint stays green on pre-constraints checkouts)."""
    if not CONSTRAINTS_PATH.exists():
        return []
    text = CONSTRAINTS_PATH.read_text()
    violations: list[str] = []
    picks_by_axis = collect_axis_picks_by_axis()
    known_bounds = spec_ids | {"PNA-DEFINITION"}
    table = parse_constraint_table(text)
    blocks = parse_constraint_blocks(text)

    # Registry table ↔ detail blocks: same set of IDs.
    for cid in sorted(table.keys() - blocks.keys()):
        violations.append(f"{cid}: in the registry table but has no '### {cid}' detail block.")
    for cid in sorted(blocks.keys() - table.keys()):
        violations.append(f"{cid}: has a detail block but no registry-table row.")

    for cid in sorted(table.keys() | blocks.keys()):
        if cid in table:
            violations += _validate_constraint_fields(
                f"{cid} (registry table)", table[cid], picks_by_axis, known_bounds)
        if cid in blocks:
            violations += _validate_constraint_fields(
                f"{cid} (detail block)", blocks[cid], picks_by_axis, known_bounds)
        if cid in table and cid in blocks:
            t, b = table[cid], blocks[cid]
            for field, what in (("triggered", "Triggered-by"), ("bounds", "Bounds")):
                if set(t[field]) != set(b[field]):
                    violations.append(
                        f"{cid}: {what} differs between the registry table "
                        f"({', '.join(t[field]) or '∅'}) and the detail block "
                        f"({', '.join(b[field]) or '∅'}).")
            for field, what in (("frontier", "Frontier"), ("detect", "Detectability")):
                if t[field] != b[field]:
                    violations.append(
                        f"{cid}: {what} differs between the registry table "
                        f"({t[field]}) and the detail block ({b[field]}).")
    return violations


def _parse_design_manifest(text: str) -> dict:
    """Parse the deliberately-simple subset of TOML a design.toml uses: comments
    (`#`), `[section]` headers, and `key = "quoted string"` lines. Returns a dict
    with top-level keys plus `flavor` and `verify` sub-dicts. Not a general TOML
    parser — the manifest format is ours and stays this simple so the lint needs
    no `tomllib` (py3.11+) and runs on any python3."""
    root: dict = {}
    section = root
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            section = root.setdefault(name, {})
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip()
        if val.startswith('"'):
            end = val.find('"', 1)
            val = val[1:end] if end != -1 else val[1:]
        else:  # bare value up to a trailing comment
            val = val.split("#", 1)[0].strip()
        section[key] = val
    return root


def collect_design_manifest_violations(spec_ids: set[str]) -> tuple[int, list[str]]:
    """Validate every reference_designs/<name>/design.toml — the conformance
    suite's machine-readable record. Returns (count, violations).

    Shape: required top keys; status/archival from their fixed vocab; toolkit
    version well-formed; [flavor] names a pick that resolves to the right axis in
    axes.md; [verify] runner is known. Honest-deferral rule: an `archived` design
    MUST carry a 40-hex commit, well-formed swhid_rev/swhid_dir with
    swhid_rev == swh:1:rev:<commit>, and a non-empty verify entrypoint; a
    `pending` (in-flight) design MAY leave those empty, but any value present MUST
    still be well-formed. Any design dir with an Architecture.md MUST have a
    manifest (an accepted design needs one)."""
    if not DESIGNS_PATH.exists():
        return 0, []
    picks_by_axis = collect_axis_picks_by_axis()
    violations: list[str] = []
    count = 0
    for sub in sorted(p for p in DESIGNS_PATH.iterdir() if p.is_dir()):
        if sub.name == "templates":
            continue
        manifest, arch = sub / "design.toml", sub / "Architecture.md"
        if not manifest.exists():
            if arch.exists():
                violations.append(
                    f"{sub.name}: has Architecture.md (an accepted design) but no design.toml.")
            continue
        count += 1
        label = f"{sub.name}/design.toml"
        m = _parse_design_manifest(manifest.read_text())

        for key in ("name", "repo", "toolkit_version", "status", "archival"):
            if not m.get(key):
                violations.append(f"{label}: missing required key '{key}'.")
        flavor, verify = m.get("flavor", {}), m.get("verify", {})
        if not isinstance(flavor, dict) or not flavor:
            violations.append(f"{label}: missing [flavor] table.")
        if not isinstance(verify, dict) or not verify:
            violations.append(f"{label}: missing [verify] table.")

        if (s := m.get("status")) and s not in DESIGN_STATUS:
            violations.append(f"{label}: status '{s}' not one of {sorted(DESIGN_STATUS)}.")
        archival = m.get("archival")
        if archival and archival not in DESIGN_ARCHIVAL:
            violations.append(f"{label}: archival '{archival}' not one of {sorted(DESIGN_ARCHIVAL)}.")
        if (tv := m.get("toolkit_version")) and not re.fullmatch(r"\d+\.\d+", tv):
            violations.append(f"{label}: toolkit_version '{tv}' is not MAJOR.MINOR.")

        for axis, pick in (flavor.items() if isinstance(flavor, dict) else []):
            axis_picks = picks_by_axis.get(axis)
            if axis_picks is None:
                violations.append(f"{label}: [flavor] names unknown axis '{axis}'.")
            elif pick not in axis_picks:
                violations.append(
                    f"{label}: [flavor] {axis} = '{pick}' is not a pick of that axis in axes.md.")
        if isinstance(verify, dict) and (r := verify.get("runner")) and r not in DESIGN_RUNNERS:
            violations.append(f"{label}: [verify] runner '{r}' not one of {sorted(DESIGN_RUNNERS)}.")

        # Field well-formedness (any present value must be valid, regardless of archival state).
        commit, srev, sdir = m.get("commit", ""), m.get("swhid_rev", ""), m.get("swhid_dir", "")
        if commit and not GIT_SHA_RE.match(commit):
            violations.append(f"{label}: commit '{commit}' is not a 40-hex git SHA.")
        if srev and not SWHID_REV_RE.match(srev):
            violations.append(f"{label}: swhid_rev '{srev}' is malformed (want swh:1:rev:<40-hex>).")
        if sdir and not SWHID_DIR_RE.match(sdir):
            violations.append(f"{label}: swhid_dir '{sdir}' is malformed (want swh:1:dir:<40-hex>).")
        if commit and srev and srev != f"swh:1:rev:{commit}":
            violations.append(f"{label}: swhid_rev does not match commit (want swh:1:rev:{commit}).")

        # Honest-deferral: an archived design must have the pin + a way to replicate.
        if archival == "archived":
            for key, val in (("commit", commit), ("swhid_rev", srev), ("swhid_dir", sdir)):
                if not val:
                    violations.append(f"{label}: archival='archived' requires '{key}'.")
            if not (isinstance(verify, dict) and verify.get("entrypoint")):
                violations.append(f"{label}: archival='archived' requires a [verify] entrypoint.")
    return count, violations


def expected_toolkit_minor() -> str | None:
    """The MAJOR.MINOR series from /VERSION (e.g. '0.1' from '0.1.0-draft')."""
    if not VERSION_PATH.exists():
        return None
    m = re.match(r"\s*(\d+\.\d+)", VERSION_PATH.read_text())
    return m.group(1) if m else None


def check_toolkit_versions() -> tuple[str | None, list[str]]:
    """Every versioned artifact must stamp a Toolkit-Version matching /VERSION."""
    failures: list[str] = []
    minor = expected_toolkit_minor()
    if minor is None:
        return None, ["/VERSION file missing or unparseable at repo root."]
    paths = [REPO / p for p in VERSIONED_ARTIFACTS]
    paths += [f for f in sorted((REPO / "contracts").glob("*"))
              if f.is_file() and f.name != "README.md"]
    for p in paths:
        if not p.is_file():
            continue
        head = "\n".join(p.read_text(errors="ignore").splitlines()[:30])
        m = TOOLKIT_VERSION_RE.search(head)
        rel = p.relative_to(REPO)
        if not m:
            failures.append(f"{rel}: missing 'Toolkit-Version: {minor}' stamp in head.")
        elif m.group(1) != minor:
            failures.append(f"{rel}: Toolkit-Version {m.group(1)} != /VERSION {minor}.")
    return minor, failures


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
        if "yes" in rev_values and not REVERSAL_FIELD_RE.search(ex_text):
            failures.append("exceptions.md: 'Reversible: yes' present but no 'Reversal:' field.")
        failures.extend(f"exceptions.md: {v}" for v in collect_strength_violations(ex_text))

    # --- Constraints (spec/constraints.md) ---
    constraint_ids = collect_constraint_ids()
    failures.extend(f"constraints.md: {v}" for v in collect_constraint_violations(spec_ids))

    # --- Reference-design manifests (reference_designs/<name>/design.toml) ---
    n_manifests, manifest_failures = collect_design_manifest_violations(spec_ids)
    failures.extend(manifest_failures)

    # --- Toolkit version stamps ---
    toolkit_minor, version_failures = check_toolkit_versions()
    failures.extend(version_failures)

    if failures:
        print(f"lint-spec-ids: {len(failures)} violation(s) found.")
        for line in failures:
            print(f"  - {line}")
        return 1

    n_realizing = sum(1 for v in contract_realizes.values() if v)
    print("lint-spec-ids: OK")
    print(f"  toolkit version {toolkit_minor} (/VERSION: {VERSION_PATH.read_text().strip()})")
    print(f"  spec defines {len(spec_ids)} AC IDs")
    print(f"  {n_realizing}/{len(contract_realizes)} contract files declare a 'Realizes:' header")
    print(f"  exceptions.md defines {len(exception_ids)} exception ID(s)")
    print(f"  constraints.md defines {len(constraint_ids)} constraint ID(s)")
    print(f"  reference designs: {n_manifests} design.toml manifest(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
