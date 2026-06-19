#!/usr/bin/env python3
# Toolkit-Version: 0.1
"""rearchive — re-archive an accepted reference design on Software Heritage and
refresh its toolkit manifest pin in one deterministic step.

Re-archival recurs every time an accepted reference design moves to a new commit
— a new release, or (as for prm) a re-pin after upstream spec changes land. By
hand it is a multi-step, drift-prone chore: compute the SWHIDs, request Save Code
Now, paste commit / swhid_rev / swhid_dir *consistently* into design.toml, refresh
the bundled Architecture.md + evaluate-report.json copies, and re-run the lint.
This tool does the deterministic, in-toolkit parts and prints paste-ready help for
the parts that need human judgement (the README / CHANGELOG narrative) or that live
in the design's own repo (tagging, the PR).

WHAT IT DOES (deterministic, all inside this toolkit repo):
  1. Reads reference_designs/<name>/design.toml for the canonical repo URL.
  2. Delegates to tools/swh-save.sh to request Save Code Now AND compute the
     git-compatible SWHIDs (swh:1:rev == commit, swh:1:dir == tree) from your local
     clone — one source of truth for the archival POST and the `^{commit}` peel.
  3. Refreshes the bundled Architecture.md + evaluate-report.json copies from the
     clone *at the archived ref* via `git show <ref>:<path>` (no checkout needed).
  4. Rewrites design.toml's commit / swhid_rev / swhid_dir and flips archival to
     "archived", preserving comments and column alignment.
  5. Runs tools/lint-spec-ids.py to cross-check the result (commit ↔ swhid_rev, …).

WHAT IT DOES NOT DO (left to you — paste-ready help is printed at the end):
  - Tag the design's own repo, or open the toolkit PR (cross-repo, policy-laden).
  - Rewrite the README archival bullet / CHANGELOG / index narrative (prose).
  - Regenerate a commit-stamped evaluate-report.json. The bundled report is copied
    as-committed at the ref; if its `candidate.commit` lags the pinned commit, a
    warning prints the exact regenerate recipe (the design's own [verify] emitter,
    run in a worktree at the ref). Regenerating is the design emitter's job, not
    this tool's — emitters and runners differ per design.

Usage:
  python3 tools/rearchive.py <design-name> <git-ref> <clone-path>
                             [--no-save] [--arch-src REL] [--report-src REL]

  <clone-path>   a local clone of the design's repo (needed for SWHIDs + copies).
  --no-save      skip the Save Code Now POST; compute + apply everything else
                 (equivalent to SWH_SAVE_NO_REQUEST=1 — offline / dry archival).
  --arch-src     repo-relative path to the canonical Architecture doc in the clone
                 (default: docs/Architecture.md).
  --report-src   repo-relative path to the emitted evaluate report in the clone
                 (default: docs/conformance/<[verify].emits_report>).

Exits 0 on success (lint clean), 1 on any error or a lint violation. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SWH_SAVE = REPO / "tools" / "swh-save.sh"
LINT = REPO / "tools" / "lint-spec-ids.py"

# The bare SWHID lines swh-save.sh prints under "SWHIDs for … :" (anchored so the
# `swhid_rev = "swh:1:rev:…"` paste-block line below it is NOT matched).
SWHID_LINE_RE = re.compile(r"^(swh:1:(rev|dir)):([0-9a-f]{40})$")


def fail(msg: str) -> "int":
    print(f"rearchive: error: {msg}", file=sys.stderr)
    return 1


def parse_manifest(text: str) -> dict:
    """The deliberately-simple subset of TOML a design.toml uses (comments,
    [section] headers, key = "quoted"). Mirrors tools/lint-spec-ids.py's parser so
    the two agree on the format; returns top-level keys plus sub-dicts."""
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


def run_swh_save(repo_url: str, ref: str, clone: str, *, save: bool) -> tuple[str, str, str]:
    """Delegate archival + SWHID computation to tools/swh-save.sh and parse the
    git-compatible SWHIDs it prints. Returns (commit, swhid_rev, swhid_dir).
    Raises RuntimeError if the SWHIDs can't be parsed (no clone / bad ref)."""
    env = dict(os.environ)
    if not save:
        env["SWH_SAVE_NO_REQUEST"] = "1"
    cp = subprocess.run(["bash", str(SWH_SAVE), repo_url, ref, clone],
                        capture_output=True, text=True, env=env)
    sys.stdout.write(cp.stdout)            # surface the archival request + SWHIDs verbatim
    if cp.stderr:
        sys.stderr.write(cp.stderr)
    if cp.returncode != 0:
        raise RuntimeError(f"swh-save.sh exited {cp.returncode}")
    rev = dir_ = None
    for line in cp.stdout.splitlines():
        m = SWHID_LINE_RE.match(line.strip())
        if m and m.group(2) == "rev":
            rev = m.group(3)
        elif m and m.group(2) == "dir":
            dir_ = m.group(3)
    if not rev or not dir_:
        raise RuntimeError(
            "swh-save.sh did not print git-compatible SWHIDs — a local clone with "
            f"the ref {ref!r} is required (got clone={clone!r}).")
    return rev, f"swh:1:rev:{rev}", f"swh:1:dir:{dir_}"


