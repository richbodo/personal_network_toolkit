# Harvesting reusable code from reference designs

*Design note · 2026-06 · status: **Tier-0 adopted + goal reached (2026-06-19)** —
`tools/realization-index.py` emits [`../realization-index.md`](../realization-index.md),
drift-gated in `just ci` with a self-test; the `path:symbol` attestation-determinism nudge
landed in the Architecture template; **both reference designs are at 100% realization-pointer
coverage** (fellows #289, PRM #60, re-synced via `just rearchive`). Tiers 1–2 remain proposals.
Checkpoints a 2026-06-19 discussion (Rich + Claude Code) prompted by the toolkit's
`just rearchive` helper ([PR #83](https://github.com/richbodo/personal_network_toolkit/pull/83)) —
a convenience tool for re-archiving an accepted reference design — about how tested,
portable code should be **found and reused** across reference designs and by new PNA builds.
The asset-dual of the field-notes practice
([`2026-06-capturing-conformance-lessons.md`](2026-06-capturing-conformance-lessons.md)):
field notes capture what an AC is easy to get *wrong*; this captures where the
proven code that gets it *right* already lives. Indexed in
[`../PriorArt.md` § Design notes](../PriorArt.md).*

> **Not a commitment, and not a spec change.** This records a problem, the conventional
> reuse mechanisms, and a staged recommendation. It imposes no obligation on any design
> and adds no AC. The point is to write the thinking down so we can pilot, adopt, or
> reject it on the record.

## The problem

The toolkit's `just rearchive` helper (PR #83) is a re-archive convenience tool. The pattern
is portable — any reference design re-archives on every release or re-pin — so the question
is general: **how should reusable code move between reference designs, and to a brand-new PNA
build?** A building
team (developer + agent) adapting the closest reference design should be able to *find*
the parts worth copying, judge that they are tested and portable, and lift them with
their provenance intact — instead of re-deriving a pattern another design already proved.

Two facts about this toolkit shape every answer:

- **The source lives in separate, SWHID-archived, independently-released repos.** The
  toolkit keeps each accepted design's `Architecture.md` + `evaluate-report.json` + a
  `design.toml` SWHID pin — *not* the source. So for most reusable code the lever is
  **discovery + provenance-stamped pointers**, not a vendored shared library; centralizing
  app source would fight the independence/archival model and the stdlib-only-no-deps rule.
- **The primary "builder" is an AI agent** reading the spec. The reuse surface therefore
  has to be *agent-legible*: structured, greppable, keyed to stable IDs.

What exists today gets you *most* of the way and is worth saying plainly (Rich invited
"maybe we're already doing enough"): attestation tables point at code per AC with
`file:line`; field notes capture the generalizable lessons; templates +
[`SKILL.md`](../../pna-toolkit/SKILL.md) build-flow step 6 already say *adapt the closest
design*; and ecosystem tooling already flows upstream (`just rearchive`, `loopback-surface-lint`).
The **specific** gap: there is no **aggregated, cross-design, reuse-framed, agent-queryable**
view. To find "who has realized ST-6 (the auto-backup ring), and where," an agent must open
every design's `Architecture.md` and read AC-by-AC. No index answers the question directly.

## The core insight

1. **There are two kinds of reusable code, and they want different mechanisms.** The
   re-archive workflow blends them; keeping them apart is what unlocks clean answers.

   - **Type A — ecosystem-participation tooling.** Code that exists *because the design
     plugs into the toolkit*: re-archiving, the `evaluate-report.json` emitter, the
     conformance reporter, the loopback lint. Its natural home is **the toolkit itself** —
     which already *is* the shared library for this category and already absorbs these.
     Re-archival is the textbook case, and it is a **two-repo dance**: the toolkit owns the
     **toolkit-side** half — `just rearchive` (PR #83): compute SWHIDs, rewrite the
     `design.toml` pin, refresh bundled copies, lint — while the **design-side** half
     (regenerate the design's own commit-stamped `evaluate-report.json`, tag, push) is
     *irreducibly* per-design and lives in each design's repo (PRM already carries it in
     `scripts/evaluate_report.py` + `scripts/conformance_report.py`). As `tools/rearchive.py`
     itself says, "emitters and runners differ per design," so you cannot hoist the
     design-side half upstream — the reuse lever there is a copyable template script, not
     centralization.

   - **Type B — application implementation patterns.** Real app code realizing a mechanical
     feature within a slot: the OPFS auto-backup ring (ST-6/AC-9), the worker RPC pending-Map
     dispatch (ST-3), the atomic stage→validate→swap with orphan preview (ST-8/SH-5/AC-10),
     the advisory single-writer file-lock (AC-PRM-C/AC-11). These are substrate-specific and
     live in archived independent repos. You **cannot centralize** them; you can only
     **index, annotate, and point at** them.

2. **The AC / sub-contract is the natural index** — the same reason field notes are AC-keyed.
   Builders and validators already work sub-contract-by-sub-contract; the spec already
   decomposes a PNA into named sub-contracts (`WS-`, `ST-`, …). That decomposition *is* the
   reuse granularity for Type B: "want to implement ST-6? here are the reference realizations."

3. **The harvest index is the asset-dual of field notes — and it is mostly already written.**
   Every `conformant` row in a design's attestation table already carries a **Realization**
   (`file:func` pointers) and a **Verification** (`test::name`). The toolkit keeps a copy of
   each accepted design's `Architecture.md`. So the raw material for "who realizes ST-6, and
   where" *already exists and is already maintained under the attestation discipline.* The
   only gaps: it is organized **by design×AC** (not aggregated by AC across designs), it is
   framed as *how we conform* (not *worth lifting*), and it points at live `main` (not the
   **archived SWHID commit**).

   > field note → *what an AC is easy to get wrong* (liabilities, negative invariants)
   > harvest index → *proven code for this sub-contract and where to get it* (assets)

   Same keys, same consumable layer, read by the same build/evaluate flows.

### Two cross-cutting principles (these are what keep it from rotting)

This repo's recurring failure mode is rot (the dead `Reversible:` check; deferrals living
only in comments). Two disciplines, both inherited from existing practice:

- **Derive, don't hand-maintain, wherever possible.** Generate the cross-design index *from*
  the attestation tables the toolkit already requires, as a checked artifact (regen + lint,
  like everything else here). A generated index can't drift from the evidence it summarizes.
- **Tested-not-asserted, and provenance travels.** Only mark something harvest-worthy if a
  **negative test** pins it — the same bar as a `conformant` row, so the index never becomes
  a pile of unproven snippets. Every harvest pointer names the **archived SWHID commit** (not
  `main`, so it's reproducible and rot-proof) and the **source license** (copying across repos
  crosses a license boundary; the toolkit already requires OSI-approved + SWH-archivable).

## The candidate mechanisms (mapped to this toolkit's grain)

1. **Shared library / package.** Right for **Type A** (the toolkit already is it); **wrong
   for Type B** — vendoring archived app code fights independence/archival and the no-deps
   rule. *Premature anyway under the **rule of three**: with two designs, almost no pattern
   has been seen three times — extracting a shared library now is speculative abstraction.*
2. **Template / scaffold.** Already exists (`reference_designs/templates/`). Extend to *code*
   skeletons: the Type-A design-side script, and Type-B starting points. Low cost, on-grain.
3. **Cookbook / annotated pattern catalog.** Annotated excerpts + pointers; fits the
   "80/20 toward description, not a runner" philosophy. The **Type-B** answer at maturity.
4. **In-repo code annotations (`@harvest`, a `REUSE.md`).** Low friction, lives with the
   code — but scattered across repos the toolkit can't govern, drifts, and can't be enforced
   centrally. Weak as a primary mechanism.
5. **Machine-readable index keyed by AC/sub-contract.** The agent-legible search surface —
   and, crucially, **derivable from data the toolkit already keeps.** Highest leverage.
6. **Conformance tests as reusable artifacts.** The negative tests pin invariants; a builder
   adapts the *test*, not just the code. Already half-present in every attestation row.

## Recommendation — staged, so we stop at the tier the ecosystem has earned

Build the self-reinforcing minimum, then add curation only as designs accumulate — don't
front-load a registry for two designs.

- **Tier 0 (near-free, highest leverage): a *derived* realization index.** A small stdlib
  tool parses the bundled `reference_designs/*/Architecture.md` attestation tables and emits
  `docs/realization-index.md` (or JSON): per AC/sub-contract → which designs realize it, the
  `file:line`, the verifying test, the status. Generated + fault-injection-self-tested like
  every other lint here. Add one clause to `SKILL.md` build-flow step 6: *"…and consult the
  realization index for proven realizations of your sub-contracts."* This alone closes the
  actual gap, at almost zero new maintenance, because it reuses evidence we already require.
- **Tier 1 (thin curation): mark the harvest-worthy subset + portability.** Not every
  realization is worth copying, and portability varies (substrate-bound `opfs-sqlite-wasm`
  vs. substrate-neutral). A light `harvest = true` + a one-line portability note on the rows
  that generalize gives the index the judgment layer it lacks. Keep it small.
- **Tier 2 (the cookbook, only when earned): AC-keyed harvest notes** mirroring the
  field-notes format — Pattern, where it lives (design + path + archived SWHID commit),
  substrate constraints, the negative tests that travel with it, the source license. Honest
  decline beats empty notes, same as field notes. Write one only when a *third* design would
  otherwise re-derive the pattern (the rule of three, applied per pattern).
- **Type A seam (orthogonal to the tiers):** keep centralizing the toolkit-side half upstream
  (done). For the irreducibly design-side half, ship a template script in
  `reference_designs/templates/scripts/` (re-archive + emit-report skeleton) and point new
  designs at `prm`'s `scripts/` as the worked reference — better, lean on `design.toml`'s
  `[verify]` block (it already declares `entrypoint` / `emits_report`) so the design-side
  emitter is **contract-driven rather than copy-pasted**. Document the toolkit-side/design-side
  boundary once, in `CONTRIBUTING.md` (it owns contribution policy).

## Status and next step

**Tier 0 spiked and pressure-tested (2026-06-19).** `tools/realization-index.py` (stdlib,
~260 lines) parses the two bundled `Architecture.md` attestation tables + their `design.toml`
pins and emits [`../realization-index.md`](../realization-index.md): **25 ACs, 43 (AC×design)
rows, 2 designs.** It tolerates both attestation conventions in the wild (PRM links its AC
cells, fellows uses plain text + a separate not-applicable table), normalizes status, harvests
realization/verification pointers, and stamps each row with the design's archived commit +
`swhid_dir`. A `--check` mode is the anti-drift gate. The coverage summary is the most
immediately useful output: it names the **12 ACs realized by both designs** — the prime harvest
candidates, where a builder has two realizations to compare.

**The headline finding — and it's a finding about the *attestation convention*, not the tool.**
Realization-pointer recall is uneven: **PRM 12/14 non-N/A rows yield a file pointer, fellows
only 13/23.** The cause is prose style — PRM writes `file:symbol` (`core/lock.py:file_lock`),
fellows often names a bare function (`previewFellowsDbSwap()`, `refuseIfVersionSkew()`) with no
containing path, so a high-precision path-anchored extractor can't harvest it. The index stays
useful regardless (the *verification* column almost always carries file paths, and every row
points at the right AC×design to open), but the cheap lift that would make Tier 0 materially
better is a one-line nudge in `ARCHITECTURE_TEMPLATE.md`: **cite realizations as `path:symbol`,
not a bare `symbol()`.** That nudge is Tier-1-adjacent and worth doing before curation.

Smaller warts (acceptable for a spike, listed for honesty): `::name` test-ref continuations
print without their parent file; HTTP routes (`/api/...`) and `.md` doc links occasionally leak
into the pointer column; the N/A-reason cell truncates mid-token.

**Tier 0 adopted (2026-06-19).** `tools/realization-index.py` is wired into `just ci` via a
`--check` drift gate (lockfile discipline — a stale committed index fails CI), with a
`lint_selftest.py` case pinning the extraction contract + the gate; the `just realization-index`
recipe, the `docs/users-guide.md` *The realization index* section, and the `CHANGELOG` entry
landed alongside. The four spike warts are fixed (and a `path:symbol` / full `path::test`
determinism nudge landed in `ARCHITECTURE_TEMPLATE.md`). The coverage metric is baked into the
index — and it immediately earned its keep: PRM's `AC-PRM-A` realization cited only a doc link,
so the metric correctly shows it uncovered (PRM 11/14, not 12/14).

**The goal — full realization-pointer coverage — reached (2026-06-19).** Both reference designs
are now at **100%**: fellows_local_db 23/23 (PR [#289](https://github.com/richbodo/fellows_local_db/pull/289))
and PRM 14/14 (PR [#60](https://github.com/richbodo/prm/pull/60)), each editing its `Architecture.md`
to cite realizations as `path:symbol` and verifications as full `path::test`, then re-synced into
the bundled copies via `just rearchive` with the index regenerated and drift-gate-clean. Both coverage
commits were then **submitted to Software Heritage Save Code Now** (2026-06-19, origin-save requests
2368289 / 2368290); the recorded SWHIDs are git-computed/content-addressed and resolve once ingest
completes (async). Tiers 1–2 (harvest/portability
mark, cookbook notes) still accrete only as N grows.

*Endgame worth naming, not building (v0.3+):* record when design X *harvested* pattern Y.
That citation graph tells you which patterns are load-bearing across the ecosystem — the
most-reused are the candidates to promote toward a contract or a canonical reference
implementation. The "used-by-N-repos" signal, premature with two designs.

## Worked example (illustrative — the target shape)

What a Tier-0 derived index row might look like, aggregated across designs for one
sub-contract:

> **ST-6 — Auto-backup ring (realizes AC-9).**
> - `prm` · `core/snapshots.py` (pre-apply ring via sqlite online-backup, `KEEP=20`,
>   per-mutation cadence) · verified by `tests/unit/test_apply.py::test_snapshot_and_restore`
>   · `conformant` · pin `swh:1:rev:…` · *portable (substrate-neutral: any sqlite file).*
> - `fellows_local_db` · per-boot debounced OPFS snapshots outside the SAH-pool dir ·
>   verified by … · `conformant` · pin `swh:1:rev:…` · *substrate-bound (OPFS).*
>
> A builder on `native-sqlite-via-filesystem` lifts `prm`'s; a builder on
> `opfs-sqlite-wasm` lifts `fellows_local_db`'s. The index makes that choice a lookup, not
> an archaeology dig.
