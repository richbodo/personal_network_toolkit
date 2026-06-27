# Visual Validator — implementation plan

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> The *how/when* of building a static viewer for evaluate-reports. The *why* lives in the
> brainstorms: the **validation dashboard** ("web app: parse a validation report → render")
> in [`brainstorms/2026-06-05-pnt-positioning.md`](../brainstorms/2026-06-05-pnt-positioning.md)
> (lines 126–132), the parked **validation library → voluntary-validation registry**
> (same file, lines 133–134), and the thin-slice **[T1+A1+C1]** scope decision in
> [`brainstorms/2026-06-07-pnt-scope-roadmap.md`](../brainstorms/2026-06-07-pnt-scope-roadmap.md)
> (line 44 names this viewer as the rendering surface). The artifact it renders already
> ships: [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)
> (the item-4 typed report, done — see [`plans/pnt-next-steps-plan.md`](pnt-next-steps-plan.md)).

## What this is

A **static, zero-dependency HTML/JS viewer** that renders instances of the typed
evaluate-report artifact into a human-readable page — in a **developer** register
(per-AC/EX/CST table with code citations) and an **end-user** register (good / at-risk /
how-to-be-safer), shown alone or **side by side**. The side-by-side pairing is what turns
the report into a teaching tool: the plain-language verdict next to the technical evidence
for the *same* finding is how a non-expert learns what a privacy guarantee means in code.
It is **viewer-first**: report *generation* stays with the agent-driven
evaluate flow in [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md); a
static page can't run an LLM. The plan builds up to the thing the average person actually
wants — point it at a **directory of reports** and **flip through them with ← / →**, one
report per app you dropped in.

## Guardrails (why a viewer doesn't make this repo "an application")

[`CLAUDE.md`](../CLAUDE.md) says this is a spec/lint/docs repo, **not** an application. The
viewer stays on the *tooling* side of that line by construction:

- **Static, no build step, no framework, no runtime deps** — vanilla JS only, the JS
  analogue of the toolkit's stdlib-only-`python3` rule. No npm, no bundler, no `node_modules`.
- **Engine-agnostic; no Chromium-only APIs.** Runs on Firefox and Safari as well as Chromium.
  We deliberately avoid the File System Access API (`showDirectoryPicker`) and other
  single-engine capabilities. The lesson from `fellows_local_db` is that Chromium-only gates
  are too restrictive to build on — restrictive enough that we're unlikely to ship another PWA
  reference design at all — so a *tool for reading reports about apps* must not repeat that
  mistake. (See [`spec/constraints.md`](../spec/constraints.md) — `CST-PWA-PRIVATE-SNAPSHOT`
  and the Chromium-only-capability-gap implementation note.)
- **Not a backend.** It does not run the evaluate flow, call any model, or serve dynamic
  content. The only server it ever uses is stdlib `python3 -m http.server` to read local files.
- **Not the public daily dashboard.** The live, agent-updated red-light dashboard (cadence
  axis **C2**) stays parked per the scope-roadmap; this is the local, on-demand viewer (C0/C1).
- **Renders only what the schema carries.** The typed JSON instance is the source of truth;
  every register is a *view* over it and invents no data the report doesn't assert.

## Where it lives

- `tools/report-viewer/index.html` — the viewer (inline CSS/JS; single-file ethos).
- `tools/report-viewer/sample-reports/` — representative report instances (fixtures + the
  seed "directory of reports").
- `justfile` — a `just view-reports [dir]` recipe (stdlib `http.server`, see Phase 5).

## Phasing (cheapest-first; 80/20 = Phases 1–3, the user-facing payoff = Phase 5)

### Phase 1 — Sample reports + render contract *(de-risks everything downstream)*
- Author 2–3 real `evaluate-report.schema.json` instances under
  `tools/report-viewer/sample-reports/`, spanning the cases the viewer must render:
  a mostly-**conformant** report; one with **non-conformant** findings plus an
  undeclared-deviation; one exercising **`EX-*`** and **`CST-*`** findings and `evidence`
  entries tagged by `source` (`deterministic` / `llm` / `human`).
