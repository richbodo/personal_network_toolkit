# Paper 2 — Generative + Evaluative Application-Class Blueprints in the AI Era: A Personal Network Toolkit Case Study

> **Status:** skeleton + executive summary + section-by-section outline for expansion. This is a *working draft scaffold*, not a finished paper. Key claims and citations are placed under each heading; full prose is to be written from this frame.
>
> **Type:** **case study / experience report**, *not* a proposal for a new standard. The strong claim — that the four-tradition recombination this paper describes is currently *unoccupied* — is offered as a surveyed-and-not-found result; the stronger gloss ("we created a field") is flagged throughout as a **wager**, to be earned by a second worked example, not asserted.
>
> **Companion:** Paper 1 ("Where the personal-network-application class sits" — the behavioral directed graph positioning PNAs among local-first / sovereignty / assurance / machine-followable-spec families). The two papers share one asset (the directed graph) and split the work: **Paper 1 places the *application class*; Paper 2 (this one) places the *method* used to specify it.**
>
> **Source provenance:** distilled from the toolkit's own artifacts (`spec/PNA_Spec.md`, `pna-toolkit/SKILL.md`, `docs/PriorArt.md`, `docs/PriorArtReferences.md`) and the R2/R4 research synthesis in `brainstorms/2026-06-14-pnt-direction-grill.md` (Q9 R4 findings; R2 SYNTHESIS Family IV + its conformance-model sub-axis). Citations below were web-verified June 2026.

---

## Executive summary

Software is increasingly *regenerated* rather than maintained: developers and non-developers alike now compose and re-compose applications by prompting AI agents, and an app's correctness is increasingly measured by how faithfully an agent adheres to a specification rather than by the durability of hand-written code. In that world the **durable, machine-checkable specification — not the code — becomes the natural unit of software**, because it is what carries the safety, privacy, and architecture context you do not want to re-explain on every "add this feature." A year ago treating the spec as the artifact-of-record was abnormal; today it is becoming normal.

The Personal Network Toolkit (PNT) is a worked instance of a specific, and we argue currently **unoccupied**, kind of artifact: a **goal-anchored, machine-checkable blueprint for a whole *class* of applications** (here, "personal network applications" — local-first, private-by-default apps that mirror SaaS contact data into a user-owned store) that is **both generative and evaluative**. One artifact (goals → constraints → architectural commitments → typed contracts, plus axes/flavors, reference designs, lints, an LLM-judge evaluate flow, and human review, packaged as an agent skill) is read by AI agents to **build** conformant instances *and* read by AI agents to **evaluate** whether an arbitrary candidate conforms.

We position this method in a white space bounded by **four mature traditions**, of which PNT is a novel recombination:

1. **Software Product Lines (SPL) / FODA / FORM / Generative Programming** — PNT's *axes and flavors* are, structurally, a **feature model** (specifically an *orthogonal variability model*), and FORM's split of *domain engineering* vs *application engineering* maps onto PNT's *build-the-spec* vs *build-an-instance*. **What PNT changes: it replaces the automated code generator with an AI agent as the "application engineer."**
2. **Common Criteria Protection-Profile (PP) *authoring* methodology** — the only widely standardized "blueprint-for-blueprints" (a PP describes requirements for a *category* of products; a per-product Security Target attests against it; the paired Common Evaluation Methodology says how to evaluate). **What PNT changes: it adopts the PP/ST *structure* but drops its *certification authority* — conformance is "checked, not awarded."**
3. **W3C spec + test-suite methodology** — the discipline that "a spec is real only when independent implementations demonstrate each feature" (the two-interoperable-implementations exit criterion + machine-readable implementation reports). PNT's rule that *reference designs must demonstrate every change* is this discipline. **What PNT changes: it targets a multi-flavor *class*, not a single technology, so "demonstrate the feature" becomes "demonstrate the feature at a flavor."**
4. **AI-era spec-driven development (SDD): GitHub Spec Kit, AWS Kiro, OpenSpec, and the SDD survey** — AI-builds-from-spec, plus a "constitution"/steering layer and cross-artifact consistency checks. **What PNT changes / what these miss: per-project, single-app scope — no class scope, no multi-flavor variability, and no flow for evaluating an *arbitrary third-party candidate.***

**The cleanest novel claim** is a **bidirectional spec**: *one* goal-anchored, machine-checkable artifact that both **generates** conformant instances of a multi-flavor application class **and evaluates** arbitrary candidates of that class — built by AI agents, with conformance **checked** (deterministic lint + LLM-as-judge + human review) rather than **awarded**, and shipped as an **agent skill**.

**Recommendation (evidence-safe):** publish *now* as a **case study**. A generalized meta-repo — a PP-style "authoring guide for AI-era application-class blueprints" — is the genuinely-lacking upstream artifact, but it is warranted only **once a second application class validates the method's generality**. Until then, lead with the single worked example and treat "this is a new field" as a wager, not a finding.

**Candidate venues:** SPLC (Software Product Line Conference — the variability-model home), Onward! (where the local-first essay landed; tolerant of method/experience papers), MODELS (variability + model-driven engineering), an arXiv preprint for timestamped reach, and a local-first community whitepaper for the practitioner audience.