def git_show(clone: str, ref: str, rel: str) -> str | None:
    """The blob at <ref>:<rel> in the clone, or None if absent at that ref. Uses
    `git show` so no checkout/worktree is needed and the clone is left untouched."""
    cp = subprocess.run(["git", "-C", clone, "show", f"{ref}:{rel}"],
                        capture_output=True, text=True)
    return cp.stdout if cp.returncode == 0 else None


def set_manifest_value(lines: list[str], key: str, value: str) -> bool:
    """Replace the quoted value of a top-level `key = "…"` line in place,
    preserving alignment and any trailing comment. Returns True if found."""
    pat = re.compile(rf'^(\s*{re.escape(key)}\s*=\s*")[^"]*(".*)$')
    for i, ln in enumerate(lines):
        m = pat.match(ln)
        if m:
            lines[i] = f"{m.group(1)}{value}{m.group(2)}"
            return True
    return False


def update_manifest(text: str, commit: str, srev: str, sdir: str) -> str:
    """Rewrite commit / swhid_rev / swhid_dir and flip archival → archived,
    preserving comments + layout. Inserts the pin block after the `archival` line
    if a field is absent (a first-time pending → archived transition)."""
    lines = text.splitlines()
    set_manifest_value(lines, "archival", "archived")
    pins = {"commit": commit, "swhid_rev": srev, "swhid_dir": sdir}
    missing = {k: v for k, v in pins.items() if not set_manifest_value(lines, k, v)}
    if missing:
        # Insert after the archival line, aligned like the templates (commit + 4 sp).
        at = next((i for i, ln in enumerate(lines)
                   if re.match(r"^\s*archival\s*=", ln)), len(lines) - 1)
        block = [f'{k:<9}= "{v}"' for k, v in
                 (("commit", missing.get("commit", commit)),
                  ("swhid_rev", missing.get("swhid_rev", srev)),
                  ("swhid_dir", missing.get("swhid_dir", sdir))) if k in missing]
        lines[at + 1:at + 1] = [""] + block
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def refresh_copy(design_dir: Path, clone: str, ref: str, rel_src: str,
                 dst_name: str) -> str:
    """Copy <ref>:<rel_src> from the clone into design_dir/<dst_name>. Returns a
    status string for the summary (warns rather than fails on an absent source)."""
    content = git_show(clone, ref, rel_src)
    if content is None:
        return f"⚠ {dst_name}: {rel_src} not found at {ref} in the clone — refresh it by hand."
    (design_dir / dst_name).write_text(content, encoding="utf-8")
    return f"✓ {dst_name}: refreshed from {rel_src}@{ref}"


def check_report_stamp(design_dir: Path, dst_name: str, commit: str,
                       clone: str, ref: str, entrypoint: str, report_src: str) -> str | None:
    """If the refreshed report embeds a `candidate.commit` that lags the pinned
    commit, return a warning with the exact regenerate recipe; else None. (The
    report is committed *before* the merge it pins exists, so this often lags and
    is fixed only by re-running the design's own emitter at the ref.)"""
    path = design_dir / dst_name
    if not path.exists():
        return None
    try:
        embedded = json.loads(path.read_text()).get("candidate", {}).get("commit")
    except (ValueError, OSError):
        return None
    if not embedded or embedded == commit:
        return None
    return (
        f"⚠ {dst_name}: candidate.commit pins {embedded[:12]}, not the archived "
        f"{commit[:12]}.\n"
        f"    The report is committed before its own merge exists, so it lags. To stamp\n"
        f"    the archived commit, regenerate with the design's own emitter at the ref:\n"
        f"      git -C {clone} worktree add --detach /tmp/rearch {ref}\n"
        f"      ( cd /tmp/rearch && {entrypoint} )   # the [verify] emitter; writes {report_src}\n"
        f"      cp /tmp/rearch/{report_src} {path}\n"
        f"      git -C {clone} worktree remove --force /tmp/rearch")


