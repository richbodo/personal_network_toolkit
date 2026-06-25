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
     IDs, or the PNA-DEFINITION sentinel — and names no un-relaxable-floor AC
     (AC-18/19/MCP-B; § Scope discipline): a floor AC in a Relaxes is a malformed
     exception, since the floor may not be relaxed even with consent.
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
  9. Every 'Goal N' reference resolves to a goal the spec defines (a '### Goal N'
     heading in PNA_Spec.md), checked on the AC table's 'Serves' column, constraints'
     'Bounds:', and exceptions' 'Stresses:'; and no AC's 'Serves' names more than two
     goals (the primary + at-most-one-cross-cut cardinality cap).
  10. Every RZ-* realization in spec/axes.md (a row in a table with an 'RZ' ID
     column) names the AC(s) it realizes in a 'Realizes' column, and each named AC
     is a defined AC — the realization-layer analog of the contract 'Realizes:'
     check. A realization is Layer 2 and is never itself an AC (it carries no AC-*
     ID); it must point up at the Layer-1 commitment it realizes.
  11. The user-mediation mechanism (spec/user_mediation.md — the third general
     mechanism, alongside Exceptions and Constraints): every AC named in its
     'Unifies:' header resolves to a defined AC (so a renamed/retired AC cannot
     silently dangle the mechanism). UM-1/2/3 property IDs are counted for the summary.

The lint validates the *shape* of declarations (presence + ID/vocabulary/
version resolution), not their behavioral correctness — that is the LLM
evaluate flow's job (see pna-toolkit/SKILL.md § Evaluate flow).

Exits 0 if clean, 1 if any violation found. Designed to be CI-friendly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# A table-cell ID may be preceded by a stable deep-link anchor
# (`<a id="ac-1"></a>AC-1`) so reference-design conformance reports can link to a
# specific row. ID columns are located by HEADER NAME, not position, so the ID
# can sit in any column (it lives in the last column as of the readability pass);
# see iter_tables() / _ids_by_header() below.
ANCHOR_PREFIX = re.compile(r'<a id="[^"]*"></a>\s*')
AC_ID_RE = re.compile(r"AC-[A-Z0-9-]+")
EX_ID_RE = re.compile(r"EX-[A-Z0-9-]+")
CST_ID_RE = re.compile(r"CST-[A-Z0-9-]+")
UM_ID_RE = re.compile(r"UM-[0-9]+")
REALIZES_RE = re.compile(r"Realizes:\s*((?:AC-[A-Z0-9-]+(?:\s*,\s*)?)+)", re.IGNORECASE)

# ID-column headers per family (lowercased). The PNA_Spec AC table heads its ID
# column "ID"; the axes AC tables head theirs "AC"; the registries use "EX"/"CST".
# Handler-clause IDs (EX-H1..EX-H8) are list items, not table rows, so they are
# deliberately never collected as registry exceptions.
AC_ID_HEADERS = {"id", "ac"}
EX_ID_HEADERS = {"ex"}
CST_ID_HEADERS = {"cst"}
# User-mediation property IDs (UM-1/2/3) live in the "UM" column of the contract
# table in spec/user_mediation.md; the mechanism's `Unifies:` header (below) names
# the ACs it is the named invariant beneath.
UM_ID_HEADERS = {"um"}
# Realizations (Layer 2) carry their own RZ-* family in axes.md, in tables headed
# with an "RZ" ID column + a "Realizes" column. They are deliberately NOT collected
# as ACs (RZ-* does not match AC_ID_RE), so the AC collector skips them; the RZ
# traceability check (collect_realization_violations) validates them instead.
RZ_ID_RE = re.compile(r"RZ-[0-9]+")
RZ_ID_HEADERS = {"rz"}
# Inverse of REALIZES_RE. Tokens may be AC-*, EX-*, or the PNA-DEFINITION
# sentinel (the PNA definition is prose in vocab-pna, not an `| AC-X |` row).
# `\**` tolerates the markdown-bold field form (`**Relaxes:** PNA-DEFINITION, …`)
# the same way REVERSIBLE_RE does; without it this matched only the backtick
# *example* in § Header conventions, never a real exception's bold `**Relaxes:**`
# field — so the floor / not-known checks below never saw the actual tokens.
RELAXES_RE = re.compile(
    r"Relaxes:\**\s*((?:(?:AC-[A-Z0-9-]+|EX-[A-Z0-9-]+|PNA-DEFINITION)(?:\s*,\s*)?)+)",
    re.IGNORECASE,
)
# The `Unifies:` header in spec/user_mediation.md names the AC-* commitments the
# user-mediation mechanism is the named invariant beneath — the third-mechanism
# analog of a contract's `Realizes:` / a constraint's `Bounds:`. AC tokens only.
UNIFIES_RE = re.compile(r"Unifies:\**\s*((?:AC-[A-Z0-9-]+(?:\s*,\s*)?)+)", re.IGNORECASE)
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
# The un-relaxable floor (spec/exceptions.md § Scope discipline): guarantees no
# exception may relax, even with consent. An exception that names a floor AC in its
# `Relaxes:` header is malformed. Charter members — keep in sync with § Scope discipline.
FLOOR_ACS = {"AC-18", "AC-19", "AC-MCP-B"}