---

## Paper outline (top level)

1. Introduction — why now, and the artifact in one paragraph
2. Background: the personal network toolkit as a concrete object
3. The four bounding traditions (related work, told as a map not a list)
4. The white space and the bidirectional-spec contribution
5. Method in detail: how PNT generates *and* evaluates from one artifact
6. "Checked, not awarded": the conformance model and why it diverges from certification
7. Lessons learned (the experience-report core)
8. Limitations, threats to the claim, and what would falsify it
9. Generalization & recommendation: when a meta-repo is warranted
10. Conclusion
- Appendix A: tradition-by-tradition comparison table (the load-bearing figure)
- Appendix B: the bidirectional-spec object model (goals → constraints → ACs → contracts; axes/flavors; lint/LLM/human layers)
- Appendix C: mapping PNT vocabulary ↔ SPL vocabulary (adopt the established terms)

---

## Section-by-section skeleton

### 1. Introduction — why now, and the artifact in one paragraph

**Purpose:** state the "why now," the thesis, and the artifact, before any related work.

**Key claims**
- **"Why now."** AI agents now routinely *write and re-write* application code from natural-language prompts; the spec-driven-development movement has consolidated around the position that the spec, not the code, is the load-bearing human-authored artifact, and that a behavior is only really *specified* when its conformance is checked by code (schema/test/eval/runtime-guard) rather than asserted in prose. Cite the SDD survey and Spec Kit for the consolidation; cite PNT's own internal discipline ("convert an absent guarantee into a red test, never a silent pass," `CLAUDE.md`) as a field-independent restatement that the R2-D survey found the wider field converging on.
- **The unit-of-software shift.** When code is cheap to regenerate and easy to make ephemeral, the *durable* thing worth owning is the machine-checkable spec that carries the safety/architecture context — so that an agent re-deriving the app does not silently drop a privacy guarantee. This was abnormal a year ago and is becoming normal; frame as the paper's motivating observation, not a proven law.
- **The artifact in one paragraph.** PNT is a goal-anchored, machine-checkable blueprint for a *class* of apps that is read by agents to *build* conformant instances and to *evaluate* arbitrary candidates — one artifact, two directions.
- **Stance.** This is an experience/case-study paper. The recombination-is-unoccupied claim is strong and survey-backed; the "new field" framing is a wager.

**Citations**
- Piskala, *Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants*, arXiv 2602.00180 (Jan 2026). https://arxiv.org/abs/2602.00180
- GitHub Spec Kit. https://github.com/github/spec-kit · design doc: https://github.com/github/spec-kit/blob/main/spec-driven.md
- (Internal, for contrast) PNT `CLAUDE.md` lint-discipline section; `docs/PriorArt.md` working definition.

---

### 2. Background: the personal network toolkit as a concrete object

**Purpose:** give the reader enough of the actual artifact that the rest of the paper is grounded; keep it descriptive.

