# PNA Toolkit Roadmap

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> **What this doc owns:** the *prioritization and sequencing* across the toolkit's work, and the
> **inbound-findings registry**. It links to the per-plan detail and the normative spec rather than
> restating them. Success criteria live in [`README.md` § Status](../README.md#status); the strategic
> reasoning behind the 2026-06-14 re-grounding is captured in
> [`brainstorms/2026-06-14-pnt-direction-grill.md`](../brainstorms/2026-06-14-pnt-direction-grill.md)
> (see its `## OUTPUT WORK QUEUE` and `## R2 SYNTHESIS`). *Prior dated snapshots are superseded by the
> one below; git history preserves them.*

## Progress snapshot — 2026-06-24

**The v0.1 spine is complete; three things have moved since the 2026-06-14 re-grounding, and they
reshape the near-term sequence.** The headline: the v0.2 cut is now *smaller* than the 2026-06-14 plan
described (the layering pass absorbed one rider and deferred another), and **user-mediation has become
the load-bearing v0.2 item** — independently corroborated from three directions.

- **Done — the v0.1 spine (unchanged):** `fellows_local_db` keystone **archived** with a deterministic
  `[verify]` entrypoint; **PRM accepted + archived** as the 2nd reference design (2026-06-10). `VERSION`
  stays `0.1.0-draft` until the v0.2 cut.

- **① Paper 1 positioning landed** (PR #91, 2026-06-24 — in `main`). The behavioral-space survey
  resolved into a **four-family taxonomy read off a coded 96-source matrix**: **Substrate · Sovereignty
  · Verification · Disclosure**, with **threat-modeling** a cross-cut (figures + corpus under
  [`docs/papers/figures/`](papers/figures/)). Three results bear on the spec:
  - **Disclosure** (runtime governance of the live act of egress — payload preview, channel choice,
    LLM-as-transport) surfaced as a *first-class family*, and it is **PNA's home turf** (the spec's
    Goal 3). The old hand-drawn "assurance/protection" family dissolved into Sovereignty + Disclosure.
  - **The PNA is *not* the lone four-family composite** — it sits in a small **composite group**
    {PNA, EUDI Wallet, IDS-RAM, Inrupt/Solid}; its distinct corner is *governed **outbound egress** of a
    downstream-mirrored personal relationship graph, **checked-not-awarded**, AI modeled as
    egress + runtime adversary + spec consumer*. Stated as a **wager**, evidence-safe.
  - **The "evolutionary stance"** — the spec is deliberately *partial on Substrate by design* (forgoes
    CRDT live-sync because the rules to keep users safe across sync aren't known yet); it **earns**
    complexity rather than assuming it, taking on harder capabilities only once simpler ones are proven
    usable + safe. *This is new positioning the spec itself has not yet absorbed* → the
    **positioning-reconciliation** work below.

- **② L1/L2 layering pass — IN-FLIGHT, not yet merged** (branches `docs/l1-l2-layering-pass` +
  `docs/resync-flavor-sweep`; `main` does not yet contain it). It factors the spec into three layers
  (L0 Goals · L1 ACs · L2 realizations): realizations moved out of the `AC-*` namespace to **`RZ-*`**,
  conditional ACs consolidated into `PNA_Spec.md`, `axes.md` → pure Layer 2, plus two new universal ACs
  — **AC-22** (honest capability assessment) and **AC-23** (source-available-for-verification). **This
  merge is the first domino for the v0.2 cut**, which is paused on it
  ([`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md)).

- **③ The v0.2 cut re-scoped** by the layering pass (see [`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md)):
  rider **B1** (distribution verifiability) became universal **AC-23** — *done in the pass*; rider **B2**
  (AC-PRM-E/F AI-write tiers) is **deferred to PRM v0.2**; **A** (4-goal restructure) and **C**
  (countermeasure-library + Harden) already landed in `main`. **Remaining v0.2-cut work = B3
  (user-mediation) + D (exceptions-hardening) + the mechanical version bump.**

- **④ PRM v0.2 / the data-floor — in progress** (manual testing underway 2026-06-24). It builds the
  **AC-MCP-C / PR-7 / EX-H9** trio (sealed-by-default disclosure tiers + projection-bound cloud MCP
  surface + a blast-radius strength dimension) — the concrete demonstrator for the **Disclosure** family
  Paper 1 identifies as PNA's distinctive contribution. The trio's graduation upstream is gated on PRM
  attesting it.

> **The user-mediation convergence (why B3 is the v0.2 headline).** Three independent lines now point at
> the *same* structure — *the human is the actuator; the proposer (AI / network / importer) only stages*:
> issue **#40** (fellows egress side), **#64 rider 3** (PRM mutation side), and **Paper 1's** bottom-up
> finding that PNA's Exception/Constraint/Harden "honest-deviation" machinery is a distinctive leaf. That
> triple corroboration raises **B3 (UM-1/2/3)** from "a rider" to the load-bearing v0.2 spec move — a
> candidate *third general mechanism* alongside Exceptions (`EX-*`) and Constraints (`CST-*`).

## Operating rule (unchanged)

**Knock out dependencies first** — sequence by the dependency graph, not the calendar. Value lens for
tie-breaks: weight near-certain, compounding value (learning / spec-feedback, recruiting artifact,
dogfood) over speculative reach; prefer low-cost, high-reversibility moves.

## The critical path (dependency graph)

```
[NOW] merge the L1/L2 layering pass ──► unblocks the v0.2 cut
   (3-layer factoring · RZ-* realizations · AC-22 · AC-23 [= #64 rider 1])
        │
[T0] v0.2 spec cut ──► drops the "draft" label; satisfies README criteria 3 & 5
   =  B3 user-mediation (UM-1/2/3)  +  D exceptions-hardening  +  positioning-reconcile  +  the cut
      (A 4-goal · C countermeasure/Harden · B1→AC-23 already landed; B2 deferred to PRM v0.2)
        │
        ├──► [T1, runs in parallel — testing now] PRM v0.2 / data-floor
        │         └──► GRADUATION wave: data-floor trio (AC-MCP-C/PR-7/EX-H9)
        │              + B2 (AC-PRM-E/F AI-write tiers) land upstream (demonstrator-gated)
        ├──► [T2] Papers → full drafts → publication · Harden build-out · validation-as-product
        │         · audit-flow UX (#55 /pna-evaluate, #62 end-user register) · reference-drift lint
        └──► [T3] R4-mission reference design (mutual-aid) → unlocks R3–R4 spec growth
[T4] vision-park: working-the-graph (sociogram/ZK-community) · cross-device (#42) · Tonsky-sync · multi-PNA ecosystem
```

## Priority tiers

### Tier 0 — the v0.2 spec cut *(do first; mostly formalization of already-demonstrated work)*
The near-term keystone. Lands the re-grounding as **v0.2** and drops the "draft" label. Detailed plan:
[`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md). **Prerequisite: the L1/L2 layering pass
merges to `main`** (the cut is paused on it).
- **A. 4-goal restructure** — **DONE** (in `main`): `spec/PNA_Spec.md` carries G1–G4 + the per-goal
  template + the cardinality table; README/users-guide reflect it.
- **B1. Distribution verifiability** — **DONE** as universal **AC-23** (in the layering pass; re-scoped
  from a distribution-pick split to a universal source-available-for-verification AC).
- **B2. Safe-AI-write tiers (AC-PRM-E/F)** — **deferred to PRM v0.2** (Tier 1). AC-PRM-F is
  user-mediation at the MCP-write boundary (folds into B3); AC-PRM-E's additive append-only/free-write
  tiers are undemonstrated until PRM ships them.
- **B3. User-mediation `UM-1/2/3`** — **TODO, the v0.2 headline.** Promote user-mediation to a normative
  mechanism: the *actuation* boundary — proposer stages, principal disposes (**UM-1 no-bypass**, enforced
  at the data layer not UI-only · **UM-2 separation** · **UM-3 legibility**), bounded to
  separation/legibility/attribution, **not** comprehension. Demonstrators: fellows egress (PR #261 —
  no-bypass landed; separation + legibility pending) + PRM mutation. Triple-corroborated (see snapshot).
- **C. Countermeasure-library + Harden reframe** — **DONE** (in `main`): `spec/exceptions.md`
  § Countermeasure library + the Harden flow; `pna-toolkit/SKILL.md` ships the 4th flow.
- **D. exceptions-hardening** — **TODO**: promote the `(Proposed, RFC)` amendments in `spec/exceptions.md`
  — `pna-active` predicate split · EX-H7 fail-closed · the un-relaxable floor — to normative **where a
  demonstrator supports it** (fellows ships the `EX-CLOUD-LLM` handler + `<body data-pna-mode>` signal);
  hold any unsupported part RFC-tagged.
- **Positioning-reconciliation (NEW, toolkit-fix class)** — fold the **evolutionary stance** and the
  **Disclosure / governed-outbound-egress** framing from the now-merged Paper 1 into the spec's Preamble
  + § Scope. Imposes no new obligation on designs (evidence-safe positioning), so it rides as a small PR
  before/with the cut. Drafted as its own branch; see `plans/v0.2-spec-cut-plan.md`.
- **The cut** — **TODO**: `VERSION` → `0.2.0`; Toolkit-Version stamp sweep; both designs to
  `toolkit_version = "0.2"`; README "draft" removed (3 places); CHANGELOG `## v0.2`; tag `v0.2.0`.
- **Done-when:** `just ci` green; `VERSION` = `0.2.0`; README "draft" gone; CHANGELOG + users-guide
  updated in the same PRs. Keep the cut PR separate/last (mostly-mechanical, reviewable diff).

### Tier 1 — PRM v0.2 *(the reference-design long pole; runs parallel; in progress)*
PRM's next milestones: custom relationship schema · per-field AI-write tiers (append-only / free-write)
· the **data-floor** demonstrator (sealed-by-default disclosure tiers + projection-bound MCP surface) ·
the workspace `EX-CLOUD-LLM` consent gate (EX-H2–H5/H9). Multi-source dedup consumes the shipped
**Atlas**. *State (2026-06-24): manual testing underway; the load-bearing data-floor code
(query-layer enforcement, cross-process consent state, the handler) is being built — see
PRM's `plans/ex-cloud-llm-workspace-handler.md`.*
- **Unblocks upstream (the GRADUATION wave):** once PRM v0.2 demonstrates + attests them, the
  **data-floor trio** (AC-MCP-C / PR-7 / EX-H9) and the **B2 AI-write tiers** (AC-PRM-E/F) land in the
  spec (demonstrator-gated, per CONTRIBUTING). This is the second PRM-driven spec evolution — README
  criterion 5, deepened.
- **Two open questions PRM raises for the toolkit** (resolve in the graduation wave): EX-H7
  *best-effort vs enforced* (PRM will enforce consent at its own surface, stronger than current
  normative text — note this composes with D's best-effort promotion, two steps not a conflict); and
  **AC-PRM-H** (generalize AC-2 "delivery channel not a service" to the local RW daemon; PR #59 landed
  the loopback auth + lint).

### Tier 2 — toolkit-goal surfaces + publication *(value-driven; no hard deps)*
- **Audit-flow UX (from real dogfooding):** **#55** deterministic `/pna-evaluate` (alias `/audit`) slash
  command — walks scope → run → emit + `report-lint` + save → posture; **the lowest-friction, highest-value
  flow ("is this app safe to install?") should be the most discoverable entry.** **#62** plain-language
  end-user register for the Visual Validator. Both self-contained; good parallel-agent work.
- **Harden flow** build-out (the advisement skill + the external-countermeasure catalog).
- **Validation-as-product:** `just validate <path>` → Mode-2 goal-impact reads → the behavior-based
  chooser + voluntary-validation registry; validating comms tools as their own class. *(Drift guardrail:
  the validator-as-service stays a tactic in service of the build mission, not the project's identity.)*
- **Papers → full drafts → publication** (P1: Onward!/local-first/arXiv — alignment + figures landed,
  full-prose author pass remains; P2: SPLC/Onward!/arXiv — still a skeleton).
- **Reference-drift lint** (from Paper 1 § 9): ~70 of the 96 survey-corpus URLs have drifted out of
  [`docs/PriorArtReferences.md`](PriorArtReferences.md). *Reconcile, not merge* — keep `PriorArtReferences.md`
  the human source of truth + the corpus the machine source, joined on URL, with a lint that fails on a
  corpus URL missing from the list (repo lint-discipline; needs a fault-injection self-test).

### Tier 3 — the R4-mission reference design *(unlocks the "why" layer)*
A **mutual-aid / community-care** PNA ([`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md)
item 5) — the R3–R4 mission made concrete. As a new reference design it lets the spec grow toward the
community-mental-health goal and is the natural demonstrator for any R3–R4 ACs. Its "needs help" field is
health/vulnerability-adjacent, so it stress-tests G2/G3 harder than any prior design.

### Tier 4 — vision-park *(future; seams sized, no design yet)*
- **Working the graph** — sociogram / reachability-for-help-seeking / ZK community-detection → a NEW
  protocol + NEW reference design + NEW separate sensitive DB; part of the multi-PNA ecosystem vision.
- **Cross-device replication** over commodity channels (#42 — 4 candidates: replication artifact ·
  keep-everything import · ephemeral viewer · AI reconciliation); **Tonsky commodity file-sync** as an
  axis pick (reading-gated, next-steps item 6). *This is the "richer Substrate" the evolutionary stance
  defers until the simpler floor is proven usable + safe.*
- **Multi-PNA ecosystem** (v0.2+ target; contracts already sized for it).

## Inbound-findings registry (updated 2026-06-24)

| Finding | Source | Track | Demonstrator | Status |
|---|---|---|---|---|
| Distribution = verifiability spectrum | prm#8 / #64 r1 | AC-23 | PRM | **DONE** — re-scoped to universal **AC-23** in the layering pass (lands in `main` on that merge) |
| User-mediation UM-1/2/3 | fellows#252 / #40 / #64 r3 | B3 | fellows (egress, PR #261) + PRM (mutation) | **Tier 0 — the v0.2 headline.** Triple-corroborated (incl. Paper 1's honest-deviation finding); gated on the fellows demonstrator finishing separation + legibility |
| Tiered safe-AI-write (AC-PRM-E/F) | prm / #64 r2 | B2 | PRM | **Deferred to PRM v0.2** (Tier 1) → graduation wave |
| Data-floor / disclosure tiers (AC-MCP-C/PR-7/EX-H9) | design note / PR #34 | graduation | PRM v0.2 | **In progress** (PRM manual testing 2026-06-24); the **Disclosure-family** demonstrator (ties to Paper 1) |
| EUDI/IDS/Inrupt open questions: EX-H7 enforced · AC-PRM-H (AC-2 → local daemon) | prm | graduation | PRM (PR #59 loopback auth + lint) | **Resolve in the graduation wave** with the data-floor |
| Paper 1 positioning → evolutionary stance + Disclosure framing | R2 survey / PR #91 | positioning-reconcile | landed paper | **Tier 0 toolkit-fix** — fold into spec Preamble + § Scope (this work) |
| Reference drift: corpus ↔ PriorArtReferences | Paper 1 § 9 | ref-drift lint | — | **Tier 2 toolkit-fix** — reconcile-not-merge + a drift lint |
| Countermeasure library + Harden (environmental threats) | 2026-06-14 + R3 | C / Harden | fellows/PRM (intrinsic) + toolkit-advised | **Reframe DONE** (Tier 0 C, in `main`) → **Harden build-out** Tier 2 |
| EAR rejected for live store; encrypt-in-transit | fellows#256 / #41 | #41 | fellows | **Locked; re-confirmed by R3** — don't revive at-rest EAR; Harden countermeasures instead; in-transit note landed (PR #58) |
| Cross-device over commodity channels | fellows#257 / #42 | #42 | fellows (prototype pending) | **Tier 4** (vision-park) — the deferred "richer Substrate" |
| Per-run toolkit retro (learning loop → spec/lint/skill) | #89 | meta | — | **Tier 2** — stand up a *minimal* cadence early so findings compound; defer heavy mechanization |
| Cross-design code reuse: realization index + `path:symbol` attestation | 2026-06-19 | [design note](design-notes/2026-06-harvesting-reusable-code.md) | fellows/PRM | **DONE (2026-06-19)** — `tools/realization-index.py` drift-gated in `just ci`; 100% pointer coverage in both designs; Save Code Now submitted (SH 2368289 / 2368290) |
| Verify SWH ingest for the fellows keystone | #56 | admin | — | **Action-and-close** — SWHIDs are content-addressed, so the `archived` claim is honest regardless |

## Research outputs

| # | Project | Output | Status |
|---|---|---|---|
| R1 | Contact Data Format Atlas | [`docs/contact-data-format-atlas.md`](contact-data-format-atlas.md) | **Shipped** (golden corpus = manual follow-up) |
| R2 | Behavioral-space survey → Paper 1 | [`docs/papers/paper1-pna-positioning.md`](papers/paper1-pna-positioning.md) + [`figures/`](papers/figures/) | **Alignment + figures landed** (PR #91, 2026-06-24); full-prose author pass → publication (Tier 2) |
| R3 | Data-protection vs OS-automation AI | feeds the Harden countermeasure catalog | **Done** (re-confirms EAR-deprecation) |
| R4 | Application-class-blueprint meta-method → Paper 2 | [`docs/papers/paper2-blueprint-method.md`](papers/paper2-blueprint-method.md) | Skeleton drafted (Tier 2) |

## Fit with README success criteria

- **Criteria 1, 4, 6** (toolkit proven end-to-end · durable archival · AC-as-identity) — **met** (keystone).
- **Criterion 3** (a contributor submits a design end-to-end) — **met** (PRM); awaits a first *external* contribution.
- **Criterion 5** (the spec evolves ≥1 minor version from a design's findings) — **met at the v0.2 cut**
  (Tier 0, unblocked once the layering pass merges); **deepened** by the PRM-driven graduation wave (the
  data-floor trio + AI-write tiers).
- **Criterion 2** (a user audits a candidate → AC-keyed report) — exercised by the evaluate flow, surfaced
  by the Visual Validator; deepened by the audit-flow UX (#55/#62) and validation-as-product (Tier 2).

## Deprecations / closed

- **Encryption-at-rest for the live private store — DEPRECATED, re-confirmed by R3:** dominated by
  full-disk encryption for the off-device threat, and useless against a live, user-privileged agent
  (which reads the decrypted bytes like any legitimate tool). The agent-boundary threat is handled by the
  **Harden** countermeasures (sandbox the agent / mediate the access path / detect) — all of which
  preserve tool-readability. Crypto's sanctioned home is **encrypt-in-transit** (the portable export).
- **"PNA is the lone four-family composite"** — retired by Paper 1's adversarial pass; the honest claim is
  the PNA's *corner within* a composite group {EUDI, IDS-RAM, Inrupt}, carried as a wager (§ 6 of the paper).
- Carried over from v0.1: the "lock-my-data" lineage and the per-call cloud-LLM "workspace bridge" remain closed.

## Planning-doc associations

- **Tier 0** → [`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md) (the layering-pass plan
  lands with the `docs/l1-l2-layering-pass` merge); `spec/PNA_Spec.md`, `spec/exceptions.md`, `spec/axes.md`.
- **Tier 1** → PRM's own `plans/` (notably `plans/ex-cloud-llm-workspace-handler.md`).
- **Tier 2** → [`plans/visual-validator-plan.md`](../plans/visual-validator-plan.md); issues #55 / #62 / #89;
  the `just validate` + chooser design notes; [`docs/papers/`](papers/).
- **Tier 3** → [`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5.
- **Tier 4** → [`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md) (R1–R5);
  next-steps item 6; issue #42.
