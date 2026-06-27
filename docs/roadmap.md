# PNA Toolkit Roadmap

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> **What this doc owns:** the *prioritization and sequencing* across the toolkit's work, and the
> **inbound-findings registry**. It links to the per-plan detail and the normative spec rather than
> restating them. Success criteria live in [`README.md` § Status](../README.md#status); the strategic
> reasoning behind the 2026-06-14 re-grounding is captured in
> [`brainstorms/2026-06-14-pnt-direction-grill.md`](../brainstorms/2026-06-14-pnt-direction-grill.md)
> (see its `## OUTPUT WORK QUEUE` and `## R2 SYNTHESIS`). *Prior dated snapshots are superseded by the
> one below; git history preserves them.*

## Progress snapshot — 2026-06-27

**The v0.2 cut has shipped.** `VERSION` is `0.2.0`, tag `v0.2.0` is cut, the README "draft" label is gone,
and `CHANGELOG.md` carries the released **`## v0.2 (2026-06-25)`** section. The entire Tier-0 normative
spine is merged to `main`; the mechanical bump and the design re-sync are done, and the final
documentation-stamp reconciliation (this doc, the plans, `llms.txt`, the design.toml template) lands with
the drift-fix PR. **Since the cut**, three post-v0.2 changes have merged to `main` (now in the
`CHANGELOG.md` `## Unreleased` section): the **AC-1 restatement** (#106 — "Sovereign, sealed private
layer"; the two-store split demoted to canonical *realization*), the **Toolkit self-check** agent practice
(#108), and the **`evaluations/` casebook** with the Signal Desktop evaluation (#109). The next keystone is
the PRM-driven **graduation wave** (a separate upstream PR; see Tier 1).

- **Done — the two-design spine:** `fellows_local_db` + **PRM** archived as the two reference designs,
  both re-attested at **Toolkit-Version 0.2**. `VERSION` is `0.2.0` (tag `v0.2.0`).

- **L1/L2 layering pass — MERGED** (#95). Three layers (L0 Goals · L1 ACs · L2 realizations);
  realizations factored out of the `AC-*` namespace to **`RZ-*`**; conditional ACs consolidated into
  `PNA_Spec.md`; `axes.md` → pure Layer 2; two new universal ACs — **AC-22** (honest capability
  assessment) + **AC-23** (source-available-for-verification, = #64 rider 1).

- **User-mediation (B3) — MERGED** (#96). The **third general mechanism** alongside Exceptions and
  Constraints: `spec/user_mediation.md` (UM-1 no-bypass · UM-2 separation · UM-3 legibility, bounded to
  separation/legibility/attribution, **not** comprehension), with a `UM-*` lint + self-test. Both
  reference designs already attest UM-1/2/3 `conformant` — the triple-corroboration (fellows#252 / #40,
  PRM mutation, Paper 1's honest-deviation finding) held.

- **Exceptions-hardening (D) — partially MERGED.** **D3, the un-relaxable floor** (#98) — normative +
  **lint-enforced** (a `Relaxes:` naming AC-18/19/MCP-B fails CI; en route it fixed a latent `RELAXES_RE`
  gap). **D1, the `pna-active` predicate split** (#100) — normative + a new **`not-pna-active`**
  evaluate-report posture (schema · fixtures-lint · Visual Validator · a demonstrating sample).
  **D2 (EX-H7 fail-closed) stays RFC** — the one item gated on PRM v0.2's enforced-consent demonstrator;
  it rides the graduation wave. *(Correction to the 2026-06-14 plan: the demonstrator-gated D item is
  EX-H7, not the floor — fellows attests EX-H7 best-effort, PRM v0.2 is the hardened model.)*

- **Positioning-reconciliation — MERGED** (#94): the **evolutionary stance** + Disclosure /
  governed-outbound-egress framing from Paper 1 folded into the spec Preamble + § Scope.

- **Paper 1 positioning — MERGED** (#91): the four-family taxonomy (**Substrate · Sovereignty ·
  Verification · Disclosure** + threat-modeling cross-cut), the composite-group analysis (PNA within
  {EUDI, IDS-RAM, Inrupt}), the evolutionary stance.

- **PRM v0.2 — near merge** (in final testing 2026-06-27). Builds the **AC-MCP-C / PR-7 / EX-H9** data-floor
  trio (the **Disclosure**-family demonstrator) + the enforced-consent surface that demonstrates D2.

> **What the cut needed, and where each piece landed.** v0.2 stamped the already-merged normative content
> (layering · UM · D3 · D1) independently of PRM. The two real dependencies — **neither a PRM "upstream PR
> to the toolkit"** — resolved as:
> - **The design re-sync** — the **AC-22/23 + UM attestation rows** on fellows/PRM, `just rearchive` of the
>   bundled copies, and the realization index — **done**: both designs re-attest at Toolkit-Version 0.2 at a
>   taggable ref (a maintainer `just rearchive`, not a PR PRM filed here).
> - **The data-floor graduation** (AC-MCP-C / PR-7 / EX-H9 + D2 EX-H7 + B2 AI-write tiers) **is** a separate
>   upstream PR, demonstrator-gated on PRM v0.2 — it did **not** gate the cut and lands in v0.2.x. **The cut
>   was independent of it.**

## Operating rule (unchanged)

**Knock out dependencies first** — sequence by the dependency graph, not the calendar. Value lens for
tie-breaks: weight near-certain, compounding value (learning / spec-feedback, recruiting artifact,
dogfood) over speculative reach; prefer low-cost, high-reversibility moves.

## The critical path (dependency graph)

```
[DONE — all in `main`]  L1/L2 layering pass (#95) · user-mediation B3 (#96) · D3 floor (#98)
   · D1 pna-active (#100) · positioning-reconcile (#94) · Paper 1 (#91)
        │  ► every v0.2-cuttable normative commitment is merged
        │
[T0 — DONE ✓] the v0.2 cut ──► dropped the "draft" label; satisfied README criteria 3 & 5
   =  design re-sync (AC-22/23 + UM attestation on fellows/PRM · just rearchive · realization index)  ✓
      +  the mechanical version bump (VERSION 0.2.0 · stamp sweep · README · CHANGELOG · tag v0.2.0)   ✓
        │
        ├──► [T1 — testing now] PRM v0.2 / data-floor
        │         └──► GRADUATION wave (a *separate* upstream PR): data-floor trio (AC-MCP-C/PR-7/EX-H9)
        │              + D2 EX-H7 fail-closed + B2 (AC-PRM-E/F) — rides v0.2 if it precedes the cut, else v0.2.x
        ├──► [T2] Papers → publication · Harden build-out · validation-as-product · audit UX (#55, #62) · ref-drift lint
        └──► [T3] R4-mission reference design (mutual-aid) → unlocks R3–R4 spec growth
[T4] vision-park: working-the-graph (sociogram/ZK-community) · cross-device (#42) · Tonsky-sync · multi-PNA ecosystem
```

## Priority tiers

### Tier 0 — the v0.2 spec cut *(DONE — shipped 2026-06-27)*
All the normative content is merged to `main`, and the **design re-sync + the mechanical bump** have
shipped: `VERSION` is `0.2.0`, tag `v0.2.0` is cut, README is de-drafted, and the released `## v0.2`
CHANGELOG section is in place. Detailed plan: [`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md).
- **A. 4-goal restructure** — **DONE** (in `main`).
- **B1. Distribution verifiability** — **DONE** as universal **AC-23** (#95).
- **B2. Safe-AI-write tiers (AC-PRM-E/F)** — **deferred to PRM v0.2 → graduation wave.** AC-PRM-F is
  user-mediation at the MCP-write boundary (subsumed by B3/UM); AC-PRM-E's additive tiers await PRM.
- **B3. User-mediation `UM-1/2/3`** — **DONE** (#96): `spec/user_mediation.md` + `UM-*` lint + self-test.
- **C. Countermeasure-library + Harden reframe** — **DONE** (in `main`).
- **D. Exceptions-hardening** — **D3 floor DONE** (#98) · **D1 `pna-active` DONE** (#100) · **D2 EX-H7
  fail-closed → deferred to the graduation wave** (gated on PRM v0.2's enforced-consent demonstrator).
- **Positioning-reconciliation** — **DONE** (#94): evolutionary stance + Disclosure framing in the spec.
- **The cut (DONE):**
  1. **Design re-sync** — **done**: AC-22/23 + UM attestation rows on fellows/PRM `Architecture.md`,
     `just rearchive` of both bundled copies, realization index regenerated (both re-attest at 0.2).
  2. **Mechanical bump** — **done**: `VERSION` = `0.2.0`; both designs `toolkit_version = "0.2"`; README
     "draft" removed; CHANGELOG released **`## v0.2`**; tag `v0.2.0`. The trailing documentation-stamp
     reconciliation (this roadmap, the plans, `llms.txt`, the design.toml template) landed with the
     drift-fix PR, which also brought the durable docs under the version-stamp lint so they can't rot again.
- **Done-when (all met):** `just ci` green; `VERSION` = `0.2.0`; README "draft" gone; CHANGELOG v0.2 + tag.

### Tier 1 — PRM v0.2 *(the reference-design long pole; nearly complete)*
PRM's v0.2: custom relationship schema · per-field AI-write tiers · the **data-floor** demonstrator
(sealed-by-default disclosure tiers + projection-bound MCP surface) · the workspace `EX-CLOUD-LLM`
consent gate (EX-H2–H5/H9) enforced at its own surface (the D2 demonstrator). *State (2026-06-27):
in final testing, near merge — see PRM's `plans/ex-cloud-llm-workspace-handler.md`. Once it merges, the
design re-sync (Architecture re-attestation + `just rearchive`) and the graduation-wave upstream PR are the
follow-on toolkit work to prepare for.*
- **Feeds the cut:** PRM v0.2's `Architecture.md` (attesting AC-22/23 + UM + toolkit_version 0.2 at a
  taggable ref) is what the cut's PRM-side re-sync consumes.
- **Unblocks the GRADUATION wave (a separate upstream PR):** once PRM v0.2 attests them, the **data-floor
  trio** (AC-MCP-C / PR-7 / EX-H9), **D2 EX-H7 fail-closed**, and the **B2 AI-write tiers** (AC-PRM-E/F)
  land in the spec (demonstrator-gated). This is the second PRM-driven spec evolution — README
  criterion 5, deepened.
- **Also resolve in graduation:** **AC-PRM-H** (generalize AC-2 "delivery channel not a service" to the
  local RW daemon; PR #59 landed the loopback auth + lint).

### Tier 2 — toolkit-goal surfaces + publication *(value-driven; no hard deps)*
- **Audit-flow UX (from real dogfooding):** **#55** deterministic `/pna-evaluate` (alias `/audit`) slash
  command — the lowest-friction, highest-value flow should be the most discoverable entry. **#62**
  plain-language end-user register for the Visual Validator. Both self-contained; good parallel-agent work.
- **Harden flow** build-out (the advisement skill + the external-countermeasure catalog).
- **Validation-as-product:** `just validate <path>` → Mode-2 goal-impact reads → the behavior-based
  chooser + voluntary-validation registry; validating comms tools as their own class. *(Drift guardrail:
  the validator-as-service stays a tactic in service of the build mission, not the project's identity.)*
- **Papers → full drafts → publication** (P1: Onward!/local-first/arXiv — alignment + figures landed,
  full-prose author pass remains; P2: SPLC/Onward!/arXiv — still a skeleton).
- **Reference-drift lint** (from Paper 1 § 9): ~70 of the 96 survey-corpus URLs have drifted out of
  [`docs/PriorArtReferences.md`](PriorArtReferences.md). *Reconcile, not merge* + a drift lint.

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

## Inbound-findings registry (updated 2026-06-27)

| Finding | Source | Track | Demonstrator | Status |
|---|---|---|---|---|
| `egress-lint` blind spot: static scan misses dynamic / config-driven egress (false negatives) | Signal Desktop evaluation (2026-06-27) | [design note](design-notes/2026-06-egress-lint-dynamic-egress-blind-spot.md) | — | **Captured (Tier 2 toolkit-fix)** — docstring + note land the honesty fix; LLM/human tiers stay load-bearing. Next move: app-class warning banner (self-tested) |
| Distribution = verifiability spectrum | prm#8 / #64 r1 | AC-23 | PRM | **DONE** — universal **AC-23**, merged (#95) |
| User-mediation UM-1/2/3 | fellows#252 / #40 / #64 r3 | B3 | fellows (egress) + PRM (mutation) | **DONE** — `spec/user_mediation.md`, the third general mechanism, merged (#96) |
| Exceptions-hardening — un-relaxable floor | exceptions existential review | D3 | fellows (`EX-CLOUD-LLM` respects it) | **DONE** — normative + lint-enforced, merged (#98) |
| Exceptions-hardening — `pna-active` predicate split | exceptions existential review | D1 | fellows (`<body data-pna-mode>`) | **DONE** — normative + `not-pna-active` posture, merged (#100) |
| Exceptions-hardening — EX-H7 fail-closed | exceptions existential review | D2 | PRM v0.2 (enforced consent) | **Deferred → graduation wave** (gated on PRM v0.2; fellows attests only best-effort) |
| Tiered safe-AI-write (AC-PRM-E/F) | prm / #64 r2 | B2 | PRM | **Deferred to PRM v0.2** → graduation wave |
| Data-floor / disclosure tiers (AC-MCP-C/PR-7/EX-H9) | design note / PR #34 | graduation | PRM v0.2 | **In progress** (PRM in final testing 2026-06-27); the **Disclosure-family** demonstrator (ties to Paper 1) |
| EUDI/IDS/Inrupt open questions: EX-H7 enforced · AC-PRM-H (AC-2 → local daemon) | prm | graduation | PRM (PR #59 loopback auth + lint) | **Resolve in the graduation wave** with the data-floor |
| Paper 1 positioning → evolutionary stance + Disclosure framing | R2 survey / PR #91 | positioning-reconcile | landed paper | **DONE** — folded into the spec Preamble + § Scope (#94) |
| Reference drift: corpus ↔ PriorArtReferences | Paper 1 § 9 | ref-drift lint | — | **Tier 2 toolkit-fix** — reconcile-not-merge + a drift lint |
| Countermeasure library + Harden (environmental threats) | 2026-06-14 + R3 | C / Harden | fellows/PRM (intrinsic) + toolkit-advised | **Reframe DONE** (Tier 0 C, in `main`) → **Harden build-out** Tier 2 |
| EAR rejected for live store; encrypt-in-transit | fellows#256 / #41 | #41 | fellows | **Locked; re-confirmed by R3** — Harden countermeasures, not at-rest EAR; in-transit note landed (PR #58) |
| Cross-device over commodity channels | fellows#257 / #42 | #42 | fellows (prototype pending) | **Tier 4** (vision-park) — the deferred "richer Substrate" |
| Per-run toolkit retro (learning loop → spec/lint/skill) | #89 | meta | — | **Tier 2** — stand up a *minimal* cadence early so findings compound |
| Cross-design code reuse: realization index + `path:symbol` attestation | 2026-06-19 | [design note](design-notes/2026-06-harvesting-reusable-code.md) | fellows/PRM | **DONE (2026-06-19)** — `tools/realization-index.py` drift-gated in `just ci`; 100% pointer coverage |
| Verify SWH ingest for the fellows keystone | #56 | admin | — | **Action-and-close** — SWHIDs are content-addressed, so the `archived` claim is honest regardless |

## Research outputs

| # | Project | Output | Status |
|---|---|---|---|
| R1 | Contact Data Format Atlas | [`docs/contact-data-format-atlas.md`](contact-data-format-atlas.md) | **Shipped** (golden corpus = manual follow-up) |
| R2 | Behavioral-space survey → Paper 1 | [`docs/papers/paper1-pna-positioning.md`](papers/paper1-pna-positioning.md) + [`figures/`](papers/figures/) | **Alignment + figures landed** (PR #91); full-prose author pass → publication (Tier 2) |
| R3 | Data-protection vs OS-automation AI | feeds the Harden countermeasure catalog | **Done** (re-confirms EAR-deprecation) |
| R4 | Application-class-blueprint meta-method → Paper 2 | [`docs/papers/paper2-blueprint-method.md`](papers/paper2-blueprint-method.md) | Skeleton drafted (Tier 2) |

## Fit with README success criteria

- **Criteria 1, 4, 6** (toolkit proven end-to-end · durable archival · AC-as-identity) — **met** (keystone).
- **Criterion 3** (a contributor submits a design end-to-end) — **met** (PRM); awaits a first *external* contribution.
- **Criterion 5** (the spec evolves ≥1 minor version from a design's findings) — **met** at the v0.2 cut
  (shipped 2026-06-27: `VERSION` 0.2.0, tag `v0.2.0`); **deepened** by the PRM-driven graduation wave.
- **Criterion 2** (a user audits a candidate → AC-keyed report) — exercised by the evaluate flow, surfaced
  by the Visual Validator (now with the `not-pna-active` posture); deepened by the audit-flow UX (#55/#62).

## Deprecations / closed

- **Encryption-at-rest for the live private store — DEPRECATED, re-confirmed by R3:** dominated by
  full-disk encryption for the off-device threat, and useless against a live, user-privileged agent. The
  agent-boundary threat is handled by the **Harden** countermeasures (sandbox / mediate / detect) — all of
  which preserve tool-readability. Crypto's sanctioned home is **encrypt-in-transit** (the portable export).
- **"PNA is the lone four-family composite"** — retired by Paper 1's adversarial pass; the honest claim is
  the PNA's *corner within* a composite group {EUDI, IDS-RAM, Inrupt}, carried as a wager.
- Carried over from v0.1: the "lock-my-data" lineage and the per-call cloud-LLM "workspace bridge" remain closed.

## Planning-doc associations

- **Tier 0** → [`plans/v0.2-spec-cut-plan.md`](../plans/v0.2-spec-cut-plan.md) (the layering pass has
  merged; its Phase-1 B/D items are now done bar D2); `spec/PNA_Spec.md`, `spec/exceptions.md`, `spec/axes.md`.
- **Tier 1** → PRM's own `plans/` (notably `plans/ex-cloud-llm-workspace-handler.md`).
- **Tier 2** → [`plans/visual-validator-plan.md`](../plans/visual-validator-plan.md); issues #55 / #62 / #89;
  the `just validate` + chooser design notes; [`docs/papers/`](papers/).
- **Tier 3** → [`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5.
- **Tier 4** → [`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md) (R1–R5);
  next-steps item 6; issue #42.
