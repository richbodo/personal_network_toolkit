# Personal Network Toolkit

The Personal Network Toolkit is a blueprint for building **personal network applications (PNAs)** — local-only apps for viewing contact data and working on relationship data over a firewalled private data layer. PNAs run on the user's device, never as SaaS, and bridge SaaS-held contact data into a private workspace.

Three deliverables, in dependency order:

1. **Foundational specs.** Universal vocabulary, goals, axes, architectural commitments, and typed contracts for a PNA. — **shipping in v0.1 (draft)**.
2. **Production-ready reference applications.** Working PNAs you can install, study, and adapt. — first reference design is a distributed directory archive (lives at [richbodo/fellows_local_db](https://github.com/richbodo/fellows_local_db)).
3. **MCP servers.** Composability-layer (Software 3.0) bridges so AI clients (Claude Desktop, Cursor, local Ollama agents) can drive a PNA on the user's behalf. — three v1 stdio servers ship inside `fellows_local_db/mcp_servers/`; typed contracts for all five canonical MCP servers live here in [`spec/contracts/`](spec/contracts/).

This toolkit augments human-AI builder teams; it doesn't auto-build applications itself; it is a blueprint for agents to implement and humans to customize and verify.  Verification is made simply by composable contract specifications.

## Entry points

Read in this order if you're new:

- **[`PNA_Spec.md`](PNA_Spec.md)** — universal PNA specification. Vocabulary, goals, use cases, axes, composition, universal architectural commitments, slot map with 57 sub-contracts, scope/versioning. **Start here.**
- **[`axes.md`](axes.md)** — the six Axes a PNA varies along, attested picks per Axis, and the flavor-derived ACs each pick triggers.
- **[`use_cases.md`](use_cases.md)** — attested classes of PNA (Directory Archive realized; Personal Relationship Manager draft; Multi-PNA ecosystem target).
- **[`spec/contracts/`](spec/contracts/)** — typed contracts for the load-bearing interfaces: JSON Schema for the worker init handshake + RPC protocol, OpenAPI for distribution auth, SQL DDL for the two database schemas, TypeScript for the Communications transport interface, JSON Schema for the five canonical MCP server tool surfaces.
- **[`CHANGELOG.md`](CHANGELOG.md)** — spec version history.
- **[`llms.txt`](llms.txt)** — discovery file for the spec (humans + AI agents land here cold).

## Reference designs

A reference design is a working, deployed PNA that demonstrates one valid combination of axis picks against the spec. Each lives in its own repository so it can ship under its own release cadence.

- **[fellows_local_db](https://github.com/richbodo/fellows_local_db)** — first reference design. Directory Archive use case. Flavor: `distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`. Its [`docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) declares spec-version conformance and the per-slot specializations.

When a second reference design (e.g. a Personal Relationship Manager) lands, it'll be linked from here.

## Status

**v0.1 (draft).** Spec content is feature-complete for v0.1 — all universal ACs, axes, use cases, slot map with sub-contracts, and typed contracts are in place. Substantive changes from this point bump the spec version per [`CHANGELOG.md`](CHANGELOG.md).

Reference implementations of the canonical MCP servers ship today in [`fellows_local_db/mcp_servers/`](https://github.com/richbodo/fellows_local_db/tree/main/mcp_servers) (Shared Data Ops, Private Data Ops, Communications). Ingestion and Diagnostics tool surfaces are spec-level placeholders awaiting first reference implementations.

## Plans

`plans/` holds long-form proposals for toolkit extensions. Today: [`memorize-plugin-plan-v0.2.md`](plans/memorize-plugin-plan-v0.2.md) — a plugin proposal.

## License

[LICENSE](LICENSE).
