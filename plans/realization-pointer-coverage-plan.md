# Plan — raise both reference designs to 100% realization-pointer coverage

> **Goal (today, 2026-06-19):** every non-N/A AC row in each accepted design's
> `docs/Architecture.md` resolves to a `path:symbol` code pointer, so the derived
> [realization index](../docs/realization-index.md) reports **100%** for both designs.
> Closes the open goal in [`docs/roadmap.md`](../docs/roadmap.md) § Inbound-findings
> registry and [`docs/design-notes/2026-06-harvesting-reusable-code.md`](../docs/design-notes/2026-06-harvesting-reusable-code.md).

## Why this is the 80/20 reuse win

`tools/realization-index.py` harvests a code pointer from each attestation row's
**Realization** cell. A row whose prose names a symbol *without its file* (e.g.
`previewFellowsDbSwap()` rather than `app/static/app.js:previewFellowsDbSwap`) is invisible
to the index. Today: **fellows_local_db 13/23 (57%), prm 11/14 (79%)**. Fixing the citation
form turns "find proven code for AC-X" into a lookup and de-noises the index for builders —
the highest-leverage, lowest-cost reuse improvement from the design-note discussion. (The
other mechanisms — Tier-1 portability marks, Tier-2 cookbook notes, a design-side script
template — stay deferred until a third design; premature at N=2.)

## The convention (both designs) — a citation-form edit, not a conformance change

Edit the **canonical** `docs/Architecture.md` in each design's own repo:

1. **Realization cells** — cite each code reference as `path/to/file.ext:symbol`
   (e.g. `core/snapshots.py:rotate`), never a bare `symbol()`. HTTP routes (`/api/...`) and
   doc links (`*.md`) are not code pointers — name the file that *implements* the behavior.
2. **Verification cells (same pass — the 80/20 add-on):** write each test as the full
   `path/to/test.py::name`; expand any bare `::name` continuation to repeat its file. The
   index tool stitches these for now, but the source should be clean — see the rule landed
   in [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md).
3. **Don't invent pointers and don't change a Status.** Cite the file that *already* realizes
   the row; if a row genuinely has no single code home, keep its honest status and say so. The
   metric measures citation completeness, not new conformance.

## Section A — fellows_local_db *(agent works in `../fellows_local_db`)*

Coverage **13/23**. Add a `path:symbol` realization pointer to these **10** rows (the current
prose names the symbol/route without a file — open the cited code and add `file:symbol`):

- **AC-5** (stale session never locks out) — the three-tier `window.__dataProvider` hot-swap
- **AC-6** (diagnostic escape) — the `?gate=1` force-gate + Reset Everything handler
- **AC-10** (opt-in non-destructive re-imports) — `previewFellowsDbSwap` / `applyFellowsDbSwap`
- **AC-11** (concurrent-access detection) — `isOwnershipConflictError` / `OWNERSHIP_CONFLICT`
- **AC-12** (capability detection inside worker) — the worker `init` `opfsCapable` report
- **AC-16** (user-driven transport selection) — the group/fellow export transport picker
- **AC-18** (transports cannot read message contents) — the `mailto:`/`tel:`-only path
- **AC-19** (user-visible payload before send) — the group export/compose panel
- **AC-PRM-A** (LLM calls are transports) — the `EX-CLOUD-LLM` consent/default-local path
- **AC-PRM-D** (re-ingestion is user-initiated) — the About-page refresh button handler

Commit + push; tag a ref for archival (e.g. `pnt-ref-0.1.x`) or note the HEAD sha.

## Section B — prm *(agent works in `../prm`)*

Coverage **11/14**. Add a `path:symbol` realization pointer to these **3** rows:

- **AC-MCP-A** (cloud consent for Private DB) — cite the shared/dedup MCP server module(s); the
  realization currently has no file path.
- **AC-PRM-A** (LLM calls are transports) — the realization cites only a design-note `.md`; cite
  the code that defaults/recommends the local model and signals cloud use.
- **AC-PRM-D** (re-ingestion is user-initiated) — cite the `prm import` / `reimport` entrypoint.

Commit + push; tag/note the ref.

## Section C — toolkit resync *(one agent, in the toolkit, after A + B are pushed)*

1. Re-archive each design at its new ref (refreshes the bundled `Architecture.md` copy + pin):
   - `just rearchive fellows_local_db <ref> ~/src/fellows_local_db`
   - `just rearchive prm <ref> ~/src/prm`
   - (`--no-save` for an offline re-pin if not requesting Save Code Now in this pass.)
2. Regenerate the index: `just realization-index`.
3. `just ci` — the drift gate must pass; `python3 tools/realization-index.py --json` must read
   **100%** for both designs.
4. Flip the open goal to **closed**: the roadmap registry row + the design note's "open goal"
   section + a `CHANGELOG.md` note.
5. Open the toolkit PR (resynced bundled copies + new pins + regenerated index).

## Done criteria

- `python3 tools/realization-index.py --json` → **fellows_local_db 23/23 (100%), prm 14/14 (100%)**.
- `just ci` green. Roadmap registry + design note marked closed.

## Out of scope (deferred until a 3rd design — not today's 80/20)

Tier-1 harvest/portability marks; Tier-2 AC-keyed cookbook notes; the Type-A design-side script
template. Rule of three — revisit when the reference set grows.
