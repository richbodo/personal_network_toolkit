# prm

**Maintainer:** Rich Bodo (https://github.com/richbodo/prm)
**License:** see upstream repo
**Validated against:** Toolkit-Version 0.1, 2026-06-10
**Status:** active

## Acceptance & validation

- **Accepted:** 2026-06-10 · accepted-by Rich Bodo (maintainer) · validated against Toolkit-Version 0.1. The merge of [PR #61](https://github.com/richbodo/personal_network_toolkit/pull/61) is the acceptance; this line is the durable record of what was validated.
- **Validated against:** Toolkit-Version 0.1. The AC attestation — universal + flavor-derived, the
  `EX-CLOUD-LLM` exception, and the `UM-1/2/3` user-mediation rows — is in [`Architecture.md`](Architecture.md);
  every `conformant` row's Verification cites a real, passing test, and the design's own evidence lint
  (`tests/conformance/test_attestation_has_evidence.py`) gates it.
- **Posture:** [`evaluate-report.json`](evaluate-report.json) — deterministically emitted from the attestation
  table by `scripts/evaluate_report.py` and satisfying the toolkit's [`report-fixtures-lint.py`](../../tools/report-fixtures-lint.py)
  render contract — is **conformant** for the declared flavor: 12 conformant, 2 partial-conformance
  (flagged for human review: `AC-PRM-A`, `AC-MCP-A` — consent + signaling, because an MCP server cannot
  identify the consuming LLM), 4 not-applicable (`comms:none`) across 18 evaluated ACs.
- **Archival:** `archival = "archived"` — source pinned at `prm@pnt-ref-0.1` (`a70d35b`, the PR [#35](https://github.com/richbodo/prm/pull/35)
  squash-merge to `main`): `swh:1:rev:a70d35bcf5765001322b29d0acdc14b1ae14ae11`,
  `swh:1:dir:9d73887ae6a3b277a9232a5267be359387edb00f` (computed via `tools/swh-save.sh`; Save Code Now ingest
  requested). The `[verify].entrypoint` is `just conformance` in the canonical repo.

## Summary

`prm` is the **second PNT reference design** — a local-only **Personal Relationship Manager** that mirrors a
person's contacts from everywhere they're scattered (Google, Apple, LinkedIn, Facebook, loose vCard/CSV) into
one store they own, **deduplicates** them, and lets an AI *propose* merges the human applies. It is the first
design to exercise the **multi-source dedup** contract (`AC-PRM-B`) and the **native-sqlite-via-filesystem**
substrate (`AC-PRM-C`), and the first **build-from-verifiable-source** distribution demonstrator. The canonical
repo is https://github.com/richbodo/prm; its Architecture document lives at `docs/Architecture.md` upstream.

## Axis picks at first acceptance

`distribution:never-distributed-single-user + storage:native-sqlite-via-filesystem + ingestion:multi-source-merge-with-dedup + workspace-shell:vanilla-js-spa + comms:none + mcp-exposure:shared-only`

## Contributions to the spec

This submission rides four spec changes, each demonstrated by working code in the canonical repo:

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

## Reproducibility notes

Python ≥ 3.10; runtime deps `vobjectx` + the official `mcp` SDK (everything else stdlib). `pip install -e ".[dev]"`
(or `just setup`); **`just conformance`** is the `[verify]` entrypoint — it regenerates + shape-checks the
attestation and runs the full suite. Local-only by design (no external services; the daemon binds `127.0.0.1`).
See the canonical repo's `README.md` + `docs/users-guide.md`.

## Architecture document

A copy of upstream `docs/Architecture.md` is included here as [`Architecture.md`](Architecture.md), carrying the
AC attestation table (Realization / Verification / Status per applicable AC), the `EX-CLOUD-LLM` exception
attestation, and the `UM-1/2/3` user-mediation rows (mutation side).
