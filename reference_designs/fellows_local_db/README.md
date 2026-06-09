# fellows_local_db

**Maintainer:** Rich Bodo (https://github.com/richbodo/fellows_local_db)
**License:** see upstream repo
**First accepted:** Toolkit-Version 0.1, 2026-05-31
**Status:** active

## Acceptance & validation

- **Accepted:** 2026-05-31, by the maintainer (Rich Bodo). As the design the toolkit was distilled from, `fellows_local_db` is accepted *by definition* for Toolkit-Version 0.1 (see [`CONTRIBUTING.md` § Acceptance process](../../CONTRIBUTING.md#acceptance-process)).
- **Validated against:** Toolkit-Version 0.1. The AC + `EX-CLOUD-LLM` exception attestation is in [`Architecture.md`](Architecture.md); its Verification column cites real tests that are lint-green in CI.
- **Archival commit:** `dc3e0cffbbca44547c6987602fbbb1003d6920e6` — fellows `main` at the post-#267 state (the deterministic `just evaluate-report` emitter; supersedes the `bbaf66e` / `046584c` / `v0.1.0` snapshots). The manifest is now `archival = "archived"`: the `[verify]` entrypoint (`just evaluate-report`) has landed and the SWHIDs are git-verified.
- **Software Heritage SWHID:**
  - `swh:1:dir:d69ecdfbee779a45d8c5a129e6787b623f6bc4c4` (the archived source tree — canonical permanent identifier)
  - `swh:1:rev:dc3e0cffbbca44547c6987602fbbb1003d6920e6` (the accepted revision)
  - These are git-compatible (SH's `dir`/`rev` identifiers equal the git tree/commit hashes), computed at the archived commit. The Software Heritage *Save Code Now* request `2352911` was submitted 2026-06-09 for `https://github.com/richbodo/fellows_local_db`; the identifiers are content-addressed and resolve unchanged once ingest completes (asynchronous — minutes to hours). Re-run any time via [`tools/swh-save.sh`](../../tools/swh-save.sh).

## Summary

`fellows_local_db` is the first PNA reference design — a Directory Archive PNA realizing the Knack-export → static-PWA + magic-link distribution flavor. It is the design from which most of the v0.1 toolkit was distilled. The canonical repo lives at https://github.com/richbodo/fellows_local_db; its Architecture document is at `docs/Architecture.md` upstream.

## Axis picks at first acceptance

`distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`

## Contributions to the spec

The bulk of the v0.1 toolkit — every universal AC except those flagged `[draft]`, every sub-contract under `WS-`, `ST-`, `SH-`, `PR-`, `DB-`, `IN-`, `CO-`, `DI-`, and the realized axis picks in `axes.md` — derives from learnings on this design. The detailed contribution list and the SWHID are backfilled in Phase 5 of `plans/reorganization-plan.md`.

**The Exceptions concept (originating contribution).** `spec/exceptions.md` — the raise/catch/handle model, PNA-mode vs non-PNA-mode, the `EX-H1`–`EX-H8` handler contract, the `Relaxes:`/`Reversible:`/`Stresses:` header conventions, the per-dimension strength-profile vocabulary, and the first registry entry `EX-CLOUD-LLM` — together with the `tools/lint-spec-ids.py` traceability extension and the SKILL evaluate-flow exceptions step, were distilled from this design. They are demonstrated by its cloud-MCP consent handler: a pre-raise consent gate, the persistent "Going rogue — not a PNA" banner, the `#/exception/<id>` explainer (surfacing the strength profile), the return-to-PNA-mode control, and a best-effort consent-propagation notice in the MCP servers' `instructions`. See the `EX-CLOUD-LLM` row in this design's Architecture document (§ Exception attestation) and `docs/architectural_findings.md` upstream.

**The Constraints concept (originating contribution).** `spec/constraints.md` — the dual of Exceptions: a platform/substrate-imposed ceiling (`CST-*`) inherited automatically by axis picks, the compile-time-error metaphor, the `Triggered-by:`/`Bounds:`/`Frontier:`/`Detectability:` header conventions, the meta-principle that *capability presence ≠ usefulness ≠ permanence*, and the seven-entry `CST-PWA-*` registry (the forced worker-owned single-connection architecture is captured directly in AC-3 rather than as a separate constraint) — together with the `tools/lint-spec-ids.py` constraint checks (CST IDs, Triggered-by → axis-pick resolution, Bounds/Frontier/Detectability well-formedness, Mitigated/Solved-* require a Workaround, and registry-table ↔ detail-block consistency) and the SKILL build-flow "enumerate inherited Constraints" + evaluate-flow "detect and verify Constraints" steps, were distilled from this design. They are demonstrated by its **private-data capability gate**: folder mode (File System Access) makes the private store a real, MCP-readable file on Chromium desktop (`CST-PWA-SANDBOX-SEALED`, `CST-PWA-PRIVATE-SNAPSHOT` Solved/handled), with data-layer refusal of durable private writes off-folder (browse-only, not false durability), a Web-Lock single-owner guard (`CST-PWA-SINGLE-OWNER`), per-boot opportunistic backups (`CST-PWA-NO-BACKGROUND`), an in-db workspace identity for canonical-copy disambiguation (`CST-PWA-NO-SYNC`), and a Never-SaaS distribution-only server (`CST-PWA-SERVER-FLOOR`). The originating finding (an MCP handoff that broke because the OPFS store was sealed) is in `docs/architectural_findings.md` upstream § 2026-06-01. See the § Constraint attestation in this design's Architecture document.

## Architectural learnings

Pending Phase 5 backfill. The PWA-doesn't-work-for-most-PNAs insight from real user feedback is the canonical one — captured today in the universal architectural commitments via AC-3, AC-12, AC-13, and the `dist:pwa`-triggered AC-14.

## Reproducibility notes

See upstream repo's README for current build instructions. SWHID-archived snapshot will be added in Phase 5.

## Architecture document

A copy of upstream `docs/Architecture.md` is included here as [`Architecture.md`](Architecture.md), carrying the AC attestation table (Realization / Verification / Status per applicable AC), the `EX-CLOUD-LLM` exception attestation, and the § Constraint attestation (the `CST-PWA-*` registry mapped to fellows' per-platform handling). Brought current with the Exceptions and Constraints contributions; the broader Phase-5 backfill of historical learnings continues separately.