# --- Constraints (spec/constraints.md) ---
# Constraint registry IDs are read from the "CST" column of the registry table
# (see CST_ID_HEADERS / iter_tables). Detail blocks open with a '### CST-...' heading.
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
USER_MEDIATION_PATH = REPO / "spec" / "user_mediation.md"
AXES_PATH = REPO / "spec" / "axes.md"
VERSION_PATH = REPO / "VERSION"

# Toolkit artifacts that must carry a Toolkit-Version stamp matching /VERSION.
# (contracts/* are added at runtime via glob.) Absent files are skipped so the
# lint stays usable on partial checkouts.
VERSIONED_ARTIFACTS = [
    "spec/PNA_Spec.md", "spec/axes.md", "spec/use_cases.md", "spec/exceptions.md",
    "spec/constraints.md", "spec/user_mediation.md",
    "pna-toolkit/SKILL.md", "CONTRIBUTING.md", "README.md",
    "tools/lint-spec-ids.py", "tools/egress-lint.py", "tools/export-readable-lint.py",
    "tools/attestation-evidence-lint.py", "tools/loopback-surface-lint.py", "tools/validate.py",
    "tools/evaluate-report.schema.json", "tools/swh-save.sh", "tools/rearchive.py",
    "tools/realization-index.py",
    "reference_designs/templates/TEMPLATE.md",
    "reference_designs/templates/ARCHITECTURE_TEMPLATE.md",
]


def _split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", line)) and "-" in line


