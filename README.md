# Personal Network Toolkit

The Personal Network Toolkit is a [generative application-class blueprint](docs/prior_art.md) for building **[personal network applications (PNAs)](spec/PNA_Spec.md#goals)** — local-only apps for viewing contact data and working on relationship data over a firewalled private data layer. PNAs run on the user's device, never as SaaS, and bridge SaaS-held contact data into a private workspace. **[Why do this?](spec/PNA_Spec.md#preamble)**

When building a PNA, specs are foundational because users will increasingly compose software by prompting AI agents, and success is measured by adherence to them.

Three deliverables, in dependency order:

1. **Foundational specs.** Universal vocabulary, goals, axes, architectural commitments, and typed contracts for a PNA. — **shipping in v0.1 (draft)**.
2. **Production-ready reference applications.** Working PNAs you can install, study, and adapt. — first reference design is a distributed directory archive (lives at [richbodo/fellows_local_db](https://github.com/richbodo/fellows_local_db)).
3. **MCP servers.** Composability-layer (Software 3.0) bridges so AI clients (Claude Desktop, Cursor, local Ollama agents) can drive a PNA on the user's behalf. — three v1 stdio servers ship inside `fellows_local_db/mcp_servers/`; typed contracts for all five canonical MCP servers live here in `[contracts/](contracts/)`.

That combination best satisfies the composability model of Software 3.0 in this context. It should ensure that both the humans and the AIs in modern human-AI builder teams can build PNAs that they understand fully and that behave as expected. The Personal Network Toolkit augments the human-AI builder teams; it doesn't automatically build applications itself.

This toolkit augments human-AI builder teams; it doesn't auto-build applications itself; it is a blueprint for agents to implement and humans to customize and verify.  Verification is made simply by composable contract specifications made primarily for AIs, derived from goals made for humans to read.

Note: This does not quite fit into a /skill or I would make it one.  Building the reference apps feeds the spec and the apps in a virtuous loop, so there is no conventional path that makes this more accessible like adding to /skill repos.

## Status

**v0.1 alpha.** The spec is feature-complete for v0.1 — universal ACs, axes, use cases, slot map with sub-contracts, and typed contracts are all in place. We say "alpha" rather than "draft" because the contribution workflow described in `[plans/reorganization-plan.md](plans/reorganization-plan.md)` hasn't yet been validated against `fellows_local_db` as the first reference design.

What we're working toward — success looks like:

1. A new builder can read `README.md` + `CONTRIBUTING.md` and build a conformant PNA using the skill.
2. A new user can ask an LLM (via the skill) to audit a candidate PNA's source and get an actionable AC-keyed report.
3. A new contributor can submit a reference design end-to-end without maintainer hand-holding beyond review.
4. Every accepted design has a permanent Software Heritage identifier that survives upstream repo deletion.
5. The PNA Spec evolves at least one minor version based on a contributed reference design's findings.
6. Every AC in the spec carries a stable ID; every typed contract names the AC(s) it realizes; every Architecture document maps each applicable AC to a verification mechanism.

Step-by-step instructions for each of those goals live in [`docs/users-guide.md`](docs/users-guide.md).

Substantive changes from v0.1 bump the spec version per `[CHANGELOG.md](CHANGELOG.md)`.

## Entry points

Read in this order if you're new:

- `**[spec/PNA_Spec.md](spec/PNA_Spec.md)`** — universal PNA specification. Vocabulary, goals, use cases, axes, composition, universal architectural commitments, slot map with 57 sub-contracts, scope/versioning. **Start here.**
- `**[docs/users-guide.md](docs/users-guide.md)`** — step-by-step instructions for each of the success criteria in § Status (building a PNA, auditing one, submitting a reference design).
- `**[spec/axes.md](spec/axes.md)`** — the Axes a PNA varies along, attested picks per Axis, and the flavor-derived ACs each pick triggers.
- `**[spec/use_cases.md](spec/use_cases.md)**` — attested classes of PNA (Directory Archive realized; Personal Relationship Manager draft; Multi-PNA ecosystem target).
- `**[contracts/](contracts/)**` — typed contracts for the load-bearing interfaces: JSON Schema for the worker init handshake + RPC protocol, OpenAPI for distribution auth, SQL DDL for the two database schemas, TypeScript for the Communications transport interface, JSON Schema for the five canonical MCP server tool surfaces.
- `**[CHANGELOG.md](CHANGELOG.md)**` — spec version history.
- `**[llms.txt](llms.txt)**` — discovery file for the spec (humans + AI agents land here cold).

## Reference designs

A reference design is a working, deployed PNA that demonstrates one valid combination of axis picks against the spec. Each lives in its own repository so it can ship under its own release cadence.

- **[fellows_local_db](https://github.com/richbodo/fellows_local_db)** — first reference design. Directory Archive use case. Flavor: `distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`. Its `[docs/Architecture.md](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md)` declares spec-version conformance and the per-slot specializations.

When a second reference design (e.g. a Personal Relationship Manager) lands, it'll be linked from here.

## Plans

`plans/` holds long-form proposals for PNT itself. Today: `[reorganization-plan.md](plans/reorganization-plan.md)` — the unified reorg plan covering repo restructure, spec formalization (RFC-style normative language, stable IDs, bidirectional traceability), per-design Architecture documents with AC attestation, Software Heritage archival, and a single skill that lets AI agents build, evaluate, and contribute PNAs.

## License

[LICENSE](LICENSE).
