# Prior Art References

Companion reference list to [`PriorArt.md`](./PriorArt.md), the analytical survey. This file catalogs the sources uncovered during the prior-art conversation (Claude / Anthropic, May 2026), organized by category, each with a one-line note on relevance to the PNA Toolkit.

## Primary sources

- **[Contract-Driven AI Development (C-DAD)](https://medium.com/software-architecture-in-the-age-of-ai)** — Enrico Piovesan (Autodesk), Oct 2025 white paper. The maximalist, enterprise-scale statement of the toolkit's core bet: typed, versioned contracts as the load-bearing artifact for human–AI build teams.
- **[Why Spec-Driven Development Has Reached Its Limit](https://medium.com/software-architecture-in-the-age-of-ai/why-spec-driven-development-has-reached-its-limit-6e9bfed9ee13)** — Enrico Piovesan, "Software Architecture in the Age of AI" (Medium), Nov 2025. Argues specs must become living *runtime* contracts; the position the toolkit diverges from (the toolkit keeps contracts design-time and file-based).

## Spec-Driven Development tooling

- **[GitHub Spec Kit](https://github.com/github/spec-kit)** — The most prominent SDD tool: a four-phase workflow (specify, plan, task, implement) plus a `constitution.md` of immutable principles governing generation. ([design doc](https://github.com/github/spec-kit/blob/main/spec-driven.md).)
- **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** — Fission-AI (MIT). Lightweight, vendor-neutral SDD layer closest in spirit to the toolkit; propose→apply→archive delta loop with ADRs kept alongside specs.
- **[AWS Kiro](https://kiro.dev)** — Spec-driven agentic IDE (requirements→design→tasks→code); the enterprise/IDE incarnation of the workflow the toolkit collapses into axis selection.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** — Multi-agent "agile AI" orchestration (PM/architect/dev/QA roles); the heaviest end of the spectrum, a contrast to the toolkit's solo/community-builder target.
- **[Tessl (Framework + Spec Registry)](https://tessl.io)** — Guy Podjarny / Tessl. Spec-as-source-of-truth platform with a registry of pre-built library specs; the most C-DAD-aligned commercial effort and a model for "publish specs others' agents consume."
- **[Google Antigravity](https://antigravity.google)** — Google DeepMind, Nov 2025. Agent-first IDE (VS Code fork) where agents plan/implement/verify from objectives.
- **[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)** — Deepak Babu Piskala, arXiv 2602.00180, Jan 2026. Canonical academic framing of SDD as executable contracts that constrain what AI agents generate.
- **[BCMS — Spec-Driven Development definitive guide (2026)](https://thebcms.com/blog/spec-driven-development)** — Industry survey of the 2026 SDD landscape (Spec Kit, Kiro, BMAD-METHOD, OpenSpec, Tessl, Antigravity).
- **[Augment Code — What is Spec-Driven Development](https://www.augmentcode.com/guides/what-is-spec-driven-development)** — Industry-oriented framing of SDD as "executable contracts that constrain what AI agents generate."
- **[EARS (Easy Approach to Requirements Syntax)](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)** — Alistair Mavin et al., Rolls-Royce, RE'09 (2009). A constrained natural-language requirement grammar that parses cleanly for agents; a candidate format for the toolkit's human-readable goals layer. (Primary source: alistairmavin.com/ears.)

## Agent-interface standards (what an agent reads)

- **[Agent Skills / SKILL.md](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** — Anthropic (open standard; community hub at [agentskills.io](https://agentskills.io)). The skill format the toolkit already ships in; progressive disclosure (name + description first, body on demand) is how the toolkit's spec and slot map are meant to be consumed.
- **[AGENTS.md](https://agents.md)** — Open convention; the project-level "agent README" emitted by Spec-Kit/OpenSpec. Worth having at the root of each toolkit reference design.
- **[llms.txt](https://llmstxt.org)** — Jeremy Howard / Answer.AI. Discovery-file convention for pointing agents at canonical docs; the toolkit ships one and routes it to the SKILL.md.

## AI app-builder system prompts & architectures

- **[x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)** — Canonical leaked-prompts collection with extracted system prompts for v0, Cursor, Lovable, Replit Agent, Bolt, Devin, Windsurf, Claude Code, and others.
- **[elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S)** — Mirror collection of AI system prompts framed as a transparency project.
- **[Lovable Agent Prompt](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Lovable/Agent%20Prompt.txt)** — Lovable's production system prompt, notable for rigorous design-system enforcement and a "PERFECT ARCHITECTURE" refactoring check on a fixed React + Vite + Tailwind + shadcn + Supabase stack.
- **[Replit Agent breakoutagents case study (LangChain)](https://www.langchain.com/breakoutagents/replit)** — Architectural breakdown of Replit Agent's multi-agent ReAct-style design with initial-codegen and follow-up agents.
- **[Pliny the Liberator — Replit Agent leak (X)](https://x.com/elder_plinius/status/1914774065937891398)** — April 2025 disclosure revealing Replit Agent uses two cooperating agents rather than one monolithic prompt.
- **[Replit Enterprise Custom Templates](https://docs.replit.com/teams/custom-templates)** — The strongest published official analog to a generative blueprint: customers create `custom_instruction/instructions.md` files injected into Agent's system prompt. The mechanism would accept a toolkit-shaped artifact without modification.
- **[Lovable Prompting Handbook (Jan 2025)](https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook)** — Lovable's official guidance for project-level constraints, design tokens, and backend structure documents.
- **[ML6 — The Anatomy of a Lovable App](https://www.ml6.eu/en/blog/the-anatomy-of-a-lovable-app-and-its-boundaries-in-enterprise-software)** — Third-party but accurate description of what a stack-coupled application archetype looks like in production.

## Conformance test suites & standards

- **[Solid Conformance Test Harness](https://github.com/solid-contrib/conformance-test-harness)** — The strongest direct analog to the toolkit by domain (decentralized personal data) and intent (ecosystem interop), though evaluative rather than generative.
- **[Inrupt — Interoperability tests for Solid developers](https://www.inrupt.com/blog/interoperability-tests-for-solid-developers)** — Plain-English overview of how the Solid community uses the CTH.
- **[xAPI LRS Conformance Test Suite](https://xapi.com/conformance-test/)** — 1,300-criterion conformance suite for Learning Record Stores with a public registry of certified implementations.
- **[HL7 FHIR CapabilityStatement](https://www.hl7.org/fhir/capabilitystatement.html)** — Healthcare-app conformance resource where each implementation publishes a structured declaration of which profiles and operations it supports; the closest "axis-attestation" model in a mature standard.
- **[W3C EARL (Evaluation and Report Language) Schema](https://www.w3.org/TR/EARL10-Schema/)** — Standard vocabulary for machine-readable conformance pass/fail reports, used by Solid CTH and other W3C-adjacent conformance work.
- **[EU Interoperability Test Bed (ITB)](https://www.itb.ec.europa.eu/docs/guides/latest/definingYourTestConfiguration/index.html)** — Generic harness with the test-subject + actor + test-suite model that Solid's CTH borrowed from.
- **[NIST — What is this thing called Conformance?](https://www.nist.gov/itl/ssd/information-systems-group/what-thing-called-conformance)** — Foundational framing of conformance testing, validation, and certification.

## Contract testing & interface specification

- **[Pact](https://pact.io)** — Pact Foundation / SmartBear. Consumer-driven contract testing; the decades-proven "verify an implementation honors its contract" pattern the toolkit's evaluate flow re-creates for ACs.
- **[OpenAPI Specification](https://www.openapis.org)** — Standard for typed HTTP interfaces (the toolkit uses it for distribution auth); mature conformance-validation tooling can wire straight into a reference design's CI.
- **[AsyncAPI](https://www.asyncapi.com)** — The event/message-driven analogue to OpenAPI; relevant if a PNA's comms transport becomes event-based.
- **[JSON Schema](https://json-schema.org)** — Underpins the toolkit's worker-handshake and MCP tool-surface contracts; the schemas double as machine-checkable conformance fixtures.

## Architecture standards & verification frameworks

- **[OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)** — Level-based verification framework where applications attest to a specific conformance level rather than passing a binary check.
- **[SLSA — Supply chain Levels for Software Artifacts](https://slsa.dev/)** — Level-based attestation framework for build provenance; the same per-implementation attestation pattern at a different problem.

## Coding-agent benchmarks & evals

- **[Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)** — Anthropic's published methodology for designing capability evals that graduate into regression suites for agent reliability.
- **[SWE-bench Verified](https://www.swebench.com/verified.html)** — Human-validated subset of 500 GitHub-issue tasks used to evaluate whether coding agents can patch real repos.
- **[Terminal-Bench](https://www.tbench.ai/)** — Benchmark suite measuring tool-using agents on realistic terminal tasks.
- **[SWE-bench Pro / SWE-Bench-CL](https://arxiv.org/pdf/2507.00014)** — Harder and continual-learning evaluation variants beyond SWE-bench Verified.
- **[Anthropic's $20K C compiler experiment (WebProNews)](https://www.webpronews.com/anthropics-20000-experiment-how-16-parallel-ai-agents-built-a-100000-line-c-compiler-from-scratch-in-rust/)** — Coverage of Anthropic's 16-parallel-agent C compiler build, which reached for the *existing* C conformance test suite rather than authoring its own.

## MCP conformance

- **[Issue #1990 — Add an official MCP conformance test suite](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1990)** — Open request for an official MCP conformance test suite, still pending as of this survey.
- **[MCP roadmap — Conformance Test Suites](https://modelcontextprotocol.io/development/roadmap)** — Roadmap item: "automated verification that clients, servers, and SDKs correctly implement the specification."
- **[DinCoder MCP — Conformance documentation](https://glama.ai/mcp/servers/@flight505/MCP_DinCoder/blob/6c67715293c9863a9246c0e3a094e2d184e74572/docs/conformance.md)** — Example of an individual MCP implementation publishing its own per-section conformance checklist against the spec.

## Local-first software & sync infrastructure

- **[Local-first software — the seven ideals](https://www.inkandswitch.com/local-first/)** — Kleppmann, Wiggins, van Hardenberg, McGranaghan (Ink & Switch, 2019). The seminal essay defining the ideals the toolkit's ACs operationalize for the contact-data domain. ([Wikipedia overview](https://en.wikipedia.org/wiki/Local-first_software).)
- **[Home-Cooked Software and Barefoot Developers](https://maggieappleton.com/home-cooked-software)** — Maggie Appleton, Local-First Conf 2024. Names the toolkit's exact audience (community-embedded "barefoot developers" building "home-cooked" apps with AI); references Robin Sloan's "An app can be a home-cooked meal."
- **[Local-first, forever](https://tonsky.me/blog/crdt-filesync/)** — Nikita Prokopov (Tonsky). Proposes sync over commodity file-syncing (append-only per-client op logs + CRDT merge underneath), a candidate PNA axis pick for multi-device sharing without a SaaS root.
- **[Automerge](https://automerge.org)** — Ink & Switch (Automerge 3.0, May 2025). Mature CRDT library (Rust core, ~10× lower memory) underpinning the file-sync pattern above; relevant if a PNA needs conflict-free multi-writer state.
- **[Yjs](https://yjs.dev)** — Kevin Jahns. Dominant CRDT for collaborative text editing; reference point if a PNA ever needs shared rich-text notes.
- **[Loro](https://loro.dev)** — Loro (1.0, 2024). Newer CRDT library with movable-tree and rich-text types targeting gaps Automerge/Yjs leave.
- **[ElectricSQL](https://electric-sql.com)** — Server-streams-Postgres-to-client sync engine ("Electric Next"); a sync-boundary alternative to the toolkit's static-mirror ingestion.
- **[PowerSync](https://www.powersync.com)** — Cross-platform SQLite sync with native SDKs; relevant comparison for the storage/sync axes.
- **[LiveStore](https://livestore.dev)** — Johannes Schickling. Event-sourced reactive-SQLite local-first data layer (Riffle lineage); an architectural cousin to the toolkit's OPFS-SQLite reference design.
- **[PGlite](https://pglite.dev)** — Electric. Full Postgres compiled to WASM in the browser; a substrate option if a PNA outgrows SQLite.
- **[Beehive](https://www.inkandswitch.com)** — Ink & Switch, 2024. Local-first, capability-based decentralized access control; relevant if the toolkit's magic-link distribution ever needs principled sharing/revocation. (Link is the lab root; confirm the current project page.)
- **[awesome-local-first](https://github.com/alexanderop/awesome-local-first)** — Curated index of local-first essays, libraries, and sync engines; a maintained map of this whole space.
- **[Behavioural Types for Local-First Software](https://arxiv.org/pdf/2305.04848)** — Academic work on formal verification of local-first systems; the most rigorous treatment of correctness for this app class.

## Contact-data standards

- **[CardDAV (RFC 6352)](https://datatracker.ietf.org/doc/rfc6352/)** — IETF protocol standard for contact-data servers; directly domain-relevant to the toolkit's application class.
- **[vCard (draft-ietf-vcarddav-vcardrev-02)](https://www.ietf.org/archive/id/draft-ietf-vcarddav-vcardrev-02.html)** — The contact-data format underlying CardDAV and most contact-exchange systems.
- **[Defensics vCard Test Suite (Black Duck)](https://www.blackduck.com/fuzz-testing/defensics/protocols/vcard.html)** — Commercial fuzz/robustness conformance suite for vCard implementations.

## Behavioral exceptions & consent propagation

Sources for [`PriorArt.md` § 9](./PriorArt.md) — prior art for the Exceptions concept (a PNA deliberately, honestly departing from a guarantee) and its per-dimension strength profiles.

- **[Macaroons: Cookies with Contextual Caveats for Decentralized Authorization](https://research.google/pubs/pub41892/)** — Birgisson, Politz, Erlingsson, Taly, Vrable, Lentczner (Google, 2014). Bearer credentials whose authority can only be *attenuated* (narrowed) by adding caveats as they pass through intermediaries, never amplified. The closest formal analog to handler clause EX-H7 — consent must reach the ultimate human; a proxy cannot manufacture it.
- **[IAB Europe Transparency & Consent Framework (TCF)](https://iabeurope.eu/transparency-consent-framework/)** — A consent string propagated down a multi-party (ad-tech) delegation chain; prior art — cautionary as much as exemplary — for carrying a consent signal across actors.
- **[Kantara Initiative — User-Managed Access (UMA) & Consent Receipts](https://kantarainitiative.org/)** — Standards for user-controlled delegated authorization and for issuing a machine-readable receipt that a specific consent was given; relevant to recording and propagating the human's consent under an exception.
- **[Common Criteria — Evaluation Assurance Levels (ISO/IEC 15408)](https://www.commoncriteriaportal.org/)** — Graded assurance levels (EAL1–7); the canonical "grade the strength" precedent the strength profile borrows from while rejecting a single collapsed level.
- **[OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)** — Application Security Verification Standard; level-based (L1–L3) assurance — another graded-strength precedent.
- **[SLSA](https://slsa.dev/)** — Supply-chain Levels for Software Artifacts; graded build-integrity assurance levels.
- **[W3C EARL — Evaluation and Report Language](https://www.w3.org/TR/EARL10-Schema/)** — pass / fail / cannot-tell reporting vocabulary; the model for reporting exception handling by ID, including "unable-to-determine".
- **[Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)** — Mitchell et al., 2019. Fixed-structure disclosure of a model's intended use, performance, and limitations; precedent for surfacing strengths *and* limitations legibly (the per-dimension strength profile applies this to a behavioral exception).
- **[Datasheets for Datasets](https://arxiv.org/abs/1803.09010)** — Gebru et al., 2018. Standardized dataset documentation (provenance, composition, limitations); same legible-disclosure lineage as model cards.
- **Apple App Store privacy "nutrition labels"** — Per-app privacy summaries in a fixed structure; a consumer-facing instance of legible strength/limitation labeling.

---

*Reference list compiled from a conversation with Claude (Anthropic), May 2026. See [`PriorArt.md`](./PriorArt.md) for the analytical survey that uses these sources.*
