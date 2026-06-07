# Plan: PNA Toolkit Reorganization

## Status (2026-05-25)

Phases 1–4 landed on branch `reorg-phases-1-4` (in a PR pending review). Phase 4.5 (User's Guide + skill preflight enhancement) is the next-up work and lands in the same PR; it is intentionally pre-Phase-5 so the User's Guide can be exercised against `fellows_local_db` as the first reference-design submission in Phase 5.

Subsequent phases (5: Archival tooling and first design record; 6: Validation tooling; 7: Dogfood with a second contribution) remain as written below.

## What this plan supersedes

This plan is the unified successor to:

- `plans/community-contribution-model.md` (the most current planning prior to this; carried forward in substance and structure)
- `plans/pna-rfc-conversion-plan.md` (spec-formalization ideas folded in; the hello-world and Tolaria-composition phases dropped as superseded by the contribution-driven model below)
- Issue #4 "Pass for conventional terminology and form" (folded in; closed when this plan landed)

The memorize-plugin plan was removed separately; it belongs in a downstream reference design's repository, not in the toolkit.

## Background

The PNA Toolkit currently bundles spec documents and refers to one reference design (`fellows_local_db`) in a single project. Two parallel pressures motivate reorganization:

1. **Contribution model.** As the toolkit matures, external contributors should be able to submit reference designs derived from their own production applications, with spec changes evolving in response to what production reality reveals.

2. **Spec formalization.** The toolkit is a *generative + evaluative* application-class blueprint: AI agents read it to build conformant PNAs, and (increasingly) AI agents read it to evaluate whether a candidate application is safe to use as a PNA. Both modes benefit from sharper formalization than plain markdown prose — RFC-style normative language and stable IDs across spec, contracts, and reference-design attestations.

This plan combines both threads. The contribution-model substance survives largely intact; the spec-formalization layer is added on top.

## Working hypotheses

**Hypothesis 1 — Reference designs derived from production applications are more valuable than purpose-built lab designs.** Reality surfaces architectural constraints that first-principles reasoning cannot. The PWA-doesn't-work-for-most-PNAs insight that came from `fellows_local_db`'s real user feedback is the canonical example: that constraint would not have been discovered by writing a lab demo. The toolkit's contribution model privileges snapshots of running production apps.

**Hypothesis 2 — Conformance evaluation is a first-class deliverable.** The most likely retail use of the toolkit's evaluative side is a user pointing an LLM at someone else's PNA source and asking: *"before I use this application, make sure it conforms to PNA specs and is safe for me to use."* The user trusts the spec; they want to know whether a specific candidate app honors it. Builders use the same evaluator on their own in-progress code to find gaps. The toolkit needs to support evaluation explicitly, not just generation.

**Hypothesis 3 — Evaluation is described in the toolkit, not implemented by the toolkit.** The toolkit ships descriptions of what conformance checking looks like; an LLM consuming those descriptions performs the actual evaluation. Deterministic tooling stays small (file presence, license check, schema validity); LLMs handle the architectural-conformance layer; humans review contributed designs. This is the layering principle below.

## Principle: layering of verification

Verification of PNA conformance happens at three layers, each owned by a different kind of agent:

- **Deterministic layer** — file presence, license check, schema validity, contract-shape lints. Owned by small scripts in `tools/`.
- **Architectural-conformance layer** — does the application's behavior and structure honor the spec? "Does this app send Private DB rows to a cloud service?" "Does the auth gate let stale sessions fall through to cached data?" Prose questions about behavior, well within reach for an LLM reading source.
- **Judgment-and-review layer** — does the design's Architecture document accurately describe the design? Does the design genuinely contribute what it claims? Owned by humans reviewing contribution PRs.

The toolkit writes deterministic tooling for the first layer (bounded), describes evaluator behavior for the second (no Python eval harness; the description is the deliverable), and writes contribution-review guidance for the third. Investment ratio is roughly 80/20 toward description-and-process.

The *specifics* of which test verifies which AC live per-design, in each Architecture document. The spec declares ACs and their normative content; each Architecture document declares how its design verifies each AC. This keeps the spec light (no brittle per-AC tags that go stale as LLM capabilities evolve) and pushes per-implementation flexibility to where it belongs.

## Goals

1. The toolkit becomes a thin canonical repository: spec, typed contracts, reference-design records, skill packaging, tooling. No bundled application code.

2. Reference designs live in their authors' own repos, under their own release cadence. The toolkit references them by permanent identifier (v0.1: Software Heritage SWHIDs; the spec itself declares this commitment).

3. Spec changes must be accompanied by a reference design that demonstrates the change in working code.

4. Each accepted design ships an Architecture document declaring conformance to a specific Toolkit-Version, declaring per-axis picks and their versions, attesting per-AC conformance, and **mapping each applicable AC to the specific test(s) or review mechanism(s) that verify it in the design**. Test coverage of the AC list is an acceptance criterion.

5. Archival is robust to upstream repo deletion. The toolkit does not undertake routine maintenance of contributed code.

6. The toolkit skill is the canonical way for AI agents to consume the toolkit — when building a new PNA, when evaluating whether an existing application conforms, and when authoring a contribution PR back to the toolkit. The skill points into `spec/`, `contracts/`, and `reference_designs/`; it is not a separate copy that drifts.

7. The spec keeps its readable prose. Conformance-bearing statements use unambiguous language (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY); informative prose stays as it is. Every conformance-bearing requirement is testable in principle, by an LLM if not by a script.

8. Every architectural commitment carries a stable ID, used as the join key between spec prose, typed contracts, and per-design Architecture documents. Bidirectional traceability holds at the AC level.

9. Conformance evaluation is a first-class deliverable. The spec and the skill together describe how an LLM evaluates a candidate PNA; the toolkit does not implement the evaluator as code.

10. Claude Code (or any equivalent LLM agent) can use the skill to author a contribution PR back to the toolkit end-to-end. When a builder finds a spec ambiguity or gap, the skill walks the agent through producing a well-formed PR — spec diff, design record, Architecture document, SWHID-archival request — without maintainer hand-holding.

## Non-goals

1. The toolkit does not host runnable application code. Designs run from their own repos.

2. The toolkit does not certify implementations against marketing claims. Acceptance signals "this design contributed something to the spec," not "this is a recommended production app." There is no certifying body. *Conformance is something you check, not something you are awarded.*

3. The toolkit does not run a registry service or website beyond the GitHub repo itself.

4. The toolkit does not ship a Python conformance test runner beyond the trivially mechanical lints. The architectural-conformance layer is described, not implemented.

5. The toolkit does not hand-maintain a parallel YAML/JSON spec. Prose remains canonical. Lightweight derived indexes may be generated on demand if needed.

6. The toolkit does not adopt Common Criteria terminology wholesale. The Protection Profile / Security Target *model* is the conceptual ancestor; the toolkit keeps its own vocabulary ("PNA Spec," "Architecture document").

## Key design decisions (resolved)

These are settled here so subsequent work doesn't relitigate.

**No first-party in-repo designs.** All reference designs — including those Rich maintains personally, such as `fellows_local_db` — are external. The toolkit references snapshots, never bundles code.

**Software Heritage SWHID is the canonical permanent identifier (v0.1).** When a design is accepted, Save Code Now is triggered on the contributor's repo at the submitted commit; the resulting SWHID is recorded in the design entry. Software Heritage archives source permanently with content-addressed identifiers. The PNA Spec itself states this v0.1 commitment; future toolkit versions may revise.

**Optional secondary fork for high-signal designs.** A `pnt-archive` GitHub-organization fork is at maintainer discretion for designs the toolkit wants belt-and-braces archival on. SWHID alone is sufficient for the archival promise.

**Linear SemVer for the PNA Spec; per-axis versioning declared in each design's Architecture document.** Patch for clarifications, minor for additive, major for breaking. Individual axes can evolve at different rates; a design declares which axis version it implements for each axis it picks.

**Every accepted contribution ships an Architecture document with a complete AC attestation table.** It declares conformance to a specific Toolkit-Version, declares per-axis picks and versions, documents implementation choices per axis, and includes an AC attestation table that maps every applicable AC to (a) how the design realizes it and (b) the specific test(s) or review mechanism(s) that verify it. A row missing the verification field is a rejected PR. This is the load-bearing acceptance check.

**Architecture document = Security Target in role.** The Common Criteria Protection Profile / Security Target model maps cleanly: the PNA Spec acts as the Protection Profile (class-level requirements); each design's Architecture document acts as the Security Target (this design's declared conformance, with implementation details and test pointers). The toolkit keeps its own terminology — no rename — but the model is what we're building.