**Key claims**
- **The application class.** A PNA is local-first, private-by-default, mirrors SaaS-held contact data into a user-owned store, operates on relationship data with no remote authority, and runs on the user's device (never SaaS). (Summarize from `spec/PNA_Spec.md`; do not restate the normative goals verbatim — link.)
- **The layered object.** The spec is layered: **Goals** (human-readable outcomes) → **Constraints** (the human-readable layer that motivates the architectural layer) → **Architectural Commitments (ACs)** (stable-ID'd, RFC-2119, the unit of identity) → **typed contracts** (JSON Schema / OpenAPI / SQL DDL / TypeScript) that *realize* named ACs. Under ACs sit platform-ceiling constraints (`CST-*`) and user-relaxable **Exceptions** (`EX-*`).
- **Variability.** A PNA *varies* along **axes** (e.g. distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure); each **pick** (flavor) triggers flavor-derived ACs. Use "variable language" about axis counts (the set may evolve) — this itself is a feature-modeling instinct.
- **Reference designs.** Working, deployed PNAs that demonstrate one valid combination of picks: `fellows_local_db` (Directory Archive) and `prm` (Personal Relationship Manager). Each is archived (Software Heritage SWHID) and carries an AC attestation table.
- **Four flows, one skill.** **Build**, **evaluate**, **contribute** — the generative + evaluative + feedback loop — plus an advisory fourth, **harden** (secure the *operating environment* a PNA runs in; adds no AC, awards no pass/fail), are packaged as an Anthropic **Agent Skill** (`pna-toolkit/SKILL.md`) that an agent auto-discovers.
- **The toolkit is versioned as a unit** (VERSION `0.1.0-draft`); every artifact carries a `Toolkit-Version:` stamp.

**Citations**
- Internal: `spec/PNA_Spec.md`, `spec/axes.md`, `pna-toolkit/SKILL.md`, `contracts/`, the two reference-design repos (richbodo/fellows_local_db, richbodo/prm).
- Anthropic Agent Skills (for the packaging): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview · engineering post "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills · open-standard hub: https://agentskills.io
- Software Heritage (durable archival of reference designs): https://www.softwareheritage.org

---

### 3. The four bounding traditions (related work as a map)

**Purpose:** the related-work section, but framed as the four sides of a bounded region rather than a flat list. Each subsection ends with **"what PNT inherits"** and **"what PNT changes."**

#### 3.1 Software Product Lines, FODA/FORM, feature models, Generative Programming

**Key claims**
- **FODA introduced feature models** to domain engineering: capture the common and variable features of a *family* of systems and the relationships among them. PNT's axes/picks are exactly a feature model — a set of variation points with legal configurations.
- **FORM** splits the lifecycle into **domain engineering** (build the reusable assets/architecture for the family) and **application engineering** (instantiate a concrete product from those assets). **This is PNT's build-the-spec vs build-an-instance split**, made explicit.
- **Orthogonal Variability Model (OVM)** (Pohl/Böckle/van der Linden): model variability as a *separate, cross-cutting* artifact linked to the base assets — the closest formal cousin to PNT's "axes are a layer of their own, referenced by ACs and contracts." Adopt OVM language in the paper.
- **Generative Programming** (Czarnecki & Eisenecker): a *generative domain model* + a configuration step yields a concrete product *on demand*. PNT is recognizably the same two-stage cycle.
- **Tractable analysis.** Feature models support automated analysis (consistency, dead features, valid configurations) via SAT/CSP/BDD solvers — an opportunity PNT has not yet exploited and could (a lint that checks axis-pick combinations are satisfiable). Cite as future work, honestly labeled as not-yet-done.
- **What PNT inherits:** variability-as-first-class; the domain/application split; configuration-yields-product.
- **What PNT changes:** the "application engineer" / generator is an **AI agent reading the spec**, not a code generator or a human picking from a configurator; the generated artifact is *human-customized and human-verified*, not auto-emitted.

**Citations**
- Kang, Cohen, Hess, Novak, Peterson, *Feature-Oriented Domain Analysis (FODA) Feasibility Study*, CMU/SEI-90-TR-021 (1990). https://www.researchgate.net/publication/215588323_Feature-Oriented_Domain_Analysis_FODA_feasibility_study · overview: https://en.wikipedia.org/wiki/Feature-oriented_domain_analysis
- Kang, Kim, Lee, Kim, Shin, Huh, *FORM: A Feature-Oriented Reuse Method with Domain-Specific Reference Architectures*, Annals of Software Engineering 5 (1998) 143–168. https://link.springer.com/article/10.1023/A:1018980625587
- Pohl, Böckle, van der Linden, *Software Product Line Engineering: Foundations, Principles, and Techniques* (Springer, 2005) — OVM. https://link.springer.com/book/10.1007/3-540-28901-1 · OVM-in-practice: https://link.springer.com/article/10.1007/s11219-011-9156-5
- Czarnecki & Eisenecker, *Generative Programming: Methods, Tools, and Applications* (Addison-Wesley, 2000). https://dl.acm.org/doi/10.5555/345203
- Benavides, Segura, Ruiz-Cortés, *Automated Analysis of Feature Models 20 Years Later: A Literature Review*, Information Systems 35(6) (2010) 615–636 — SAT/CSP/BDD analysis. https://www.sciencedirect.com/science/article/abs/pii/S0306437910000025 · (SAT scalability) https://arxiv.org/pdf/1506.05198

#### 3.2 Common Criteria Protection-Profile *authoring* methodology

**Key claims**
- A **Protection Profile (PP)** specifies security requirements for a *category* of products; a per-product **Security Target (ST)** declares "I implement this PP, here is how"; the **Common Evaluation Methodology (CEM)** defines how an evaluator checks it. **This is the only widely standardized "blueprint-for-blueprints" with a paired evaluation methodology** — structurally the deepest precedent for PNT's *spec + per-instance attestation + defined evaluation procedure*.
- The modern **collaborative PP (cPP)** + **international Technical Community (iTC)** + **exact conformance** machinery is even closer to PNT's intent: a community authors the class spec; an ST must contain exactly the mandatory requirements (plus declared optional/selection-based ones) — a strikingly "axis-pick"-like discipline (mandatory ACs + flavor-triggered ACs).
- **The trajectory toward agent-relevant profiles** is worth noting (CC/iTC communities are actively producing PPs/cPPs for new component categories, and AI-agent security is an active 2026 standards topic) — but state this as *direction of travel*, **not** as a confirmed named "agent Protection Profile," to stay evidence-safe.
- **What PNT inherits:** class-scoped requirements; per-instance attestation against the class; a *named, repeatable* evaluation procedure (PNT's evaluate flow is its CEM analogue).
- **What PNT changes:** PNT **drops the certification authority**. CC ends in an accredited lab *awarding* a credential (EAL/assurance). PNT's conformance is *checked* by whoever runs the skill (an LLM + lints + a human reviewer) and is never *awarded* — no body, no badge. PNT also generalizes from "security requirements" to *goal-anchored architectural* requirements, and is generative (CC PPs are purely evaluative).

**Citations**
- Common Criteria / ISO-IEC 15408; Protection Profiles & Security Targets. https://www.commoncriteriaportal.org · overview: https://en.wikipedia.org/wiki/Common_Criteria
- collaborative PP for Network Devices (worked example of cPP + iTC + exact conformance + CEM reference). https://www.commoncriteriaportal.org/files/ppfiles/CPP_ND_V2.1.pdf
- (Direction-of-travel, for the agent angle — cite as context, not as a named PP) AI-agent security as a 2026 standards topic: https://www.helpnetsecurity.com/2026/06/03/research-ai-agent-security-capability/

#### 3.3 W3C specification + test-suite methodology

**Key claims**
- W3C's process makes implementation evidence a *gate*: to advance, a spec must show **independent interoperable implementations of each feature** (commonly "two interoperable implementations"), demonstrated via a **test suite + machine-readable implementation reports**. The governing idea: *a spec is only real when independent implementations demonstrate it.*
- **PNT's rule "reference designs demonstrate changes"** (a spec change is accepted only with a working design that exercises it — `CONTRIBUTING.md`) is this discipline transplanted. The reference designs are PNT's "interoperable implementations"; the AC attestation tables + evaluate-report artifact are its "implementation reports."
- **What PNT inherits:** no-feature-without-a-demonstrator; reports as machine-readable evidence (PNT even reuses W3C **EARL**'s pass/fail/cannot-tell vocabulary shape in its `unable-to-determine` status).
- **What PNT changes:** W3C demonstrates *one technology's* features; PNT demonstrates *a multi-flavor class*, so "two interoperable implementations of feature X" becomes "a reference design that exercises feature X **at the flavor that triggers it**." Demonstrators therefore tile a *configuration space*, not a single feature list.

**Citations**
- W3C Process — implementation experience / Candidate Recommendation exit criteria (two interoperable implementations per feature). https://www.w3.org/2023/Process-20230612/ · test-development FAQ: https://www.w3.org/QA/WG/2005/01/test-faq · "specification food chain": https://www.w3.org/blog/2006/specification-101/
- W3C testing how-to: https://github.com/w3c/testing-how-to · implementation reports model: https://www.w3.org/wiki/ImplementationReport
- W3C EARL (Evaluation and Report Language) — pass/fail/cannot-tell vocabulary. https://www.w3.org/TR/EARL10-Schema/
- (Domain-adjacent evaluative precedent) Solid Conformance Test Harness. https://github.com/solid-contrib/conformance-test-harness

#### 3.4 AI-era spec-driven development (Spec Kit, Kiro, OpenSpec, the SDD survey)

**Key claims**
- **Spec Kit** introduced a four-phase agent workflow (specify → plan → task → implement) plus a **`constitution.md`** of immutable principles, and an **`/analyze` cross-artifact consistency check** — structurally the closest analogue to PNT's universal ACs (constitution ≈ ACs) and PNT's lints (`/analyze` ≈ `tools/lint-spec-ids.py`).
- **Kiro** formalizes requirements (EARS-notation acceptance criteria) → design → tasks, with a **steering** layer (AGENTS.md-style guidelines) — "specs become the anchor" against context drift.
- **OpenSpec** is a vendor-neutral propose→apply→archive delta loop kept alongside specs.
- The **SDD survey** is the canonical academic framing: distinguish specs that *execute as validation gates* from specs that are merely read.
- **What these miss (the gap PNT fills):** all are **per-project / single-app**. The spec is written for *one* application by *one* team. None defines a *class* with multiple legitimate flavors, and none has a flow for **evaluating an arbitrary third-party candidate** against the spec (they govern *how an agent builds your* app, not *whether someone else's* app conforms).
- **What PNT inherits:** spec-as-contract-for-agents; a constitution/priority-ordered policy layer; cross-artifact consistency checks; the skill/slash-command packaging.
- **What PNT changes:** lifts the spec from *project* to *application class*; adds *multi-flavor variability* (the SPL half); adds the *evaluate-arbitrary-candidate* direction (the CC/W3C half).

**Citations**
- GitHub Spec Kit. https://github.com/github/spec-kit · spec-driven.md: https://github.com/github/spec-kit/blob/main/spec-driven.md
- AWS Kiro — spec-driven (requirements/design/tasks + steering, EARS). https://kiro.dev/ · guide: https://builder.aws.com/content/39juiKF2uwxhek0RuYHhjf24JjL/kiro-the-complete-guide-for-teams
- OpenSpec (Fission-AI). https://github.com/Fission-AI/OpenSpec
- Piskala, SDD survey, arXiv 2602.00180. https://arxiv.org/abs/2602.00180
- (EARS grammar, used by Kiro and a candidate for PNT's readable goals) Mavin et al., *Easy Approach to Requirements Syntax*, RE'09. https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax

---

### 4. The white space and the bidirectional-spec contribution

**Purpose:** the heart of the paper — name the unoccupied region and the single cleanest claim.

**Key claims**
- **The map result.** Plot the four traditions on two axes that matter for this artifact: *scope* (single-app → application-class) and *direction* (generative ↔ evaluative), with a third dimension for *builder* (human/codegen → AI agent). The corner **{class-scoped, generative + evaluative, AI-built, multi-flavor, checked-not-awarded}** is occupied by none of them. (This corroborates, from the *method* side, Paper 1's finding from the *application-class* side that the PNA node is the only one drawing on all four behavioral families — including Family IV, "machine-followable spec & verification," with its checked-vs-certified conformance sub-axis.)
- **The cleanest novel claim — the bidirectional spec.** *One* goal-anchored, machine-checkable artifact serves **both** directions:
  - **Generative:** an agent reads goals → constraints → ACs → typed contracts (for the chosen flavor) and builds a conformant instance, adapting from the nearest reference design.
  - **Evaluative:** an agent reads the *same* artifact and audits an arbitrary candidate AC-by-AC, emitting a typed, diffable report.
  The two directions are not two specs kept in sync; they are *one* spec consumed two ways. This is the contribution most clearly absent from all four traditions (SPL/GP are generative-only; CC/W3C-tests are evaluative-only; SDD is generative + per-project).
- **Each prior tradition has half of it.** SPL/GP: generative + class-scoped, but not evaluative-of-arbitrary-candidates and not AI-built. CC-PP: class-scoped + evaluative + has an evaluation methodology, but not generative and *awards* a credential. W3C: demonstrator-gated + evaluative, but single-technology. SDD: AI-built + generative + consistency-checked, but per-project, single-flavor, no evaluate-arbitrary flow. PNT is the recombination.
- **Why the recombination is more than the sum.** The same goal-anchored layering that lets an agent *build* (because the contracts are typed and the ACs are stable-ID'd) is exactly what lets an agent *evaluate* (cite the AC, trace the contract, attach evidence). Bidirectionality falls out of the layering; it is not a second mechanism bolted on.

**Citations**
- Internal: `pna-toolkit/SKILL.md` (the two flows over one artifact); `tools/evaluate-report.schema.json` (typed, diffable evaluate output); `docs/PriorArt.md` (the four-property "generative + class-scoped + multi-flavor + machine-checkable" working definition and its proximity matrix).
- Cross-reference Paper 1 (the directed-graph positioning; Family IV conformance-model sub-axis) — shared asset.
- Re-cite the four anchors from §3 as the four corners.

---

### 5. Method in detail: how PNT generates *and* evaluates from one artifact

**Purpose:** the reproducible mechanics — what an implementer would copy.

**Key claims**
- **The object model (defer details to Appendix B).** Goals (outcome-altitude, human-readable) → Constraints (readable motivation layer) → ACs (RFC-2119, stable IDs, *the unit of identity*) → typed contracts that carry a `Realizes: AC-X` header → axes/picks (the variability/feature-model layer) → `CST-*` ceilings and `EX-*` relaxations beneath specific ACs.
- **The generate flow.** Read spec end-to-end → choose axis picks with the user → enumerate inherited constraints and plan their handling at the *data layer* → author an Architecture document → pull the typed contracts for the picks → adapt the nearest reference design → build → fill the AC attestation table (each AC: realization + the test/rubric/review that verifies it, with *negative invariants pinned by negative tests*) → self-run the evaluate flow.
- **The evaluate flow.** For each applicable AC (universal + flavor-derived) decide `conformant` / `non-conformant` / `not-applicable` / `unable-to-determine`, citing code; audit attestation evidence (a cited test must *exist and pass*; a doc pointer is not evidence; an `xfail` row is a finding); detect undeclared Exceptions and over-claimed Constraints; emit a typed `evaluate-report.json` and render prose as a *view* over it.
- **The three-layer conformance check (the engine of "checked, not awarded").**
  1. **Deterministic** — stdlib lints in `tools/` (e.g. `lint-spec-ids.py` for AC↔contract traceability; `egress-lint.py` for off-device egress) run in CI.
  2. **LLM-as-judge** — the agent performs the architectural-conformance reasoning the lints can't, emitting evidence tagged `source: llm`.
  3. **Human** — PR review is the deliberately-non-automated judgment gate.
  Investment is ~80/20 toward description-and-process over a bespoke test runner.
- **Honest deferrals as a method rule.** A guarantee the code doesn't yet deliver must be an explicit in-artifact status (a strict-`xfail` with a tracking issue, a `partial`/`Open` attestation, a CHANGELOG "deferred" note) — never a bare comment that *claims* the property. "Convert an absent guarantee into a red test (or a lint failure), never a silent pass" is the method's spine and is independently echoed by the SDD field.
- **Packaging.** All four flows (the three conformance flows + the advisory **harden** flow) ship as one Anthropic Agent Skill; progressive disclosure (name+description always loaded; body on demand) is what makes a class blueprint *discoverable by an agent without context cost*.

**Citations**
- Internal: `pna-toolkit/SKILL.md`; `tools/lint-spec-ids.py`, `tools/egress-lint.py`, `tools/attestation-evidence-lint.py`, `tools/evaluate-report.schema.json`; `CONTRIBUTING.md`; `CLAUDE.md` (lint discipline + honest deferrals).
- LLM-as-judge (the evaluative layer's grounding, incl. its known biases to disclose as a limitation): Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023 Datasets & Benchmarks. https://arxiv.org/abs/2306.05685
- Agent Skills progressive disclosure. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

---

### 6. "Checked, not awarded": the conformance model and why it diverges from certification

**Purpose:** isolate the one place PNT deliberately departs from its closest structural ancestor (CC), because that departure is itself a contribution.

**Key claims**
- **The conformance sub-axis** (from the R2-C/R2-D synthesis): conformance models split into **checked/validated** (anyone can run the published, machine-checkable criteria — W3C QA, OWASP ASVS/MASVS, ISO-27560) vs **certified/awarded** (an accredited body grants a credential — Common Criteria, FedRAMP). PNT sits firmly on the **checked** pole and *rejects* the certified pole.
- **Why reject certification here.** The toolkit's users are community/"barefoot" developers and end users; a certifying body is the wrong cost structure and the wrong trust model. A user trusts an app because they (or an LLM running the skill) *checked* it against the spec, not because it carries a badge. This also keeps the artifact honest: no authority to over-claim on your behalf.
- **Graded strength without a single collapsed level.** PNT borrows CC/ASVS/SLSA's *grade-the-strength* idea but **rejects one collapsed level**, using per-dimension strength classes (so "the boundary is enforced" and "the provider's data handling is unverifiable" cannot be hidden behind one number) — directly relevant to a class blueprint where flavors differ in how strongly they can keep a guarantee.
- **The honest-deviation primitive (Exceptions).** Framing a *deliberate* departure from a guarantee as a first-class, stable-ID'd, caught-and-handled **Exception** with a per-dimension strength profile appears to have no prior-art description language; PNT borrows the *mechanics* (graded assurance, attenuated-consent propagation à la macaroons, cannot-tell reporting) but the exception-as-class-concept is novel. Note this is *adjacent* to the paper's main claim, included because it is what "checked, not awarded" looks like when an instance must legitimately bend a rule.

**Citations**
- Common Criteria EAL / assurance (the awarded pole). https://www.commoncriteriaportal.org
- OWASP ASVS (levels; checked-pole graded assurance). https://owasp.org/www-project-application-security-verification-standard/
- SLSA (graded build-integrity attestation). https://slsa.dev/
- W3C EARL (cannot-tell reporting). https://www.w3.org/TR/EARL10-Schema/
- Macaroons (attenuating delegated consent — EX-H7 analogue): Birgisson et al., Google, 2014. https://research.google/pubs/pub41892/
- Internal: `spec/exceptions.md`, `docs/PriorArt.md` §9.

---

### 7. Lessons learned (the experience-report core)

**Purpose:** what makes this a *case study* and not a position paper — the things only building it taught.

**Key claims (each a lesson, stated as a transferable finding)**
- **Bidirectionality is nearly free *if* the spec is built layered and ID'd from day one** — the same stable-ID'd ACs + typed contracts power both build and evaluate; retrofitting evaluability onto a prose spec would not work.
- **A lint with no fault-injection self-test silently rots.** PNT's rule "every check needs a fault-injection case in the same change" came from a dead check that stayed green while enforcing nothing. Generalizable to anyone who claims machine-checkable conformance: the *checker* needs a checker.
- **Evidence discipline is the hard part, not the spec text.** The recurring failure mode is a `conformant` row whose "evidence" is a doc pointer, a happy-path-only test, or an `xfail` — i.e., *over-claiming a guarantee*. The deterministic/LLM/human layering exists precisely because no single layer catches all of these; naming the seam (what each layer can and cannot prove) was a real lesson.
- **Goals were initially mis-stated as mechanisms.** "Store two databases" is a *mechanism*; the goal is *usable, human-understandable protection*. Re-pitching at outcome altitude — and adding a human-readable Constraints view — was necessary for the *generative* direction (an agent and a non-developer both need the "why"). Transferable: a class blueprint needs a human-readable goal layer *above* the machine layer, not just contracts.
- **"Goals must divide the labor."** If goals are vague, every constraint cross-cuts and the goals do no partitioning work; testing the AC→goal assignment empirically (does each AC single-home?) is a usable design check for any class spec.
- **Demonstrators tile a configuration space.** Two reference designs at very different flavors (browser/OPFS vs native-SQLite; single-source vs multi-source-dedup) surfaced different ACs; one demonstrator is not enough for a multi-flavor class. (This is also why the *generality* claim needs a second *class*, not just a second instance.)
- **AI-built doesn't mean AI-alone.** The toolkit augments human–AI teams; it does not auto-build apps. The human-verify + human-review gates are load-bearing, not vestigial.

**Citations**
- Internal: `CLAUDE.md` (lint discipline, honest deferrals, docs-currency rule), `docs/PriorArt.md` design-notes log (the xfail-as-evidence finding; the goals-readability pass; the at-rest scope decision), the two reference designs' attestation histories.

---

### 8. Limitations, threats to the claim, and what would falsify it

**Purpose:** evidence-safe honesty; pre-empt the reviewer.

**Key claims**
- **N=1 application class.** The method is demonstrated on *one* class (PNAs) with *two* reference designs. Generality of the *method* is therefore a **wager**, not a result — explicitly stated.
- **"Unoccupied region" is a not-found, not a proof of nonexistence.** The survey is broad (four mature traditions web-verified) but absence of evidence is not proof; an adjacent artifact may exist under different vocabulary. State the search method so others can refute it.
- **LLM-as-judge is fallible.** The evaluative layer inherits known biases (position, verbosity, self-enhancement) and limited reasoning; this is why deterministic lints and human review bracket it. Cite Zheng et al. and frame the layering as the mitigation.
- **No automated variability analysis yet.** PNT does not (yet) run SAT/CSP analysis over its feature model to prove axis-pick combinations are satisfiable / free of dead picks; a hand-maintained lint is weaker than the SPL state of the art. Honest gap.
- **Conformance "checked not awarded" trades authority for accessibility.** Without a certifying body, two evaluators could disagree; reproducibility rests on the deterministic layer + the typed diffable report, not on an accredited verdict. State the trade-off plainly.
- **What would falsify the central claim:** (a) discovery of a published artifact that is class-scoped, generative + evaluative, multi-flavor, and AI-built; (b) a second class that the method *cannot* express (would bound generality); (c) evidence that the bidirectional spec is in practice two specs in disguise (drift between the build and evaluate readings).

**Citations**
- Zheng et al., LLM-as-judge biases. https://arxiv.org/abs/2306.05685
- Benavides et al. (the analysis capability PNT lacks). https://www.sciencedirect.com/science/article/abs/pii/S0306437910000025

---

### 9. Generalization & recommendation: when a meta-repo is warranted

**Purpose:** the actionable recommendation, sequenced.

**Key claims**
- **The genuinely-lacking upstream artifact** is a **meta-repo / authoring guide for AI-era application-class blueprints** — a "Protection-Profile-authoring methodology" for the AI era: how to write goals at outcome altitude, model axes as a feature model, derive ACs, type the contracts, wire the three-layer check, and package as a skill. The R4 finding is that *no such artifact exists*.
- **But it is premature.** A meta-repo generalizes a *method*; you cannot responsibly generalize from one class. **Recommendation: publish the case study now; spin out the meta-repo only after a second application class is specified with the same method and validates its generality.** This matches the project's evidence-safe stance (bold claims as wagers, earned by a second worked example).
- **Adopt established vocabulary in the generalization.** When the meta-repo comes, speak SPL/Generative-Programming/OVM (domain vs application engineering, variation points, feature model) so the work is legible to the SPL community rather than re-coining terms — this paper already does the translation (Appendix C).
- **Candidate second classes** (name a few to make the "second example" concrete and to show the method isn't PNA-specific): e.g. a *comms-tool* class ("can it guarantee E2E?"), a *personal-data-vault* class, or another local-first sovereign-data class — without committing.

**Citations**
- Internal: `brainstorms/2026-06-14-pnt-direction-grill.md` R4 recommendation; `CONTRIBUTING.md` (the demonstrator-gated discipline that the meta-repo would generalize).
- The four anchors (SPL/CC/W3C/SDD) as the traditions the meta-repo would synthesize.

---

### 10. Conclusion

**Key claims**
- Restate the shift (spec as the unit of software in an AI-regeneration world) and the artifact (one bidirectional, goal-anchored, machine-checkable class blueprint, AI-built, checked-not-awarded, shipped as a skill).
- Restate the map result (white space bounded by SPL/GP, CC-PP, W3C-tests, SDD) and the cleanest claim (the bidirectional spec).
- Restate the recommendation and the wager: a case study now; a meta-repo when a second class proves the method generalizes. Invite the second example.

---

## Appendix A — Tradition-by-tradition comparison table (the load-bearing figure)

Columns: **Tradition · Scope (single-app vs class) · Direction (generative / evaluative / both) · Variability (multi-flavor?) · Builder (human / codegen / AI agent) · Conformance model (checked vs awarded) · Has paired evaluation method?**

Rows (fill from §3 + `docs/PriorArt.md` proximity matrix):
- SPL / FODA / FORM / Generative Programming — class · generative · multi-flavor ✓ · codegen/human · n/a (build-time) · n/a
- Common Criteria PP / cPP — class · evaluative · "flavors" via optional/selection SFRs · human · **awarded** · ✓ (CEM)
- W3C spec + test suite — single technology · evaluative (demonstrator-gated) · partial · human · **checked** · ✓ (test suite + impl reports)
- SDD (Spec Kit / Kiro / OpenSpec) — **single project** · generative · ✗ · **AI agent** · checked (consistency) · partial (`/analyze`)
- **PNT** — **class** · **both** · **multi-flavor ✓** · **AI agent** · **checked** · ✓ (the evaluate flow)

(This is the figure that visually shows the unoccupied corner. Mirror/extend `docs/PriorArt.md`'s existing proximity matrix.)

## Appendix B — The bidirectional-spec object model

Diagram + prose: Goals → Constraints (readable) → ACs (RFC-2119, stable IDs, `Realizes`-linked) → typed contracts; the axes/flavors variability layer cross-cutting the ACs; `CST-*`/`EX-*` beneath specific ACs; the three verification layers (lint / LLM / human) shown bracketing the evaluate flow; the Agent-Skill wrapper with progressive disclosure. Show the *single* artifact feeding *two* arrows (build →, ← evaluate).

## Appendix C — PNT ↔ SPL vocabulary map

| PNT term | SPL / GP / OVM term |
|---|---|
| build-the-spec vs build-an-instance | domain engineering vs application engineering (FORM) |
| axes + picks (flavors) | feature model / variation points + variants (FODA); orthogonal variability model (Pohl et al.) |
| flavor-derived ACs | feature-dependent / selection-based requirements |
| the AI agent that builds an instance | application engineer / product instantiation (here: generator = LLM) |
| reference design | concrete product / family member (also W3C "interoperable implementation") |
| typed contract (`Realizes: AC-X`) | reusable core asset bound to a feature |
| evaluate flow | (CC) CEM evaluation procedure / (W3C) test-suite run |
| checked-not-awarded | validated conformance (W3C QA / OWASP ASVS) vs certified (CC EAL / FedRAMP) |

---

## Consolidated citations (web-verified June 2026)

**Software Product Lines / feature models / generative programming**
- FODA (Kang et al., CMU/SEI-90-TR-021, 1990): https://en.wikipedia.org/wiki/Feature-oriented_domain_analysis · https://www.researchgate.net/publication/215588323_Feature-Oriented_Domain_Analysis_FODA_feasibility_study
- FORM (Kang et al., Annals of SE 5, 1998): https://link.springer.com/article/10.1023/A:1018980625587
- OVM / SPL textbook (Pohl, Böckle, van der Linden, 2005): https://link.springer.com/book/10.1007/3-540-28901-1
- Generative Programming (Czarnecki & Eisenecker, 2000): https://dl.acm.org/doi/10.5555/345203
- Automated analysis of feature models (Benavides, Segura, Ruiz-Cortés, 2010): https://www.sciencedirect.com/science/article/abs/pii/S0306437910000025 · SAT scalability: https://arxiv.org/pdf/1506.05198

**Common Criteria Protection Profiles**
- CC portal / PP & ST: https://www.commoncriteriaportal.org · https://en.wikipedia.org/wiki/Common_Criteria
- cPP + iTC + exact conformance + CEM (Network Devices cPP example): https://www.commoncriteriaportal.org/files/ppfiles/CPP_ND_V2.1.pdf
- AI-agent security as a 2026 standards context (direction-of-travel only): https://www.helpnetsecurity.com/2026/06/03/research-ai-agent-security-capability/

**W3C spec + test methodology**
- W3C Process (impl experience / two interoperable implementations): https://www.w3.org/2023/Process-20230612/
- Test-development FAQ: https://www.w3.org/QA/WG/2005/01/test-faq · testing how-to: https://github.com/w3c/testing-how-to · impl reports: https://www.w3.org/wiki/ImplementationReport
- EARL: https://www.w3.org/TR/EARL10-Schema/
- Solid CTH (domain-adjacent evaluative harness): https://github.com/solid-contrib/conformance-test-harness

**AI-era spec-driven development**
- Spec Kit: https://github.com/github/spec-kit · spec-driven.md: https://github.com/github/spec-kit/blob/main/spec-driven.md
- AWS Kiro: https://kiro.dev/ · guide: https://builder.aws.com/content/39juiKF2uwxhek0RuYHhjf24JjL/kiro-the-complete-guide-for-teams
- OpenSpec: https://github.com/Fission-AI/OpenSpec
- SDD survey (Piskala, arXiv 2602.00180): https://arxiv.org/abs/2602.00180
- EARS (Mavin et al.): https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax

**Anthropic Agent Skills**
- Overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Engineering post: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Open standard: https://agentskills.io

**LLM-as-judge**
- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023: https://arxiv.org/abs/2306.05685

**Graded assurance / consent (for the "checked-not-awarded" section)**
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/ · SLSA: https://slsa.dev/ · Macaroons (Birgisson et al., 2014): https://research.google/pubs/pub41892/

---

## Venue notes
- **SPLC (Software Product Line Conference)** — best fit for the variability/feature-model framing and the "LLM as application engineer" recombination; audience already owns the SPL half.
- **Onward! (SPLASH)** — fit for the experience/essay register and the "why now / new unit of software" argument; where the local-first essay tradition is welcome.
- **MODELS** — variability + model-driven engineering; good for Appendix B/C (the object model + vocabulary map).
- **arXiv preprint** — timestamp the white-space claim and reach the SDD/agent community quickly.
- **Local-first community whitepaper** — practitioner audience (the "barefoot developer"); pairs with Paper 1.

## Open authoring decisions (for the expander)
- One paper or two: keep Paper 1 (class placement) and Paper 2 (method) separate, sharing the directed graph, or merge. Default: two.
- How hard to push the "new field" wager in the title/abstract vs body. Recommendation: wager stays in the body; title/abstract claim only the *recombination* and the *bidirectional spec*.
- Whether to include the Exceptions/strength-profile material (§6) in full or cite Paper 1 / a separate note — it is adjacent to the core claim.
- Whether to add a small worked walkthrough (one AC, shown both generated and evaluated) as a figure — strongly recommended for the case-study register.
