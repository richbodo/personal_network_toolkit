# Reference designs

A reference design is a working, deployed PNA that demonstrates one valid combination of axis picks against the PNA Spec. Each lives in its author's own repository, under its own release cadence; the PNA Toolkit references each design by Software Heritage SWHID (the v0.1 permanent identifier — see `spec/PNA_Spec.md § Vocabulary`).

The toolkit's contribution model is reference-driven: spec changes are accompanied by a reference design that demonstrates the change in working code. The reference designs collected here are therefore not just illustrations — each one contributed something to the spec.

## How to contribute a design

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md). Briefly:

1. Build a PNA in your own repo, under an OSI-approved license.
2. While building or operating it, identify a spec ambiguity, gap, or constraint not yet captured.
3. Author an Architecture document for the design per [`templates/ARCHITECTURE_TEMPLATE.md`](templates/ARCHITECTURE_TEMPLATE.md), including the AC attestation table with verification references.
4. Open a PR with the spec diff, a design record, the Architecture document, and your repo's canonical URL + commit SHA.

The skill at [`../pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) walks an LLM agent through this end-to-end as its **contribute flow**.

## Templates

- [`templates/TEMPLATE.md`](templates/TEMPLATE.md) — the per-design record template (lives at `<design-name>/README.md`)
- [`templates/ARCHITECTURE_TEMPLATE.md`](templates/ARCHITECTURE_TEMPLATE.md) — the Architecture document template (lives at `<design-name>/Architecture.md`)

## Accepted designs

- [`fellows_local_db/`](fellows_local_db/) — Directory Archive PNA; magic-link distributed PWA flavor. The design from which most of the v0.1 toolkit was distilled. *(Status: placeholder — SWHID and full AC attestation pending Phase 5 of the reorganization plan.)*

When a second design lands, it'll be linked here.
