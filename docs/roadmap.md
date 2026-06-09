# PNA Toolkit Roadmap

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> **What this doc owns:** the *prioritization and sequencing* across the toolkit's plans, and
> the **inbound-findings registry** (findings raised in reference designs that the toolkit
> tracks as demonstrator-gated spec-change candidates). It does **not** restate the per-plan
> detail or the normative spec — it links. The *success criteria* live in
> [`README.md` § Status](../README.md#status); per-phase detail lives in the plans linked below.

## Progress snapshot — 2026-06-09

One day past the 2026-06-08 snapshot below; every delta pushes the **same** critical path forward.
Verified against live PRs/issues **plus** the three local checkouts (not just merged-PR claims).

**Headline: the Tier-0 keystone is COMPLETE.** fellows #267 merged → `fellows_local_db` **archived** @
`dc3e0cf` → `[verify].entrypoint = just evaluate-report` → `just ci` green (24/24). (Finalized later on
2026-06-09; the bullets below record what the blocker was and how it closed — see the Tier 0 § for the
done-state.)
- **fellows PR #267** (merged 2026-06-09) added **`just evaluate-report`** — a
  deterministic, stdlib-only emitter that derives a **schema-valid `evaluate-report.json`** from
  `docs/Architecture.md`'s attestation table + git HEAD (no LLM audit; byte-stable on re-run; deploy-gated).
  This **is** the reproducible `[verify].entrypoint` Tier 0 was waiting on. Report posture **conformant**
  (23 conformant / 2 N/A / 0 non-conformant). Merge-ready — blocks on review, not code.
- **Re-pin consequence (new, load-bearing):** the keystone's archival commit is pinned at `bbaf66e`, which
  **predates #267**. Because `[verify].entrypoint = just evaluate-report` must be runnable *at the archived
  commit*, the archival target MUST advance to a **post-#267** commit: merge #267 → Save-Code-Now at the new
  HEAD → re-record SWHIDs → set entrypoint → flip `archived`. (`bbaf66e` already carries the UM attestation
  (#265), so nothing is lost by moving forward.)
- **Drift still open (new):** the toolkit's `reference_designs/fellows_local_db/Architecture.md` copy does
  **not** yet carry fellows' **User-mediation § (UM-1/2/3)** from #265 — it was synced for #248/AC-5/EAR but not
  UM. Fold the UM § into the same post-#267 re-sync. Toolkit `just ci` is **green**.

**fellows — Wave 1 done; UM MVD (Tier 1.5 Step A) DONE; only #267 left on the critical path.**
- #258/#261/#262 + #263/#264/#265 merged; #256/#154/#156 closed; #260 done.
- **UM MVD attestation merged (#265):** UM-1/2/3 green, #259 restore-legibility gap attested as an **honest
  frontier** (not a blocker), workspace-AI **proposer** stance pinned, fellows AI-writes feature **deferred**.
  Tier 1.5 Step A is **complete**, not "upcoming."
- Off-critical-path: telemetry #147 Phase B/C; app-UX issues (#169/#145/#138/#107/#87) — prune/park.

**PRM — M0–M5 + EX-H7 all merged; M6 (attestation) is the only milestone left; unblocked NOW.**
- M2–M5 (#16–#27), EX-H7 (#28), dedup-doc consolidation (#29–#32) all merged. No open PRs; clean tree.
- **M6 has not started**, and **none** of its submission artifacts exist yet (`docs/Architecture.md`,
  `design.toml`, `docs/conformance/evaluate-report.json` — all missing). Est. ~2–3 days. **M6 does NOT depend
  on Tier 0** — it runs fully parallel.
- Two M6 risks surfaced from the checkout: **AC-7 debug-substrate scope** (attest partial/deferred honestly)
  and a **test-suite bootstrap** gap (`vobjectx` missing in the venv — confirm the suite is green before
  attesting). EX-H2–H5 workspace consent stays v0.2 (the server-side EX-H7 handshake is the v0.1 surface).
- **Note:** PRM **end-user testing** of the usable slice (import → add private fields → fill → set permissions)
  is a *separate track* from M6 attestation; the demo can precede the submission.

**Visual Validator — ahead of the roadmap.** Wave 3 expected Phases 1–3; **Phases 1–5 shipped** + the
Playwright e2e suite + the `viewer-e2e` CI job. Only the optional VV **Phase 4 "generate" seam** is unbuilt
(low priority). fellows' real `evaluate-report.json` is already its content.

---

## Progress snapshot — 2026-06-08

Where the three repos stand right now (claimed progress confirmed via merged PRs — implementation
correctness not re-reviewed; no open PRs in any of the three repos as of this snapshot). The detailed
waves below remain the plan; this is the *state*, written for a context reset.

**Toolkit (this repo) — Visual Validator built; Wave-2 keystone partly started.**
- **Visual Validator: Phases 1–5 shipped** (merged to `main`): the render-contract lint + 3 sample
  reports; the static viewer with **developer + end-user registers** and a finding-aligned
  **side-by-side**; the report-set **← / → flip-through** + `just view-reports`; a **13-test
  Playwright suite** and the dedicated **`viewer-e2e` CI job**. Good stopping point.
  **Remaining:** VV **Phase 4** — the thin "generate" seam (not started).
- **CI hygiene:** GitHub Actions bumped off Node 20 (`checkout`/`setup-python` → v6, `cache` → v5)
  ahead of the 2026-06-16 cutoff.
- **Wave 2 keystone (fellows attestation): partly started.** Toolkit PR #54 synced the toolkit's copy
  of fellows `Architecture.md` (AC-5 ref fix + EAR non-goal). **Remaining:** finalize `design.toml`
  (SWHID archival via `just swh-save` — maintainer-run — + `[verify].entrypoint` + flip
  `archival = "archived"`), reconcile the README↔manifest SWHID drift, fold in the #41
  encrypt-in-transit CST note. *The second gate is closing:* fellows now ships a conformance
  report + ship-time gate (fellows #249/#262), which is the `evaluate-report.json` emission the
  `[verify].entrypoint` needs.

**fellows_local_db — Wave 1 COMPLETE; upstream contributions staged.**
- Wave 1 done & merged: data-layer write-guard (#261), EAR decision recorded (#258), test debt + guard
  citations (#262); the lock-my-data lineage pruned. The **workspace user-mediation invariant**
  (fellows #252) is demonstrated **test-first** (#261/#262), and the upstream PNT contributions
  (exceptions / constraints / **user-mediation**) are **staged** (#263) — ready to ride up to toolkit
  #40 as the candidate **3rd general mechanism**.
- **User-mediation reframed (2026-06-08): MVD-primary, demonstrate-now.** The two fellows plans were
  reframed into one **arc** (`plans/pna_toolkit_user_mediation_contribution.md` is now the spine; the
  AI-write-proposals feature is a *deferred* satellite). The decision: demonstrate the invariant **now**
  via fellows' already-green proofs (UM-1 #261/#260, UM-2 `mode=ro` MCP, UM-3 egress export/compose)
  **plus PRM as a built second demonstrator** (its merged propose→review→apply loop covers the
  mutation-diff half on a *second* substrate) — *without* building the fellows AI-writes feature. This
  pulls #40 out of "tracked, not scheduled": the fellows MVD prep runs **now, parallel to the keystone**;
  the PNT spec draft follows the keystone, citing fellows **+** PRM. See **Tier 1.5** below.

**PRM — v0.1 nearly done; only M6 (attestation) left.**
- M2→M5 shipped & merged: read-only workspace, **private store + dedup** (M3), **propose-only MCP +
  workspace apply** (M4, "AI loop closed"), **opt-in non-destructive re-import** (M5).
- **EX-H7 cloud-LLM consent handshake (prm #28, 2026-06-08):** the *server-side half* of `EX-CLOUD-LLM`
  now ships on both MCP servers via the MCP `instructions` handshake (honest signaling, not a gate) —
  a v0.1 surface obligation closed, making **PRM a second EX-H7 demonstrator** (parity with fellows).
  The full enforced handler (workspace consent gate, EX-H2–H5) stays v0.2. *(As of this snapshot #28 is
  ready/awaiting its manual-QA merge.)*
  **Remaining: M6 — the AC attestation table**, which makes PRM **submittable as the 2nd reference
  design**. M6 now rides an **expanded rider set** (see Tier 1): core attestation + distribution-axis
  split (prm#8 / toolkit#39) + **user-mediation boundary list** (Tier 1.5 Step B, mutation side) + EX-H7
  (prm#28) + AC-PRM-E/F.

**Next phase (after the context reset):** (1) **toolkit** — finalize the Wave-2 keystone now that
fellows emits a conformance report, then VV Phase 4; (2) **fellows (parallel, off critical path)** —
the user-mediation **MVD prep** (Tier 1.5 Step A): frame the green UM-1/2/3 tests, boundary audit
(attest the #259 restore gap, don't block on it), attest in `docs/Architecture.md`; (3) **PRM** — M6
attestation → submit as the 2nd reference design, carrying a user-mediation boundary list (Tier 1.5
Step B); (4) **fellows → toolkit** — draft the user-mediation spec mechanism (#40), test-first, after
the keystone, citing fellows **+** PRM (Tier 1.5 Step C). (Also tracked, lower priority: VV's `?dir=`
registry idea, and reconciling SKILL ↔ report-schema EX-*/CST- keying.)

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
[T0] Finalize fellows keystone  ✓ DONE 2026-06-09 (fellows #267 merged → archived @ dc3e0cf → [verify].entrypoint=`just evaluate-report` + Architecture.md re-synced incl UM § + flipped archived; the #41 CST note remains as an off-path toolkit note)
        ├──► conformance-suite Phase 4 activates (first archived design + verify entrypoint)
        ├──► README success criteria 1 / 3 / 4 / 6 satisfied (toolkit proven end-to-end)
        └──► evaluate flow runs on fellows ──► a REAL evaluate-report.json
                                                   └──► Visual Validator has real content (not synthetic samples)

[T1] PRM (M2–M5 MERGED; EX-H7 handshake prm#28; only M6 attestation left) ──► full attestation at its M6 ──► 2nd reference design (drops "draft"; criteria 3 & 5)
        ├──► demonstrator for the distribution-axis split (#39 ⇄ prm#8)
        ├──► carries a user-mediation boundary list (mutation side) ──► [T1.5] Step B
        ├──► 2nd EX-H7 demonstrator (prm#28 server-side handshake) + AC-PRM-E/F safe-AI-write demonstrator
        ├──► unblocks AC-PRM-* validation + community-care use case (next-steps item 5)
        └──► pulls in multi-source ingestion ──► Contact Data Format Atlas (Phase 1)

[T1.5] User-mediation = 3rd general mechanism (MVD-primary, demonstrate-now)   [parallelizes with T0/T1]
        A) fellows MVD prep — DONE (#265 merged 2026-06-08): UM-1/2/3 green + #259 gap attested as honest frontier + workspace-AI proposer stance pinned
        B) PRM M6 carries the mutation-side boundary list ──► two designs, two substrates
        C) PNT spec draft (after T0 frees the toolkit instance; test-first; cites fellows + PRM) ──► toolkit #40 ──► criterion 5 (spec evolves ≥1 minor) reinforced
        └──► builds on merged Exceptions + Constraints (done); files only on maintainer go-ahead

[T3] remaining findings mature in their demonstrators (fellows test-first) ──► ride up to the toolkit later
```

## Cross-repo execution order (open issues & PRs)

The toolkit is now the **orchestrator** for its reference designs, so the work that moves the
milestones lives across three repos (fellows_local_db, prm, the toolkit). This is the suggested
order to clear the open issues/PRs that matter — **dependency-first**. Items not listed here are
low-utility (ideas / stale bugs / app-UX) and are classified in the snapshot below; prune them,
don't schedule them. Each wave names its **owning Claude Code instance** (one per repo — so you can
dispatch "do Wave N" to the right one); each step notes the Tier it serves.

### Wave 1 — Land the ready fellows work; prune the deprecated lineage · **owner: fellows instance** *(unblocks an honest keystone)*
The fellows attestation is about to change (an EAR non-goal note + new data-layer guards). Land
those **before** archiving the keystone (Wave 2), or you archive a commit that is immediately stale.
1. Merge **fellows PR #258** (record the EAR decision) → the deprecation is official **[T3/EAR]**.
2. Close **fellows #256** (decision half done by #258) and **fellows #154** (auto-lock — *moot*: there is no live-store lock anymore). Prune the lock-my-data lineage.
3. Merge **fellows PR #261** (data-layer write-guard) → lands property 1 (no-bypass) of the user-mediation invariant **and** fixes a real off-folder private-store leak **[T3/#40]**.
4. **fellows #260** (fix the off-folder red tests + cite the new guards in `docs/Architecture.md`) → makes the fellows attestation honest & current.
5. Close **fellows #156** as done (the AC-MCP-A consent gate shipped in fellows PR #226; only "file upstream" remains — a toolkit action, not dev work).

### Wave 2 — Finalize the keystone · **owner: toolkit instance** *(T0 — proves the toolkit end-to-end)*
Now that fellows's attestation reflects Wave 1:
6. Re-sync `reference_designs/fellows_local_db/Architecture.md` to the post-Wave-1 state (guard citations + EAR non-goal note); run the evaluate flow → a **real `evaluate-report.json`**.
7. Finalize `design.toml`: archival via `just swh-save`, fill `commit`/`swhid_*`/`[verify].entrypoint`, flip `archival = "archived"`; reconcile the README↔manifest SWHID drift. *(Second gate: the `[verify].entrypoint` must emit a schema-shaped `evaluate-report.json`, which fellows does not yet — that's fellows's own `conformance_report_and_gate.md`. Until it ships, either keep `archival = "pending"` or point the entrypoint at `just conformance` as an interim and flip to archived later.)*
8. Fold the **toolkit #41** encrypt-in-transit CST frontier note into the same re-sync (a non-normative line on `CST-PWA-NO-SYNC` / `-PRIVATE-SNAPSHOT`; confirms the PR-#19 scope decline — *no new AC*). → Conformance-suite Phase 4 is now activatable; README criteria 1/3/4/6 met.

### Wave 3 — Value surface fed by the keystone · **owner: toolkit instance** *(T2 — parallelizable)*
9. **✓ toolkit PR #38 (Visual Validator plan) merged (2026-06-07);** build its Phases 1–3 — fed by the **real** fellows report from Wave 2 (samples stop being synthetic). Targeted for the week of Jun 15–19, alongside testing non-reference (third-party) apps through the evaluate flow.

### Wave 4 — PRM toward the 2nd reference design · **owner: prm instance** *(T1 — the long pole; runs parallel to Waves 2–3)*
10. **✓ Done (2026-06-07):** **prm #16** (M2 read-only workspace + justfile) merged — basic functionality verified under manual test (not yet user-test-ready).
11. **Break the distribution circular dep:** write up the **verifiability spectrum** (toolkit #39 / prm #8) *decoupled from the installer*, so the spec change is ready to land with PRM's contribution. (Today the installer is deferred pending the distribution decision, and the distribution decision was deferred pending the installer — writing the spectrum first cuts the loop.)
12. **PRM v0.2 (in flight):** custom relationship schema (~1 day) + per-field **AI-write tiers** (this week) → the first usable slice — *import → add private fields → fill values → set permissions* — targeted for user testing the week of Jun 15. Multi-source dedup pulls in the Contact Data Atlas (Phase 1). PRM's **reference-design attestation** (its M6 — `Architecture.md` + `design.toml` + AC attestation + archival) is the actual Tier-1 milestone: at attestation the distribution-axis split graduates (#39) and README criteria **3 & 5** are met, dropping the "draft" label. (PRM's own `plans/v0.1-implementation-plan.md` holds its M-chain detail.)

> **PRM timing.** M2 (read-only) is **merged**; **v0.2** (custom schema + AI-write tiers) is in flight,
> aimed at a usable demo slice for mid/late-June user testing (see the indicative timeline below). Full
> *reference-design attestation* is PRM's **M6** and follows the demo; a minimal attestation of an earlier
> flavor remains a possible bridge if Tier 1 is wanted sooner.

### Wave 4.5 — User-mediation, MVD-primary · **owner: fellows (Step A/B) → toolkit (Step C)** *(T1.5 — promoted out of Wave 5; parallelizes with Waves 2–4)*
> Reframed 2026-06-08 (the arc spine is fellows `plans/pna_toolkit_user_mediation_contribution.md`).
> The invariant no longer waits on a feature build: it is demonstrated **now** via fellows' green proofs
> + PRM's built propose→apply loop. The fellows AI-write-proposals feature is **deferred** (a richer
> 3rd boundary, not a prerequisite).
13a. **Step A — fellows MVD prep (now; parallel to the Wave-2 keystone; off the critical path):** frame the green UM-1 (#261/#260) / UM-2 (`mode=ro` MCP) / UM-3-egress (export/compose) tests under the invariant; boundary audit — **honestly attest the private-data restore legibility gap, frontier = #259, do NOT block on it**; pin the workspace-AI stance; attest in fellows `docs/Architecture.md` § User-mediation.
13b. **Step B — PRM M6 carries the mutation-side boundary list** (Wave 4) → two designs, two substrates demonstrate the invariant.
13c. **Step C — toolkit #40 spec draft** (after the Wave-2 keystone frees the toolkit instance): test-first, building on PR #18's as-built; `spec/user_mediation.md` (or a `PNA_Spec.md` section) + `UM-*`/`Mediates:`/`Proposer:`/`Dispose:` lint + SKILL steps; cites fellows **+** PRM; **Minor** bump; files only on maintainer go-ahead.

### Wave 5 — Exploration rides up as demonstrators mature · **owner: fellows → toolkit** *(T4)*
14. **fellows #257 / toolkit #42** cross-device replication (exploratory) — gated on the #259 decision + local-AI; the relocated EAR crypto envelope (encrypt-in-transit) lands here. (Note: **#259** — off-folder durability model / ephemeral-viewer tier — is now *also* the user-mediation restore frontier, attested by Wave 4.5 Step A rather than blocking it.)

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
- **Wave 4.5 (user-mediation)** → the user-mediation invariant becomes a new spec doc, demonstrated by fellows (MVD) + PRM; arc spine = fellows `plans/pna_toolkit_user_mediation_contribution.md`.
- **Wave 5 (exploration)** → [`pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5 (community-care) lands if PRM hosts it; items 2 / 6 stay parked; cross-device (#42) is gated on #259 + local-AI.

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
- **Status:** **DONE (2026-06-09).** fellows **PR #267 merged** (the deterministic `just evaluate-report`
  emitter); the maintainer ran Save-Code-Now at the post-#267 HEAD **`dc3e0cf`** (request `2352911`). The
  toolkit keystone was then finalized: `reference_designs/fellows_local_db/Architecture.md` **re-synced** to
  `dc3e0cf` (now carries the User-mediation § UM-1/2/3 + the encrypt-in-transit note + updated `CST-PWA-*`
  rows); `design.toml` re-pinned (`commit`/`swhid_rev`/`swhid_dir` → `dc3e0cf`),
  **`[verify].entrypoint = "just evaluate-report"`**, **`archival = "archived"`**; README SWHIDs reconciled;
  the two `lint_selftest.py` fault anchors moved with the manifest. **`just ci` green (24/24)**; authoritative
  `attestation-evidence-lint` against the fellows checkout green (every `conformant` row cites live evidence).
  **Conformance-suite Phase 4 is now activatable; README criteria 1/4/6 met** and the precondition for **3** is
  in place. *Remaining (off the critical path — not archival blockers):* (1) the toolkit-side **#41**
  encrypt-in-transit CST frontier note in `spec/constraints.md` (non-normative; the Architecture.md copy
  already carries the design-side note); (2) confirm SH ingest completed — tracked in toolkit **#56**
  (async; the SWHIDs are git-verified regardless); (3) VV `/audit`-style entry UX → toolkit **#55**.
- **Unblocks:** conformance-suite Phase 4 ([`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md));
  README criteria 1/3/4/6; the real `evaluate-report.json` is now the Visual Validator's content.

### Tier 1 — PRM as the second reference design + the spec change it carries
- **What:** take **PRM** ([richbodo/prm](https://github.com/richbodo/prm)) through the contribute
  flow ([`plans/reorganization-plan.md`](../plans/reorganization-plan.md) Phase 7) — Architecture doc +
  `design.toml` + AC attestation + archival. Graduate the **distribution-axis verifiability split**
  (#39 ⇄ prm#8) to a spec change in [`spec/axes.md`](../spec/axes.md), with PRM as the demonstrator
  (it is the build-from-verifiable-source case).
- **M6 rides an expanded rider set** (all attest together in PRM's one M6 pass):
  1. **Core reference-design attestation** → 2nd reference design (criteria 3 & 5).
  2. **Distribution-axis verifiability split** (prm#8 ⇄ toolkit#39) → `spec/axes.md` change.
  3. **User-mediation boundary list** (Tier 1.5 Step B) — PRM's M4a/M4b propose→review→apply loop is the
     **mutation-side** UM-1/2/3 demonstration the fellows MVD lacks. *(Verify the M4b apply UI renders a
     deterministic, human-readable, escaped diff before dispose — UM-3 — when attesting; don't assume it.)*
  4. **EX-H7** (prm#28 server-side cloud-LLM consent handshake) → PRM as a 2nd EX-H7 demonstrator.
  5. **AC-PRM-E/F** (the proposed tiered safe-AI-write model) → PRM as the demonstrator, provisional until
     accepted upstream.
- **Why:** drops the toolkit's **"draft"** label; validates README criteria **3** (a contributor
  submits end-to-end) and **5** (the spec evolves ≥1 minor version from a contributed design's
  findings); second dogfood of the contribute flow. R2–R3 value (PRM is the relationship-memory app).
- **Status:** **M0–M5 merged; only M6 left.** The M-chain is done (M3 private store + dedup, M4 MCP
  propose + workspace apply, M5 re-import all merged), and prm#28 closes the v0.1 EX-H7 cloud-LLM surface
  (awaiting its manual-QA merge). M6 (attestation + full test pass + conformance review + the deferred
  AC-7 debug substrate) is the remaining milestone — **much closer than the earlier "weeks" estimate**.
  Runs parallel to Tiers 0/1.5/2.
- **Unblocks:** AC-PRM-* validation; the **community-care / mutual-aid use case**
  ([`plans/pnt-next-steps-plan.md`](../plans/pnt-next-steps-plan.md) item 5) if PRM hosts it; multi-source
  ingestion → the Atlas (Tier 2).

### Tier 1.5 — User-mediation as the 3rd general mechanism *(MVD-primary; promoted from Tier 3 on 2026-06-08; parallelizes with Tiers 0/1)*
- **What:** name the **user-mediation invariant** ("the human is the actuator; the workspace is the locus
  of ground truth") as the third general PNT mechanism, dual to Exceptions and Constraints — `UM-1` no-bypass /
  `UM-2` separation / `UM-3` legibility, with the honest **bounded claim** (separation + legibility +
  attribution, *not* comprehension). Spec mechanism (`spec/user_mediation.md` or a `PNA_Spec.md` section) +
  `lint-spec-ids.py` `UM-*`/`Mediates:`/`Proposer:`/`Dispose:` machinery + SKILL build+evaluate steps, built
  on PR #18's as-built. Arc spine: fellows `plans/pna_toolkit_user_mediation_contribution.md`.
- **Why now (the reframe):** the reference designs caught up to the finding. fellows already has the
  evidence green (UM-1 #261/#260, UM-2 `mode=ro` MCP, UM-3-egress export/compose) and **PRM already ships
  the mutation-side propose→review→apply loop** on a second substrate (M2–M5 merged). So the invariant can
  ride up as a **two-design, two-substrate** demonstration — stronger than Exceptions or Constraints had —
  **without building the fellows AI-writes feature** (deferred). This is the unusual case where the
  near-certain, compounding artifact (a third dual mechanism, completing the trio) is also cheap.
- **Sequence (test-first):** **A)** fellows MVD prep — *now, parallel to the Tier-0 keystone, off the
  critical path*; **B)** PRM carries a user-mediation boundary list at its M6; **C)** toolkit #40 spec draft
  *after* the keystone frees the toolkit instance, written to match what A/B proved, citing fellows + PRM;
  **Minor** bump; files only on maintainer go-ahead. **D)** the fellows AI-writes feature is an optional
  later richer demonstrator.
- **Status:** **MVD-ready.** Step A is unblocked and parallel-safe today; the one open issue it touches —
  **fellows #259** (off-folder durability / Restore-affordance) — is handled by *honest attestation of the
  restore legibility gap*, not by completion. No hard dependency on Tiers 0/1/2.
- **Unblocks:** completes the matched trio (user-raised / platform-imposed / actuation-boundary); reinforces
  README criterion **5** (the spec evolves ≥1 minor version from a contributed design's findings).

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
- **#40** (fellows#252) — workspace user-mediation invariant → **3rd general mechanism. PROMOTED to Tier 1.5 (scheduled) on 2026-06-08** — MVD-primary, demonstrate-now (fellows MVD + PRM 2nd demonstrator); #261 merged (UM-1 proven). No longer "tracked, not scheduled."
- **#41** (fellows#256) — EAR rejected for the live store; light CST frontier note (encrypt-in-transit). *Decision recorded: fellows PR #258; toolkit note pending (toolkit-fix PR).*
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
| Workspace user-mediation invariant ("human is the actuator; workspace is ground truth") | fellows#252 | **#40** | **fellows_local_db + PRM** (two substrates) | fellows MVD (UM-1/2/3 green) + PRM mutation-side at M6 — test-first | new mechanism doc, sibling to `exceptions.md`/`constraints.md` | **MVD-ready → Tier 1.5 (scheduled).** UM-1 proven (#261 merged); demonstrate-now decided 2026-06-08, fellows AI-writes feature deferred |
| EAR rejected for live store; encrypt the portable export instead | fellows#256 | **#41** | fellows_local_db | decision recorded | non-normative frontier note on `CST-PWA-NO-SYNC` / `-PRIVATE-SNAPSHOT` | **Decision locked** (fellows PR #258); toolkit note pending (folds in via a toolkit-fix PR; no AC) |
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
and **5**. Tier 1.5 (user-mediation) **reinforces criterion 5** — a third minor-version spec evolution
driven by reference-design findings, demonstrated across two designs/substrates. Criterion **2** (a user
audits a candidate and gets an AC-keyed report) is exercised by the evaluate flow throughout and surfaced
visually by the Tier-2 Visual Validator.
