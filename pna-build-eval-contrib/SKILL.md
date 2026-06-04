---
name: pna-build-eval-contrib
description: 'Use when building, extending, or evaluating a Personal Network Application (PNA) — local-first, private-by-default applications that mirror SaaS contact data into a user-owned workspace and operate on relationship data with no remote authority. Triggers on requests to build a local-first contact app, relationship manager, private CRM-like tool, or any app built around personal-network data; on requests to audit an existing application for PNA-spec conformance ("is this app safe to install?", "does my app conform?"); and on requests to propose a change back to the PNT spec when a builder finds a gap. Three flows: build a conformant PNA from the spec, evaluate whether an existing application conforms, and author a contribution PR back to PNT.'
---

# Building, Evaluating, and Contributing to PNAs

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).

A PNA is a local-first application built to the PNT spec. The spec defines the architectural commitments (ACs) all PNAs share and the axes along which they legitimately differ. Conformance is satisfied by implementing the typed contracts in `contracts/` for each declared axis pick and honoring every applicable AC.

PNT itself is a *generative + evaluative* application-class blueprint:

- **Generative.** AI agents read it to build conformant PNAs. The spec + contracts + reference designs are the materials.
- **Evaluative.** AI agents read it to evaluate whether an existing application conforms. The user trusts the spec; they want to know whether a specific candidate honors it.

This skill covers three flows: **build**, **evaluate**, **contribute**. Use whichever the user's request fits.

## Build flow

Use when the user is starting or extending a PNA.

