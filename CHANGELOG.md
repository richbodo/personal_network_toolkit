# PNT Changelog

## v0.1 draft (in progress)

### Private-DB portability (PR-6)

- **PR-6: human-readable export (SHOULD).** New Private-schema sub-contract: implementations SHOULD export the Private DB to a flat, tool-free format (CSV per table, schema-embedded JSON, or a Markdown vault) *in addition to* the canonical SQLite file, readable with a generic CSV/JSON/Markdown reader and no PNA tooling. Closes the practical-ownership gap in Goal 4 — owning the bytes is not the same as being able to read them without a SQLite browser. The export is explicitly **one-way**: implementations MUST NOT treat it as a guaranteed re-import surface; re-import stays on the PR-5 SQLite path. Sub-contract count: `PR-` (6), 58 total.
- **`tools/export-readable-lint.py`.** Deterministic PR-6 checker (mirrors `egress-lint.py`): every file in a human-readable export must parse with a Python stdlib reader and require no project code. Clean/dirty fixtures + a CI self-test job. The canonical `.sqlite` binary in an export is the textbook failure it catches. Motivated by mapping the spec against the Ink & Switch "local-first software" ultimate-ownership ideal; see `richbodo/fellows_local_db#216`. Demonstrating reference-design attestation (fellows_local_db) is the companion follow-up.

### Formalization pass (Phase 3 of the reorg plan)

- **RFC 2119 normative language.** Every AC and every sub-contract in `spec/PNA_Spec.md` and `spec/axes.md` was reworded so that conformance-bearing statements use MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. Readable prose around the keywords preserved (motivation, examples, why-it-matters). A short "Normative language" note added at the top of each AC-bearing section.
- **Bidirectional traceability (AC ↔ contract).** Every typed contract file in `contracts/` now carries a `Realizes: AC-X, AC-Y` header (as a `$comment` field in JSON Schemas; as a top-of-file comment in YAML / SQL / TypeScript). AC IDs are now the load-bearing join key between spec prose and typed contracts.
- **Spec ID lint.** `tools/lint-spec-ids.py` checks (a) every AC has a stable ID, (b) every contract names at least one AC, (c) every claimed AC exists in the spec. Wired into CI via `.github/workflows/spec-lint.yml`.
- **Software Heritage SWHID declared in the spec.** Added to the reference-design vocabulary entry: v0.1 commits to SWHIDs as the canonical permanent identifier for accepted reference designs.
- **Vision future-direction note.** Added a paragraph about conformance evaluation as a potential precondition for runtime interop between PNAs in a multi-PNA ecosystem (a systems-level test requiring spec rethinking; flagged direction for a later version).
- **Variable-language pass.** Numeric axis counts ("six Axes") replaced with variable language ("the Axes", "these Axes", "the independent Axes") so the spec doesn't drift if the axis set evolves.

### v0.1 baseline

Initial release of the toolkit (PNA Spec + typed contracts). Establishes:

- Vocabulary (Use case, Axis, Axis pick, Flavor, Composition model, MCP server, Universal vs flavor-derived AC).
- Goals (1-5: private data sovereignty, mirror centralized sources locally, secure communication options, portable/durable/recoverable user data, locally diagnosable).
- Use cases attested: Directory Archive (realized in fellows_local_db), Personal Relationship Manager [draft], Multi-PNA ecosystem [target v0.2+].
- Axes: distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure.
- Two target environments for a single PNA (Browser PNAs and CLI / native PNAs) plus one runtime cooperation pattern across PNAs (the ecosystem reference design, mediated by canonical MCP servers).
- Universal ACs: AC-1, AC-4, AC-6, AC-7, AC-9, AC-10, AC-11, AC-15, AC-16, AC-17, AC-18, AC-19, AC-PRM-A, AC-PRM-D, AC-MCP-A, AC-MCP-B (16 in v0.1).
- Flavor-derived ACs: AC-2, AC-3, AC-5, AC-8, AC-12, AC-13, AC-14 from the original set; AC-PRM-B and AC-PRM-C as [draft] PRM-flavor commitments.
- Slot map: five slots (Ingestion, Storage, Workspace, Communications, Distribution) + three interfaces (Shared schema, Private schema, Debug contract).
- Sub-contract decomposition: each slot and interface decomposes into named sub-contracts under a per-slot two-letter prefix — `WS-` (10), `ST-` (11), `IN-` (4), `CO-` (6), `DI-` (6), `SH-` (6), `PR-` (5), `DB-` (9). 57 sub-contracts total in v0.1. Cross-slot threads (build-label discipline, opt-in directory update, restore data flow, capability-failure surfacing, …) are formalized in the same section. The spec is now self-contained: builders can cite sub-contracts by ID without consulting the working triage.
- Five canonical MCP server contracts: Shared Data Ops, Private Data Ops, Ingestion, Communications, Diagnostics. The original "Data operations" server was split along the Shared / Private privacy boundary so AC-MCP-A's cloud-client consent rule targets exactly the Private Data Ops surface — a user can wire a cloud client to Shared Data Ops alone without crossing the boundary. v1 reference implementations of Shared Data Ops, Private Data Ops, and Comms ship in `fellows_local_db/mcp_servers/`; JSON Schemas live alongside this CHANGELOG in `contracts/mcp-shared-data-ops.schema.json`, `mcp-private-data-ops.schema.json`, and `mcp-comms.schema.json`. Ingestion and Diagnostics remain spec stubs (no reference implementation yet).
- MCP-exposure axis picks restructured from {`none`, `data-ops-only`, `data-ops+comms`, `full`} to {`none`, `shared-only`, `shared+private`, `shared+private+comms`, `full`} to reflect the split; fellows_local_db's attested pick is `shared+private+comms`.

Spec scaffolding (`_pna_triage.md` working triage doc + `_pna_spec_format_landscape.md` format-choice notes) retired in v0.1 after all spec-side and repo-side migrations landed. The spec is now self-contained: `spec/PNA_Spec.md`, `spec/axes.md`, `spec/use_cases.md`, and the typed contracts under `contracts/`.

Items deliberately deferred to future versions: privacy reclassification migration mechanics, multi-source dedup migration (beyond AC-PRM-B's draft form), per-database transport requirements, cross-device sync, federated p2p, formal verification.