def print_prose_stubs(name: str, repo_url: str, ref: str, commit: str,
                      srev: str, sdir: str) -> None:
    """Paste-ready prose + cross-repo commands for the steps this tool deliberately
    leaves to the human."""
    short = commit[:7]
    print("\n" + "─" * 72)
    print("NEXT — these are yours to do (prose + cross-repo); paste-ready below:\n")
    print(f"1. Tag the design repo at the archived commit (human-readable pin):")
    print(f'     git -C <clone> tag -a <tag> {commit} -m "…"  &&  git -C <clone> push origin <tag>\n')
    print(f"2. reference_designs/{name}/README.md — update the **Archival** bullet, e.g.:")
    print(f"     - **Archival:** `archival = \"archived\"` — source pinned at `{short}`:")
    print(f"       `{srev}`, `{sdir}` (computed via `tools/swh-save.sh`; Save Code Now ingest requested).\n")
    print(f"3. reference_designs/README.md — update the index line for `{name}/` to `{short}` / `{sdir}`.")
    print(f"4. CHANGELOG.md — ADD a new `###` entry at the top (do NOT rewrite prior archival history).")
    print(f"   If this commit lands a newly-accepted AC, add a 'Contributions to the spec' bullet too.\n")
    print(f"5. Commit the reference_designs/{name}/ + CHANGELOG changes on a branch and open the toolkit PR.")
    print("─" * 72)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="rearchive", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="reference design name (reference_designs/<name>/)")
    ap.add_argument("ref", help="git ref to pin (commit / tag / branch) in the design's repo")
    ap.add_argument("clone", help="path to a local clone of the design's repo")
    ap.add_argument("--no-save", action="store_true",
                    help="skip the Save Code Now POST (compute + apply everything else)")
    ap.add_argument("--arch-src", default="docs/Architecture.md",
                    help="repo-relative Architecture doc in the clone (default: docs/Architecture.md)")
    ap.add_argument("--report-src", default=None,
                    help="repo-relative emitted report in the clone "
                         "(default: docs/conformance/<emits_report>)")
    args = ap.parse_args(argv)

    design_dir = REPO / "reference_designs" / args.name
    manifest_path = design_dir / "design.toml"
    if not manifest_path.exists():
        return fail(f"no manifest at {manifest_path.relative_to(REPO)} — unknown design {args.name!r}.")
    if not Path(args.clone).is_dir():
        return fail(f"clone path {args.clone!r} is not a directory.")

    manifest = parse_manifest(manifest_path.read_text())
    repo_url = manifest.get("repo")
    if not repo_url:
        return fail(f"{args.name}/design.toml has no `repo` URL to archive.")
    verify = manifest.get("verify", {})
    emits = (verify.get("emits_report") if isinstance(verify, dict) else None) or "evaluate-report.json"
    entrypoint = (verify.get("entrypoint") if isinstance(verify, dict) else None) or "<verify entrypoint>"
    report_src = args.report_src or f"docs/conformance/{emits}"

    print(f"rearchive: {args.name} → {args.ref}  (repo {repo_url})\n")

    # 1–2. Archive + compute SWHIDs (single source of truth: swh-save.sh).
    try:
        commit, srev, sdir = run_swh_save(repo_url, args.ref, args.clone, save=not args.no_save)
    except RuntimeError as exc:
        return fail(str(exc))

    # 3. Refresh the bundled copies from the clone, at the archived ref.
    notes = [
        refresh_copy(design_dir, args.clone, args.ref, args.arch_src, "Architecture.md"),
        refresh_copy(design_dir, args.clone, args.ref, report_src, emits),
    ]
    stamp_warn = check_report_stamp(design_dir, emits, commit, args.clone, args.ref,
                                    entrypoint, report_src)

    # 4. Rewrite the manifest pin in place.
    manifest_path.write_text(update_manifest(manifest_path.read_text(), commit, srev, sdir))
    notes.append(f"✓ design.toml: pinned commit {commit[:12]}, swhid_rev/swhid_dir, archival=archived")
    notes.append("ⓘ design.toml: trailing comments on the pin lines are kept verbatim — "
                 "review them for staleness.")

    print("\nApplied:")
    for n in notes:
        print(f"  {n}")
    if stamp_warn:
        print("\n" + stamp_warn)

    # 5. Validate.
    print("\nValidating (tools/lint-spec-ids.py):")
    lint = subprocess.run([sys.executable, str(LINT)], capture_output=True, text=True)
    sys.stdout.write("  " + (lint.stdout or "").replace("\n", "\n  ").rstrip() + "\n")
    if lint.returncode != 0:
        sys.stderr.write(lint.stderr)
        return fail("lint-spec-ids reported violations (above) — review the manifest.")

    print_prose_stubs(args.name, repo_url, args.ref, commit, srev, sdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
