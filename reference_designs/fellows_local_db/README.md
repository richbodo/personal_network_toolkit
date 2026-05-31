# fellows_local_db

**Maintainer:** Rich Bodo (https://github.com/richbodo/fellows_local_db)
**License:** see upstream repo
**First accepted:** PNA Spec v0.1, <YYYY-MM-DD pending>
**Status:** active (Software Heritage SWHID pending maintainer archival post-merge; AC + exception attestation now present in `Architecture.md`)

## Summary

`fellows_local_db` is the first PNA reference design — a Directory Archive PNA realizing the Knack-export → static-PWA + magic-link distribution flavor. It is the design from which most of the v0.1 spec was distilled. The canonical repo lives at https://github.com/richbodo/fellows_local_db; its Architecture document is at `docs/Architecture.md` upstream.

## Axis picks at first acceptance

`distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`

## Contributions to the spec

The bulk of PNA Spec v0.1 — every universal AC except those flagged `[draft]`, every sub-contract under `WS-`, `ST-`, `SH-`, `PR-`, `DB-`, `IN-`, `CO-`, `DI-`, and the realized axis picks in `axes.md` — derives from learnings on this design. The detailed contribution list and the SWHID are backfilled in Phase 5 of `plans/reorganization-plan.md`.

**The Exceptions concept (originating contribution).** `spec/exceptions.md` — the raise/catch/handle model, PNA-mode vs non-PNA-mode, the `EX-H1`–`EX-H8` handler contract, the `Relaxes:`/`Reversible:`/`Stresses:` header conventions, the per-dimension strength-profile vocabulary, and the first registry entry `EX-CLOUD-LLM` — together with the `tools/lint-spec-ids.py` traceability extension and the SKILL evaluate-flow exceptions step, were distilled from this design. They are demonstrated by its cloud-MCP consent handler: a pre-raise consent gate, the persistent "Going rogue — not a PNA" banner, the `#/exception/<id>` explainer (surfacing the strength profile), the return-to-PNA-mode control, and a best-effort consent-propagation notice in the MCP servers' `instructions`. See the `EX-CLOUD-LLM` row in this design's Architecture document (§ Exception attestation) and `docs/architectural_findings.md` upstream.

## Architectural learnings

Pending Phase 5 backfill. The PWA-doesn't-work-for-most-PNAs insight from real user feedback is the canonical one — captured today in the universal architectural commitments via AC-3, AC-12, AC-13, and the `dist:pwa`-triggered AC-14.

## Reproducibility notes

See upstream repo's README for current build instructions. SWHID-archived snapshot will be added in Phase 5.

## Architecture document

A copy of upstream `docs/Architecture.md` is included here as [`Architecture.md`](Architecture.md), carrying the AC attestation table (Realization / Verification / Status per applicable AC) and the `EX-CLOUD-LLM` exception attestation. Brought current with the Exceptions contribution; the broader Phase-5 backfill of historical learnings continues separately.
