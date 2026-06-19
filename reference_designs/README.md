# Reference designs

A reference design is a working, deployed PNA that demonstrates one valid combination of axis picks against the PNA Spec. Each lives in its author's own repository, under its own release cadence; the PNA Toolkit references each design by Software Heritage SWHID (the v0.1 permanent identifier — see `spec/PNA_Spec.md § Vocabulary`).

The toolkit's contribution model is reference-driven: spec changes are accompanied by a reference design that demonstrates the change in working code. The reference designs collected here are therefore not just illustrations — each one contributed something to the spec.

## How to contribute a design

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md). Briefly:

1. Build a PNA in your own repo, under an OSI-approved license.
2. While building or operating it, identify a spec ambiguity, gap, or constraint not yet captured.
3. Author an Architecture document for the design per [`templates/ARCHITECTURE_TEMPLATE.md`](templates/ARCHITECTURE_TEMPLATE.md), including the AC attestation table with verification references.
4. Open a PR with the spec diff, a design record, the Architecture document, and your repo's canonical URL + commit SHA.

The skill at [`../pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md) walks an LLM agent through this end-to-end as its **contribute flow**.

## Templates

- [`templates/TEMPLATE.md`](templates/TEMPLATE.md) — the per-design record template (lives at `<design-name>/README.md`)
- [`templates/ARCHITECTURE_TEMPLATE.md`](templates/ARCHITECTURE_TEMPLATE.md) — the Architecture document template (lives at `<design-name>/Architecture.md`)

## Accepted designs

- [`fellows_local_db/`](fellows_local_db/) — Directory Archive PNA; magic-link distributed PWA flavor (`web-bundle-with-magic-link` + `opfs-sqlite-wasm` + `single-source-static-mirror` + `vanilla-js-spa` + `mailto-only` + `shared+private+comms`). The design from which most of the v0.1 toolkit was distilled, and the originating contributor of the Exceptions and Constraints mechanisms. Accepted 2026-05-31; re-archived at `98b283f` (fellows #289 — 100% realization-pointer coverage) (`swh:1:dir:1bb784328e99fe888addf2e04fc2bbdf66b5ec05`; SH Save Code Now submitted 2026-06-19, req 2368289, ingest async).
- [`prm/`](prm/) — Personal Relationship Manager PNA; never-distributed single-user native-SQLite flavor (`never-distributed-single-user` + `native-sqlite-via-filesystem` + `multi-source-merge-with-dedup` + `vanilla-js-spa` + `none` + `shared-only`). First multi-source-dedup demonstrator (`AC-PRM-B`) and the build-from-verifiable-source distribution case. Accepted 2026-06-10; re-archived at `prm@pnt-ref-0.1.2` / `7bd4a28` (prm #60 — 100% realization-pointer coverage) (`swh:1:dir:87d3d263759092a46f9459d95234cd2cedc6edfb`; SH Save Code Now submitted 2026-06-19, req 2368290, ingest async).

When a further design lands, it'll be linked here.