- These double as the viewer's render fixtures **and** schema fixtures. Add a small
  stdlib check (fold into `tools/tests/lint_selftest.py`) asserting every sample parses
  as JSON and carries the schema's required top-level keys (`summary`, `findings`), so a
  future schema change that breaks the samples **fails loudly** rather than silently
  rotting the viewer. Per the lint-discipline rule, that check ships with its own
  fault-injection case in the same change.
- **Done-when:** ≥3 representative reports exist; the stdlib check passes clean and fails
  on an injected malformed sample; the set is documented as the viewer's render contract.

### Phase 2 — Single-report renderer (MVP)
- `tools/report-viewer/index.html`: load one report three ways — file picker, drag-drop,
  and `?report=<path>` — and render: the `summary` posture up top, then one card per
  finding keyed by **AC / EX / CST ID**, each with a status badge
  (`conformant` / `non-conformant` / `not-applicable` / `unable-to-determine`), cited code
  locations, and any `evidence` entries with their `source` tag.
- Vanilla JS, no deps, no build; the file-picker / drag-drop paths work opened directly
  over `file://` (no server needed).
- **Done-when:** open the page, load any Phase-1 sample, and see a faithful, readable
  rendering of every field the schema carries — nothing dropped, nothing invented.

### Phase 3 — Two registers: toggle **and** side-by-side *(the educational payoff)*
The same loaded report renders in two registers — and the *pairing itself* is a primary
goal of this tool, not a nicety. Seeing the non-technical and technical accounts of the
same finding together is the most educational thing the viewer does: it teaches a
non-expert what a privacy guarantee actually means in code, and shows a developer the
human stakes behind an AC.
- **Developer (A0):** per-AC/EX/CST table, code citations, raw evidence.
- **End-user (A1):** plain-language **good / at-risk / how-to-be-safer**, organized by
  Goals 1–5, leading with the most concerning sovereignty/comms/durability findings —
  carrying the liability-safe caveat from the brainstorm: *"evaluated against this specific
  spec's commitments; the app may not be trying to be a PNA,"* not "App X is unsafe."
- **Two view modes:** (a) a **toggle** that flips one pane between registers, and (b) a
  **side-by-side** mode showing A1 and A0 together, **finding-aligned**, so a reader takes
  in the plain-language verdict and the technical evidence for the same AC at a glance.
- Both registers derive entirely from the same JSON (no new data). Remember the last chosen
  mode/register in `localStorage`; default configurable.
- **Done-when:** one load renders correctly as toggle *and* side-by-side; in side-by-side
  the registers stay finding-aligned; the A1 view leads with the load-bearing Goal-1–5
  non-conformances and shows the caveat.

### Phase 4 — Generate seam (thin, honest, deferred-friendly)
- The "generate a report through the web interface" half, kept honest about the static-page
  limit. Provide: (a) a copy-paste / `just` path that runs the **agent evaluate flow** and
  writes a schema-valid JSON into the reports directory; (b) a **"+ New report"** affordance
  in the UI that surfaces that exact prompt/command (and links the schema) rather than
  pretending to generate in-page.
- This is the declared seam where a *real* generate-button plugs in later, **if/when** a
  local runtime exists — declared, not faked.
- **Done-when:** from the UI a user can copy a ready-to-run prompt/command that drops a
  schema-valid report into the watched directory; the seam is documented as the future
  generator's plug point.

### Phase 5 — Directory library + ←/→ flip-through *(the user-facing payoff)*
- Point the viewer at a **directory of reports** and flip through them with **← / →** keys
  (plus on-screen prev/next), one app per report. A thin index/sidebar lists the apps; each
  report header shows app name + toolkit-version + date. Target user: *"drop reports for the
  apps on your system, then flip through them"* — a left/right arrow and a JS viewer is all
  the average person needs.