**Skill packages the spec for AI agents — three flows in one skill.** The skill (`pna-build-eval-contrib/SKILL.md`) is one consumption view — it points into `spec/`, `contracts/`, and `reference_designs/`. It covers three flows: building a new PNA, evaluating an existing PNA, and authoring a contribution PR back to the toolkit. If any flow grows large enough to need its own SKILL.md, split later.

**Single evaluation flow, not two named modes.** Mechanics, inputs, and output shape of an LLM evaluating a PNA are the same whether the consumer is a user auditing someone else's app or a builder checking their own in-progress code. The flow takes a source tree (or description), walks the AC list, and produces an AC-ID-keyed report (conformant / non-conformant / not-applicable / unable-to-determine, with citations). Callers can ask the evaluator to emphasize specific Goals at runtime (e.g., "focus on Goal 1 — private data sovereignty") if they have a particular concern; that's a runtime variation, not a structural split.

**All OSI-approved licenses accepted.** No license restriction beyond OSI approval. Software licensing is a relatively low-friction concern in the LLM era — derivative work in this space is shaped more by the spec and contracts than by copying source lines. Revisit if friction emerges.

**Verification specifics live per-design, not in the spec.** The spec declares ACs and what they require; it does *not* declare how each AC must be verified (no per-AC `[Verify: deterministic | LLM | human]` tags in the spec itself). Each Architecture document declares how its design verifies each applicable AC, in the AC attestation table. Rationale: verification-method tagging at the spec level is brittle (LLM capabilities evolve; what's "human-only" today may be machine-verifiable tomorrow), encourages mis-tagging, and adds visual noise to the spec. Per-design specifics keep the spec lean and let each design pick the verification approach that fits its tooling.

**Language about axis counts is variable, never numeric.** The spec says "the architectural axes," never "the six axes." Numeric counts drift when the axis set changes; variable language doesn't.

**RFC 2119 normative language for conformance-bearing prose.** The spec is not converted to YAML or to a stripped-down RFC skeleton — readable prose stays. But conformance-bearing statements within the prose use MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. The wording around each AC and sub-contract is sharpened as a side effect: vague statements get re-worded to pin what's normatively required.

**Stable IDs as the join key.** ACs already have IDs (`AC-1`, `AC-MCP-A`, etc.). This work makes them load-bearing: every typed contract in `contracts/` names the AC(s) it realizes; every Architecture document attests AC-by-AC. Bidirectional traceability is established at the AC level for v1; deepening to the 57-sub-contract level is deferred until contribution review surfaces it as friction.

## Target repository layout

```
personal_network_toolkit/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── spec/
│   ├── PNA_Spec.md                              # Canonical spec — readable prose, RFC-style normative statements
│   ├── axes/                                    # Per-axis definitions
│   │   ├── storage.md
│   │   ├── distribution.md
│   │   └── ...
│   ├── use_cases.md
│   └── glossary.md
├── contracts/                                   # Typed contracts (JSON Schema, OpenAPI, SQL DDL, TS)
│   ├── README.md                                # Index; each contract names the AC(s) it realizes
│   └── ...
├── reference_designs/
│   ├── README.md                                # Index of accepted designs + intro to the contribution model
│   ├── templates/
│   │   ├── TEMPLATE.md                          # Per-design record template
│   │   └── ARCHITECTURE_TEMPLATE.md             # Architecture document template (Security Target role)
│   └── <design-name>/
│       ├── README.md                            # Design record + architectural learnings notes
│       └── Architecture.md                      # The design's Architecture, copied at acceptance
├── pna-build-eval-contrib/
│   └── SKILL.md                                 # Agent-consumption view — build, evaluate, contribute
├── tools/
│   ├── swh-save.sh                              # Trigger Save Code Now; capture SWHID
│   ├── validate-architecture.py                 # Lint Architecture documents against the template
│   └── lint-spec-ids.py                         # Check ID rigor across spec and contracts
├── docs/
│   ├── PriorArt.md                              # Prior-art survey (was: research/prior_art_survey.md)
│   └── PriorArtReferences.md                    # Annotated source list for the survey
├── plans/                                       # This file lives here
└── archive/                                     # Optional: forked snapshots of high-signal designs
    └── <design-name>/                           # Git submodule pointing at pnt-archive/<design-name>
```

Notes on the layout:

- `reference_designs/` (renamed from `designs/` in the prior draft) — clearer for first-time readers that everything here is a *reference* design.
- `reference_designs/templates/` groups the per-design templates separately from the actual design records.
- Each `reference_designs/<design-name>/` directory carries a design record (`README.md`, which can hold architectural learnings notes as the design evolves) and the Architecture document copied at acceptance.
- Prior-art research moves under `docs/`, which is more conventional than top-level placement.

## Spec formalization details

The spec-formalization work is the largest single addition over the prior community-contribution plan. Concretely:

**Readable prose stays.** The spec is not converted to YAML or stripped to an RFC skeleton. Vocabulary, preamble, motivation, why-it-matters, vision — all stays as prose, because both humans and LLMs read prose comfortably.

**Conformance-bearing statements get unambiguous language.** Every AC and every sub-contract is reworded so that conformance-bearing statements use MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. The wording around them may shift to accommodate the keyword. Some statements that were vague today will get sharper as a side effect — that's the point.

**Stable IDs are load-bearing.** Every typed contract in `contracts/` opens with a header naming the AC(s) it realizes (e.g., `# Realizes: AC-1, AC-4`). Every reference design's Architecture document includes an AC attestation table where each applicable AC is annotated with (a) how the design implements it (or "not applicable" with reason), and (b) the specific test or review mechanism that verifies it. The AC ID is the join key across spec, contracts, and design.

**Test mapping is a hard requirement.** Every Architecture document maps every applicable AC to one or more verification mechanisms: a deterministic test file, an LLM evaluation prompt or rubric, or a human-review note explaining why no automated test is feasible (with the review record itself archived in the design's repo). LLMs make this mapping cheap to author and audit; there is no friction reason to defer it. A submission without complete AC-to-verification mapping is not accepted.

**Sub-contract-level traceability deferred.** The 57 named sub-contracts in `PNA_Spec.md § Sub-contracts per slot` stay as they are. Bidirectional links at the sub-contract level are deferred until a contribution review surfaces them as friction.

## Per-design record template

`reference_designs/templates/TEMPLATE.md`:

```markdown
# <design-name>

**Maintainer:** <name> (<canonical-repo-url>)
**License:** <OSI-approved license SPDX identifier>
**First accepted:** Toolkit-Version <X.Y>, <YYYY-MM-DD>
**Status:** active | archived | superseded

## Summary

One paragraph describing what this design is and what it demonstrates.

## Axis picks at first acceptance

| Axis | Pick | Axis version |
|---|---|---|
| storage | opfs-sqlite-wasm | v1 |
| ... | ... | ... |

## Contributions to the spec

### Toolkit-Version <X.Y> — <short title> (PR #<n>)
- Reference design version: commit `<sha>`
- Software Heritage: `swh:1:dir:<id>`
- Optional archive: `archive/<design-name>` at commit `<sha>`
- Summary: <2–4 sentences>

## Architectural learnings

Notes that emerged from building or operating this design — constraints first-principles
reasoning would have missed, design-tradeoff stories, things that surprised the
maintainer. These accumulate as the design evolves.

## Reproducibility notes

Build/run instructions sufficient for someone to make a fighting attempt from the
archived source.

## Architecture document

See [Architecture.md](./Architecture.md), the design's Security Target, copied at first acceptance.
```

## Architecture document requirements

The Architecture document plays the Security Target role: it is the design's declared conformance against the PNA Spec (the Protection Profile). To be accepted, it must contain:

1. **Toolkit-Version declaration.** "This design conforms to Toolkit-Version 0.7."
2. **Axis pick declaration with per-axis versions.** A table naming each axis the design exercises and the version it implements.
3. **Per-axis implementation notes.** A short section per axis explaining the implementation choices.
4. **AC attestation table — the load-bearing artifact.** For each AC that applies to the design's flavor, a row stating:
   - **Realization:** how the design realizes the AC, with code/file references.
   - **Verification:** the specific test file(s), LLM evaluation rubric, or human-review note that verifies it for this design.
   - **Status:** conformant, partial-conformance with known gap, or not-applicable (with reason).
5. **Contributions claim.** What spec changes (if any) this submission proposes, with a clear statement of what working code demonstrates each change.
6. **Reproducibility notes.** Sufficient information for a future reader to build the archived source.

A row missing the verification field is a rejected PR. This is the mechanical check the contribution workflow leans on.

## Contribution workflow

1. Contributor builds (or already has) a PNA in their own repo, under an OSI-approved license.
2. While building or operating it, contributor identifies a spec ambiguity, gap, or constraint not yet captured.
3. Contributor authors an Architecture document describing the design and the proposed contribution, including the AC attestation table with verification references.
4. Contributor opens a PR against the toolkit containing:
   - Spec diff (if any)
   - New or updated record at `reference_designs/<design-name>/README.md`
   - Copy of the Architecture document at `reference_designs/<design-name>/Architecture.md`
   - Canonical repo URL and commit SHA being submitted
5. Maintainers review:
   - Spec change is motivated by the design and is well-formed
   - Architecture document is complete (AC attestation table maps every applicable AC to a verification mechanism)
   - Reference design actually demonstrates the claimed contribution (clone, inspect, optionally run the evaluator skill against the source)
   - License is OSI-approved
6. On merge:
   - Spec changes land (including any new AC IDs, sub-contracts, or axis-pick additions)
   - Maintainer runs `tools/swh-save.sh <repo-url> <commit-sha>` and records the returned SWHID in the design record
   - Maintainer decides whether the design warrants an `archive/` fork
   - Toolkit version bumped per SemVer rules

**Automated contribution path.** The skill (see below) walks an LLM through steps 3–4 end-to-end. A builder using Claude Code can ask the agent to "open a PR adding this design to the toolkit" and the skill guides the agent through authoring the Architecture document, generating the AC attestation table from the design's source, and producing the PR. Maintainer review at step 5 is the human-judgment gate that's intentionally not automated.

## SKILL.md content (sketch)

```markdown
---
name: pna-build-eval-contrib
description: Use when building, extending, or evaluating a Personal Network Application (PNA) — local-first, private-by-default applications operating on personal contact and relationship data with no remote authority. Also triggers when proposing changes to the PNA Toolkit spec back to its canonical repo. Three flows: build a conformant PNA from the spec, evaluate whether an existing application conforms (e.g. "is this app safe to install?"), and author a contribution PR back to the toolkit when a spec gap is found.
---

# Building, Evaluating, and Contributing to PNAs

A PNA is a local-first application built to the PNA Toolkit spec. The spec defines the architectural commitments (ACs) all PNAs share and the axes along which they legitimately differ. Conformance is satisfied by implementing the typed contracts in `contracts/` for each declared axis pick and honoring every applicable AC.

## Build flow

1. Read `spec/PNA_Spec.md` end-to-end.
2. Determine the user's axis picks. Each axis has options in `spec/axes/`.
3. Author an Architecture document for the design declaring Toolkit-Version, axis picks, and per-axis implementation choices.
4. Pull the typed contracts from `contracts/` for each axis pick.
5. Find a reference design in `reference_designs/` that shares as many axis picks as possible. Visit its archived source (SWHID linked in the design record) and study its implementation.
6. Build against the contracts. Treat them as load-bearing. Do not deviate without proposing a spec change per the contribute flow below.
7. Fill in the AC attestation table for the design, mapping each applicable AC to the test or review mechanism that verifies it.
8. Run the evaluate flow on the in-progress code as a self-check.

## Evaluate flow

Given a candidate PNA source tree and a declared or inferred set of axis picks:

1. For each AC in `spec/PNA_Spec.md` that applies to the candidate's flavor, decide conformance:
   - Read the relevant source files; trace the data flow or control flow the AC constrains.
   - Cite specific code locations supporting the decision.
   - If the candidate has an Architecture document with an AC attestation table, check that the cited verification mechanism actually runs and passes.
2. For each typed contract relevant to the candidate's axis picks, check that the candidate implements the contract correctly.
3. Produce a structured report keyed by AC ID:
   - `conformant` — with cited code locations.
   - `non-conformant` — with cited code locations showing the violation and the AC's stated requirement.
   - `not-applicable` — with reason (typically: the candidate's flavor doesn't trigger this AC).
   - `unable-to-determine` — with explanation; defaults to flagging for human review.
4. Summarize at the top: overall posture and the most concerning non-conformances (especially anything compromising Goals 1–5: private data sovereignty, mirroring centralized sources locally, secure communication, portability, locally diagnosable).

Callers may ask the evaluator to emphasize specific Goals or axes at runtime (e.g., "focus on private-data sovereignty"). That's a runtime variation, not a separate evaluation mode.

## Contribute flow

When a builder discovers a spec ambiguity, gap, or constraint not yet captured:

1. Read `CONTRIBUTING.md`.
2. Frame the contribution as a spec diff motivated by the working code in the design.
3. Author or update the design record at `reference_designs/<design-name>/README.md`.
4. Author or update the Architecture document at `reference_designs/<design-name>/Architecture.md`, including the AC attestation table with verification references.
5. Open a PR with: spec diff, design record, Architecture document, canonical repo URL, and commit SHA.
6. After merge, the maintainer triggers Software Heritage archival and records the returned SWHID.

## Key resources

- `spec/PNA_Spec.md` — canonical spec
- `spec/axes/` — per-axis definitions and options
- `contracts/` — typed contracts
- `reference_designs/README.md` — index of accepted reference designs
- `reference_designs/templates/` — per-design templates
- `tools/` — validators
```

## CONTRIBUTING.md content (sketch)

Sections to write:

1. **Philosophy.** The toolkit evolves through reference-driven specification. Spec changes must be accompanied by a working reference design. The spec is generative + evaluative: AI agents read it to build conformant PNAs and to evaluate whether a candidate application is safe to use as one.

2. **What we accept.** Reference designs derived from working applications, under any OSI-approved license, with an Architecture document conforming to the requirements above — including a complete AC attestation table with verification references for every applicable AC.

3. **What we don't accept.** Spec changes without a demonstrating reference design. Designs whose license prevents Software Heritage archival. Architecture documents missing the AC attestation table or its verification field. Designs that maintainers can't get to build at all.

4. **PR contents required.** Spec diff, design record, Architecture document, repo URL, commit SHA.

5. **Acceptance process.** Maintainer review at the judgment-and-review layer. The skill's contribute flow is the canonical happy path; manually authored PRs are also fine.

6. **Versioning.** Linear SemVer for the PNA Spec. Per-axis versioning declared in each design.

7. **Archival.** Software Heritage SWHID is the canonical archive. The toolkit may additionally fork high-signal designs to a `pnt-archive` org at maintainer discretion. The toolkit does not maintain forks; they are frozen at the accepted commit.

## Phased implementation

Phases are sized for Claude Code sessions. Each ends in a committable, working state. The phases below carry forward from the prior plan; we'll revisit and re-sequence after this pass settles.

### Phase 1 — Repo restructure

- [x] Create new directory layout: `spec/`, `contracts/`, `reference_designs/`, `reference_designs/templates/`, `pna-build-eval-contrib/`, `tools/`, `docs/`, `archive/`.
- [x] Move existing spec documents into `spec/`.
- [x] Move existing typed contracts from `spec/contracts/` into top-level `contracts/`.
- [x] Relocate `research/prior_art_survey.md` to `docs/prior_art.md` (later split into `docs/PriorArt.md` (prose survey) + `docs/PriorArtReferences.md` (annotated source list)).
- [x] Create `reference_designs/fellows_local_db/` with a placeholder README pointing to the external repo (SWHID added in Phase 5).
- [x] Update root `README.md` to reflect the new layout (the `## Status` section is the home for success criteria).

### Phase 2 — Documentation scaffolding

- [x] Write `CONTRIBUTING.md`.
- [x] Write `reference_designs/README.md` (index + introduction to the contribution model).
- [x] Write `reference_designs/templates/TEMPLATE.md`.
- [x] Write `reference_designs/templates/ARCHITECTURE_TEMPLATE.md`, including the AC attestation table format with the Verification field.
- [x] Audit existing spec prose for numeric axis counts and replace with variable language.
- [x] Add to `spec/PNA_Spec.md`: declaration that v0.1 uses Software Heritage SWHIDs as the permanent identifier for reference designs.
- [x] Add to `spec/PNA_Spec.md § Vision`: forward note about conformance evaluation as a potential precondition for multi-PNA ecosystem interop in a future toolkit version, framed as a systems-level test that will require rethinking the spec at that level.

### Phase 3 — Spec formalization pass

- [x] RFC 2119 keyword pass on `spec/PNA_Spec.md`: every AC and sub-contract reworded with MUST / SHOULD / MAY where conformance-bearing. Readable prose preserved around them. Document the pass in `CHANGELOG.md`.
- [x] Bidirectional-traceability pass on `contracts/`: every typed contract file gets a header naming the AC(s) it realizes. Update the contracts index.
- [x] Write `tools/lint-spec-ids.py`: verify every AC has an ID; every contract names at least one AC. Wire into CI.

### Phase 4 — Skill packaging

- [x] Write `pna-build-eval-contrib/SKILL.md` per the sketch above — build, evaluate, contribute flows in one skill.
- [x] Verify the skill description triggers correctly on representative test prompts for each flow.
- [x] If a single skill shows friction, split — but only then.

### Phase 4.5 — User's Guide and contribute-flow preflight

- [x] Write `docs/users-guide.md` — concise step-by-step instructions organized around the six success criteria in `README.md § Status`. The reference-design submission workflow gets the most space (since `fellows_local_db` is the first user of it in Phase 5).
- [x] Enhance `pna-build-eval-contrib/SKILL.md`'s contribute flow with an explicit **preflight validation** step (does the design have all required files? is the Architecture document complete and accurate against the code?), the **"what's interesting architecturally?"** prompt — with three valid patterns documented (new AC, existing pattern on a new platform, ecosystem-value-add) — and explicit **interactive** guidance for creating the Architecture document when it doesn't yet exist.
- [x] Link `docs/users-guide.md` from `README.md`.

Phase 4.5 lands in the same PR as Phases 1–4 so the User's Guide is exercisable against `fellows_local_db` immediately in Phase 5.

### Phase 5 — Archival tooling and first design record

- [ ] Write `tools/swh-save.sh`.
- [ ] Archive `fellows_local_db` at its current canonical commit.
- [ ] Complete `reference_designs/fellows_local_db/README.md` with SWHID, axis picks, and a backfilled contributions list.
- [ ] Copy `fellows_local_db`'s Architecture document to `reference_designs/fellows_local_db/Architecture.md` and backfill the AC attestation table — including the Verification reference per AC, even if the verification mechanism today is "human review during this PR." This exercise validates the AC-attestation format before the workflow opens to external contributions and surfaces the first concrete list of "ACs this design conforms to but doesn't yet have automated tests for."

### Phase 6 — Validation tooling

- [ ] Write `tools/validate-architecture.py`: lints an Architecture document against the template; fails on missing AC attestation rows or missing Verification fields.
- [ ] Wire `lint-spec-ids.py` and `validate-architecture.py` into CI.

### Phase 7 — Dogfood with a second contribution

- [ ] Identify a second production app (Rich's or a friend's) suitable as a reference design.
- [ ] Take it through the full contribution workflow, ideally driven end-to-end by Claude Code through the skill's contribute flow.
- [ ] Note friction points (especially around AC attestation, evaluator-skill use, automated PR authoring) and revise.

## Open questions and risks

1. **Build reproducibility.** Software Heritage preserves source, not build environments. Designs whose dependencies vanish may become unrunnable even with archived source. Mitigation: rich reproducibility notes per design; `archive/` fork option for high-signal designs.

2. **Maintainer capacity.** As contributions arrive, review workload grows. The Architecture-document validator and the skill's contribute flow reduce some of it. Long-term, may need additional maintainers or a tiered acceptance model.

3. **Skill format stability.** SKILL.md format is still young. If it evolves significantly, the skill packaging may change. Mitigation: the skill is one view of the canonical artifact, not the artifact itself.

4. **Discovery.** New builders won't find the toolkit without external discovery (blog posts, awesome-lists, integration with SDD tools). Out of scope for this plan but flagged.

5. **Sub-contract-level traceability.** Bidirectional links at the AC level are committed; the 57 sub-contracts stay as they are. Deepen if contribution review surfaces it as friction.

6. **Single-skill packaging.** Build, evaluate, and contribute flows share one SKILL.md in v1. Split only if friction shows up.

7. **Future direction — conformance evaluation as a precondition for ecosystem interop.** A future multi-PNA ecosystem (per `PNA_Spec.md § Vision`) might require runtime conformance attestation before two PNAs are wired together. This is a systems-level test that requires rethinking the PNA Spec at that level. Flagged in the Vision section of the spec as a future direction; not in scope for v0.

## Success criteria

Success criteria live in `README.md § Status`, where they double as user-facing project state. The plan succeeds when those criteria are met.

---

*Plan derived from working conversations with Claude (Anthropic) in May 2026. Unifies the prior community-contribution-model plan, the prior PNA-RFC-conversion plan, and GitHub issue #4. Intended to be executed iteratively with Claude Code, phase by phase.*