def iter_tables(text: str):
    """Yield (headers_lowercased, [data_row_cells, …]) for every GitHub-flavored
    markdown table. The basis for all header-aware (column-order-independent)
    table parsing in this lint."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if (lines[i].lstrip().startswith("|") and i + 1 < len(lines)
                and _is_table_sep(lines[i + 1])):
            headers = [h.lower() for h in _split_cells(lines[i])]
            rows, j = [], i + 2
            while (j < len(lines) and lines[j].lstrip().startswith("|")
                   and not _is_table_sep(lines[j])):
                rows.append(_split_cells(lines[j]))
                j += 1
            yield headers, rows
            i = j
        else:
            i += 1


def _ids_by_header(text: str, id_headers: set[str], id_re) -> set[str]:
    """IDs read from whichever column is headed by one of `id_headers`, in every
    table that has such a column. Anchor prefix stripped; column order-agnostic.
    Tables without that header (Slots, Interfaces, strength profiles, …) are
    skipped, so an ID mentioned in a prose cell is never miscollected."""
    out: set[str] = set()
    for headers, rows in iter_tables(text):
        col = next((k for k, h in enumerate(headers) if h in id_headers), None)
        if col is None:
            continue
        for cells in rows:
            if col < len(cells):
                m = id_re.match(ANCHOR_PREFIX.sub("", cells[col]))
                if m:
                    out.add(m.group(0))
    return out


def collect_spec_ac_ids() -> set[str]:
    """All AC IDs from the AC tables in the spec (PNA_Spec.md + axes.md)."""
    ids: set[str] = set()
    for path in (REPO / "spec" / "PNA_Spec.md", REPO / "spec" / "axes.md"):
        if not path.exists():
            print(f"FAIL: spec file missing: {path}")
            sys.exit(1)
        ids |= _ids_by_header(path.read_text(), AC_ID_HEADERS, AC_ID_RE)
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


def collect_realization_violations(spec_ac_ids: set[str]) -> tuple[int, list[str]]:
    """The realization-layer analog of the contract 'Realizes:' check. Every RZ-*
    row in spec/axes.md (a table with an 'RZ' ID column) MUST name the AC(s) it
    realizes in a 'Realizes' column, and each named AC MUST be defined in the spec.
    A realization is Layer 2 and never an AC, so it points *up* at the Layer-1
    commitment it realizes. Returns (count, violations). Absent axes.md → (0, [])."""
    if not AXES_PATH.exists():
        return 0, []
    text = AXES_PATH.read_text()
    violations: list[str] = []
    count = 0
    for headers, rows in iter_tables(text):
        rz_col = next((k for k, h in enumerate(headers) if h in RZ_ID_HEADERS), None)
        if rz_col is None:
            continue
        realizes_col = next((k for k, h in enumerate(headers) if h == "realizes"), None)
        for cells in rows:
            if rz_col >= len(cells):
                continue
            m = RZ_ID_RE.match(ANCHOR_PREFIX.sub("", cells[rz_col]))
            if not m:
                continue
            rz = m.group(0)
            count += 1
            if realizes_col is None or realizes_col >= len(cells):
                violations.append(f"axes.md: {rz} has no 'Realizes' column naming the AC it realizes.")
                continue
            realized = AC_ID_RE.findall(cells[realizes_col])
            if not realized:
                violations.append(f"axes.md: {rz} 'Realizes' names no AC.")
            for ac in realized:
                if ac not in spec_ac_ids:
                    violations.append(f"axes.md: {rz} realizes {ac}, which is not a defined AC.")
    return count, violations


def collect_exception_ids() -> set[str]:
    """EX-* registry IDs from spec/exceptions.md. Empty if the file is absent."""
    if not EXCEPTIONS_PATH.exists():
        return set()
    return _ids_by_header(EXCEPTIONS_PATH.read_text(), EX_ID_HEADERS, EX_ID_RE)


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
    return _ids_by_header(CONSTRAINTS_PATH.read_text(), CST_ID_HEADERS, CST_ID_RE)


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
    """The summary registry table, keyed by CST id → normalized fields. Columns
    are located by header name (CST / Triggered-by / Bounds / Frontier /
    Detectability), so their order in the table doesn't matter."""
    out: dict[str, dict] = {}
    for headers, rows in iter_tables(text):
        idx = {h: k for k, h in enumerate(headers)}
        if "cst" not in idx:
            continue

        def cell(cells, name, idx=idx):
            k = idx.get(name)
            return cells[k] if k is not None and k < len(cells) else ""

        for cells in rows:
            m = CST_ID_RE.match(ANCHOR_PREFIX.sub("", cell(cells, "cst")))
            if not m:
                continue
            out[m.group(0)] = _constraint_fields(
                cell(cells, "triggered-by"), cell(cells, "bounds"),
                cell(cells, "frontier"), cell(cells, "detectability"))
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


def collect_user_mediation_violations(spec_ac_ids: set[str]) -> tuple[int, list[str]]:
    """spec/user_mediation.md defines the user-mediation mechanism (the third general
    mechanism, alongside Exceptions and Constraints): the always-on actuation invariant
    UM-1/2/3 beneath the action / egress ACs. Shape checks (the lint validates shape,
    not behavior):
      - every AC named in a `Unifies:` header resolves to a defined AC — the
        third-mechanism analog of the contract `Realizes:` / RZ realizes / CST `Bounds:`
        cross-reference, so a renamed or retired AC cannot silently dangle the mechanism;
      - at least one `Unifies:` header is present naming >=1 AC.
    Returns (UM-* property count, violations). Absent file -> (0, []) so the lint stays
    green on checkouts that haven't adopted the mechanism."""
    if not USER_MEDIATION_PATH.exists():
        return 0, []
    text = USER_MEDIATION_PATH.read_text()
    violations: list[str] = []
    um_ids = _ids_by_header(text, UM_ID_HEADERS, UM_ID_RE)
    unifies_acs: list[str] = []
    for m in UNIFIES_RE.finditer(text):
        unifies_acs.extend(AC_ID_RE.findall(m.group(1)))
    if not unifies_acs:
        violations.append("no 'Unifies:' header naming the AC(s) the mechanism is the "
                          "named invariant beneath.")
    for ac in unifies_acs:
        if ac not in spec_ac_ids:
            violations.append(f"Unifies names {ac}, which is not a defined AC.")
    return len(um_ids), violations


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


GOAL_HEADING_RE = re.compile(r"^### Goal (\d+)\b", re.MULTILINE)
GOAL_REF_RE = re.compile(r"Goal[- ](\d+)")


