# prm

**Maintainer:** Rich Bodo (https://github.com/richbodo/prm)
**License:** see upstream repo
**Validated against:** Toolkit-Version 0.1, 2026-06-10
**Status:** active

## Acceptance & validation

- **Accepted:** 2026-06-10 · accepted-by Rich Bodo (maintainer) · validated against Toolkit-Version 0.1. The merge of [PR #61](https://github.com/richbodo/personal_network_toolkit/pull/61) is the acceptance; this line is the durable record of what was validated.
- **Validated against:** Toolkit-Version 0.1. The AC attestation — universal + conditional, the
  `EX-CLOUD-LLM` exception, and the `UM-1/2/3` user-mediation rows — is in [`Architecture.md`](Architecture.md);
  every `conformant` row's Verification cites a real, passing test, and the design's own evidence lint
  (`tests/conformance/test_attestation_has_evidence.py`) gates it.
- **Posture:** [`evaluate-report.json`](evaluate-report.json) — deterministically emitted from the attestation
  table by `scripts/evaluate_report.py` and satisfying the toolkit's [`report-fixtures-lint.py`](../../tools/report-fixtures-lint.py)
  render contract — is **conformant** for the declared flavor: 12 conformant, 2 partial-conformance
  (flagged for human review: `AC-20`, `AC-MCP-A` — consent + signaling, because an MCP server cannot
  identify the consuming LLM), 4 not-applicable (`comms:none`) across 18 evaluated ACs.
- **Archival:** `archival = "archived"` — source pinned at `prm@pnt-ref-0.1.2` (`7bd4a28`, PR [#60](https://github.com/richbodo/prm/pull/60),
  which adds `path:symbol` realization pointers → 100% realization-pointer coverage; supersedes the `pnt-ref-0.1.1` / `1551896`
  snapshot): `swh:1:rev:7bd4a28106f2496e0fd7548e0b6be5e2bb593089`,
  `swh:1:dir:87d3d263759092a46f9459d95234cd2cedc6edfb` (computed via `tools/swh-save.sh`). The Save Code Now request for
  `7bd4a28` was **submitted 2026-06-19** (origin-save request `2368290`); the prior request (2026-06-18) covered `1551896`.
  Identifiers are content-addressed and resolve once ingest completes. The `[verify].entrypoint` is `just conformance` in the canonical repo.

## Summary

`prm` is the **second PNT reference design** — a local-only **Personal Relationship Manager** that mirrors a
person's contacts from everywhere they're scattered (Google, Apple, LinkedIn, Facebook, loose vCard/CSV) into
one store they own, **deduplicates** them, and lets an AI *propose* merges the human applies. It is the first
design to exercise the **multi-source dedup** contract (`AC-PRM-B`) and the **native-sqlite-via-filesystem**
substrate (`RZ-5`), and the first **build-from-verifiable-source** distribution demonstrator. The canonical
repo is https://github.com/richbodo/prm; its Architecture document lives at `docs/Architecture.md` upstream.

## Axis picks at first acceptance

`distribution:never-distributed-single-user + storage:native-sqlite-via-filesystem + ingestion:multi-source-merge-with-dedup + workspace-shell:vanilla-js-spa + comms:none + mcp-exposure:shared-only`

## Contributions to the spec

This submission rides five spec changes, each demonstrated by working code in the canonical repo:

- **`comms: none` pick** (`spec/axes.md`): a PNA whose loop stops at *recording* relationship data — no
  outreach surface. PRM is the demonstrator.
- **Distribution-axis verifiability split** ([#39](https://github.com/richbodo/personal_network_toolkit/issues/39) ⇄ [prm#8](https://github.com/richbodo/prm/issues/8)):
  `never-distributed-single-user` collapses *build-from-verifiable-source* with *opaque-binary* delivery; they
  differ in **independent verifiability**. PRM is the build-from-source case — a friend clones, builds, and
  runs `just conformance` before trusting it.
- **Formalize `AC-PRM-E` / `AC-PRM-F`** (the tiered safe-AI-write model — review-required / append-only /
  free-write; no MCP path commits a review-required write directly, it stages a changeset the workspace
  applies). PRM ships the **review-required** tier: `mcp_servers/dedup_ops.py` (propose-only — no apply tool)
  + `core/apply.py` (the workspace applier).
- **User-mediation `UM-1/2/3` (mutation side)**: PRM's propose→review→apply loop is the **mutation-side**
  demonstration the egress-focused fellows MVD lacked (the proposer stages; the principal disposes).
- **`AC-PRM-H` — "no ungoverned app-opened surface over private data"** (`spec/axes.md`, conditional;
  generalizes `AC-2`'s intent to the loopback daemon): a same-host surface a PNA stands up over its own data
  (here the loopback HTTP daemon) MUST be loopback-bound and authenticated to the user's own session. PRM is the
  **loopback-daemon demonstrator** — daemon session-auth (a per-process token + Host/Origin guard + loopback-pin)
  in `daemon/server.py`, gated by a static "checked, not asserted" lint (`scripts/loopback_surface_lint.py`).
  Full analysis: the design's `docs/design-notes/local-daemon-trust-surface.md`.

## Reproducibility notes

Python ≥ 3.10; runtime deps `vobjectx` + the official `mcp` SDK (everything else stdlib). `pip install -e ".[dev]"`
(or `just setup`); **`just conformance`** is the `[verify]` entrypoint — it regenerates + shape-checks the
attestation and runs the full suite. Local-only by design (no external services; the daemon binds `127.0.0.1`).
See the canonical repo's `README.md` + `docs/users-guide.md`.

## Architecture document

A copy of upstream `docs/Architecture.md` is included here as [`Architecture.md`](Architecture.md), carrying the
AC attestation table (Realization / Verification / Status per applicable AC), the `EX-CLOUD-LLM` exception
attestation, and the `UM-1/2/3` user-mediation rows (mutation side).