- **The static-page directory-listing problem** (a browser can't enumerate a folder over
  `file://`). Two supported paths, recommend the first:
  1. **`just view-reports [dir]`** — serve the directory with stdlib `python3 -m http.server`
     and open the viewer; it fetches a small `index.json` manifest (or generated listing)
     and renders prev/next over it. Stdlib-only, matches the repo ethos.
  2. **Drag-drop a multi-file selection** onto the page — zero setup, no server; JS reads
     them all and you flip through the loaded set. The `file://`-friendly fallback.
- **Done-when:** given a directory of N report JSONs (via `just view-reports` or drag-drop),
  the user can ←/→ through all N, each rendered in their chosen register.
- **Parked extension — the validation *registry* (out of scope here).** The brainstorm's
  *validation library → registry of voluntary software validations* (positioning lines
  133–134): `{SWHID + AC-keyed report + attester identity + toolkit-version}` in an
  append-only / transparency-log structure (OpenSSF-badge-style self-attestation, or
  Sigstore/Rekor-style signed log), leveraging the toolkit's **existing SWHID archival** —
  which is already half of it. This local directory viewer is its thin, reversible
  precursor; the registry stays parked until demand shows (mirroring the scope-roadmap's
  C2-parked call), and its hard part is the *trust model*, not storage.

## Decisions (locked for this pass)
- **Stack:** static, zero-dependency, no-build **vanilla JS** in `tools/report-viewer/` —
  the JS analogue of the stdlib-only Python rule; keeps the repo *tooling, not an app*.
- **Input:** renders the typed `evaluate-report.schema.json` instance as source of truth;
  registers and prose are views over it.
- **Audience:** **both** registers (developer A0 / end-user A1), available as an in-UI
  **toggle *and* a finding-aligned side-by-side** view — the side-by-side pairing is a
  first-class, educational goal of the tool (Phase 3), not a nicety.
- **Scope:** **viewer-first** — generation stays in the agent evaluate flow; web-generate is
  a declared future seam (Phase 4), not built now.
- **Directory serving:** stdlib `python3 -m http.server` via `just view-reports`, with
  multi-file drag-drop as the no-server fallback.
- **Directory enumeration:** browser-agnostic only — an `index.json` manifest served over
  `just view-reports` (primary) + multi-file drag-drop (no-server fallback). The File System
  Access API (`showDirectoryPicker`) is **rejected**: it is Chromium-only
  ([`spec/constraints.md`](../spec/constraints.md) — `CST-PWA-PRIVATE-SNAPSHOT` and the
  Chromium-only-capability-gap note), and a viewer that worked on only one engine would
  repeat the PWA restrictiveness we're moving away from. It must run on Firefox and Safari.
- **Sample-report home:** `tools/report-viewer/sample-reports/`, co-located with the viewer.
  It doubles as a legit reports directory on a developer box — e.g. a cron job that runs the
  evaluate flow and drops a dated report there, then flips through them via Phase 5.

## Open decisions (deferred)
- Whether the A1 wording lives in the viewer or is precomputed into the report artifact (a
  richer `summary`), so any viewer renders the end-user register identically.

## Process riders (land with the implementing PRs, not this plan)
- **Docs-currency rule** ([`CLAUDE.md`](../CLAUDE.md)): the PR that adds `just view-reports`
  (and the viewer as a developer-facing tool) MUST update
  [`docs/users-guide.md`](../docs/users-guide.md) in the same PR — the *Working in this repo*
  command table plus a short *View a report* entry — and add a `CHANGELOG.md` line.
- **Lint discipline:** the Phase-1 schema check ships with a fault-injection self-test in
  the same change; a check with no self-test can silently rot.

## Fit with the existing roadmap
- Renders the item-4 artifact (`tools/evaluate-report.schema.json`, done) — gives the
  "occasionally re-check we didn't drift" workflow a *visual* surface over the diffable JSON.
- Realizes the brainstorm's **validation dashboard** (the #2 dwebcamp deliverable) and the
  thin-slice **[T1+A1+C1]** rendering surface; the daily public dashboard (C2) and the
  voluntary-validation registry stay parked.
- Phases 1–3 are in-repo, static, and landable independently; Phase 4 is a thin seam;
  Phase 5 is the user-facing flip-through. No dependency on the Phase-5 conformance harness.
