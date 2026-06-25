#!/usr/bin/env python3
# Toolkit-Version: 0.2
"""Self-tests for the PNA Toolkit's deterministic lints (Tier A of the conformance suite).

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

import json
import os
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
        # The strength-class check (collect_strength_violations) had no fault case —
        # the same dead-check rot that bit the Reversible: check in PR #18. It now
        # also guards the Countermeasure library's Strength column, so pin it here:
        # mutate the honeytoken catalog row's (unique) `recoverable-only` strength.
        name="exceptions: countermeasure-catalog Strength column off the EX-H8 vocabulary",
        file="spec/exceptions.md",
        old="| recoverable-only | environmental (Harden) |",
        new="| made-up-class | environmental (Harden) |",
        expect="strength-profile names unknown class",
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
        old="**Toolkit-Version:** 0.2",
        new="**Toolkit-Version:** 0.1",
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
        # The clean fellows manifest is now archival="archived" with valid SWHIDs and
        # a [verify] entrypoint (the Tier-0 keystone). To exercise the archived→requires-pin
        # check, this fault empties the commit — an archived design MUST carry its commit pin.
        name="manifest: archived design without its SWHID pin (honest-deferral)",
        file="reference_designs/fellows_local_db/design.toml",
        old='commit    = "15be80dedb22973d11651e8eb89b0611937ac5be"',
        new='commit    = ""',
        expect="requires 'commit'",
    ),
    dict(
        name="manifest: malformed SWHID value",
        file="reference_designs/fellows_local_db/design.toml",
        old='swhid_dir = "swh:1:dir:f139d27207eb6d814eaf031d374f9cfb795aba17"',
        new='swhid_dir = "swh:1:dir:not-a-real-hash"',
        expect="malformed",
    ),
    dict(
        # The 4-goal renumber is otherwise unguarded: a 'Serves' cell pointing at a goal
        # the spec no longer defines must fail loudly (check 9, collect_goal_ref_violations).
        name="goals: AC 'Serves' references an undefined goal",
        file="spec/PNA_Spec.md",
        old='| Goal 4 | <a id="ac-4"></a>AC-4 |',
        new='| Goal 9 | <a id="ac-4"></a>AC-4 |',
        expect="not a defined goal",
    ),
    dict(
        # The cardinality cap (one primary + at most one cross-cut): a third goal on one AC fails.
        name="goals: AC 'Serves' exceeds the two-goal cardinality cap",
        file="spec/PNA_Spec.md",
        old='| Goal 1, Goal 3 | <a id="ac-1"></a>AC-1 |',
        new='| Goal 1, Goal 2, Goal 3 | <a id="ac-1"></a>AC-1 |',
        expect="cardinality cap",
    ),
    dict(
        # The RZ traceability check (collect_realization_violations, check 10): a Layer-2
        # realization that realizes a nonexistent AC must fail loudly — the realization-layer
        # analog of the contract 'Realizes:' check. Mutates RZ-2's 'Realizes' cell.
        name="axes: an RZ realization realizes an AC the spec doesn't define",
        file="spec/axes.md",
        old='| AC-22 | `storage:opfs-sqlite-wasm`. | <a id="rz-2"></a>',
        new='| AC-999 | `storage:opfs-sqlite-wasm`. | <a id="rz-2"></a>',
        expect="not a defined AC",
    ),
    dict(
        # The user-mediation mechanism check (collect_user_mediation_violations, check 11):
        # a `Unifies:` AC the spec doesn't define must fail loudly — the third-mechanism
        # analog of the contract 'Realizes:' / RZ / CST-Bounds cross-reference checks.
        # Mutates the (unique) tail of user_mediation.md's `Unifies:` header.
        name="user-mediation: Unifies names an AC the spec doesn't define",
        file="spec/user_mediation.md",
        old="AC-21, AC-MCP-B",
        new="AC-21, AC-999",
        expect="not a defined AC",
    ),
    dict(
        # The un-relaxable floor (D3, check 5): an exception that relaxes a floor AC
        # (AC-18/19/MCP-B) is malformed and must fail loudly. EX-CLOUD-LLM relaxes only
        # PNA-DEFINITION + AC-MCP-A; injecting a floor AC into its Relaxes trips the check.
        name="exceptions: an exception relaxes an un-relaxable floor AC",
        file="spec/exceptions.md",
        old="**Relaxes:** PNA-DEFINITION, AC-MCP-A",
        new="**Relaxes:** PNA-DEFINITION, AC-MCP-A, AC-19",
        expect="un-relaxable floor",
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


def case_validate(results: list) -> None:
    """tools/validate.py (the `just validate` assembler) must (a) emit a report that
    passes the render contract, (b) exit 1 only when a deterministic check found a
    violation, and (c) honor the honesty contract from the validate design note: a
    CLEAN scan maps AC-1 to `unable-to-determine` (never `conformant`), a DIRTY scan
    to `non-conformant`. Reuses the egress fixtures as candidate inputs."""
    with tempfile.TemporaryDirectory() as td:
        for kind, fixture, want_status, want_code in (
            ("clean", "tools/egress-lint-fixtures/clean", "unable-to-determine", 0),
            ("dirty", "tools/egress-lint-fixtures/dirty", "non-conformant", 1),
        ):
            out = Path(td) / f"{kind}.json"
            cp = _run(REPO, "tools/validate.py", str(REPO / fixture), "--out", str(out))
            _record(results, f"validate: {kind} fixture exits {want_code}",
                    cp.returncode == want_code,
                    "" if cp.returncode == want_code else f"exit={cp.returncode}\n{cp.stdout}{cp.stderr}")
            rl = _run(REPO, "tools/report-fixtures-lint.py", str(out))
            _record(results, f"validate: {kind} report passes the render contract",
                    rl.returncode == 0, "" if rl.returncode == 0 else rl.stdout + rl.stderr)
            status = None
            if out.exists():
                acs = [f for f in json.loads(out.read_text())["findings"] if f["ac_id"] == "AC-1"]
                status = acs[0]["status"] if acs else None
            _record(results, f"validate: {kind} fixture -> AC-1 {want_status}",
                    status == want_status,
                    "" if status == want_status else f"got AC-1 status {status!r}")


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


def case_attestation_pytestmark(results: list) -> None:
    """A deferred test must not dodge the marker-state rule by hoisting its
    marker to a module-level `pytestmark` global. The dirty fixture cites such a
    test; the lint must name it (catching the file-wide xfail, not just decorators)."""
    d = _run(REPO, "tools/attestation-evidence-lint.py",
             "tools/attestation-evidence-lint-fixtures/dirty")
    out = d.stdout + d.stderr
    ok = d.returncode != 0 and "test_module_marked.py" in out and "xfail" in out
    _record(results, "attestation-evidence-lint: flags module-level pytestmark xfail",
            ok, "" if ok else f"exit={d.returncode}, missing pytestmark finding in:\n{out}")


def case_swh_save_annotated_tag(results: list) -> None:
    """swh-save.sh must report `swh:1:rev:` as the *commit*, not the annotated-tag
    object. `git rev-parse <annotated-tag>` returns the tag object's hash, but a
    SWH revision is the commit it points to. The bug (caught during the prm
    archival, toolkit PR #65) emitted a tag hash where a commit SHA belonged — a
    wrong-but-lint-clean SWHID, since swhid_rev still matched the (wrong) commit.
    This pins the `^{commit}` peel. The network POST is skipped via
    SWH_SAVE_NO_REQUEST so the test stays offline and never spams Save Code Now."""
    name = "swh-save.sh: annotated tag → rev is the commit, not the tag object"
    git = shutil.which("git")
    if git is None:
        _record(results, name + " (SKIP: no git)", True, "")
        return
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.x",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.x"}

    def g(repo: Path, *a: str) -> subprocess.CompletedProcess:
        return subprocess.run([git, "-C", str(repo), *a],
                              capture_output=True, text=True, env=env)

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "fixture"
        repo.mkdir()
        g(repo, "init", "-q")
        (repo / "f.txt").write_text("x\n")
        g(repo, "add", "f.txt")
        g(repo, "commit", "-q", "-m", "c")
        g(repo, "tag", "-a", "v-test", "-m", "rel")   # annotated — the bug's trigger
        commit = g(repo, "rev-parse", "v-test^{commit}").stdout.strip()
        tagobj = g(repo, "rev-parse", "v-test").stdout.strip()
        if not commit or commit == tagobj:
            _record(results, name, False,
                    "fixture did not produce an annotated tag (tag object == commit)")
            return
        cp = subprocess.run(
            ["bash", str(REPO / "tools/swh-save.sh"),
             "https://example.com/x", "v-test", str(repo)],
            capture_output=True, text=True,
            env={**env, "SWH_SAVE_NO_REQUEST": "1"},
        )
        out = cp.stdout + cp.stderr
        ok = (f"swh:1:rev:{commit}" in out) and (f"swh:1:rev:{tagobj}" not in out)
        _record(results, name, ok, "" if ok else
                f"expected swh:1:rev:{commit} (commit), not the tag object {tagobj}; got:\n{out}")


def case_swh_save_ref_not_found(results: list) -> None:
    """swh-save.sh must distinguish "no clone given" from "clone given but the ref
    doesn't resolve in it". The old code printed "No local clone provided" for BOTH,
    sending a maintainer hunting for a clone they had already passed — when the real
    cause was a tag-name typo ('pnt-ref-0.2.0' vs the actual 'pnt-ref-0.2'). Pin the
    ref-not-found branch: a real clone + a bogus ref names the missing ref and does
    NOT print the no-clone message. Offline via SWH_SAVE_NO_REQUEST."""
    name = "swh-save.sh: clone present but ref absent → names the ref, not 'no clone'"
    git = shutil.which("git")
    if git is None:
        _record(results, name + " (SKIP: no git)", True, "")
        return
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.x",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.x"}

    def g(repo: Path, *a: str) -> subprocess.CompletedProcess:
        return subprocess.run([git, "-C", str(repo), *a],
                              capture_output=True, text=True, env=env)

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "fixture"
        repo.mkdir()
        g(repo, "init", "-q")
        (repo / "f.txt").write_text("x\n")
        g(repo, "add", "f.txt")
        g(repo, "commit", "-q", "-m", "c")
        cp = subprocess.run(
            ["bash", str(REPO / "tools/swh-save.sh"),
             "https://example.com/x", "pnt-ref-0.2.0", str(repo)],  # a ref that does NOT exist
            capture_output=True, text=True,
            env={**env, "SWH_SAVE_NO_REQUEST": "1"},
        )
        out = cp.stdout + cp.stderr
        ok = ("has no ref" in out) and ("No local clone provided" not in out)
        _record(results, name, ok, "" if ok else
                "expected a 'has no ref' message and NOT 'No local clone provided'; "
                f"got:\n{out}")


def case_loopback_advisory(results: list) -> None:
    """Pin the L1-gates / L2-advisory split (the soft-spot fix): the no-auth fixture
    is an L2 advisory that does NOT gate by default (exit 0, but reported), and DOES
    gate under --strict (exit 1). A heuristic must neither silently fail CI nor
    silently vanish — so both halves are asserted, not just the L1 clean/dirty pair."""
    base = "tools/loopback-surface-lint-fixtures/noauth"
    d = _run(REPO, "tools/loopback-surface-lint.py", base)
    out = d.stdout + d.stderr
    ok = d.returncode == 0 and "[L2]" in out and "advisory" in out.lower()
    _record(results, "loopback-surface-lint: L2 is advisory (no gate) by default", ok,
            "" if ok else f"exit={d.returncode}, expected exit 0 + an [L2] advisory in:\n{out}")
    s = _run(REPO, "tools/loopback-surface-lint.py", base, "--strict")
    out2 = s.stdout + s.stderr
    ok2 = s.returncode != 0 and "[L2]" in out2
    _record(results, "loopback-surface-lint: --strict promotes L2 to a gating error", ok2,
            "" if ok2 else f"exit={s.returncode}, expected exit 1 + [L2] in:\n{out2}")


def case_rearchive_offline(results: list) -> None:
    """tools/rearchive.py end-to-end, offline (--no-save): against a throwaway design
    clone it must rewrite the named design's design.toml pin (commit / swhid_rev /
    swhid_dir + archival=archived), refresh the bundled Architecture.md copy from the
    clone at the ref, WARN when the report's candidate.commit lags the pinned commit,
    and leave the manifest lint-clean. Runs from a copy of the repo so the real
    reference_designs/ is never mutated; the Save Code Now POST is skipped (offline)."""
    name = "rearchive.py: offline re-pin + copy refresh + stale-report warning"
    git = shutil.which("git")
    if git is None:
        _record(results, name + " (SKIP: no git)", True, "")
        return
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.x",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.x"}

    def g(repo: Path, *a: str) -> subprocess.CompletedProcess:
        return subprocess.run([git, "-C", str(repo), *a], capture_output=True, text=True, env=env)

    with tempfile.TemporaryDirectory() as td:
        # (a) a throwaway "design clone" carrying the canonical paths rearchive reads.
        clone = Path(td) / "clone"
        (clone / "docs" / "conformance").mkdir(parents=True)
        (clone / "docs" / "Architecture.md").write_text("# Fixture Architecture\nMARKER-9173\n")
        (clone / "docs" / "conformance" / "evaluate-report.json").write_text(
            json.dumps({"candidate": {"commit": "0" * 40}, "findings": []}))  # stamp lags on purpose
        g(clone, "init", "-q")
        g(clone, "add", "-A")
        g(clone, "commit", "-q", "-m", "fixture")
        commit = g(clone, "rev-parse", "HEAD^{commit}").stdout.strip()
        tree = g(clone, "rev-parse", "HEAD^{tree}").stdout.strip()
        if not commit or not tree:
            _record(results, name, False, "fixture clone produced no commit/tree")
            return

        # (b) run rearchive from a COPY of the toolkit repo, re-pinning the prm design.
        root = Path(td) / "repo"
        shutil.copytree(REPO, root, ignore=IGNORE)
        cp = subprocess.run(
            [PY, str(root / "tools/rearchive.py"), "prm", commit, str(clone), "--no-save"],
            capture_output=True, text=True, cwd=str(root), env=env)
        out = cp.stdout + cp.stderr
        manifest = (root / "reference_designs/prm/design.toml").read_text()
        arch = root / "reference_designs/prm/Architecture.md"
        checks = {
            "exit 0": cp.returncode == 0,
            "commit pinned": f'"{commit}"' in manifest,
            "swhid_rev pinned": f"swh:1:rev:{commit}" in manifest,
            "swhid_dir pinned": f"swh:1:dir:{tree}" in manifest,
            "archival=archived": 'archival = "archived"' in manifest,
            "Architecture refreshed from clone": arch.exists() and "MARKER-9173" in arch.read_text(),
            "stale-report warning emitted": "candidate.commit pins" in out,
            "manifest stays lint-clean": "lint-spec-ids: OK" in out,
        }
        failed = [k for k, v in checks.items() if not v]
        _record(results, name, not failed,
                "" if not failed else f"unmet: {failed}\n--- rearchive output ---\n{out}")


def case_realization_index(results: list) -> None:
    """tools/realization-index.py (the `just realization-index` generator) must:
    (a) emit a model with the designs + ACs and NO extraction warts — no HTTP route
    (`/api/...`) or doc link (`*.md`) leaking into a realization pointer, and no bare
    `::name` test continuation left unresolved in a verification ref; (b) report the
    committed docs/realization-index.md as current (`--check` → 0); and (c) flag a STALE
    index (`--check` → 1) — the lockfile-style drift gate `just ci` runs."""
    j = _run(REPO, "tools/realization-index.py", "--json")
    model = json.loads(j.stdout) if j.returncode == 0 else {}
    _record(results, "realization-index: emits a model (>=2 designs)",
            j.returncode == 0 and len(model.get("designs", [])) >= 2,
            "" if j.returncode == 0 else j.stdout + j.stderr)
    pts = [p for rs in model.get("acs", {}).values() for r in rs for p in r["realization"]]
    vers = [v for rs in model.get("acs", {}).values() for r in rs for v in r["verification"]]
    clean = (not any(p.startswith("/") for p in pts)
             and not any(p.lower().endswith((".md", ".txt", ".rst")) for p in pts)
             and not any(v.startswith("::") for v in vers))
    _record(results, "realization-index: no route/doc/::-continuation extraction warts",
            clean, "a route/doc pointer or an unstitched `::` continuation leaked through")
    c = _run(REPO, "tools/realization-index.py", "--check")
    _record(results, "realization-index: committed index is current (--check → 0)",
            c.returncode == 0, "" if c.returncode == 0 else c.stdout + c.stderr)
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / "repo"
        shutil.copytree(REPO, dst, ignore=IGNORE)
        idx = dst / "docs" / "realization-index.md"
        idx.write_text(idx.read_text() + "\nstale drift\n", encoding="utf-8")
        s = _run(dst, "tools/realization-index.py", "--check")
        _record(results, "realization-index: stale index fails --check (drift gate)",
                s.returncode != 0 and "stale" in (s.stdout + s.stderr).lower(),
                "" if s.returncode != 0 else "a stale index was not flagged")


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
    case_fixture_lint(results, "tools/report-fixtures-lint.py",
                      "tools/report-viewer/sample-reports",
                      "tools/report-fixtures-lint-fixtures/dirty")
    case_fixture_lint(results, "tools/loopback-surface-lint.py",
                      "tools/loopback-surface-lint-fixtures/clean",
                      "tools/loopback-surface-lint-fixtures/dirty")
    case_loopback_advisory(results)
    case_validate(results)
    case_attestation_marker_message(results)
    case_attestation_pytestmark(results)
    case_swh_save_annotated_tag(results)
    case_swh_save_ref_not_found(results)
    case_rearchive_offline(results)
    case_realization_index(results)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"\nlint-selftest: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