1. **Read the spec end-to-end first.** `spec/PNA_Spec.md` covers vocabulary, goals, axes, universal architectural commitments, and the slot map with 57 sub-contracts. The universal ACs are non-negotiable.
2. **Determine axis picks with the user.** Each axis has documented options in `spec/axes.md`. The axes in v0.1: distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure. The spec uses variable language because the set may evolve.
3. **Enumerate inherited Constraints.** From the chosen axis picks, list every Constraint they inherit (`spec/constraints.md`, via each pick's `Triggered-by:` and the cross-references in `spec/axes.md`). For each, state the handling you will implement — per-platform capability reduction, "enough power to be useful, not enough to be dangerous" — and its frontier. A `web-bundle` × `opfs-sqlite-wasm` PNA inherits the full `CST-PWA-*` family; plan the folder-mode-vs-OPFS-only split and the honest non-Chromium messaging up front, not as an afterthought. A capability reduction MUST enforce at the data layer, not UI-only.
4. **Author an Architecture document for the design.** Use the template at `reference_designs/templates/ARCHITECTURE_TEMPLATE.md`. It declares the Toolkit-Version, axis picks and their versions, and per-axis implementation choices.
5. **Pull the typed contracts.** For each axis pick, the relevant contracts live in `contracts/`. Each contract opens with a `Realizes: AC-X, AC-Y` header naming the ACs it realizes. Treat the contracts as load-bearing — do not deviate without proposing a spec change (contribute flow).
6. **Find a reference design that shares axis picks.** Each `reference_designs/<name>/` directory has a record with the design's flavor and a Software Heritage SWHID linking the archived source. Study the design that's closest to what the user wants.
7. **Build against the contracts.**
8. **Fill in the AC attestation table for the design.** For every applicable AC, name (a) how the design realizes it, with code references, and (b) the specific test, LLM evaluation rubric, or human-review note that verifies it for this design. A `conformant` row needs executable evidence (a resolvable test) or an explicitly declared review kind — a bare doc pointer is not evidence. Enumerate each row's **negative invariants** and pin each with a **negative test**. This is required for any future contribution PR.
9. **Run the evaluate flow on the in-progress code as a self-check.**

## Evaluate flow

Use when the user wants to audit an application for PNA conformance — either someone else's candidate ("is this app safe to install?") or their own in-progress design ("does my app conform yet?"). Mechanics are the same in both cases; the user's framing tells you which ACs to emphasize.

Inputs: a candidate PNA's source tree (or a description sufficient to read its behavior), and either a declared set of axis picks (from an Architecture document, if present) or picks you can infer from the source.

1. **For each AC in `spec/PNA_Spec.md` that applies to the candidate's flavor**, decide conformance:
   - Read the relevant source files; trace the data flow or control flow the AC constrains.
   - Cite specific code locations supporting the decision.
   - If the candidate has an Architecture document with an AC attestation table, check that the declared verification mechanism actually runs and passes.
2. **For each flavor-derived AC in `spec/axes.md`** triggered by the candidate's axis picks, do the same.
3. **For each typed contract relevant to the candidate's axis picks**, check that the candidate implements the contract correctly. Contract headers (`Realizes: AC-X, AC-Y`) tell you which ACs the contract serves.
4. **Attestation evidence audit — the Security Target is only as good as its executable evidence.** For each AC/CST the candidate attests `conformant`:
   - **Confirm the named test exists and passes.** A Verification that doesn't resolve to a real, passing test — or to an explicitly declared review kind (`human-review` / `LLM rubric` / `code inspection` / `by architecture` / `by bounding` / `by construction`) — is a finding, not evidence. A bare doc pointer is **not** evidence: a doc that *asserts* a property does not *prove* it.
   - **Enumerate the row's negative invariants** ("X must NOT happen"; "off-folder there is no durable private store") and confirm a **negative test** pins each. The happy-path test ("X happens when enabled") does not cover the negative — over-claiming a negative is a silent conformance failure.
   - **Deferred / partial / Open rows must carry an honest status.** A deferral that lives only in a code comment ("lands later", "inert for now") is itself a finding — it belongs in the attestation table or as a `@pytest.mark.xfail(strict=True)` test carrying a `tracking: #NNN` **issue** anchor (an issue, not a PR — see `reference_designs/templates/ARCHITECTURE_TEMPLATE.md` § Deferrals). Mind the asymmetry: a strict-xfail trips only on accidental *success*, never on abandoned deferral — so a `conformant` row citing an `xfail` test is a finding, since a declared-false invariant is not evidence.
   - A portable checker for the first two bullets ships at [`tools/attestation-evidence-lint.py`](../tools/attestation-evidence-lint.py) (stdlib, fixture-tested). It is the *deterministic* half: it proves each cited test exists and is a live, non-`xfail`/`skip` assertion — but a static lint cannot prove the test *passes*. Confirm passing by running the design's suite at its user-exposure gate (ship / per-PR / release). A `conformant` row citing an `xfail` test is the textbook false-evidence case it catches.
5. **Detect and verify Exceptions** (see `spec/exceptions.md`). For each Exception the candidate can raise — declared in its Architecture document's exception attestation, or inferred from the source where undeclared:
   - **Caught & handled?** Confirm consent is obtained *before* the raise (EX-H2), a persistent non-PNA-mode signal is shown while active (EX-H3), and a runtime active-set explainer exists (EX-H4). Cite code/UX for each.
   - **Reversibility?** Read the `Reversible:` declaration; if `yes`, trace the `Reversal:` mechanism and decide whether the code/UX delivers a practical path back to PNA mode. Mode only — do not credit a handler that implies returning to PNA mode undoes prior disclosure (EX-H5).
   - **Consent reaches the human?** Where an agent/proxy can drive the app, check the handler makes a best-effort attempt to propagate consent to the ultimate human and does not let an intermediary self-consent (EX-H7).
   - **Strength profile accurate?** Check each dimension's class (EX-H8) against the code/UX; the lint already confirmed the classes are valid vocabulary — you judge whether they're truthful (e.g. nothing about the provider's behavior is claimed above `provider-asserted`).
   - **Undeclared deviations.** You are the backstop: if the candidate departs from an AC or the PNA definition WITHOUT declaring an Exception, that is a silent (uncaught) deviation — a conformance failure. Flag it and name the `EX-*` it should have raised.
6. **Detect and verify Constraints** (see `spec/constraints.md`). For each Constraint the candidate's axis picks inherit:
   - **Detected honestly?** Confirm the app determines whether the ceiling is active using a sound signal for that constraint's `Detectability:` class (`feature-detect` / `empirical-probe` / `ua-sniff`). Flag capability checks trusted where presence ≠ usefulness ≠ permanence (M1) — e.g. trusting `showDirectoryPicker in window` for a *durable* store, or `persist()`'s boolean.
   - **Handled by capability reduction?** Confirm the app offers only what the platform can keep, and that any durability promise (badges, "saved" affordances) matches reality. The reduction must hold at the data layer — a gated capability whose write still happens (or whose RPC still succeeds from a console) is not reduced. Cite code/UX.
   - **Frontier honest?** Read the `Frontier:` declaration; confirm the design does not claim to `Solve` what it only `Mitigated`, and that a `Workaround:` (where claimed) actually exists in code/UX.
   - **Over-reach (the backstop).** If the candidate promises a capability the platform cannot keep WITHOUT acknowledging the ceiling — false durability — that is a silent conformance failure, the dual of an undeclared Exception. Flag it and name the `CST-*` it should have handled.
   Report each finding by `CST-*` ID.
7. **Produce a structured report keyed by AC or EX ID.** The canonical form is the typed artifact at `tools/evaluate-report.schema.json` (JSON Schema). Emit an instance of that schema as the source of truth, then render the human-readable report as a *view* over it — don't hand-write the prose report and skip the artifact. Emitting the typed form is what makes two runs on the same candidate diffable (which ACs changed status). Per-AC status is one of:
   - `conformant` — with cited code locations.
   - `non-conformant` — with cited code locations showing the violation and the AC's stated requirement.
   - `not-applicable` — with reason (typically: the candidate's flavor doesn't trigger this AC).
   - `unable-to-determine` — with explanation; defaults to flagging for human review.

   Each finding may also carry `evidence` entries tagged by `source` (`deterministic` / `llm` / `human`). When a deterministic check in `tools/` (e.g. the egress lint) has run against the candidate, fold its output in as a `source: deterministic` evidence entry on the AC it bears on, so the deterministic and LLM layers land on one finding.
8. **Summarize at the top** (the artifact's `summary` object): overall posture and the most concerning non-conformances. Goals 1–5 are the load-bearing user-facing concerns — anything compromising private-data sovereignty (Goal 1), sourced-data honesty (Goal 2), user-controlled communication (Goal 3), durability (Goal 4), or local diagnosability (Goal 5) leads the summary.

Callers may ask you to emphasize specific Goals or axes at runtime (e.g., "focus on private-data sovereignty"). Treat that as a hint for the summary, not a structural variation.

## Contribute flow

Use when the user has built or operated a PNA and wants to submit it back to PNT as a reference design — whether they found a spec gap and want to propose a fix, or they have a working design that adds ecosystem value at a flavor not yet attested. The flow has two phases: **preflight validation** (is the design submission-ready?) and **PR authoring** (open the actual PR).

### Preflight validation

Before authoring the PR, validate that the design is submission-ready. This step is interactive — ask the user questions, walk them through gaps, iterate until clean.

1. **Locate the design's Architecture document.** Typically at `docs/Architecture.md` (or equivalent) in the design's own repo.
   - **If it exists**, validate it against the code. For each AC attested as `conformant`, check the cited code locations and confirm the realization matches. For each AC with a Verification mechanism declared, check that the cited test/rubric/note actually exists and (where automated) passes.
   - **If it doesn't exist**, walk the user through creating one interactively. Use `reference_designs/templates/ARCHITECTURE_TEMPLATE.md` as the template. Ask about each section in turn:
     - Which Toolkit-Version does the design conform to?
     - For each axis in `spec/axes.md`, which pick does the design use, and at which axis version?
     - For each axis, how does the design realize the pick? (Read the code to help fill this in.)
     - For each applicable AC (universal in `spec/PNA_Spec.md`, plus any flavor-derived AC in `spec/axes.md` triggered by the picks): how does the design realize it? What test/rubric/note verifies it?

2. **Ask the user what's interesting architecturally about this design.** Three patterns are valuable enough to justify submission:
   - **New architectural commitment.** The design demonstrates a constraint the spec doesn't yet name. (Most valuable — the PR includes a spec diff.)
   - **Existing patterns on a new platform.** The design exercises existing ACs on a substrate or use-case not yet attested in the reference set. (Valuable — no spec change needed; the design's flavor expands the ecosystem.)
   - **Ecosystem value-add.** The design fills a use-case gap, brings accessibility, or makes something easier that no existing design demonstrates. (Valuable.)

   If the design fits any of these patterns, encourage submission. If it's purely identical to an existing reference with no novelty, surface that and ask what motivated the submission — if nothing surfaces, the PR may not be worth the maintenance overhead.

3. **Report what's broken or missing** in a structured list. The user needs to address these before the PR will be accepted:
   - Missing files (Architecture document, design record)
   - Missing sections in the Architecture document
   - Missing Verification field on any row of the AC attestation table
   - A `conformant` row whose only evidence is a doc pointer (doc-only is not evidence) or an undeclared verification kind
   - A `conformant` row whose cited test is `xfail` or unconditionally `skip` — a declared-false/unrun invariant is not evidence (`tools/attestation-evidence-lint.py` flags it; a conditional `skipif` guard is fine)
   - A negative invariant ("X must NOT happen") with no negative test pinning it
   - A deferral living in a code comment instead of the attestation or a `strict=True` xfail; or a strict-xfail with no `tracking: #NNN` issue anchor
   - AC realizations whose cited code doesn't match the claim
   - Failing or missing tests on the Verification side
   - A missing or malformed `design.toml` manifest — no `[verify]` entrypoint declared, a `[flavor]` pick that doesn't resolve in `spec/axes.md`, or (once `archival = "archived"`) a missing/malformed SWHID
   - License problems (must be OSI-approved; must permit Software Heritage archival)

4. **Iterate.** When the user fixes things, re-run preflight. Keep going until the report is clean.

### PR authoring

Once preflight passes:

1. **Read `CONTRIBUTING.md`** for the acceptance rules.
2. **Frame the contribution.** If proposing a spec change, write the spec diff and explain what working code in the design demonstrates each change. If purely additive (no spec change), say so in the design record's contributions section.
3. **Author the design record** at `reference_designs/<design-name>/README.md` per `reference_designs/templates/TEMPLATE.md`.
4. **Author the machine-readable manifest** at `reference_designs/<design-name>/design.toml` per `reference_designs/templates/design.toml`. This is the source of truth the conformance suite reads: `name`, `repo`, `toolkit_version`, `status`, `archival`, the `[flavor]` axis picks (each must resolve in `spec/axes.md`), and the `[verify]` block declaring the one command that builds and runs the design's attested tests (`tools/lint-spec-ids.py` validates the shape). While archival is still pending, leave `commit`/`swhid_rev`/`swhid_dir` empty (`archival = "pending"`); the lint permits that for an in-flight design.
5. **Copy the Architecture document** to `reference_designs/<design-name>/Architecture.md`. (PNT keeps its own copy at acceptance time; the design's own repo may evolve after.)
6. **Open the PR** with: spec diff (if any), design record, `design.toml`, Architecture document, canonical repo URL, and the commit SHA being submitted.

After merge, the maintainer triggers Software Heritage archival on the design's repo at the accepted commit (planned tooling: `tools/swh-save.sh`, landing in Phase 5; until then, archival is performed manually via Software Heritage's Save Code Now), then records the returned `swh:1:dir`/`swh:1:rev` and the commit SHA **into `design.toml`** and flips `archival = "archived"` (at which point the lint requires those fields and checks `swhid_rev` against `commit`). The SWHID also goes in the prose design record. A final preflight run against the merged state should come out clean.

A builder using Claude Code can drive both preflight and PR authoring end-to-end. Maintainer review at acceptance time is the human-judgment gate that's intentionally not automated.

## Principles to honor in every flow

- **Layering of verification.** Deterministic tools (lints in `tools/`) for the mechanical layer; LLMs (you) for the architectural-conformance layer; humans for judgment-and-review at PR time. Investment is ~80/20 toward description-and-process; PNT does not ship a Python conformance test runner beyond trivial lints.
- **The AC is the unit of identity.** Every AC has a stable ID. Every contract names the AC(s) it realizes. Every Architecture document attests AC-by-AC. When citing non-conformance, cite by AC ID.
- **Conformance is checked, not awarded.** There is no certifying body. A user trusts an app because they (or an LLM running this skill) checked it against the spec, not because the app carries a badge.
- **Variable language about axis counts.** The spec says "the axes," not "the six axes." The set may evolve; don't hardcode numbers.

## Key resources

- `spec/PNA_Spec.md` — canonical spec (vocabulary, goals, ACs, slot map, sub-contracts)
- `spec/axes.md` — axes, attested picks per axis, flavor-derived ACs, and the constraints each pick inherits
- `spec/constraints.md` — platform/substrate ceilings (`CST-*`) inherited by axis picks; the dual of exceptions.md
- `spec/use_cases.md` — attested classes of PNA (Directory Archive, PRM [draft], Multi-PNA ecosystem [target])
- `contracts/` — typed contracts (JSON Schema, OpenAPI, SQL DDL, TypeScript), each with a `Realizes: AC-X` header
- `reference_designs/README.md` — index of accepted reference designs
- `reference_designs/templates/` — the per-design record, Architecture, and `design.toml` manifest templates
- `reference_designs/<name>/design.toml` — the machine-readable design record (SWHID pin, flavor, verify entrypoint) the conformance suite consumes; see `plans/conformance-suite-plan.md`
- `tools/evaluate-report.schema.json` — typed artifact for the evaluate flow's AC-keyed report (the canonical, diffable output; the prose report is a view over it)
- `tools/egress-lint.py` — deterministic private-data-sovereignty check (AC-1): static scan for unsanctioned off-device egress vectors; `--json` emits evidence that folds into the report schema above. Run it against a candidate and fold its evidence into the AC-1 (and AC-2, server-side) finding.
- `tools/lint-spec-ids.py` — checks AC ↔ contract traceability invariants
- `CONTRIBUTING.md` — full contribution rules
- `docs/PriorArt.md` — survey of related work (annotated source list in `docs/PriorArtReferences.md`)
