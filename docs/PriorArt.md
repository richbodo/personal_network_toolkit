# Prior Art Survey: Generative Application Class Blueprints

This document surveys the landscape of related work to the PNA Toolkit — specifically, prior art for what we are calling a *generative application class blueprint*: a machine-readable specification, designed primarily for AI agents to consume, that defines what makes an instance of a *class* of applications correct, and against which many valid implementations can attest conformance.

The survey was conducted as a conversation with Claude (Anthropic) in May 2026, working through three angles: (1) what the agentic-coding industry is publishing in this space, (2) what protocol/standards bodies are doing for analogous "spec a class of artifact" problems, and (3) what production AI app-builders (Lovable, Replit, Bolt, v0) are doing internally that has become public through documentation or leaked system prompts.

The finding is that **no published artifact occupies the same position as the PNA Toolkit**. The closest analogs are either *evaluative* rather than *generative*, *per-project* rather than *per-application-class*, or *stack-coupled* rather than *architecture-coupled*. This justifies continued investment in the toolkit as a distinct category of artifact.

> **References:** the full annotated source list for this survey lives in [`PriorArtReferences.md`](./PriorArtReferences.md).

## Status
First version - May 23 2026 - [Rich and Claude learn from prior art](https://claude.ai/share/df001d9f-e700-4b8e-be4e-b28470f7f5cf) - define the class of work.

## Working definition

A **generative application class blueprint** has four properties:

1. **Generative** — primarily designed to be read by builders (AI agents) producing new applications, not by auditors evaluating finished ones.
2. **Application-class-scoped** — defines requirements for a *category* of applications (e.g. "personal network applications"), not for a single specific application or a single organization's house style.
3. **Multi-flavor** — admits multiple valid configurations (axis picks, slot choices, profiles) such that many legitimately different implementations can attest conformance.
4. **Machine-checkable** — load-bearing requirements are expressed as typed contracts (JSON Schema, OpenAPI, SQL DDL, TypeScript interfaces) so an agent can verify satisfaction at build time, not just at runtime.

The toolkit meets all four. Most prior art meets one or two.

## Findings by category

### 1. Spec-Driven Development (SDD) tooling

A consolidated 2026 methodology where humans (with AI help) author a spec, then agents implement against it. Generative but per-project, not per-class.

- **[GitHub Spec Kit](https://github.com/github/spec-kit)** — The most prominent SDD tool. Introduces a four-phase workflow (specify, plan, task, implement) and a `constitution.md` file that holds "immutable principles that govern how specifications become code." The constitution mechanism is structurally similar to the toolkit's universal architectural commitments, but Spec Kit's constitution is *project-scoped* — every project writes its own. There is no published library of pre-built constitutions for application classes.
- **[spec-kit/spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)** — Spec Kit's own design doc; the clearest published articulation of the SDD philosophy.
- **AWS Kiro, OpenSpec, BMAD-METHOD, Tessl, Google Antigravity** — Per the [BCMS 2026 SDD guide](https://thebcms.com/blog/spec-driven-development), every major AI coding tool now ships its own SDD flavor. All are project-scoped.
- **[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)** (arXiv 2602.00180, Piskala, Jan 2026) — The canonical academic framing of SDD. Distinguishes specs that *execute as validation gates* from specs that are read by humans. Useful theoretical grounding for the toolkit's contract-as-conformance model.
- **[Augment Code's SDD guides](https://www.augmentcode.com/guides/what-is-spec-driven-development)** — Industry-oriented framing of SDD as "executable contracts that constrain what AI agents generate."

**Proximity to the toolkit:** Adjacent in mechanism (specs as contracts for agents) but different in scope (per-project vs. per-application-class). Spec Kit's constitution model is the closest pattern.

### 2. AI app-builder system prompts (public via leaks)

The actual production prompts used by commercial AI app-builders. Generative, but stack-coupled rather than application-class-coupled.

- **[x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)** — The canonical leaked-prompts collection (123k stars). Contains extracted system prompts for v0, Cursor, Manus, Same.dev, Lovable, Devin, Replit Agent, Windsurf, Bolt, Augment Code, Kiro, Leap.new, Claude Code, and others.
- **[elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S)** — Mirror repo with the same intent. "AI Systems Transparency."
- **[Lovable Agent Prompt](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Lovable/Agent%20Prompt.txt)** — Notable for its rigorous design-system enforcement (`The design system is everything. You should never write custom styles in components...`) and its `PERFECT ARCHITECTURE` refactoring check. The "blueprint" is a fixed tech stack (React + Vite + Tailwind + shadcn/ui + Supabase) plus a list of architectural MUSTs. No domain-specific layer.
- **[Replit Agent architecture (LangChain breakoutagents)](https://www.langchain.com/breakoutagents/replit)** — Architectural writeup of Replit's multi-agent ReAct-style design. Two prompts (initial code-gen + follow-up) with role-specialized sub-agents (manager + editor).
- **[Pliny the Liberator's Replit Agent leak](https://x.com/elder_plinius/status/1914774065937891398)** — The April 2025 disclosure that revealed Replit Agent uses two cooperating agents rather than one.

**Proximity to the toolkit:** Informative. These prompts are the empirical record of "how production app-builders encode build rules into agents." Worth reading for the *shape* of effective rules — what's load-bearing, what's discardable. But they encode stack-and-style choices, not application-class semantics. None of them constitute a per-class blueprint library.

### 3. AI app-builder template & constitution mechanisms (official docs)

The vendor-supported mechanisms by which customers extend or customize an app-builder's behavior. The closest *mechanism* to what the toolkit plugs into, even though the *content* differs.

- **[Replit Enterprise Custom Templates docs](https://docs.replit.com/teams/custom-templates)** — The strongest official analog. Customers create a `custom_instruction/instructions.md` file that "tells Agent how your organization builds software," covering architecture patterns, coding standards, component usage, API patterns, testing requirements, and deployment guidelines. Replit injects this file into the agent's system prompt with a framing preamble. Scope is per-organization, not per-application-class — but the mechanism would accept a toolkit-shaped artifact without modification.
- **[Lovable Knowledge Base / Prompting Bible](https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook)** — Lovable's official guidance on writing project-level constraints, design tokens, and backend structure documents that the agent reads on every prompt.
- **[Lovable tech stack architecture writeup (ml6.eu)](https://www.ml6.eu/en/blog/the-anatomy-of-a-lovable-app-and-its-boundaries-in-enterprise-software)** — Third-party but accurate description of "the anatomy of a Lovable app." Useful as a contrast to the toolkit: this is what a *stack-coupled* application archetype looks like in production.

**Proximity to the toolkit:** Adjacent in mechanism. Replit Enterprise's `custom_instruction` mechanism in particular is the published artifact the toolkit would most naturally slot into. The toolkit spec could be deployed as a template instructions file with little reshaping.

### 4. Protocol & application conformance test suites (evaluative analogs)

Domain-specific conformance harnesses for classes of artifacts. These are the *evaluative* mirror of what the toolkit does generatively — they validate finished artifacts rather than guide their construction. Worth knowing as the pre-AI ancestor of this kind of work.

- **[Solid Conformance Test Harness (CTH)](https://github.com/solid-contrib/conformance-test-harness)** — The strongest direct analog by domain (decentralized personal data) and intent (ecosystem interop). Runs tests against Solid server implementations; uses EARL/RDFa for machine-readable reports; uses annotated spec documents as the source of test cases. Designed for *human implementers* running tests against finished servers — i.e., evaluative, not generative.
- **[Inrupt's CTH writeup](https://www.inrupt.com/blog/interoperability-tests-for-solid-developers)** — Best plain-English overview of how the Solid community uses the CTH.
- **[xAPI LRS Conformance Test Suite](https://xapi.com/conformance-test/)** — 1,300-criterion conformance suite for Learning Record Stores in the eLearning domain. Similar pattern: spec + public test suite + registry of certified-conformant implementations.
- **[HL7 FHIR CapabilityStatement](https://www.hl7.org/fhir/capabilitystatement.html)** — The healthcare-app analog. FHIR defines a spec for a class of applications (healthcare data exchange); each implementation publishes a `CapabilityStatement` declaring which profiles and operations it supports. Structurally the closest "axis-attestation" model in any mature standard.
- **[CardDAV (RFC 6352)](https://datatracker.ietf.org/doc/rfc6352/) + [vCard (RFC 6350)](https://www.ietf.org/archive/id/draft-ietf-vcarddav-vcardrev-02.html)** — IETF standards for contact data and contact-data servers. Direct domain relevance to the toolkit (contact-data application class). vCard has a [Defensics test suite](https://www.blackduck.com/fuzz-testing/defensics/protocols/vcard.html) for fuzz/robustness; CardDAV has informal interop tests but no canonical conformance harness.
- **[W3C EARL (Evaluation and Report Language)](https://www.w3.org/TR/EARL10-Schema/)** — The vocabulary used by Solid CTH and other W3C-adjacent conformance work for machine-readable pass/fail reports. Worth knowing as the standard for third-party conformance attestations.
- **[EU Interoperability Test Bed (ITB)](https://www.itb.ec.europa.eu/docs/guides/latest/definingYourTestConfiguration/index.html)** — Generic harness with the test-subject + actor + test-suite model that Solid's CTH borrowed from.
- **[NIST: What is this thing called Conformance?](https://www.nist.gov/itl/ssd/information-systems-group/what-thing-called-conformance)** — Foundational framing of conformance testing, validation, and certification.

**Proximity to the toolkit:** Informative. Same end-goal (ecosystem interop across many implementations of one spec) but opposite workflow (poke a finished artifact from outside vs. guide construction from inside). The toolkit can borrow the test-subject description pattern, the spec-annotation pattern, and possibly the EARL vocabulary for reports, but should not adopt the live-server testing model.

### 5. Architecture standards & Protection Profiles

Pre-existing patterns for "spec for a class of products" in other industries. These predate AI agents but are conceptually closest to the toolkit's application-class scoping.

- **Common Criteria Protection Profiles** (ISO/IEC 15408) — A Protection Profile is a document describing the security requirements for a *category* of products (e.g., "operating systems," "smart card readers"). Specific products then publish a Security Target declaring "this is the Protection Profile I implement, here's how." Structurally the closest mature analog to the toolkit's spec + axis-pick attestation model, though heavy and security-flavored.
- **[OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)** — A verification framework for "is this app secure?" with three conformance levels. Level-based attestation ("this app is Level 2 ASVS conformant") is structurally similar to the toolkit's axis-pick attestation.
- **IEEE 1471 / ISO 42010** — The architecture description standard. Defines vocabulary for architecture description but is prose-oriented and not machine-checkable.
- **TOGAF, NIST SP 800-160, GAMP 5** — Various reference architectures and validation frameworks. Mostly advisory prose; not contract-based.
- **[SLSA (Supply chain Levels for Software Artifacts)](https://slsa.dev/)** — Level-based attestation framework for build provenance. Similar attestation pattern at a different problem (supply chain rather than application class).

**Proximity to the toolkit:** Informative. The Protection Profile + Security Target pattern from Common Criteria is the closest mature precedent for "per-class spec + per-implementation attestation against it." Worth referencing as the conceptual ancestor even though the toolkit's typed contracts and AI-readability framing are new.

### 6. Coding agent benchmarks (evaluate the agent, not the application)

What the frontier AI labs publish for testing in this neighborhood. These evaluate *whether an agent can code*, not *whether the resulting code conforms to a class blueprint*. Different category entirely, but worth ruling out as "the thing labs publish that resembles the toolkit."

- **[Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)** — Anthropic's published methodology for capability evals graduating into regression suites. Directly addresses how the lab thinks about agent testing.
- **[SWE-bench Verified](https://www.swebench.com/verified.html)** — Human-validated subset of 500 GitHub-issue tasks. Evaluates "can the agent patch a real repo and pass existing tests."
- **[Terminal-Bench](https://www.tbench.ai/)** — Terminal-task benchmark for tool-using agents.
- **[SWE-bench Pro / SWE-Bench-CL](https://arxiv.org/pdf/2507.00014)** — Successor benchmarks for harder and continual-learning evaluation.
- **[Anthropic's $20K C compiler experiment](https://www.webpronews.com/anthropics-20000-experiment-how-16-parallel-ai-agents-built-a-100000-line-c-compiler-from-scratch-in-rust/)** — When Anthropic wanted a conformance target for their multi-agent C compiler experiment, they reached for the *existing* C conformance tests rather than building their own. Suggestive: even the labs treat per-class conformance specs as something they consume from standards bodies, not something they author.

**Proximity to the toolkit:** Distant. These measure the model/agent. The toolkit measures the application produced by the agent.

### 7. MCP conformance (in-progress)

Worth tracking because it's Anthropic's own protocol and the situation is evolving.

- **[Issue #1990: Add an official MCP conformance test suite](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1990)** — Open request, as of late 2025, for an official conformance test suite for MCP. Still open as of this survey.
- **[MCP roadmap: Conformance Test Suites](https://modelcontextprotocol.io/development/roadmap)** — Explicit roadmap item: "automated verification that clients, servers, and SDKs correctly implement the specification, with coverage expanding alongside each new feature area."
- **[DinCoder MCP conformance doc](https://glama.ai/mcp/servers/@flight505/MCP_DinCoder/blob/6c67715293c9863a9246c0e3a094e2d184e74572/docs/conformance.md)** — Example of an individual MCP implementation publishing its own conformance checklist against spec sections.

**Proximity to the toolkit:** Adjacent (protocol-level conformance for the protocol the toolkit's canonical MCP servers implement) but not direct (this is server-implementation conformance, not application-class conformance).

### 8. Local-first software research

Background research on the application class the toolkit targets.

- **[Local-first software (Wikipedia)](https://en.wikipedia.org/wiki/Local-first_software)** — Overview citing the 2019 Kleppmann et al. Ink & Switch paper that coined the term.
- **[Behavioural Types for Local-First Software](https://arxiv.org/pdf/2305.04848)** — Academic work on formal verification of local-first systems. Not a blueprint but the most rigorous treatment of correctness for this app class.

**Proximity to the toolkit:** Background. Defines the domain but not the class-blueprint approach.

### 9. Behavioral exceptions, consent propagation, and graded assurance

Prior art for the [Exceptions](../spec/exceptions.md) concept — a PNA *deliberately and honestly* departing from a guarantee — and for its per-dimension strength profiles. Surveyed when designing `EX-CLOUD-LLM`.

- **Graded assurance levels.** Common Criteria EAL, [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) levels, and [SLSA](https://slsa.dev/) levels (all surveyed in § 4–5) establish the *grade-the-strength* precedent. The toolkit's strength profile borrows the idea but **rejects a single collapsed level** in favor of per-dimension classes — one number would hide that "the boundary is enforced" and "the provider's data handling is unverifiable" are different *kinds* of assurance.
- **Machine-readable conformance reporting.** [W3C EARL](https://www.w3.org/TR/EARL10-Schema/)'s pass / fail / cannot-tell vocabulary is the model for the evaluate flow reporting exception handling by ID (including "unable-to-determine").
- **Consent propagation through delegation chains.** The IAB Europe [Transparency & Consent Framework](https://iabeurope.eu/transparency-consent-framework/) (a consent string propagated down an ad-tech chain), [User-Managed Access and Consent Receipts](https://kantarainitiative.org/) (Kantara), and **macaroons** (Birgisson et al., Google Research, 2014 — bearer credentials with *attenuating* caveats). Macaroons are the closest match to handler clause EX-H7: delegated authority only **narrows** as it passes through intermediaries, never amplifies — exactly the property "consent must reach the ultimate human; a proxy can't manufacture it" requires.
- **Legible strength/limitation labeling.** Apple privacy "nutrition labels", [model cards](https://arxiv.org/abs/1810.03993) (Mitchell et al., 2019), and [datasheets for datasets](https://arxiv.org/abs/1803.09010) (Gebru et al., 2018) — precedent for surfacing strengths *and* limitations in a fixed, user-readable structure. The per-dimension strength profile is this idea applied to a behavioral exception.

**Finding:** the *mechanics* — grade the strength, attest it, propagate attenuated consent, report cannot-tell — have solid precedent, and the toolkit borrows them rather than inventing. What appears genuinely new is **framing a deliberate behavioral deviation as a first-class, stable-ID'd, caught-and-handled "exception" for an application class**; no surveyed artifact offers a description language for that. The human-AI-team development context is why it surfaces now.

**Proximity to the toolkit:** Informative (mechanism). The grading, reporting, and attenuation patterns are adopted; the exception-as-class-concept is the novel part.

## Proximity matrix

| Artifact | Generative? | Class-scoped? | Multi-flavor? | Machine-checkable? | Overall proximity |
|---|---|---|---|---|---|
| **PNA Toolkit** | ✓ | ✓ | ✓ | ✓ | — |
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

## Where the PNA Toolkit fits

The PNA Toolkit is positioned at the intersection of three trends that, as of this survey, have not yet been combined in any published artifact:

1. The **Spec-Driven Development** movement (Spec Kit, Kiro, BMAD, OpenSpec, Tessl, the 2026 SDD arXiv paper) has established that machine-readable specs targeted at AI agents are a productive layer. But all of its artifacts are per-project: the spec is written for one application by one team. The toolkit lifts the spec one level — to a *class* of applications — so the same spec can guide many implementations.

2. The **conformance test suite** tradition (Solid CTH, xAPI, FHIR, W3C, CC Protection Profiles) has long handled per-class specifications, but exclusively in *evaluative* mode: validate finished artifacts against the spec. The toolkit inverts the workflow: the spec is consumed at *build time* by agents producing the artifact, and the conformance check is satisfaction of typed contracts rather than runtime test pass/fail.

3. The **AI app-builder** ecosystem (Lovable, Replit, Bolt, v0) has built sophisticated agent-prompting machinery for guiding application construction, but exclusively at the *stack* layer: the system prompt encodes "build with React + Tailwind + Supabase," not "build something that behaves like a personal network application." The application-class layer remains in the model weights, not in any spec document.

The toolkit occupies the otherwise-empty quadrant: *generative + class-scoped + multi-flavor + machine-checkable*. This is the working definition of a generative application class blueprint.

## Conclusion

The survey confirms that no published artifact does exactly what the toolkit does. The closest mechanism (Replit Enterprise's `custom_instruction`, GitHub Spec Kit's `constitution.md`) is per-project or per-organization. The closest scoping (Solid CTH, FHIR, CC Protection Profiles) is evaluative rather than generative. The closest content (Lovable's system prompt) is stack-coupled rather than class-coupled.

The toolkit therefore continues as a distinct line of work. The specific architectural constraints of local-first applications operating on contact and relationship data — local execution, firewalled private data layer, SaaS-bridge ingestion, MCP composability, no remote authority — are not adequately captured by any generic per-project SDD tool or per-org template mechanism. A class-scoped blueprint with typed contracts is the right shape for this problem.

The artifacts surveyed remain useful as references:

- **GitHub Spec Kit's constitution model** — for the universal architectural commitments pattern.
- **Replit Enterprise's custom_instruction docs** — as a target deployment mechanism for toolkit-shaped artifacts.
- **Lovable's leaked system prompt** — as empirical evidence of what kinds of rules are load-bearing for agents.
- **HL7 FHIR's CapabilityStatement** — as the most mature precedent for axis-pick attestation in a per-class spec.
- **Solid's Conformance Test Harness** — as the source of the test-subject description and spec-annotation patterns.
- **Common Criteria Protection Profiles** — as the conceptual ancestor of class-scoped specs with implementation attestations.

These references inform the toolkit's design without constraining it to any of their workflows.

## Design notes

A running log of toolkit-shaping decisions and their rationale — most often a mapping of the toolkit against the prior art above driving a spec change (or a deliberate decision *not* to make one), but also discipline and tooling decisions distilled from a real finding in a reference design. This is where the *why* of a toolkit fix lives when it isn't itself a reference design. Newest first; each entry is dated and names what it changed.

### 2026-06 — `just validate <path>`: the deterministic-baseline spine landed

The [`just validate` design note](design-notes/2026-06-validate-command-and-strength-tiers.md) sketched a
one-command audit with an S/L/F strength gradient; its **Tier-S spine is now built**
(`tools/validate.py`, `just validate <candidate>`). It runs the existing deterministic lints and folds them
into one `evaluate-report.json` — the same typed artifact the Visual Validator renders and a contribution
commits — detecting (not running) a cooperating design's Tier-F `[verify]` entrypoint. The load-bearing
decision is **honesty over a green light**: the assembler downgrades a *clean* deterministic scan to
`unable-to-determine` (necessary, not sufficient) and reserves `non-conformant` for a check that actually
finds a violation, so it never confers a `conformant` verdict on its own — a clean run is a triage baseline,
not a trust certificate (the note's "lite-as-full risk", now closed in code). Tiers L (the LLM evaluate flow)
and F (the design's entrypoint) enrich the same report afterwards; the deterministic `/pna-evaluate` UX (#55)
becomes a thin wrapper over this baseline. A six-assertion self-test pins the exit-code contract, the report's
schema-validity, and the clean→`unable-to-determine` / dirty→`non-conformant` mapping on the egress fixtures.

### 2026-06 — Goals restructured 5 → 4 (outcome altitude; mechanism ≠ goal)

The goal layer read as a list of *mechanisms* ("store two databases", "locally diagnosable") rather than
*outcomes*, which invited mis-filing and made the goals do little partitioning work. Restructured to four
app-framed, outcome-altitude goals — **Take ownership of the root · Protect the root's integrity by
validation · Protect the root from egress · Protect the root from entropy & accidents** — each with a
readable per-goal template (outcome → example mechanism → why it matters → the ACs it requires), validated
by an AC→goal categorization (all 25 ACs fit; ~92% single-home). Privacy/disclosure and communication
merged into one *egress* goal (both are "control what leaves the root"); diagnosability folded into
validation; durability kept as its own *protect-from-loss* goal; usability promoted to a preamble
assumption above the goals. **Goal ↔ AC is many-to-many, rendered primary-grouped** — each AC has one
primary home plus at most one cross-cut (capped and now lint-enforced) — and a new cardinality note states
how every spec component relates (rule of thumb: Goals are few and crisp; everything beneath composes
many-to-many, but the reading views stay clean trees). No AC requirement changed (a re-presentation, no
new obligation; Toolkit-Version stays 0.1-draft). A new lint check (check 9) plus the
**definition-before-first-use** rule (memorialized in `CLAUDE.md`) keep the renumber from silently
rotting. Worked out in the 2026-06-14 direction session.

### 2026-06 — The mitigation side of Exceptions: a countermeasure library + the Harden sibling

The Exceptions mechanism made *declaring* a deviation honest; it said little about *defending* against
the hazards a deviation (or an adversarial runtime) exposes. This reframe gives that mitigation side a
home. **EX-H6's "recommended solution" becomes a reusable [countermeasure library](../spec/exceptions.md#countermeasure-library)**
— a hazard-keyed catalog reusing the EX-H8 strength vocabulary (so the existing strength lint covers it),
each row tagged **PNA-intrinsic vs environmental** and pointing at a demonstrator. The split is
load-bearing: intrinsic countermeasures are the PNA's own code (tied to an AC, demonstrable), while
environmental ones (sandbox the OS-automation agent, a separate OS user, an MCP access broker, a
honeytoken+watchdog) live in the user's environment, where the toolkit can only **advise** — which names
a **fourth, advisory flow, Harden**, the sibling of Exceptions for *detected* (not user-raised) hazards.
It completes a four-source taxonomy of pressure on the guarantees — **Constraints** (platform ceiling) ·
**Exceptions** (user relaxation) · **Environmental threats** (adversary in the runtime) ·
**User-mediation** (actuation boundary) — and draws the line *app-security = build/evaluate/contribute;
environment-security = harden/advise*. Seeded by the data-protection-vs-OS-automation research (R3),
which **re-confirmed at-rest encryption stays deprecated**: the catalog deliberately favors mediating the
access path and detect-then-respond over encrypting the store away from its owner (tool-readability is a
PNA value; see [`constraints.md`](../spec/constraints.md), `CST-PWA-SANDBOX-SEALED`). Additive and
advisory — no new obligation; the RFC predicate-split / EX-H7 fail-closed / un-relaxable-floor proposals
are untouched and still demonstrator-gated (promotion tracked as a separate follow-up). A
fault-injection self-test now pins the strength-class lint against the new catalog (it previously had
none — the PR #18 dead-check pattern). Worked out in the 2026-06-14 direction session.

### 2026-06 — Data-floor: bound *what* an exception can disclose (proposal → PRM v0.2)

*Full stub: [`design-notes/2026-06-data-floor-disclosure-tiers.md`](design-notes/2026-06-data-floor-disclosure-tiers.md). Companion to [PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32); came out of the [existential review](design-notes/2026-06-exceptions-existential-review.md)'s tournament of alternate solutions.*

PR #32 governs the *act* of a cloud disclosure; the `EX-CLOUD-LLM` strength profile still grades the *data* at `provider-asserted` / `none`. A moderated tournament of alternate solution sets found the strongest missing piece is an **architectural data-floor**: a per-field Private-DB **disclosure tier** (`PR-7`, default `private-sealed`, workspace-only, enforced at the query layer), a **projection-bound cloud surface** that structurally cannot return a sealed field even with consent (`AC-MCP-C` — the data twin of AC-MCP-B's action-floor), and a **blast-radius** strength dimension (`EX-H9`) — verified by a static disclosure-tier lint + a dynamic egress probe. It converts the profile's worst dimensions (`none` / `provider-asserted`) toward `enforced` / `verifiable` and degrades gracefully when consent fails. Demonstrable, not speculative: `fellows_local_db` already exposes groups-only on its private MCP surface (`mcp_servers/private_data_ops.py`), and PRM already plans per-field provenance + most-protective-default AI-write tiers — the disclosure tier is the read-side mirror. Per `CONTRIBUTING.md` it lands **with** its demonstrator (**PRM v0.2**, candidate `AC-PRM-G`); this entry records the design on the stick, not a normative change.
### 2026-06 — Should the spec allow Exceptions at all? Existential review → keep, with three sharper lines

*Full deliberation: [`design-notes/2026-06-exceptions-existential-review.md`](design-notes/2026-06-exceptions-existential-review.md). Proposed changes: [PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32).*

The hardest question yet aimed at the toolkit: **does admitting `EX-*` exceptions corrupt the spec?** A PNA that raises `EX-CLOUD-LLM` (as `fellows_local_db` does to connect Claude Desktop) is deliberately leaving local-only — so once any PNA can be in a "not a PNA" mode, does "PNA" still mean anything? Worked via two **adversarial analyses** (steelman FOR vs. steelman AGAINST, each rebutting the other) plus a synthesis pass. The setup that reframes everything: an MCP server **cannot** tell a cloud LLM from a local one (`clientInfo` is self-reported, OAuth runs client→server, the host owns the data post-handoff — see PRM's `mcp-cannot-identify-the-consuming-llm` note), so local-only *at the MCP boundary* is **architecturally unenforceable**, and the real choice is *governed* vs. *ungoverned* egress, not egress vs. none.

**Conclusion: keep exceptions — the mechanism isn't the corruption; an *unverifiable purity claim* would be.** The two analyses converged on everything but one word, which located the actual fix. Three corrections (proposed in PR #32): **(1)** split the overloaded "conformant PNA in non-PNA mode" into **`pna-active`** (the mode bit a relying party / interop gate keys on — `false` while an exception is active) and **`exception-handling` conformant** (the process) — the fellows banner already says "Going rogue — not a PNA," so the spec's prose was *less honest than the reference design's own UI*. **(2)** harden **EX-H7** from best-effort to **fail-closed** — consent on a PNA-controlled surface, a best-effort "confirm in the app" relay up to cooperating clients, hard refuse down when a human can't be confirmed (this is "want vs. need" resolved into **provenance + comprehension**). **(3)** an **un-relaxable floor** (AC-18 / AC-19 / AC-MCP-B): a user may consent to *disclose data they read*, never to remove the human-in-the-loop on *action taken on their behalf*, which reaches third parties. The framing that ties it together: the north star is **informed autonomy over your own network**, not maximal confinement — and the design is made from behind a *veil of ignorance*, so the floor protects the least-technical user while the opt-out serves the one who knowingly wants it. Future-defense directions noted for later write-ups: the friendly-machine consent relay, a **runtime** egress probe complementing the static [`tools/egress-lint.py`](../tools/egress-lint.py), and opt-in OS-level alerts. Distilled from a Claude Code session alongside the PRM reference design.

### 2026-06 — What is the minimal PNA? Slots optionality + the Workspace as consent boundary

The slot map said only Distribution was optional, which is too strict: Goal 3 (outreach) is conditional, so a PNA that never reaches out needs no Communications slot. The honest split is **Required = Ingestion + Storage + Workspace; Optional = Communications + Distribution** — a *relaxation* (no existing design becomes non-conformant; a smaller app can now qualify). That named a new floor use case, the **Minimum Viable PNA / "Personal Vault"** (ingest + store + a minimal workspace; nothing leaves the device). The sharp question that fixed the framing: *can MCP servers replace the Workspace?* Not in v0.1 — and the reason is the load-bearing insight: the Workspace isn't "a UI," it is the surface that **writes private data and is the human-in-the-loop consent boundary**. MCP can take over rendering, but (a) the v1 data-ops MCP servers are read-only, so private *writes* need a non-MCP surface, and (b) AC-MCP-A/B make the Workspace the mandatory consent point (the MCP server proposes; the Workspace disposes), while EX-H7 forbids an intermediary agent from self-consenting for the human. So the Workspace stays required, its *form* is the `workspace-shell` axis, and a genuinely headless / MCP-native PNA is a v0.2+ target — reachable once write-side MCP tools land and the consent boundary moves into a thin, PNA-owned confirmation shell.

### 2026-06 — Spec readability vs. machine-contract: lead with prose, keep IDs stable

The PNA spec read as a machine contract first and a human document second: register-switching with no signposting (goals → ACs → slots → 57 sub-contracts), cryptic axes terminology ("triggered flavor-derived ACs"; a `[dist:server-backed]` "Triggered by" column), and dense reference material interleaved with narrative. A readability pass (`spec/PNA_Spec.md` + `spec/axes.md`) addressed this under a hard constraint that PR #27 had just sharpened: **the spec is also an external API** — `tools/lint-spec-ids.py` parses its tables and the `<a id>` anchors are deep-linked from reports — so we may rearrange and rename freely but must never move a stable ID or drop an anchor. The resulting rules, worth keeping: IDs were first kept in table column 1, then — once the lint was made **header-aware** (it locates each ID column by header name, so column order no longer matters) — moved to the **last** column so the prose leads in every table, with editor notes at the top of each parsed file warning that the tables are an API for the lint *and* external report writers; the densest reference (sub-contracts) is signposted "skip unless implementing" rather than moved (and now carries `<a id>` anchors, like slots and interfaces, so reports can deep-link to it); and the core `axis`/`pick`/`flavor` vocabulary is **glossed** in plain English rather than renamed, because it is load-bearing in `design.toml`, the lint, and the skill. The general lesson for a dual-audience spec: readability work is *bounded by* the machine contract — make the prose lead, but treat the IDs and table shape as the API they have become.

### 2026-06 — Attestation evidence must be *live*: the xfail-as-evidence finding → marker-state lint + deferral discipline

A `conformant` row in the fellows_local_db Security Target cited an `xfail(strict=True)` test as its proof, and every gate stayed green — the attestation-evidence checker only verified the cited test *resolved to a `def`*, never that it *passed* or wasn't deferred. A declared-false invariant was masquerading as evidence. Origin: the conformance-discipline work in `richbodo/fellows_local_db` (PR #249).

**What it drove (a toolkit fix — no spec-AC change):**

- **`tools/attestation-evidence-lint.py` (new, portable).** The reference checker the template only *described* in prose is now a real stdlib lint with clean/dirty fixtures and a self-test, mirroring `egress-lint` / `export-readable-lint`. It adds the **marker-state** rule: a `conformant` row may not cite an `xfail` or unconditional `skip` test (a conditional `skipif` environment guard is exempt). This is the *deterministic* half of "exists **and passes**" — a static lint proves a *live, non-deferred* assertion exists; *passes* is the runtime layer (run the suite).
- **Deferral discipline (`ARCHITECTURE_TEMPLATE.md` § Deferrals).** A strict-xfail must carry a `tracking: #NNN` **issue** anchor — an issue, not a PR (issues close when the *work* is done). Names the **asymmetry**: `strict=True` trips on accidental success but never on abandoned deferral, so it needs reinforcing — an abandoned-deferral check (issue closed while the test still xfails) and a low, glanceable deferral cap.
- **Validation timing (`ARCHITECTURE_TEMPLATE.md`).** The load-bearing principle is **non-conforming code must not reach users**: run lint + tests at the user-exposure boundary (ship / per-PR / release), with adding-or-removing-a-feature as the re-check trigger. The cap is secondary hygiene; the gate is the safety mechanism.

**The reusable lesson:** a portable *existence* checker created false confidence that the *passing* check was also covered — the seam between the deterministic layer (lints) and the runtime/human layer (the suite, the maintainer) was unowned. The fix names that layering explicitly instead of pretending one lint does it all. Demonstrated end-to-end by fellows_local_db (the lint, a report/log with an issue-state probe, and `just test` / `deploy-preflight` wiring).

### 2026-06 — Documentation architecture: one source of truth per fact, and a same-PR doc-currency rule

The docs had drifted behind the code: the `justfile`, the lint self-tests, `export-readable-lint`, the Constraints and Exceptions concepts, and the `design.toml` manifest had all shipped while `docs/users-guide.md` still described `swh-save` as "planned." Separately, the guide's "Goal 4 / 5 / 6" sections had become an overflow bucket — archival, version-bumping, and AC-attestation facts thrown wherever there was room, restating policy that `CONTRIBUTING.md` and the spec already owned.

Decided: (1) **one source of truth per fact** — the spec owns *what conformance means*, the skill owns *agent procedure*, `docs/users-guide.md` owns *the step-by-step how-to*, `CONTRIBUTING.md` owns *policy*; a doc links to the owner rather than restating it (every restatement is a drift surface). (2) The user's guide is a **task-ordered procedure layer** — numbered action sequences — which dissolved the incoherent goals (archival/versioning became the tail of the Contribute flow; the attestation steps folded into Build). (3) A **same-PR doc-currency rule**: any PR changing a developer-visible behavior updates the user's guide in the same PR, stated in `CLAUDE.md` and enforced by a PR-template checkbox. Recorded in `CLAUDE.md` (§ Documentation map, § Keep the docs current) and `.github/pull_request_template.md`.

The framing that ties it together: doc drift and lint-check rot (cf. the dead `Reversible:` check, PR #18) are the same disease — a guarantee quietly becoming false — so they get the same medicine: make the absence fail loudly (the doc rule socially; the lint self-tests mechanically). This entry, and the first-classing of the toolkit-fix contribution path it ships alongside, are themselves toolkit fixes following that newly-documented path.

### 2026-06 — Ink & Switch "local-first" ideals → PR-6, and the at-rest scope decision

Mapping the spec against the Ink & Switch [*local-first software*](https://www.inkandswitch.com/essay/local-first/) essay (§ 8 above) surfaced two gaps. One became a spec change; the other became an explicit decision *not* to add one. Origin: `richbodo/fellows_local_db#216`.

| Ink & Switch ideal | PNA spec coverage | Status |
|---|---|---|
| 1. No spinners (fast/local) | Implicit — AC-1 puts both DBs in local SQLite; AC-5 falls through to local cache on auth failure; AC-PRM-D forbids background polling. Not a named goal. | Structurally yes, not contractually stated |
| 2. Not trapped on one device | Goal 4 gives backup/restore + AC-9 auto-snapshots + PR-5 idempotent migrations + **PR-6 tool-free export** — manual portability, not sync. | Aligned (portability); sync deliberately deferred |
| 3. Network is optional (offline) | Strong yes. AC-5 cached fallback, AC-PRM-D no background polling, Browser PNAs run offline by construction. | Aligned |
| 4. Seamless collaboration (real-time multi-user) | Not a goal. PNAs are personal. A Directory Archive ships the same Shared DB to many users with independent Private overlays, but no merge, no CRDT, no real-time. | Deliberately not in scope |
| 5. The Long Now (longevity) | Strong, arguably more concrete than I&S. SWHID archival of reference designs is mandatory. AC-2 forbids a SaaS surface on the distribution server. The Distribution slot is optional — a single-user PNA runs forever with no server. | Aligned, arguably stronger |
| 6. Security and privacy by default | Stronger than I&S on the network threat: the Private DB never leaves the device (Goal 3) — more absolute than I&S's E2E-encrypted *sync*. AC-18, AC-19, AC-PRM-A, AC-MCP-A. **At-rest-against-local-access is the one gap — and a deliberate scope decision, not a missing AC** (see below). | Stronger on the network threat; at-rest deliberately out of scope |
| 7. Ultimate ownership and control | Aligned and explicit. Goal 2 (integrity-by-validation) requires source availability to the user — stronger than I&S, which said open source isn't required. AC-2 prevents architectural lock-in; PR-5 idempotent backup/restore. **Gap closed by PR-6:** the export is now a format a non-developer can open in another tool, not just "your data is in a SQLite file." | Aligned; export-format gap closed |

**What it drove:**

- **Ideal #7 → PR-6 (added).** The practical-ownership gap — owning the bytes is not the same as being able to *read* them without a SQLite browser — became a Private-schema sub-contract: a flat, human-readable export (CSV / schema-embedded JSON / Markdown) readable with no PNA tooling, SHOULD-level, demonstrated by `export-readable-lint.py`. The "Long Now" test (all toolkit tooling vanishes; can a non-developer still use their notes?) now has a real answer.
- **Ideal #6 → no universal at-rest AC (decided against).** The at-rest gap is real but narrow, and a universal AC is the wrong instrument. The threat it addresses — an adversary with *local access to the device* — is **outside v0.1's threat model** (which is network/platform exposure); its strongest forms are **platform-provided** (OS full-disk encryption already covers the powered-off-device case, better, and app-level encryption can't help a running, unlocked machine); a boolean "encrypted at rest" AC would invite **false assurance** under the evidence-discipline rules and tension with Goal 4 (a lost key is lost data). At-rest encryption stays a **flavor** (`native-sqlcipher`), with key-management ACs deferred until a SQLCipher reference design demonstrates them and a per-dimension **strength profile** required at attestation rather than a boolean. Recorded normatively in `spec/PNA_Spec.md` § Scope and versioning. (Notably, I&S's own answer to ideal #6 was E2E-encrypted *sync*, which the toolkit rejects by not syncing at all — so the at-rest gap is orthogonal to what I&S meant.)

**Structural differences worth keeping in mind** (why the mapping isn't 1:1): I&S's seven ideals are *properties* (observable, aspirational, framed as UX); the toolkit's ACs are *contracts* (RFC 2119 MUST/SHOULD pinned to architectural seams), which is what makes the toolkit machine-checkable where I&S isn't. The toolkit also covers ground I&S didn't anticipate — the Shared/Private split itself, and the AI-as-transport framing (AC-PRM-A, AC-MCP-A/B). And it deliberately omits what I&S centers: CRDTs, real-time collaboration, cross-device sync.

### 2026-06 — The evaluate-report has two valid producers; name the artifact so an internal readout can't be mistaken for it

Auditing `fellows_local_db` surfaced a discoverability trap: the design ships *two* conformance artifacts derived from one attestation source — a design-internal ship-gate readout at `docs/conformance/report.json` (fellows-format, carries fellows-local `UM-*` rows) and the toolkit's render-contract artifact `docs/conformance/evaluate-report.json`. An auditor landing in `docs/conformance/` reaches for `report.json` first and validates the wrong file against `tools/evaluate-report.schema.json` — a false "non-conformant report shape" signal. Two decisions came out of it, recorded as a toolkit fix (no new design obligation): **(1)** the docs now name the **canonical filename (`evaluate-report.json`)** and state explicitly that a design's other conformance readouts are not this artifact, so the artifact is identified by name+schema, not by directory convention. **(2)** A design's deterministic `[verify].entrypoint` emitter is recognized as a **first-class producer** of the artifact, co-equal with the skill's LLM evaluate flow — the deterministic path is *more* reproducible (same commit + same attestation → byte-identical output) and is the stronger evidence tier for a contribution (cf. the `[verify]`-runs-it "Tier F" in [`design-notes/2026-06-validate-command-and-strength-tiers.md`](design-notes/2026-06-validate-command-and-strength-tiers.md)). The SKILL had only ever framed the evaluate-report as the *output of the LLM flow*; both producers now appear, and the agent is told to confirm which file is a schema instance when a candidate ships several. Origin: PNT audit of `richbodo/fellows_local_db` at `6697b00` (the `evaluate-report.json` emitter, `fellows_local_db#267`, postdated that commit).

