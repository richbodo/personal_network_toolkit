# Plan — the L1/L2 layering pass (prerequisite to the v0.2 cut)

> **Goal:** make the spec's three-layer separation *crystal clear and self-consistent* — Goals (L0),
> architectural commitments (L1, technology-independent), and realizations + constraints (L2, the
> mechanical layer) — before the [v0.2 cut](v0.2-spec-cut-plan.md). The normative model is **owned by**
> [`spec/PNA_Spec.md` § How the pieces fit together](../spec/PNA_Spec.md#how-the-pieces-fit-together);
> this plan owns the *execution sequence* and the *AC audit*. **Versioning class: Minor** (additive
> structure + an additive verifiability AC), per [`CONTRIBUTING.md` § Versioning](../CONTRIBUTING.md).

## Why this gates the cut

The v0.2 riders (distribution-verifiability split, safe-AI-write, user-mediation) were hard to *place*
because the layer boundary underneath them is blurred — a fundamental architectural commitment
(*source-availability / verifiability*) was trapped inside a technology-enumeration axis
(`distribution`), and "flavor-derived ACs" silently mix **conditional L1 commitments** with **L2
realizations**. Stamping `0.2` onto that structure would bake the blur in. So: **pause the cut, factor
the layers, then resume.**

## The model (owned by the spec)

The three layers, the **survive-a-total-technology-swap** test, and the **three rules** live in
[`PNA_Spec.md` § How the pieces fit together](../spec/PNA_Spec.md#how-the-pieces-fit-together). In brief,
the three rules:

1. **The `AC-*` namespace is Layer 1 only** — every AC survives the swap test.
2. **Conditional ACs are Layer 1, but tagged** with the *behavioral property* that triggers them.
3. **A realization is never an AC** — it is Layer 2, carries no `AC-*` ID, and lives with the axis pick
   that brings it. Conditional ACs trigger on *behavioral properties*; a tech pick may *entail* a
   property but itself brings only realizations and constraints.

Vocabulary: **conditional AC** (replaces "flavor-derived AC"), **realization** (the L2 term), and
**Realizations and constraints (the mechanical layer)** as the L2 name.

## The worms (one at a time; 1→3 are a connected unit so the spec never ships self-contradictory)

- **Worm 1 — framing (DONE on this branch).** `README.md` + `PNA_Spec.md`: preamble three-layer
  paragraph; promoted top-level **§ How the pieces fit together** (layers + swap test + three rules +
  cardinalities); Vocabulary terms (conditional AC, realization); universal-AC-section intro reworded;
  relocated an orphaned diagnostic blockquote into Goal 2. *No AC content moved yet — a transitional
  note in the new section names the realizations still carrying `AC-*` IDs.*
- **Worm 2 — the AC audit (THIS PLAN, below).** Run every AC through the swap test; classify
  universal-L1 / conditional-L1 / realization-to-demote. **Awaiting maintainer confirmation on the
  borderline rows before worm 3.**
- **Worm 3 — demote realizations + retag conditionals.** Move the realizations out of the `AC-*`
  namespace into L2 realization form beside their axis pick in `axes.md`; tag conditional ACs with their
  behavioral trigger; update `tools/lint-spec-ids.py` + `tools/tests/lint_selftest.py`, both
  reference-design bundled attestations, and the realization index. Remove the transitional note.
  *Merge worms 1–3 together.*
- **Worm 4 — the verifiability AC (the B1 reframe).** Add the universal source-availability /
  verifiability commitment; demote the `distribution` axis to honest packaging (server / no-server,
  PWA / native / CLI, app-store / sideload). Demonstrators: PRM (build-from-source) + fellows
  (source-available bundle). Supersedes the old "split the distribution pick" framing of
  [#39](https://github.com/richbodo/personal_network_toolkit/issues/39)/[#64](https://github.com/richbodo/personal_network_toolkit/issues/64) rider 1.
- **Worm 5 — sub-contracts.** Relocate / clearly mark the `WS-*`/`ST-*`/… slot map as L2 realizations
  (largely fellows-derived; e.g. `WS-7` names a literal localStorage key).
- **Then:** the riders land clean (UM is already pure L1 — [#40](https://github.com/richbodo/personal_network_toolkit/issues/40)/[#64](https://github.com/richbodo/personal_network_toolkit/issues/64) rider 3;
  AC-PRM-E/F stays deferred to PRM v0.2 — see the recomposition finding), then the
  [v0.2 cut](v0.2-spec-cut-plan.md) proceeds onto a structure worth stamping.

---

## Worm 2 — the AC audit (provisional; confirm before worm 3)

The test applied to each AC: *rewrite the PNA in another language, on another OS, with another database,
delivered another way — does the statement still bind?* Yes → Layer 1 (universal or conditional). Names
or depends on a specific stack → Layer 2 realization.

### Universal ACs (`PNA_Spec.md`)

| AC | Verdict | Note |
|---|---|---|
| AC-1 two-store split | universal L1 | clean |
| AC-4 versioned handshake | universal L1 | clean (boundary types are examples) |
| AC-6 diagnostic escape | universal L1 | clean (form already declared shell-derived) |
| AC-7 field-debug substrate | universal L1 | clean |
| AC-9 auto-backup | universal L1 — **reword** | "per-boot" leaks a long-running-app assumption; PRM (per-command) had to reinterpret as per-mutation. Retitle to a user-edit cadence. |
| AC-10 opt-in non-destructive re-imports | universal L1 | clean |
| AC-11 concurrent-access detection | universal L1 | clean ("tab/process" are examples) |
| AC-15 build label | universal L1 | clean |
| AC-16 user-driven transport selection | universal L1 | vacuous without Communications |
| AC-17 sourced provenance | universal L1 | clean |
| AC-18 transports can't read content | universal L1 | product names (mailto/Signal/Slack) are illustrations of the criterion |
| AC-19 user-visible payload before send | universal L1 | clean |
| AC-PRM-A LLM-as-transport | universal L1 — **naming** | universal despite the `PRM` in the ID |
| AC-PRM-D re-ingestion user-initiated | universal L1 — **naming** | universal despite the `PRM` in the ID |
| AC-MCP-A cloud-client consent | universal L1 — **principle/realization fusion** | principle ("a non-local automated consumer of private data needs per-call consent") survives; "MCP Private Data Ops" is its realization. Candidate to split. |
| AC-MCP-B MCP stages; workspace launches | universal L1 — **is User-Mediation** | this *is* UM (proposer stages, principal disposes) in MCP terms; reconcile when UM lands. |

### Flavor-derived ACs (`axes.md`)

| AC | Verdict | Note / behavioral trigger |
|---|---|---|
| AC-2 no-SaaS surface | **conditional L1** | trigger: *operates a server over its data*. (Today triggered by `web-bundle-*` pick.) |
| AC-3 single OPFS owner | **realization → demote** | of AC-1/AC-11 on `opfs-sqlite-wasm` |
| AC-5 stale session → cache | **conditional L1** (+ HTTP realization) | trigger: *auth-gated refresh*. Names 401/403; principle survives. |
| AC-8 anti-enum + bounded analytics | **conditional L1** (+ server realization) | trigger: *operates an auth server*. Heavily HTTP; principle survives. |
| AC-12 capability-detect in worker | **realization → demote** | of "honest capability detection" — **candidate new universal L1** principle (detect honestly, never claim more than the platform delivers), with AC-12 as its browser realization. |
| AC-13 COOP/COEP | **realization → demote** | browser headers for `crossOriginIsolated` |
| AC-14 SW never owns SQLite | **realization → demote** | PWA service-worker specific |
| AC-PRM-B multi-source dedup | **conditional L1** | trigger: *mirrors more than one source*. Clean (identity/provenance semantics). |
| AC-PRM-C native file-lock | **realization → demote** | of AC-11 on `native-sqlite-via-filesystem` |
| AC-PRM-H authenticated loopback surface | **conditional L1** (+ realization) | trigger: *exposes a same-host programmatic/network surface over its data*. Names loopback/socket as examples. |

**Summary:** demote 5 (AC-3, AC-12, AC-13, AC-14, AC-PRM-C); retag 5 as conditional-L1 with behavioral
triggers (AC-2, AC-5, AC-8, AC-PRM-B, AC-PRM-H); reword AC-9; flag naming (AC-PRM-A/D) and
principle/realization fusion (AC-MCP-A/B) for follow-on.

### Open questions for the maintainer (before worm 3)

1. **AC-5 / AC-8** are the borderline calls — keep them as conditional-L1 (principle in the AC, HTTP form
   as a realization), or treat them as realizations outright? *Recommend conditional-L1.*
2. **AC-12 → a new universal "honest capability detection" AC?** Or let its principle fold into Goal 2 /
   the constraint-frontier discipline and demote AC-12 purely as a realization? *Recommend a small new
   universal AC; capability honesty survives the swap.*
3. **AC-MCP-A/B and AC-PRM-A/D naming/fusion** — split principle from realization, and/or rename the
   PRM-prefixed universals? Bigger ripple (IDs are referenced widely). *Recommend: defer renames; note
   the fusion now, reconcile AC-MCP-B with UM when UM lands.*
4. **ID stability on demotion.** When AC-3/12/13/14/PRM-C lose `AC-*` IDs, external reports + the
   realization index + both bundled attestations reference them. Plan: keep a redirect note mapping the
   retired IDs to their realization home, so nothing dangles.