def collect_defined_goals() -> set[int]:
    """The goal numbers the spec defines via '### Goal N' headings in PNA_Spec.md."""
    spec = REPO / "spec" / "PNA_Spec.md"
    if not spec.exists():
        return set()
    return {int(n) for n in GOAL_HEADING_RE.findall(spec.read_text())}


def collect_goal_ref_violations(defined: set[int]) -> list[str]:
    """Every 'Goal N' the spec references resolves to a *defined* goal, and no AC's
    'Serves' cell names more than two goals (the primary + at-most-one-cross-cut
    cardinality cap, per PNA_Spec.md § Goals). This guards the goal layer against a
    botched renumber: a Serves / Bounds / Stresses reference pointing at a goal that no
    longer exists would otherwise pass silently."""
    spec = REPO / "spec" / "PNA_Spec.md"
    if not spec.exists():
        return []
    if not defined:
        return ["PNA_Spec.md: no '### Goal N' headings found — cannot validate goal references."]

    out: list[str] = []

    def check_refs(label: str, text: str) -> int:
        nums = [int(n) for n in GOAL_REF_RE.findall(text)]
        for n in nums:
            if n not in defined:
                out.append(f"{label}: references Goal {n}, not a defined goal "
                           f"(defined: {sorted(defined)}).")
        return len(nums)

    # AC-table 'Serves' column (PNA_Spec.md): every ref resolves + the cardinality cap.
    for headers, rows in iter_tables(spec.read_text()):
        serves_col = next((k for k, h in enumerate(headers) if h == "serves"), None)
        if serves_col is None:
            continue
        id_col = next((k for k, h in enumerate(headers) if h in AC_ID_HEADERS), None)
        for cells in rows:
            if serves_col >= len(cells):
                continue
            acid = "?"
            if id_col is not None and id_col < len(cells):
                m = AC_ID_RE.match(ANCHOR_PREFIX.sub("", cells[id_col]))
                acid = m.group(0) if m else "?"
            if check_refs(f"PNA_Spec.md Serves [{acid}]", cells[serves_col]) > 2:
                out.append(f"PNA_Spec.md Serves [{acid}]: names more than two goals; the "
                           "cardinality cap is two (one primary + at most one cross-cut).")

    # Goal refs in the dual mechanisms: constraints 'Bounds:', exceptions 'Stresses:'.
    for path, field in ((CONSTRAINTS_PATH, "Bounds"), (EXCEPTIONS_PATH, "Stresses")):
        if path.exists():
            for m in re.finditer(rf"(?mi)^\**{field}:[^\n]*", path.read_text()):
                check_refs(f"{path.name} {field}", m.group(0))
    return out


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

    # --- Realizations (the RZ-* family in spec/axes.md) ---
    n_realizations, realization_failures = collect_realization_violations(spec_ids)
    failures.extend(realization_failures)

    # --- Exceptions (spec/exceptions.md) ---
    exception_ids = collect_exception_ids()
    known = spec_ids | exception_ids | {"PNA-DEFINITION"}
    for tok in collect_relaxes():
        if tok not in known:
            failures.append(
                f"exceptions.md: Relaxes names {tok}, which is not a known AC, EX, "
                "or PNA-DEFINITION."
            )
        elif tok in FLOOR_ACS:
            failures.append(
                f"exceptions.md: Relaxes names {tok}, an un-relaxable floor AC that no "
                "exception may relax, even with consent (the un-relaxable floor, "
                "spec/exceptions.md § Scope discipline) — the exception is malformed."
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

    # --- User-mediation (spec/user_mediation.md) — the third general mechanism ---
    n_um, um_failures = collect_user_mediation_violations(spec_ids)
    failures.extend(f"user_mediation.md: {v}" for v in um_failures)

    # --- Goal references (the goal layer; guards the renumber) ---
    defined_goals = collect_defined_goals()
    failures.extend(collect_goal_ref_violations(defined_goals))

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
    print(f"  spec defines {len(defined_goals)} goal(s) and {len(spec_ids)} AC IDs")
    print(f"  {n_realizing}/{len(contract_realizes)} contract files declare a 'Realizes:' header")
    print(f"  axes.md defines {n_realizations} realization (RZ-*) ID(s)")
    print(f"  exceptions.md defines {len(exception_ids)} exception ID(s)")
    print(f"  constraints.md defines {len(constraint_ids)} constraint ID(s)")
    print(f"  user_mediation.md defines {n_um} user-mediation property ID(s)")
    print(f"  reference designs: {n_manifests} design.toml manifest(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
