# Prior Art Survey: Generative Application Class Blueprints

This document surveys the landscape of related work to the Personal Network Toolkit (PNT) — specifically, prior art for what we are calling a *generative application class blueprint*: a machine-readable specification, designed primarily for AI agents to consume, that defines what makes an instance of a *class* of applications correct, and against which many valid implementations can attest conformance.

The survey was conducted as a conversation with Claude (Anthropic) in May 2026, working through three angles: (1) what the agentic-coding industry is publishing in this space, (2) what protocol/standards bodies are doing for analogous "spec a class of artifact" problems, and (3) what production AI app-builders (Lovable, Replit, Bolt, v0) are doing internally that has become public through documentation or leaked system prompts.

The finding is that **no published artifact occupies the same position as PNT**. The closest analogs are either *evaluative* rather than *generative*, *per-project* rather than *per-application-class*, or *stack-coupled* rather than *architecture-coupled*. This justifies continued investment in PNT as a distinct category of artifact.

> **References:** the full annotated source list for this survey lives in [`PriorArtReferences.md`](./PriorArtReferences.md).

## Status
First version - May 23 2026 - [Rich and Claude learn from prior art](https://claude.ai/share/df001d9f-e700-4b8e-be4e-b28470f7f5cf) - define the class of work.

## Working definition

A **generative application class blueprint** has four properties:

1. **Generative** — primarily designed to be read by builders (AI agents) producing new applications, not by auditors evaluating finished ones.
2. **Application-class-scoped** — defines requirements for a *category* of applications (e.g. "personal network applications"), not for a single specific application or a single organization's house style.
3. **Multi-flavor** — admits multiple valid configurations (axis picks, slot choices, profiles) such that many legitimately different implementations can attest conformance.
4. **Machine-checkable** — load-bearing requirements are expressed as typed contracts (JSON Schema, OpenAPI, SQL DDL, TypeScript interfaces) so an agent can verify satisfaction at build time, not just at runtime.

PNT meets all four. Most prior art meets one or two.

## Findings by category

### 1. Spec-Driven Development (SDD) tooling

A consolidated 2026 methodology where humans (with AI help) author a spec, then agents implement against it. Generative but per-project, not per-class.

- **[GitHub Spec Kit](https://github.com/github/spec-kit)** — The most prominent SDD tool. Introduces a four-phase workflow (specify, plan, task, implement) and a `constitution.md` file that holds "immutable principles that govern how specifications become code." The constitution mechanism is structurally similar to PNT's universal architectural commitments, but Spec Kit's constitution is *project-scoped* — every project writes its own. There is no published library of pre-built constitutions for application classes.
- **[spec-kit/spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)** — Spec Kit's own design doc; the clearest published articulation of the SDD philosophy.
- **AWS Kiro, OpenSpec, BMAD-METHOD, Tessl, Google Antigravity** — Per the [BCMS 2026 SDD guide](https://thebcms.com/blog/spec-driven-development), every major AI coding tool now ships its own SDD flavor. All are project-scoped.
- **[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)** (arXiv 2602.00180, Piskala, Jan 2026) — The canonical academic framing of SDD. Distinguishes specs that *execute as validation gates* from specs that are read by humans. Useful theoretical grounding for PNT's contract-as-conformance model.
- **[Augment Code's SDD guides](https://www.augmentcode.com/guides/what-is-spec-driven-development)** — Industry-oriented framing of SDD as "executable contracts that constrain what AI agents generate."

**Proximity to PNT:** Adjacent in mechanism (specs as contracts for agents) but different in scope (per-project vs. per-application-class). Spec Kit's constitution model is the closest pattern.

### 2. AI app-builder system prompts (public via leaks)

The actual production prompts used by commercial AI app-builders. Generative, but stack-coupled rather than application-class-coupled.

- **[x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)** — The canonical leaked-prompts collection (123k stars). Contains extracted system prompts for v0, Cursor, Manus, Same.dev, Lovable, Devin, Replit Agent, Windsurf, Bolt, Augment Code, Kiro, Leap.new, Claude Code, and others.
- **[elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S)** — Mirror repo with the same intent. "AI Systems Transparency."
- **[Lovable Agent Prompt](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Lovable/Agent%20Prompt.txt)** — Notable for its rigorous design-system enforcement (`The design system is everything. You should never write custom styles in components...`) and its `PERFECT ARCHITECTURE` refactoring check. The "blueprint" is a fixed tech stack (React + Vite + Tailwind + shadcn/ui + Supabase) plus a list of architectural MUSTs. No domain-specific layer.
- **[Replit Agent architecture (LangChain breakoutagents)](https://www.langchain.com/breakoutagents/replit)** — Architectural writeup of Replit's multi-agent ReAct-style design. Two prompts (initial code-gen + follow-up) with role-specialized sub-agents (manager + editor).
- **[Pliny the Liberator's Replit Agent leak](https://x.com/elder_plinius/status/1914774065937891398)** — The April 2025 disclosure that revealed Replit Agent uses two cooperating agents rather than one.

**Proximity to PNT:** Informative. These prompts are the empirical record of "how production app-builders encode build rules into agents." Worth reading for the *shape* of effective rules — what's load-bearing, what's discardable. But they encode stack-and-style choices, not application-class semantics. None of them constitute a per-class blueprint library.

### 3. AI app-builder template & constitution mechanisms (official docs)

The vendor-supported mechanisms by which customers extend or customize an app-builder's behavior. The closest *mechanism* to what PNT plugs into, even though the *content* differs.

- **[Replit Enterprise Custom Templates docs](https://docs.replit.com/teams/custom-templates)** — The strongest official analog. Customers create a `custom_instruction/instructions.md` file that "tells Agent how your organization builds software," covering architecture patterns, coding standards, component usage, API patterns, testing requirements, and deployment guidelines. Replit injects this file into the agent's system prompt with a framing preamble. Scope is per-organization, not per-application-class — but the mechanism would accept a PNT-shaped artifact without modification.
- **[Lovable Knowledge Base / Prompting Bible](https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook)** — Lovable's official guidance on writing project-level constraints, design tokens, and backend structure documents that the agent reads on every prompt.
- **[Lovable tech stack architecture writeup (ml6.eu)](https://www.ml6.eu/en/blog/the-anatomy-of-a-lovable-app-and-its-boundaries-in-enterprise-software)** — Third-party but accurate description of "the anatomy of a Lovable app." Useful as a contrast to PNT: this is what a *stack-coupled* application archetype looks like in production.

**Proximity to PNT:** Adjacent in mechanism. Replit Enterprise's `custom_instruction` mechanism in particular is the published artifact PNT would most naturally slot into. The PNT spec could be deployed as a template instructions file with little reshaping.

### 4. Protocol & application conformance test suites (evaluative analogs)

Domain-specific conformance harnesses for classes of artifacts. These are the *evaluative* mirror of what PNT does generatively — they validate finished artifacts rather than guide their construction. Worth knowing as the pre-AI ancestor of this kind of work.

- **[Solid Conformance Test Harness (CTH)](https://github.com/solid-contrib/conformance-test-harness)** — The strongest direct analog by domain (decentralized personal data) and intent (ecosystem interop). Runs tests against Solid server implementations; uses EARL/RDFa for machine-readable reports; uses annotated spec documents as the source of test cases. Designed for *human implementers* running tests against finished servers — i.e., evaluative, not generative.
- **[Inrupt's CTH writeup](https://www.inrupt.com/blog/interoperability-tests-for-solid-developers)** — Best plain-English overview of how the Solid community uses the CTH.
- **[xAPI LRS Conformance Test Suite](https://xapi.com/conformance-test/)** — 1,300-criterion conformance suite for Learning Record Stores in the eLearning domain. Similar pattern: spec + public test suite + registry of certified-conformant implementations.
- **[HL7 FHIR CapabilityStatement](https://www.hl7.org/fhir/capabilitystatement.html)** — The healthcare-app analog. FHIR defines a spec for a class of applications (healthcare data exchange); each implementation publishes a `CapabilityStatement` declaring which profiles and operations it supports. Structurally the closest "axis-attestation" model in any mature standard.
- **[CardDAV (RFC 6352)](https://datatracker.ietf.org/doc/rfc6352/) + [vCard (RFC 6350)](https://www.ietf.org/archive/id/draft-ietf-vcarddav-vcardrev-02.html)** — IETF standards for contact data and contact-data servers. Direct domain relevance to PNT (contact-data application class). vCard has a [Defensics test suite](https://www.blackduck.com/fuzz-testing/defensics/protocols/vcard.html) for fuzz/robustness; CardDAV has informal interop tests but no canonical conformance harness.
- **[W3C EARL (Evaluation and Report Language)](https://www.w3.org/TR/EARL10-Schema/)** — The vocabulary used by Solid CTH and other W3C-adjacent conformance work for machine-readable pass/fail reports. Worth knowing as the standard for third-party conformance attestations.
- **[EU Interoperability Test Bed (ITB)](https://www.itb.ec.europa.eu/docs/guides/latest/definingYourTestConfiguration/index.html)** — Generic harness with the test-subject + actor + test-suite model that Solid's CTH borrowed from.
- **[NIST: What is this thing called Conformance?](https://www.nist.gov/itl/ssd/information-systems-group/what-thing-called-conformance)** — Foundational framing of conformance testing, validation, and certification.

**Proximity to PNT:** Informative. Same end-goal (ecosystem interop across many implementations of one spec) but opposite workflow (poke a finished artifact from outside vs. guide construction from inside). PNT can borrow the test-subject description pattern, the spec-annotation pattern, and possibly the EARL vocabulary for reports, but should not adopt the live-server testing model.

### 5. Architecture standards & Protection Profiles

Pre-existing patterns for "spec for a class of products" in other industries. These predate AI agents but are conceptually closest to PNT's application-class scoping.

- **Common Criteria Protection Profiles** (ISO/IEC 15408) — A Protection Profile is a document describing the security requirements for a *category* of products (e.g., "operating systems," "smart card readers"). Specific products then publish a Security Target declaring "this is the Protection Profile I implement, here's how." Structurally the closest mature analog to PNT's spec + axis-pick attestation model, though heavy and security-flavored.
- **[OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)** — A verification framework for "is this app secure?" with three conformance levels. Level-based attestation ("this app is Level 2 ASVS conformant") is structurally similar to PNT's axis-pick attestation.
- **IEEE 1471 / ISO 42010** — The architecture description standard. Defines vocabulary for architecture description but is prose-oriented and not machine-checkable.
- **TOGAF, NIST SP 800-160, GAMP 5** — Various reference architectures and validation frameworks. Mostly advisory prose; not contract-based.
- **[SLSA (Supply chain Levels for Software Artifacts)](https://slsa.dev/)** — Level-based attestation framework for build provenance. Similar attestation pattern at a different problem (supply chain rather than application class).

**Proximity to PNT:** Informative. The Protection Profile + Security Target pattern from Common Criteria is the closest mature precedent for "per-class spec + per-implementation attestation against it." Worth referencing as the conceptual ancestor even though PNT's typed contracts and AI-readability framing are new.

### 6. Coding agent benchmarks (evaluate the agent, not the application)

What the frontier AI labs publish for testing in this neighborhood. These evaluate *whether an agent can code*, not *whether the resulting code conforms to a class blueprint*. Different category entirely, but worth ruling out as "the thing labs publish that resembles PNT."

- **[Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)** — Anthropic's published methodology for capability evals graduating into regression suites. Directly addresses how the lab thinks about agent testing.
- **[SWE-bench Verified](https://www.swebench.com/verified.html)** — Human-validated subset of 500 GitHub-issue tasks. Evaluates "can the agent patch a real repo and pass existing tests."
- **[Terminal-Bench](https://www.tbench.ai/)** — Terminal-task benchmark for tool-using agents.
- **[SWE-bench Pro / SWE-Bench-CL](https://arxiv.org/pdf/2507.00014)** — Successor benchmarks for harder and continual-learning evaluation.
- **[Anthropic's $20K C compiler experiment](https://www.webpronews.com/anthropics-20000-experiment-how-16-parallel-ai-agents-built-a-100000-line-c-compiler-from-scratch-in-rust/)** — When Anthropic wanted a conformance target for their multi-agent C compiler experiment, they reached for the *existing* C conformance tests rather than building their own. Suggestive: even the labs treat per-class conformance specs as something they consume from standards bodies, not something they author.

**Proximity to PNT:** Distant. These measure the model/agent. PNT measures the application produced by the agent.

### 7. MCP conformance (in-progress)

Worth tracking because it's Anthropic's own protocol and the situation is evolving.

- **[Issue #1990: Add an official MCP conformance test suite](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1990)** — Open request, as of late 2025, for an official conformance test suite for MCP. Still open as of this survey.
- **[MCP roadmap: Conformance Test Suites](https://modelcontextprotocol.io/development/roadmap)** — Explicit roadmap item: "automated verification that clients, servers, and SDKs correctly implement the specification, with coverage expanding alongside each new feature area."
- **[DinCoder MCP conformance doc](https://glama.ai/mcp/servers/@flight505/MCP_DinCoder/blob/6c67715293c9863a9246c0e3a094e2d184e74572/docs/conformance.md)** — Example of an individual MCP implementation publishing its own conformance checklist against spec sections.

**Proximity to PNT:** Adjacent (protocol-level conformance for the protocol PNT canonical MCP servers implement) but not direct (this is server-implementation conformance, not application-class conformance).

### 8. Local-first software research

Background research on the application class PNT targets.

- **[Local-first software (Wikipedia)](https://en.wikipedia.org/wiki/Local-first_software)** — Overview citing the 2019 Kleppmann et al. Ink & Switch paper that coined the term.
- **[Behavioural Types for Local-First Software](https://arxiv.org/pdf/2305.04848)** — Academic work on formal verification of local-first systems. Not a blueprint but the most rigorous treatment of correctness for this app class.

**Proximity to PNT:** Background. Defines the domain but not the class-blueprint approach.

## Proximity matrix

| Artifact | Generative? | Class-scoped? | Multi-flavor? | Machine-checkable? | Overall proximity |
|---|---|---|---|---|---|
| **Personal Network Toolkit (PNT)** | ✓ | ✓ | ✓ | ✓ | — |
| GitHub Spec Kit constitution | ✓ | ✗ (per-project) | ✗ | partial | Adjacent |
| Replit Enterprise custom_instruction | ✓ | ✗ (per-org) | ✗ | ✗ | Adjacent (mechanism only) |
| Lovable system prompt | ✓ | ✗ (stack-coupled) | ✗ | ✗ | Informative |
| Solid Conformance Test Harness | ✗ (evaluative) | ✓ | partial | ✓ | Informative (mirror) |
| HL7 FHIR + CapabilityStatement | ✗ (evaluative) | ✓ | ✓ | ✓ | Closest mature analog |
| xAPI LRS Conformance Suite | ✗ (evaluative) | ✓ | partial | ✓ | Informative |
| Common Criteria Protection Profile | ✗ (evaluative) | ✓ | ✓ | partial | Conceptual ancestor |
| OWASP ASVS | ✗ (evaluative) | ✓ | ✓ (levels) | partial | Conceptual ancestor |
| CardDAV / vCard RFCs | ✗ (protocol) | ✓ | partial | ✓ | Domain-relevant |
| SWE-bench / Terminal-Bench | ✗ (evaluates agent) | ✗ | ✗ | ✓ | Distant |
| Anthropic evals methodology | ✗ (evaluates agent) | ✗ | ✗ | ✓ | Distant |

## Where PNT fits

PNT is positioned at the intersection of three trends that, as of this survey, have not yet been combined in any published artifact:

1. The **Spec-Driven Development** movement (Spec Kit, Kiro, BMAD, OpenSpec, Tessl, the 2026 SDD arXiv paper) has established that machine-readable specs targeted at AI agents are a productive layer. But all of its artifacts are per-project: the spec is written for one application by one team. PNT lifts the spec one level — to a *class* of applications — so the same spec can guide many implementations.

2. The **conformance test suite** tradition (Solid CTH, xAPI, FHIR, W3C, CC Protection Profiles) has long handled per-class specifications, but exclusively in *evaluative* mode: validate finished artifacts against the spec. PNT inverts the workflow: the spec is consumed at *build time* by agents producing the artifact, and the conformance check is satisfaction of typed contracts rather than runtime test pass/fail.

3. The **AI app-builder** ecosystem (Lovable, Replit, Bolt, v0) has built sophisticated agent-prompting machinery for guiding application construction, but exclusively at the *stack* layer: the system prompt encodes "build with React + Tailwind + Supabase," not "build something that behaves like a personal network application." The application-class layer remains in the model weights, not in any spec document.

PNT occupies the otherwise-empty quadrant: *generative + class-scoped + multi-flavor + machine-checkable*. This is the working definition of a generative application class blueprint.

## Conclusion

The survey confirms that no published artifact does exactly what PNT does. The closest mechanism (Replit Enterprise's `custom_instruction`, GitHub Spec Kit's `constitution.md`) is per-project or per-organization. The closest scoping (Solid CTH, FHIR, CC Protection Profiles) is evaluative rather than generative. The closest content (Lovable's system prompt) is stack-coupled rather than class-coupled.

PNT therefore continues as a distinct line of work. The specific architectural constraints of local-first applications operating on contact and relationship data — local execution, firewalled private data layer, SaaS-bridge ingestion, MCP composability, no remote authority — are not adequately captured by any generic per-project SDD tool or per-org template mechanism. A class-scoped blueprint with typed contracts is the right shape for this problem.

The artifacts surveyed remain useful as references:

- **GitHub Spec Kit's constitution model** — for the universal architectural commitments pattern.
- **Replit Enterprise's custom_instruction docs** — as a target deployment mechanism for PNT-shaped artifacts.
- **Lovable's leaked system prompt** — as empirical evidence of what kinds of rules are load-bearing for agents.
- **HL7 FHIR's CapabilityStatement** — as the most mature precedent for axis-pick attestation in a per-class spec.
- **Solid's Conformance Test Harness** — as the source of the test-subject description and spec-annotation patterns.
- **Common Criteria Protection Profiles** — as the conceptual ancestor of class-scoped specs with implementation attestations.

These references inform PNT's design without constraining it to any of their workflows.

