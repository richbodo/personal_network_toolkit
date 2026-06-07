# PNA Toolkit Roadmap

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> **What this doc owns:** the *prioritization and sequencing* across the toolkit's plans, and
> the **inbound-findings registry** (findings raised in reference designs that the toolkit
> tracks as demonstrator-gated spec-change candidates). It does **not** restate the per-plan
> detail or the normative spec — it links. The *success criteria* live in
> [`README.md` § Status](../README.md#status); per-phase detail lives in the plans linked below.

## Operating rule (decided 2026-06-07)

**Knock out dependencies first.** Sequence by the dependency graph, not by calendar. The
dwebcamp deadline was explicitly **dropped as a forcing function** this cycle, so the two
demoables (the Visual Validator and a one-shot build demo) are prioritized on their own value,
not rushed. The good news: the keystone is cheap and *feeds* those demoables with real content,
so dependency-correct ordering and demo-readiness mostly coincide.

Value lens used for tie-breaks (from the positioning work): weight **near-certain, compounding**
value (learning / spec-feedback, artifact-for-recruiting, dogfood) over speculative reach; prefer
low-cost, high-reversibility moves.

## Dependency graph (the critical path)

```
[T0] Finalize fellows keystone  (small: archival + flip design.toml + [verify] entrypoint + reconcile README↔manifest SWHID drift)
        ├──► conformance-suite Phase 4 activates (first archived design + verify entrypoint)
        ├──► README success criteria 1 / 3 / 4 / 6 satisfied (toolkit proven end-to-end)
        └──► evaluate flow runs on fellows ──► a REAL evaluate-report.json
                                                   └──► Visual Validator has real content (not synthetic samples)

[T1] PRM matures (days) ──► Phase-7 second contribution (drops the "draft" label; criteria 3 & 5)
        ├──► demonstrator for the distribution-axis split (#39 ⇄ prm#8)
        ├──► unblocks AC-PRM-* validation + community-care use case (next-steps item 5)
        └──► pulls in multi-source ingestion ──► Contact Data Format Atlas (Phase 1)

[T3] findings mature in their demonstrators (fellows test-first) ──► ride up to the toolkit later
```

## Priority tiers

### Tier 0 — Keystone: finalize the fellows attestation *(do first; cheap; unblocks the most)*
- **What:** finish [`plans/reorganization-plan.md`](reorganization-plan.md) Phase 5. Run
  [`tools/swh-save.sh`](../tools/swh-save.sh) → Software Heritage archival; in
  [`reference_designs/fellows_local_db/design.toml`](../reference_designs/fellows_local_db/design.toml)
  fill `commit` / `swhid_rev` / `swhid_dir`, set the `[verify].entrypoint` (the container command
  that builds + runs fellows's e2e/conformance suite and emits `evaluate-report.json`), and flip
  `archival = "archived"`; **reconcile the README↔manifest SWHID drift** (the README prints a
  computed `swh:1:dir:2fff6ff…` while the manifest still says `pending` with empty fields); confirm
  `just attestation-lint reference_designs/fellows_local_db` is green.
- **Status:** **~80% done** — the `design.toml` and a substantially complete 412-line
  `Architecture.md` (full AC attestation + EX-CLOUD-LLM + CST-PWA-* attestations, mostly
  `conformant` with real test refs) already exist. What remains is archival finalization + the
  verify entrypoint + the drift reconcile. **Small.**
- **Unblocks:** conformance-suite Phase 4 ([`plans/conformance-suite-plan.md`](conformance-suite-plan.md));
  README criteria 1/3/4/6; a real `evaluate-report.json` that becomes the Visual Validator's content.

### Tier 1 — PRM as the second reference design + the spec change it carries
- **What:** take **PRM** ([richbodo/prm](https://github.com/richbodo/prm)) through the contribute
  flow ([`plans/reorganization-plan.md`](reorganization-plan.md) Phase 7) — Architecture doc +
  `design.toml` + AC attestation + archival. Graduate the **distribution-axis verifiability split**
  (#39 ⇄ prm#8) to a spec change in [`spec/axes.md`](../spec/axes.md), with PRM as the demonstrator
  (it is the build-from-verifiable-source case).
- **Why:** drops the toolkit's **"draft"** label; validates README criteria **3** (a contributor
  submits end-to-end) and **5** (the spec evolves ≥1 minor version from a contributed design's
  findings); second dogfood of the contribute flow. R2–R3 value (PRM is the relationship-memory app).
- **Status:** PRM is **days from done** (2026-06-07) → immediate after Tier 0.
- **Unblocks:** AC-PRM-* validation; the **community-care / mutual-aid use case**
  ([`plans/pnt-next-steps-plan.md`](pnt-next-steps-plan.md) item 5) if PRM hosts it; multi-source
  ingestion → the Atlas (Tier 2).

### Tier 2 — Toolkit surfaces riding on the now-proven flows *(value-driven, no deadline)*
- **Visual Validator** (Phases 1–3) — [`plans/visual-validator-plan.md`](visual-validator-plan.md).
  Renders the real fellows/PRM `evaluate-report.json` from Tiers 0–1; the **toggle + side-by-side
  educational view** is the payoff. Artifact/recruiting value; no longer deadline-gated.
- **Contact Data Format Atlas** (Phase 1: Google + Apple) —
  [`plans/contact-data-formats-research-plan.md`](contact-data-formats-research-plan.md). Feeds PRM's
  multi-source ingestion (AC-PRM-B). Start when PRM needs multi-source.

### Tier 3 — Inbound findings maturing in their demonstrators *(tracked, not scheduled)*
See the registry below. fellows writes the demonstrating work **test-first**; each finding rides up
to the toolkit at the next fellows re-sync, per the `CONTRIBUTING.md` reference-driven rule.
- **#40** (fellows#252) — workspace user-mediation invariant → candidate **3rd general mechanism**. *Demonstrator in progress: fellows PR #261.*
- **#41** (fellows#256) — EAR rejected for the live store; light CST frontier note (encrypt-in-transit). *Decision recorded: fellows PR #258.*
- **#42** (fellows#257) — cross-device over commodity channels; exploratory; 4 candidates.

### Tier 4 — Parked / later
- Conformance **living-suite roadmap R1–R4** ([`docs/conformance-scope-and-lifecycle.md`](../docs/conformance-scope-and-lifecycle.md)) — activates after Tier 0.
- next-steps **item 6** (Tonsky commodity file-sync as an axis pick; reading-gated; relates to #42).
- next-steps **item 2** (split `pna-evaluate` into its own skill; optimization, last).
- Visual Validator **registry** (the parked voluntary-validation registry).
- **Multi-PNA ecosystem** (v0.2+ target; the contracts are sized for it, no design yet).

## Inbound-findings registry

Findings raised in reference designs that the toolkit tracks as **demonstrator-gated** spec-change
candidates. Per `CONTRIBUTING.md`, new normative content (a new AC / EX / CST / mechanism / axis)
is accepted only with a demonstrating design — so each row names its demonstrator and gate.

| Finding | Source | Toolkit track | Demonstrator | Gate | Target artifact | Status |
|---|---|---|---|---|---|---|
| Distribution = verifiability spectrum (not binary); + code-only vs. code+data | prm#8 | **#39** | PRM | PRM contribution (days); finding needs a fuller write-up | `spec/axes.md` Distribution split + new dimension | Demonstrator near-ready → Tier 1; write-up pending |
| Workspace user-mediation invariant ("human is the actuator; workspace is ground truth") | fellows#252 | **#40** | fellows_local_db | fellows test-first (3 property tests) | new mechanism doc, sibling to `exceptions.md`/`constraints.md` | **Demonstrator in progress** — fellows PR #261 lands property 1 (no-bypass) |
| EAR rejected for live store; encrypt the portable export instead | fellows#256 | **#41** | fellows_local_db | decision recorded | non-normative frontier note on `CST-PWA-NO-SYNC` / `-PRIVATE-SNAPSHOT` | **Decision locked** — fellows PR #258; toolkit note folds in at next re-sync |
| Cross-device private data over commodity channels (4 candidates) | fellows#257 | **#42** | fellows_local_db | fellows prototype + local-AI | axis picks / CST frontier resolution / a skill | Exploratory |

**In-flight in the demonstrators (2026-06-07).** fellows **PR #261** fixes a real private-store
leak in the file-import path (`importRelationshipsBytes` durably wrote to evictable OPFS in
browse-only mode — even from the DevTools console), found **test-first** while building #252 and
fixed at the **worker/data layer**. It lands the first #252 no-bypass property test and doubles as a
real-world validation of the toolkit's own CST-handling rule — *"a capability reduction MUST enforce
at the data layer, not UI-only."* fellows **PR #258** records the #256 EAR decision (reject for the
live store; encrypt in-transit). fellows defers #259 (off-folder UX) / #260 (attestation citations)
to follow-ups. Net: #40's demonstrator is in progress and #41's decision is locked — both fold into
the toolkit at the next fellows re-sync (Tier 0/1), where the fellows attestation will also gain the
new data-layer-guard citations.

## Cross-repo sync state

- **Mirrored:** the three fellows findings now have toolkit tracking issues (#40/#41/#42, label
  `inbound-finding`); the distribution finding is cross-filed (#39 ⇄ prm#8, bidirectionally linked).
  In-flight demonstrator work is linked from each: fellows PR #261 → #40, fellows PR #258 → #41.
- **Drift to fix in Tier 0:** `reference_designs/fellows_local_db/` README claims a computed SWHID
  while its `design.toml` says `archival = "pending"` with empty SWHID/commit/verify fields.
- **Snapshot lag:** the toolkit's `reference_designs/fellows_local_db/` attestation predates fellows's
  folder-mode / workspace-identity (#248) / #252–#257 work; re-sync at the next archival commit (Tier 0/1).
- **Plan drift:** `reorganization-plan.md` Phase 6 ("validate-architecture.py") shipped instead as
  `attestation-evidence-lint.py` + the `lint-spec-ids.py` manifest checks; treat this roadmap as the
  prioritization layer above the (partly superseded) per-plan phases.

## Fit with README success criteria

Tier 0 satisfies criteria **1, 4, 6** and is the precondition for **3**; Tier 1 (PRM) satisfies **3**
and **5**. Criterion **2** (a user audits a candidate and gets an AC-keyed report) is exercised by the
evaluate flow throughout and surfaced visually by the Tier-2 Visual Validator.
