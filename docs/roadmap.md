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

[T1] PRM (M2 read-only MERGED 06-07; v0.2 custom-schema + AI-write tiers in flight) ──► full attestation at its M6 ──► 2nd reference design (drops "draft"; criteria 3 & 5)
        ├──► demonstrator for the distribution-axis split (#39 ⇄ prm#8)
        ├──► unblocks AC-PRM-* validation + community-care use case (next-steps item 5)
        └──► pulls in multi-source ingestion ──► Contact Data Format Atlas (Phase 1)

[T3] findings mature in their demonstrators (fellows test-first) ──► ride up to the toolkit later
```

## Cross-repo execution order (open issues & PRs)

The toolkit is now the **orchestrator** for its reference designs, so the work that moves the
milestones lives across three repos (fellows_local_db, prm, the toolkit). This is the suggested
order to clear the open issues/PRs that matter — **dependency-first**. Items not listed here are
low-utility (ideas / stale bugs / app-UX) and are classified in the snapshot below; prune them,
don't schedule them. Each step notes the Tier it serves.

### Wave 1 — Land the ready fellows work; prune the deprecated lineage *(unblocks an honest keystone)*
The fellows attestation is about to change (an EAR non-goal note + new data-layer guards). Land
those **before** archiving the keystone (Wave 2), or you archive a commit that is immediately stale.
1. Merge **fellows PR #258** (record the EAR decision) → the deprecation is official **[T3/EAR]**.
2. Close **fellows #256** (decision half done by #258) and **fellows #154** (auto-lock — *moot*: there is no live-store lock anymore). Prune the lock-my-data lineage.
3. Merge **fellows PR #261** (data-layer write-guard) → lands property 1 (no-bypass) of the user-mediation invariant **and** fixes a real off-folder private-store leak **[T3/#40]**.
4. **fellows #260** (fix the off-folder red tests + cite the new guards in `docs/Architecture.md`) → makes the fellows attestation honest & current.
5. Close **fellows #156** as done (the AC-MCP-A consent gate shipped in fellows PR #226; only "file upstream" remains — a toolkit action, not dev work).

### Wave 2 — Finalize the keystone *(T0 — proves the toolkit end-to-end)*
Now that fellows's attestation reflects Wave 1:
6. Re-sync `reference_designs/fellows_local_db/Architecture.md` to the post-Wave-1 state (guard citations + EAR non-goal note); run the evaluate flow → a **real `evaluate-report.json`**.
7. Finalize `design.toml`: archival via `just swh-save`, fill `commit`/`swhid_*`/`[verify].entrypoint`, flip `archival = "archived"`; reconcile the README↔manifest SWHID drift.
8. Fold the **toolkit #41** encrypt-in-transit CST frontier note into the same re-sync (a non-normative line on `CST-PWA-NO-SYNC` / `-PRIVATE-SNAPSHOT`; confirms the PR-#19 scope decline — *no new AC*). → Conformance-suite Phase 4 is now activatable; README criteria 1/3/4/6 met.

### Wave 3 — Value surface fed by the keystone *(T2 — parallelizable)*
9. **✓ toolkit PR #38 (Visual Validator plan) merged (2026-06-07);** build its Phases 1–3 — fed by the **real** fellows report from Wave 2 (samples stop being synthetic). Targeted for the week of Jun 15–19, alongside testing non-reference (third-party) apps through the evaluate flow.

### Wave 4 — PRM toward the 2nd reference design *(T1 — the long pole; runs parallel to Waves 2–3)*
10. **✓ Done (2026-06-07):** **prm #16** (M2 read-only workspace + justfile) merged — basic functionality verified under manual test (not yet user-test-ready).
11. **Break the distribution circular dep:** write up the **verifiability spectrum** (toolkit #39 / prm #8) *decoupled from the installer*, so the spec change is ready to land with PRM's contribution. (Today the installer is deferred pending the distribution decision, and the distribution decision was deferred pending the installer — writing the spectrum first cuts the loop.)
12. **PRM v0.2 (in flight):** custom relationship schema (~1 day) + per-field **AI-write tiers** (this week) → the first usable slice — *import → add private fields → fill values → set permissions* — targeted for user testing the week of Jun 15. Multi-source dedup pulls in the Contact Data Atlas (Phase 1). PRM's **reference-design attestation** (its M6 — `Architecture.md` + `design.toml` + AC attestation + archival) is the actual Tier-1 milestone: at attestation the distribution-axis split graduates (#39) and README criteria **3 & 5** are met, dropping the "draft" label. (PRM's own `plans/v0.1-implementation-plan.md` holds its M-chain detail.)

> **PRM timing.** M2 (read-only) is **merged**; **v0.2** (custom schema + AI-write tiers) is in flight,
> aimed at a usable demo slice for mid/late-June user testing (see the indicative timeline below). Full
> *reference-design attestation* is PRM's **M6** and follows the demo; a minimal attestation of an earlier
> flavor remains a possible bridge if Tier 1 is wanted sooner.

### Wave 5 — Mechanisms & exploration ride up as demonstrators mature *(T3/T4)*
13. fellows #252 properties 2–3 (separation, legibility) + **fellows #259** (off-folder durability-model decision; feeds an ephemeral-viewer tier) → complete the invariant demonstration → ride up to **toolkit #40** as the **3rd general mechanism** (a doc sibling to `exceptions.md` / `constraints.md`).
14. **fellows #257 / toolkit #42** cross-device replication (exploratory) — gated on the #259 decision + local-AI; the relocated EAR crypto envelope (encrypt-in-transit) lands here.

### Indicative timeline (maintainer's working projection, June 2026)

Dates are the maintainer's current estimate, **not** a re-ordering — the Waves above still govern what
unblocks what. AI-coding pace has been running ahead of conservative estimates here, and the high-level
design questions have largely settled, so treat these as realistic, not aspirational.

- **This week (→ Fri):** PRM **v0.2** — custom relationship schema (~1 day) + per-field **AI-write tiers**
  (rest of the week), in parallel with the Wave-1 fellows cleanup.
- **Week of Jun 15–19:** build the **Visual Validator** (Wave 3) + start **testing non-reference
  (third-party) apps** through the evaluate flow; **PRM user testing** of the first usable slice —
  *import contact data → add private fields → fill them with values → set their permissions.*
- **By end of June:** Visual Validator **and** PRM in **demo-shape**.

**Demo-shape ≠ full attestation:** end-of-June targets a compelling, usable demo; PRM's *reference-design
attestation* (its M6, the Tier-1 / criteria-3 & 5 milestone) follows.

### Open-work snapshot — utility & classification

High-utility (roadmap-bearing) items are in the waves above. Everything open, classified:

| Item | Repo | Utility | Class | Roadmap tie |
|---|---|---|---|---|
| PR #258 — record EAR decision | fellows | **H** | decision | T3 / EAR deprecation |
| PR #261 — data-layer write-guard | fellows | **H** | dependency | T3 / #40 (proof 1) |
| #252 — user-mediation invariant | fellows | **H** | dependency | T3 / #40 |
| #256 — EAR decision | fellows | **H** | decision | closeable after #258 |
| #260 — test debt + attestation cites | fellows | **M** | bug / dependency | T0-adjacent / #40 |
| #259 — off-folder durability model | fellows | **M** | decision | T4 / ephemeral viewer |
| #257 — cross-device replication | fellows | **M** | exploration | T4 / #42 |
| #156 — cloud-LLM consent (AC-MCP-A) | fellows | done | decision | close as done |
| #154 — auto-lock on close | fellows | **moot** | idea | close (EAR deprecated) |
| #169 — search degradation | fellows | **L** | bug (stale) | none — re-triage |
| #147 retention docs · #145 group UX · #138 filters · #107 console noise · #87 tags/notes | fellows | **L** | app-UX / docs | none — parked/prune |
| #16 — M2 read-only workspace | prm | **H** | dependency | **merged 2026-06-07** (T1) |
| #8 — distribution spectrum | prm | **H** | decision | T1 / #39 |
| #39 — distribution split | toolkit | **H** | dependency | T1 |
| #40 user-mediation · #41 EAR · #42 cross-device | toolkit | H / H / M | inbound-finding | T3 |
| PR #38 Visual Validator plan · PR #43 this roadmap | toolkit | M | docs / plan | both **merged 2026-06-07** |

### Deprecations & closed initiatives

What's being *shut down*, so it stops pulling on the roadmap:

- **Encryption-at-rest for the live private store — DEPRECATED** (the original "lock my data" requirement). Decided in **fellows #256**, recorded by **fellows PR #258**: app-EAR for the live store is *dominated* by device full-disk encryption and *contradicts* `CST-PWA-SANDBOX-SEALED` tool-readability. Lineage retired: the `feat/lock-my-data` branch (closed **fellows PR #155**, tip `eb66109`) and **fellows #154** (auto-lock → *moot*). **Toolkit effect:** removes EAR as a candidate universal AC *permanently* (confirms the PR-#19 scope decline) — toolkit-side is only a non-normative CST frontier note, **not an AC**.
- **…but the crypto is *relocated, not deleted*.** The harvested envelope (PBKDF2 / AES-GCM) moves from at-rest to **encrypt-in-transit** — the encrypted portable export (**fellows #257 / toolkit #42**). That is a *successor* initiative under T4, not part of the deprecation.
- **Per-call cloud-LLM "workspace bridge" — DECLINED** (fellows #156), replaced by the one-time install-time `EX-CLOUD-LLM` gate. The bridge sub-idea is dead; #156 is otherwise shipped.
- **PRM installer — DEFERRED** (not deprecated), gated on the distribution-axis decision (the circular dep Wave 4 step 11 breaks).
- **PRM responder / outbound-AI app — SPLIT OUT** as a separate future reference design (PRM v0.1–v0.4 builds only the querier half).

### Planning-doc associations

Which in-progress plan each wave advances:

- **Wave 2 (keystone)** → [`reorganization-plan.md`](../plans/reorganization-plan.md) Phase 5 + [`conformance-suite-plan.md`](../plans/conformance-suite-plan.md) Phase 4.
- **Wave 3 (Visual Validator)** → [`visual-validator-plan.md`](../plans/visual-validator-plan.md) (toolkit PR #38).
- **Wave 4 (PRM)** → `reorganization-plan.md` Phase 7 + PRM's own `plans/v0.1-implementation-plan.md` (M0–M6) and `docs/roadmap.md` (v0.1–v0.5); [`contact-data-formats-research-plan.md`](../plans/contact-data-formats-research-plan.md) Phase 1 feeds PRM M3.
- **Wave 5 (mechanisms / exploration)** → the user-mediation invariant becomes a new spec doc; [`pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5 (community-care) lands if PRM hosts it; items 2 / 6 stay parked.

## Priority tiers

### Tier 0 — Keystone: finalize the fellows attestation *(do first; cheap; unblocks the most)*
- **What:** finish [`plans/reorganization-plan.md`](../plans/reorganization-plan.md) Phase 5. Run
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
- **Unblocks:** conformance-suite Phase 4 ([`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md));
  README criteria 1/3/4/6; a real `evaluate-report.json` that becomes the Visual Validator's content.

### Tier 1 — PRM as the second reference design + the spec change it carries
- **What:** take **PRM** ([richbodo/prm](https://github.com/richbodo/prm)) through the contribute
  flow ([`plans/reorganization-plan.md`](../plans/reorganization-plan.md) Phase 7) — Architecture doc +
  `design.toml` + AC attestation + archival. Graduate the **distribution-axis verifiability split**
  (#39 ⇄ prm#8) to a spec change in [`spec/axes.md`](../spec/axes.md), with PRM as the demonstrator
  (it is the build-from-verifiable-source case).
- **Why:** drops the toolkit's **"draft"** label; validates README criteria **3** (a contributor
  submits end-to-end) and **5** (the spec evolves ≥1 minor version from a contributed design's
  findings); second dogfood of the contribute flow. R2–R3 value (PRM is the relationship-memory app).
- **Status:** PRM is days from a *usable read-only* milestone (prm#16 / M2), but its own plan puts
  **full reference-design attestation at M6** (M3 private store → M4 MCP → M5 re-import still ahead) —
  so this is **weeks**, not days. A minimal attestation of PRM's current flavor is a possible bridge
  (see the cross-repo execution order above, Wave 4). Runs parallel to Tiers 0/2.
- **Unblocks:** AC-PRM-* validation; the **community-care / mutual-aid use case**
  ([`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5) if PRM hosts it; multi-source
  ingestion → the Atlas (Tier 2).

### Tier 2 — Toolkit surfaces riding on the now-proven flows *(value-driven, no deadline)*
- **Visual Validator** (Phases 1–3) — [`plans/visual-validator-plan.md`](../plans/visual-validator-plan.md).
  Renders the real fellows/PRM `evaluate-report.json` from Tiers 0–1; the **toggle + side-by-side
  educational view** is the payoff. Artifact/recruiting value; no longer deadline-gated.
- **Contact Data Format Atlas** (Phase 1: Google + Apple) —
  [`plans/contact-data-formats-research-plan.md`](../plans/contact-data-formats-research-plan.md). Feeds PRM's
  multi-source ingestion (AC-PRM-B). Start when PRM needs multi-source.

### Tier 3 — Inbound findings maturing in their demonstrators *(tracked, not scheduled)*
See the registry below. fellows writes the demonstrating work **test-first**; each finding rides up
to the toolkit at the next fellows re-sync, per the `CONTRIBUTING.md` reference-driven rule.
- **#40** (fellows#252) — workspace user-mediation invariant → candidate **3rd general mechanism**. *Demonstrator in progress: fellows PR #261.*
- **#41** (fellows#256) — EAR rejected for the live store; light CST frontier note (encrypt-in-transit). *Decision recorded: fellows PR #258.*
- **#42** (fellows#257) — cross-device over commodity channels; exploratory; 4 candidates.

### Tier 4 — Parked / later
- Conformance **living-suite roadmap R1–R4** ([`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md)) — activates after Tier 0.
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
| Distribution = verifiability spectrum (not binary); + code-only vs. code+data | prm#8 | **#39** | PRM | lands with PRM's M6 attestation (weeks); break the installer↔decision circular dep by writing the spectrum first | `spec/axes.md` Distribution split + new dimension | Write-up pending → Tier 1 (Wave 4) |
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
