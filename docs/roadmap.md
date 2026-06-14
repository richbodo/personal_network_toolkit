# PNA Toolkit Roadmap

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> **What this doc owns:** the *prioritization and sequencing* across the toolkit's work, and the
> **inbound-findings registry**. It links to the per-plan detail and the normative spec rather than
> restating them. Success criteria live in [`README.md` § Status](../README.md#status); the strategic
> reasoning behind this 2026-06-14 rewrite is captured in
> [`brainstorms/2026-06-14-pnt-direction-grill.md`](../brainstorms/2026-06-14-pnt-direction-grill.md)
> (see its `## OUTPUT WORK QUEUE` and `## R2 SYNTHESIS`). *Prior dated snapshots (≤ 2026-06-09) are
> superseded by the one below; git history preserves them.*

## Progress snapshot — 2026-06-14

**The v0.1 critical path is COMPLETE, and the project just re-grounded its direction.**

- **Done — the v0.1 spine:** the `fellows_local_db` keystone is **archived** with a deterministic
  `[verify]` entrypoint; **PRM is accepted + archived as the 2nd reference design** (2026-06-10). Both
  reference designs are live. `VERSION` stays `0.1.0-draft` until the v0.2 cut (Tier 0).
- **New direction (2026-06-14 strategy session — captured in the brainstorm):**
  - **Goals restructured to FOUR**, app-framed and at outcome altitude: **G1 Take ownership of the root ·
    G2 Protect the root's integrity, by validation · G3 Protect the root from egress · G4 Protect the
    root from entropy & accidents**,
    each gaining a readable *"constraints that fall out"* layer (a plain-language view of the ACs that
    serve it). (Durability became a distinct *protect-from-loss* goal; diagnosability folded into G2 as
    *validatability*; usability → a preamble assumption above the goals.)
  - **The line — PNA-goals vs toolkit-goals:** what a *built PNA* does (G1–G4) vs what the *toolkit*
    does — **build · evaluate · contribute · harden** (a NEW 4th flow: *advise* on the operating
    environment the data lives in).
  - **Countermeasure library = the mitigation side of Exceptions** (reuse the handler paradigm; a
    catalog keyed to hazard + environment, spanning *PNA-intrinsic* ACs + *toolkit-advised external*
    tools). Its sibling for *detected environmental threats* is the **Harden** flow.
  - **Validation-as-product** named as a toolkit-goal direction: `just validate`, Mode-2 goal-impact
    reads, a behavior-based chooser, a voluntary-validation registry, and validating comms tools as
    their own class.
  - **Research done (4 projects):** the **Contact Data Format Atlas** (shipped:
    [`docs/contact-data-format-atlas.md`](contact-data-format-atlas.md)); the **behavioral directed
    graph** (→ Paper 1); **data-protection vs OS-automation AI** (→ the Harden catalog; **re-confirmed
    at-rest encryption stays deprecated** — sandbox the agent / mediate the access path / detect, don't
    encrypt the bytes); the **application-class-blueprint meta-method** survey (→ Paper 2).
  - **Two papers drafted** ([`docs/papers/`](papers/)): **P1** positions the PNA class in the
    behavioral-spec directed graph; **P2** frames the toolkit's generative+evaluative blueprint method
    as a case study.

## Operating rule (unchanged)

**Knock out dependencies first** — sequence by the dependency graph, not the calendar. Value lens for
tie-breaks: weight near-certain, compounding value (learning / spec-feedback, recruiting artifact,
dogfood) over speculative reach; prefer low-cost, high-reversibility moves.

## The critical path (dependency graph)

```
[T0] v0.2 spec cut  ──► drops the "draft" label; satisfies README criteria 3 & 5
      = 4-goal restructure  +  the demonstrated #64 riders  +  countermeasure-library/Harden reframe
        │
        ├──► [T1] PRM v0.2 (custom schema + AI-write tiers + DATA-FLOOR demonstrator)
        │         └──► unlocks data-floor (AC-MCP-C/PR-7/EX-H9) + append-only/free-write tiers upstream
        ├──► [T2] Harden flow + validation-as-product (toolkit-goal surfaces)
        ├──► [T2] Papers 1 & 2 → full drafts → publication
        └──► [T3] R4-mission reference design (mutual-aid) → unlocks R3–R4 spec growth
[T4] vision-park: working-the-graph (sociogram/ZK-community) · cross-device · Tonsky-sync · multi-PNA ecosystem
```

## Priority tiers

### Tier 0 — the v0.2 spec cut *(do first; mostly formalization of already-demonstrated work)*
The near-term keystone. Lands the 2026-06-14 re-grounding as **v0.2** and drops the "draft" label. The
detailed specs for each item are in the brainstorm's `## OUTPUT WORK QUEUE`.
- **A. 4-goal restructure** — `spec/PNA_Spec.md` + `README.md` + `docs/users-guide.md`. Per-goal
  template (Goal[outcome] → example mechanism → why-it-matters → constraints-it-requires); reorder to
  G1–G4; split the *personal network / …graph / …data* definitions; promote Goals near the top; rework
  the preamble (fold the meta-reframe + the Paper-1 placement). **Finalize the deferred goal labels
  here.** *Toolkit-fix class* (a re-presentation that imposes no new obligation on existing designs) —
  but large; its **own careful PR**. **Delicate / CI-gated.**
- **B. The demonstrated #64 riders** (new normative content — each has a green demonstrator):
  **distribution-axis verifiability split** (`spec/axes.md`; demo PRM) · **AC-PRM-E/F safe-AI-write**
  review-required tier (demo PRM) · **user-mediation UM-1/2/3** as a mechanism (demo fellows egress +
  PRM mutation).
- **C. Countermeasure-library + Harden reframe** — `spec/exceptions.md` + `pna-build-eval-contrib/SKILL.md`.
  Reframe EX-H6 "recommended solution" as a **countermeasure catalog** (each: hazard · strength-class
  [reuse EX-H8 vocab] · *PNA-intrinsic vs environmental* · demonstrator); add the **environmental-threats
  / Harden** sibling; seed the catalog from R3 (sandbox-agent/`denyRead` · MCP per-request grants ·
  separate-OS-user · honeytoken+watchdog · human-presence gating). Add the **Harden** flow to the skill.
  **Delicate / CI-gated** — every new lint check needs a fault-injection self-test (CLAUDE.md).
- **D. exceptions-hardening** — `spec/exceptions.md`: promote the RFC predicate-split (`pna-active`) +
  EX-H7 fail-closed + un-relaxable floor toward normative **where a demonstrator supports it** (fellows
  fail-closed); otherwise keep RFC-tagged.
- **Done-when:** `just ci` green; `VERSION` → `0.2`; README "draft" removed; CHANGELOG + users-guide
  updated in the same PRs. *(The normative surgery (A/C/D) likely wants its own branch + PR, separate
  from the `docs/research-outputs-2026-06-14` branch that holds the Atlas + papers.)*

### Tier 1 — PRM v0.2 *(the reference-design long pole; runs parallel; unblocks gated spec content)*
PRM's next milestones: custom relationship schema · per-field AI-write tiers (append-only / free-write)
· the **data-floor** demonstrator (sealed-by-default disclosure tiers + projection-bound MCP surface) ·
the workspace `EX-CLOUD-LLM` consent gate (EX-H2–H5). Multi-source dedup now consumes the shipped **Atlas**.
- **Unblocks upstream:** the data-floor (AC-MCP-C/PR-7/EX-H9) and the append-only/free-write AC-PRM-E/F
  tiers can land in the spec *once PRM v0.2 demonstrates them* (demonstrator-gated, per CONTRIBUTING).

### Tier 2 — toolkit-goal surfaces + publication *(value-driven; no hard deps)*
- **Harden flow** build-out (the advisement skill + the external-countermeasure catalog).
- **Validation-as-product:** `just validate <path>` (cheap assembly first) → Mode-2 goal-impact reads →
  the behavior-based chooser + voluntary-validation registry; validating comms tools as their own class.
- **Papers → full drafts → publication** (P1: Onward! / local-first; P2: SPLC / Onward! / arXiv). Watch
  the drift guardrail: the validator-as-service must stay a tactic in service of the build mission, not
  become the project's identity.

### Tier 3 — the R4-mission reference design *(unlocks the "why" layer)*
A **mutual-aid / community-care** PNA ([`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md)
item 5) — the R3–R4 mission made concrete. As a new reference design it lets the spec grow toward the
community-mental-health goal and is the natural demonstrator for any R3–R4 ACs. Its "needs help" field is
health/vulnerability-adjacent, so it stress-tests G2/G3 harder than any prior design.

### Tier 4 — vision-park *(future; seams sized, no design yet)*
- **Working the graph** — sociogram / reachability-for-help-seeking / ZK community-detection → a NEW
  protocol + NEW reference design + NEW separate sensitive DB; part of the multi-PNA ecosystem vision.
- **Cross-device replication** over commodity channels (#42); **Tonsky commodity file-sync** as an axis
  pick (reading-gated, next-steps item 6).
- **Multi-PNA ecosystem** (v0.2+ target; contracts already sized for it).

## Inbound-findings registry (updated)

| Finding | Source | Track | Demonstrator | Status |
|---|---|---|---|---|
| Distribution = verifiability spectrum | prm#8 | #64 r1 | PRM | **Tier 0** — formalize (demonstrated) |
| Tiered safe-AI-write (AC-PRM-E/F) | prm | #64 r2 | PRM (review-required) | **Tier 0** for review-required; append-only/free-write **gated on PRM v0.2** |
| User-mediation UM-1/2/3 | fellows#252 | #40 / #64 r3 | fellows (egress) + PRM (mutation) | **Tier 0** — formalize as a mechanism |
| EAR rejected for live store; encrypt-in-transit | fellows#256 | #41 | fellows | **Locked; re-confirmed by R3** — don't revive at-rest EAR; Harden countermeasures instead; in-transit note landed (PR #58) |
| Cross-device over commodity channels | fellows#257 | #42 | fellows (prototype pending) | **Tier 4** (vision-park) |
| Data-floor / disclosure tiers (AC-MCP-C/PR-7/EX-H9) | design note | PR #34 | PRM v0.2 | **gated on PRM v0.2** |
| Countermeasure library + Harden (environmental threats) | 2026-06-14 session + R3 | new | fellows/PRM (intrinsic) + toolkit-advised (external) | **Tier 0** (reframe) → **Tier 2** (Harden flow build-out) |

## Research outputs (2026-06-14)

| # | Project | Output | Status |
|---|---|---|---|
| R1 | Contact Data Format Atlas | [`docs/contact-data-format-atlas.md`](contact-data-format-atlas.md) | **Shipped** (golden corpus = manual follow-up) |
| R2 | Behavioral directed graph | [`docs/papers/paper1-pna-positioning.md`](papers/paper1-pna-positioning.md) | Skeleton drafted |
| R3 | Data-protection vs OS-automation AI | feeds the Harden countermeasure catalog | Done (re-confirms EAR-deprecation) |
| R4 | Application-class-blueprint meta-method | [`docs/papers/paper2-blueprint-method.md`](papers/paper2-blueprint-method.md) | Skeleton drafted |

## Fit with README success criteria

- **Criteria 1, 4, 6** (toolkit proven end-to-end · durable archival · AC-as-identity) — **met** (keystone).
- **Criterion 3** (a contributor submits a design end-to-end) — **met** (PRM).
- **Criterion 5** (the spec evolves ≥1 minor version from a design's findings) — **met at the v0.2 cut** (Tier 0).
- **Criterion 2** (a user audits a candidate → AC-keyed report) — exercised by the evaluate flow, surfaced
  by the Visual Validator, and deepened by the validation-as-product line (Tier 2).

## Deprecations / closed

- **Encryption-at-rest for the live private store — DEPRECATED, re-confirmed by R3 (2026-06-14):**
  dominated by full-disk encryption for the off-device threat, and useless against a live, user-privileged
  agent (which reads the decrypted bytes like any legitimate tool). The agent-boundary threat is handled by
  the **Harden** countermeasures (sandbox the agent / mediate the access path / detect) — all of which
  preserve tool-readability. Crypto's sanctioned home is **encrypt-in-transit** (the portable export).
- Carried over from v0.1: the "lock-my-data" lineage and the per-call cloud-LLM "workspace bridge" remain closed.

## Planning-doc associations

- **Tier 0** → the brainstorm's `## OUTPUT WORK QUEUE`; `spec/PNA_Spec.md`, `spec/exceptions.md`, `spec/axes.md`.
- **Tier 1** → PRM's own `plans/`.
- **Tier 2** → [`plans/visual-validator-plan.md`](../plans/visual-validator-plan.md); the `just validate`
  + chooser design notes; [`docs/papers/`](papers/).
- **Tier 3** → [`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5.
- **Tier 4** → [`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md) (R1–R5);
  next-steps item 6.
