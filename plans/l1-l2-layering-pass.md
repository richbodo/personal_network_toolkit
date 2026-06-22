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
- **Worm 3 — demote realizations, retag conditionals, promote AC-22, rename per N2 (scope DECIDED — see
  § Worm 3 below).** Demote the 5 realizations to `RZ-*` beside their axis pick in `axes.md`; consolidate
  *all* ACs (universal + conditional) into `PNA_Spec.md`; add universal **AC-22** (honest capability
  assessment); rename **AC-PRM-A → AC-20**, **AC-PRM-D → AC-21** (+ redirects); update
  `tools/lint-spec-ids.py` + `tools/tests/lint_selftest.py`, both reference-design bundled attestations,
  and the realization index; remove the transitional note. *Merge worms 1–3 together.*
- **Worm 4 — the verifiability AC (the B1 reframe) — DONE (this branch), `just ci` green.** Added universal
  **AC-23 "Source available for verification"** (Goal 2) — facet-1 of the self-legibility family, paired with
  AC-22 and threaded into Goal 2's constraints next to the build label (AC-15). The `distribution` axis stays
  honest packaging — **no pick rename** (PRM's flavor untouched) — with a note relocating verifiability to
  AC-23, orthogonal to the pick. Demonstrators: PRM (build-from-source) + fellows (source-available bundle);
  their AC-23 attestation rows re-sync at the v0.2 cut. Supersedes the old "split the distribution pick"
  framing of [#39](https://github.com/richbodo/personal_network_toolkit/issues/39)/[#64](https://github.com/richbodo/personal_network_toolkit/issues/64) rider 1. Lint now: **23 AC IDs**.
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

### Resolved (2026-06-22)

1. **AC-5 / AC-8 → conditional-L1.** Confirmed. A pure-CLI PNA (e.g. the planned CLI backup/dedup/archive
   reference design) never stands up an HTTP auth server, so neither can apply universally — the
   definition of conditional. The HTTP specifics (401/403, per-IP limits) are noted as the realization.
2. **AC-12 → a new universal AC.** Confirmed: promote the generic principle as **AC-22 — Honest
   capability assessment** (serves Goal 2); AC-12 demotes to its OPFS realization (`RZ-2`). It completes
   Goal 2's *self-legibility* family — facet 2 (capability legibility), beside facet 1 (source
   legibility = the verifiability AC-23, worm 4) and facet 3 (build/behaviour = AC-15 / AC-6 / AC-7).
   Demonstrated both ways already: fellows (worker-side OPFS detection, UA-never-gates) + PRM
   (FTS5-compiled + advisory-lock checks via `just doctor`). Draft + placement below.
3. **Naming → N2.** De-brand the two mis-provenanced universals: **AC-PRM-A → AC-20**,
   **AC-PRM-D → AC-21**, with redirects (cheaper now than later). `AC-MCP-A/B` frozen this pass (the
   principle/UM reconciliation is deferred — `AC-MCP-B` is User-Mediation in MCP terms; revisit when UM
   lands). Going forward: new ACs are plain-numeric; **provenance lives in the realization index +
   attestations + CHANGELOG, never in the ID.**
4. **ID stability.** Only the 5 realizations change ID (→ `RZ-*`) and the 2 renamed universals
   (→ AC-20/21); each carries a redirect note. Everything else frozen. Retired numbers (3/12/13/14) are
   **not** reused.

---

## Worm 3 — resolved scope + drafts

**Status: worm 3a landed (this branch), `just ci` green.** 3a = the ID-namespace surgery: AC-22 added;
AC-3/12/13/14/PRM-C → RZ-1..RZ-5 (dual-anchored for redirect; Retired-IDs table in `axes.md`);
AC-PRM-A/D → AC-20/21; both contract `Realizes:` headers + their prose updated; `PNA_Spec.md` /
`axes.md` / `use_cases.md` cross-refs updated. The lint reports **22 AC IDs** (was 26: −5 realizations,
+1 AC-22). Reference-design attestations + the realization index are **left for the v0.2 re-sync** (they
are 0.1-pinned and the lint does not cross-check them; the Retired-IDs table bridges the gap).

**Worm 3b — DONE (this branch), `just ci` green.** All three layering rules now hold and *all* ACs live
in `PNA_Spec.md`. The 5 conditional ACs (AC-2, AC-5, AC-8, AC-PRM-B, AC-PRM-H) moved into a new
`PNA_Spec.md` **§ Conditional architectural commitments**, retagged by *behavioral property* (rule 2);
`axes.md` is now pure Layer 2 (per pick → *conditional ACs entailed* [links up] + *realizations brought*
[`RZ-*` tables with an explicit Realizes column] + *constraints inherited*); a new **`RZ-*` traceability
lint check** (check 10 in `lint-spec-ids.py`) + its fault-injection self-test; redirect anchors kept in
`axes.md` so old `axes.md#ac-*` links still resolve. Lint: **22 AC IDs + 5 RZ realizations**; **44/44**
self-tests. The `flavor-derived` term is retired across the three core spec files.

**Remaining:** worm 4 (verifiability AC / the B1 reframe) and worm 5 (sub-contracts). The
reference-design attestations + the derived realization index still re-sync at the v0.2 cut. A repo-wide
`flavor-derived` → conditional/realization terminology sweep across the non-spec docs (users-guide,
SKILL, CHANGELOG, papers, templates) is also outstanding.

### ID disposition

| Disposition | IDs |
|---|---|
| **Frozen** (unchanged) | AC-1, 2, 4, 5, 6, 7, 9, 10, 11, 15, 16, 17, 18, 19; AC-PRM-B, AC-PRM-H (conditional); AC-MCP-A, AC-MCP-B (universal) |
| **Renamed** (N2, + redirect) | AC-PRM-A → **AC-20** · AC-PRM-D → **AC-21** |
| **Recategorized → `RZ-*`** (+ redirect) | AC-3 → RZ-1 · AC-12 → RZ-2 · AC-13 → RZ-3 · AC-14 → RZ-4 · AC-PRM-C → RZ-5 |
| **New** | **AC-22** (capability legibility, this pass) · *AC-23 (source legibility / verifiability, worm 4)* |

### Presentation — all ACs in `PNA_Spec.md`

- **§ Universal architectural commitments** (existing table) — gains **AC-22**; AC-PRM-A/D rows become AC-20/21.
- **§ Conditional architectural commitments** *(NEW, immediately after the universal table)* — the 5
  conditional ACs (AC-2, AC-5, AC-8, AC-PRM-B, AC-PRM-H), each with an **Applies when (behavioral
  property)** column and a link to the axis pick(s) that entail it. Draft below.
- **Realizations are NOT ACs** → they stay in `axes.md` (Layer 2) as the `RZ-*` set, beside the pick that
  brings them, each linking *up* to the AC it realizes. `PNA_Spec.md`'s AC section carries one pointer
  ("Layer-2 realizations live in `axes.md`").
- `axes.md` becomes purely Layer 2: per pick → *conditional ACs entailed* (links up to the spec),
  *realizations brought* (`RZ-*`), *constraints inherited* (`CST-*`, links to `constraints.md`). The
  current "Extra commitments these picks add" tables split into those three.

### Draft — AC-22 (new universal row, for the § Universal architectural commitments table)

> | **Honest capability assessment.** A PNA MUST establish the runtime-substrate capabilities that bear on its commitments by *sound* means — probing the substrate, not trusting an unverified self-report (a feature-presence flag, a platform / UA string) — and MUST report the outcome truthfully, including an explicit *undetermined* where a capability cannot be established. It MUST NOT claim or rely on a capability it has not verified the substrate delivers. *(Substrate-specific probes are realizations — e.g. `RZ-2` worker-side OPFS detection; a CLI's "is FTS5 compiled into this `sqlite3`" check.)* | Goal 2 | `<a id="ac-22"></a>AC-22` |

**Placement:** append to the universal table (after AC-MCP-B). Also add AC-22 to **Goal 2 § Constraints it
requires**, in the code-validation / legibility cluster, paired with the build label (AC-15) and the
diagnostic substrate (AC-6/AC-7). **Relationship to Constraints:** AC-22 is the *upstream* duty — *assess
honestly*; the Constraint `Detectability:` class (`feature-detect`/`empirical-probe`/`ua-sniff`) is *how it
is checked per inherited ceiling*; Constraint handling (*reduce capability + declare frontier*) is
downstream. Cross-link the three in `constraints.md` without duplicating the rule.

### Draft — § Conditional architectural commitments (new section in `PNA_Spec.md`)

> | Commitment | Serves | Applies when (behavioral property) | ID |
> |---|---|---|---|
> | **No SaaS surface.** A server the PNA stands up MUST be a delivery channel, not a service: no per-user RW endpoints, no private-data persistence, no admin console, no cross-device sync. | Goal 3 | the PNA **operates a server** over its data | AC-2 |
> | **Stale session never locks users out of cached data.** A rejected shared-side fetch MUST fall through to the local cache; fresh data MUST require an explicit user action. | Goal 1 | the PNA **gates data behind an authenticated refresh** | AC-5 |
> | **Anti-enumeration + abuse-bounded analytics.** Auth endpoints MUST return neutral payloads and enforce per-IP rate limits; a sanitized error sink MAY double as the analytics pipe but MUST NOT widen the privacy boundary. | Goal 3 | the PNA **operates an auth server** (with a configured error sink) | AC-8 |
> | **Multi-source dedup contract.** A stable `record_id` MUST survive merge across sources; the dedup flow MUST surface conflicts; per-source provenance MUST be recorded *per field*. | Goal 2 | the PNA **mirrors more than one source** | AC-PRM-B |
> | **Authenticated same-host surface.** A same-host-reachable surface a PNA opens over its own data MUST be loopback-bound and authenticated to the user's own session; a non-loopback bind MUST require an explicit, documented opt-out. | Goal 3 | the PNA **exposes a same-host surface** over its data | AC-PRM-H |

The HTTP/401-403 specifics of AC-5/AC-8 move to their realizations in `axes.md`; the AC keeps the
behavioral promise. (Provenance — "introduced by PRM" for AC-PRM-B/H — moves to the realization index, not
the ID, so these keep their frozen legacy IDs without the suffix meaning anything.)

### Draft — the `RZ-*` realizations (in `axes.md`, beside the pick)

> | Realization | Realizes | Substrate (axis pick) | ID |
> |---|---|---|---|
> | Single OPFS-owning worker; one writer; no main-thread OPFS. | AC-1, AC-11 | `storage:opfs-sqlite-wasm` | RZ-1 *(was AC-3)* |
> | Capability detection runs inside the OPFS-owning worker (browsers lie about main-thread OPFS); UA strings MAY inform messages but MUST NOT gate. | AC-22 | `storage:opfs-sqlite-wasm` | RZ-2 *(was AC-12)* |
> | COOP/COEP headers so `crossOriginIsolated` holds (dev + prod). | AC-1 | `opfs-sqlite-wasm` + web-served | RZ-3 *(was AC-13)* |
> | Service worker is app-shell + update only; the Shared-store URL is bypassed in its fetch handler. | AC-1 | web-bundle PWA | RZ-4 *(was AC-14)* |
> | Native single-instance file-lock; a second process refuses cleanly, naming the holder. | AC-11 | `storage:native-sqlite-via-filesystem` | RZ-5 *(was AC-PRM-C)* |

**Redirects.** A small "Retired IDs" table (in `axes.md`, near the realizations) maps each old ID → its new
home (`AC-3 → RZ-1`, …, `AC-PRM-A → AC-20`, `AC-PRM-D → AC-21`) so external reports and any stale link
resolve. Both bundled attestations + the realization index get rewritten to the new IDs in the same worm.
`tools/lint-spec-ids.py` learns the `RZ-*` family (collect IDs; a `Realizes:` on each must name a defined
AC) **+ a fault-injection self-test** for the new check (CLAUDE.md rule).

---

## Worm 3 follow-on (toolkit-goal side) — the evaluate report's self-legibility section

*Not part of the AC surgery; the **consumer** that motivates AC-22 + AC-23. Sketch only — sequence after
the ACs land.* The neglected reporting: the evaluate report
([`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)) answers per-AC findings,
exceptions, and constraints — but has no first-class place to answer *do we have the source? what stack is
this? what can it keep here? what's undetermined?* Add a `self_legibility` object that the legibility ACs
populate:

```jsonc
"self_legibility": {
  "source": { "status": "available-and-buildable | source-referenced | opaque", "note": "…" },   // AC-23
  "substrate": { "storage": "native-sqlite-via-filesystem", "shell": "cli-subcommands",
                 "runtime": "python3.12 / linux", "detected_by": "…" },                            // AC-22 + pick inference
  "capabilities": [
    { "name": "fts5", "status": "present|absent|undetermined", "detected_by": "probe" }           // AC-22
  ],
  "build_label": "2026-06-22-ab12cd3"                                                              // AC-15
}
```

This makes the toolkit's diagnostic identity legible in its *output*, mirroring the legibility the ACs
require of the *app* — the PNA-goal side (AC-22/23) and the toolkit-goal side (this report section) of the
same idea.
