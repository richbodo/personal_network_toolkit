# PNA Toolkit Changelog

## v0.1 draft (in progress)

### Reference designs re-attested at Toolkit-Version 0.2 (the v0.2 design re-sync)

- **Both reference designs now attest at Toolkit-Version 0.2** — the design-side half of the v0.2 cut.
  `prm` (re-pinned `pnt-ref-0.2`, `2d6889d`) and `fellows_local_db` (re-pinned `pnt-ref-0.2`, `15be80d`)
  each gain **AC-22** (honest capability assessment) + **AC-23** (source available for verification)
  attestation rows and carry the UM-1/2/3 user-mediation rows; bundled `Architecture.md` / `design.toml`
  / `evaluate-report.json` copies refreshed via `just rearchive`, realization index regenerated.
- **`fellows_local_db` gained a GPL-3.0 `LICENSE`** — the repo had no license file, a real gap bearing on
  AC-23 (the "rebuild" right) and the archival/OSI rule; now corrected. (`prm` is MIT.)
- Retired realizations (`AC-3/12/13/14` in fellows, `AC-PRM-C` in prm) are kept under their legacy IDs
  for now (redirect anchors in `spec/axes.md`); a clean `RZ-*` relabel pass is queued as #103.
- `just ci` green (the fellows re-pin also refreshed two hardcoded-pin fixtures in `lint_selftest.py`).

### Tooling + docs: `swh-save.sh` ref-not-found diagnostics + `just rearchive` documentation

- **`tools/swh-save.sh`** now distinguishes *"no clone provided"* from *"clone present but the ref does
  not resolve in it."* The old code printed `No local clone provided` for both — sending a maintainer
  hunting for a clone they had already passed, when the real cause was a tag-name typo (`pnt-ref-0.2.0`
  vs the actual `pnt-ref-0.2`). The new branch names the missing ref and the likely fix (`git tag -l` /
  `git fetch --tags`). Pinned by a fault-injection self-test `case_swh_save_ref_not_found` in
  `tools/tests/lint_selftest.py` — **47/47**.
- **`docs/users-guide.md`** gains a full **§ Re-archive a design (`just rearchive`)**: a per-argument
  reference (`<name>` = the `reference_designs/<name>/` directory, `<ref>` = a ref in the *design's* repo,
  `<clone>` = a local clone path) plus the `--no-save` / `--arch-src` / `--report-src` flags, what the
  recipe does vs. leaves to you, and the "run `just realization-index` after" gotcha. The `justfile`
  recipe comment is trimmed from a dense one-liner to a single real example.
- A toolkit-fix — no new obligation on any design; `just ci` green.

### Exceptions-hardening (D1): the `pna-active` / `exception-handling` predicate split is normative

- **`spec/exceptions.md` § Concept** — promotes the predicate split from `(Proposed, RFC)` to
  **normative**: the conferred verdict reports **PNA membership** (`pna-active`) only; how honestly each
  active exception is handled lives solely in the per-`EX-*` findings, never rolled up. A relying party
  (and a future interop gate) keys on `pna-active`, and nothing else ("detect, don't bless").
- **The report contract carries it (`tools/evaluate-report.schema.json`):** `summary.posture` gains a
  **`not-pna-active`** value — a cleanly-handled `EX-CLOUD-LLM` app reads it, never `conformant`.
  `tools/report-fixtures-lint.py` (`POSTURES`) and the **Visual Validator** (`tools/report-viewer/`:
  plain-language label + CSS) render it; a new sample `04-not-pna-active-exception.json` demonstrates it
  (covered in `just ci` via report-fixtures-lint, and in the opt-in viewer suite). `PNA_Spec.md`
  (vocab-pna + the Validation note) and `pna-toolkit/SKILL.md` (evaluate step 9) flip to normative.
- A reporting *clarification* — it imposes no new behavioral obligation on a built PNA, only on how the
  evaluate flow **reports**. The sole remaining exceptions RFC is **EX-H7 fail-closed** (D2), gated on
  PRM v0.2. `just ci` green.

### Exceptions-hardening (D3): the un-relaxable floor is now normative + lint-enforced

- **`spec/exceptions.md` § Scope discipline** — promotes the **un-relaxable floor** from `(Proposed, RFC)`
  to **normative**: no exception may relax it even with consent — charter members **AC-18 / AC-19 /
  AC-MCP-B** (the action-floor: no unreviewed action taken on the user's behalf, since it reaches third
  parties who consented to nothing). An exception that names a floor AC in its `Relaxes:` is malformed.
  The RFC banner now lists **two** remaining proposals (`pna-active`, EX-H7 fail-closed), and the EX-H7
  demonstrator note is corrected — **PRM v0.2** enforces fail-closed; `fellows_local_db` ships only
  best-effort.
- **Enforced, not just asserted:** `tools/lint-spec-ids.py` (check 5) now rejects a `Relaxes:` that names
  a floor AC, with a fault-injection self-test (**46/46**). En route this **fixed a latent `RELAXES_RE`
  gap** — the regex lacked the `\**` that `REVERSIBLE_RE` carries, so it matched only the backtick
  *example* in § Header conventions, never a real exception's bold `**Relaxes:**` field; the not-known
  and floor checks now see the actual tokens.
- Demonstrated by `EX-CLOUD-LLM` (relaxes only `PNA-DEFINITION` + `AC-MCP-A`, no floor AC) → no design
  goes non-conformant. `docs/users-guide.md` notes the floor. EX-H7 fail-closed (D2) stays RFC, gated on
  PRM v0.2. `just ci` green.

### User-mediation — the third general mechanism (`UM-1/2/3`)

- **`spec/user_mediation.md` (new)** — promotes user-mediation from a proposal (the `(proposed; UM-1/2/3)`
  line in `exceptions.md`) to a first-class mechanism, a sibling of `exceptions.md` and `constraints.md`:
  the standing invariant that *the proposer stages, the principal disposes*, with **UM-1** (no bypass,
  enforced at the data layer) · **UM-2** (separation) · **UM-3** (legibility) — bounded to
  separation/legibility/attribution, **not** comprehension (the same honest limit as EX-H7). Names the
  invariant beneath the action/egress ACs (its `Unifies:` header — AC-10/16/19/20/21/MCP-B) and defines
  the per-design **mediated-boundary registry**.
- **Demonstrator-gated, demonstrators in place:** both reference designs already attest UM-1/2/3
  `conformant` — `fellows_local_db` (egress side: data-layer refusal + mediated-boundary registry) and
  `prm` (mutation side: propose→review→apply). New normative content carried by working demonstrators,
  per `CONTRIBUTING.md`.
- **Lint + self-test:** `tools/lint-spec-ids.py` gains check 11 — every AC named in the `Unifies:`
  header must resolve to a defined AC (the third-mechanism analog of the contract `Realizes:` / RZ /
  CST-`Bounds:` cross-reference), plus the Toolkit-Version stamp; a fault-injection case in
  `tools/tests/lint_selftest.py` (a `Unifies:` naming an undefined AC) pins it (**45/45**).
- **Cross-refs:** `PNA_Spec.md` § Vocabulary gains a `user-mediation` entry; `exceptions.md` retires the
  `(proposed)` line; `docs/users-guide.md` + `pna-toolkit/SKILL.md` (evaluate flow) gain the mechanism.
  No reference-design re-attestation or `evaluate-report.json` schema field in this PR — the designs'
  bundled-copy sync + any report-schema `um_id` ride the v0.2 cut (honest deferral). `just ci` green.

### L1/L2 layering pass — three layers, AC-22 / AC-23, RZ-* realizations, conditional-AC consolidation

The spec is now built in three explicitly-named layers, with a single dividing test — **an
architectural commitment survives a total technology swap** (rewrite the PNA in another language, OS,
database, delivery; if the statement still binds it is Layer 1, else it is a Layer-2 realization).

- **Three layers, named.** **L0 Goals** (the four user-facing outcomes) · **L1 architectural
  commitments** (the `AC-*` namespace — every AC passes the swap test; *universal* + *conditional*) ·
  **L2 realizations and constraints** (the `RZ-*` realizations, `CST-*` constraints, and per-slot
  sub-contracts — everything that names a stack). New top-level [§ How the pieces fit together](spec/PNA_Spec.md#how-the-pieces-fit-together)
  states the model + the three rules that keep the layers clean.
- **AC namespace.** **New:** `AC-22` (honest capability assessment) and `AC-23` (source available for
  verification), completing Goal 2's self-legibility family. **De-branded (+ redirect anchors):**
  `AC-PRM-A → AC-20`, `AC-PRM-D → AC-21`. **Demoted to realizations (+ redirects):** `AC-3 → RZ-1`,
  `AC-12 → RZ-2`, `AC-13 → RZ-3`, `AC-14 → RZ-4`, `AC-PRM-C → RZ-5` — these named a technology, so they
  are Layer-2 realizations, not ACs. Retired numbers are not reused.
- **Conditional ACs consolidated.** The conditional ACs (`AC-2`, `AC-5`, `AC-8`, `AC-PRM-B`, `AC-PRM-H`)
  moved into a new [§ Conditional architectural commitments](spec/PNA_Spec.md#conditional-architectural-commitments)
  in `PNA_Spec.md`, each tagged with the *behavioral property* that triggers it. `axes.md` is now pure
  Layer 2: per pick → the conditional ACs it entails (links up) + the `RZ-*` realizations it brings + the
  constraints it inherits.
- **Terminology.** The "flavor-derived AC" term is **retired** in favor of **conditional AC** (Layer 1)
  and **realization** (Layer 2), swept across the spec and the active non-spec docs (users-guide, SKILL,
  `llms.txt`, the Architecture template, paper 2, the reference-design Architecture/README copies). Stale
  `axes.md` → `PNA_Spec.md` pointers for conditional ACs corrected. Historical CHANGELOG entries and dated
  design-notes keep the original wording.
- **Lints + tooling.** `tools/lint-spec-ids.py` learns the `RZ-*` family (each `RZ-*` must name a defined
  AC it realizes) with a fault-injection self-test (**44/44**); `tools/realization-index.py` now indexes
  `RZ-*` realizations alongside `AC-*` commitments.
- **Reference designs re-synced.** Both bundled `Architecture.md` attestations + the derived
  [realization index](docs/realization-index.md) re-synced to the new IDs (AC-20/21, RZ-1..5); `just ci`
  green.
- **Deferred to the v0.2 cut (honest):** adding `AC-22` / `AC-23` *attestation rows* to the two reference
  designs (a re-evaluation, not a mechanical re-sync) and re-syncing their bundled `evaluate-report.json`
  snapshots (+ the report schema's `ac_source` enum) — these travel with the design re-evaluation, not
  ahead of it.

### Spec preamble: the "evolutionary stance" + a Scope connector (positioning reconciliation)

- **`spec/PNA_Spec.md` § Preamble + § Scope and versioning** — folds the now-merged Paper 1 positioning
  ([`docs/papers/paper1-pna-positioning.md`](docs/papers/paper1-pna-positioning.md), PR #91) into the spec:
  an *"Earning complexity — an evolutionary stance"* paragraph (the PNA is deliberately partial/opinionated —
  it forgoes live multi-device sync because the rules that would keep the private layer safe across every sync
  scenario aren't known yet, and earns complexity only once simpler systems are proven usable + safe), plus a
  § Scope connector reframing the deferrals (cross-device sync, federation, richer substrate) as deliberate
  staging rather than omission.
- Positioning/motivation prose only — no new obligation on any design, no AC/contract/flow change (a toolkit
  fix); the rationale is preserved in Paper 1 (linked), so no separate `docs/PriorArt.md` design note. No
  `docs/users-guide.md` change required. `just ci` green (44/44 after the RZ-* self-test above).

### Both reference designs re-archived at 100% realization-pointer coverage

- **fellows_local_db re-pinned `dc3e0cf` → `98b283f`** (fellows [#289](https://github.com/richbodo/fellows_local_db/pull/289)) and **prm re-pinned `1551896` → `7bd4a28`** (`pnt-ref-0.1.2`, prm [#60](https://github.com/richbodo/prm/pull/60)) — each adds `path:symbol` realization pointers + full `path::test` verifications to its `Architecture.md`, taking the [realization index](docs/realization-index.md) to **23/23** and **14/14** (100%/100%). Re-synced into the bundled copies via `just rearchive`; index regenerated; `just ci` green (43/43, drift gate included).
- **Software Heritage submission (residual closed 2026-06-19):** both coverage commits were submitted to *Save Code Now* — fellows `98b283f` (origin-save request `2368289`) and prm `7bd4a28` (request `2368290`), both `accepted`; ingest is async (the git-computed SWHIDs resolve unchanged once it completes). The design.toml `archival` comments and the per-design README archival bullets record the request IDs.
- Closes the open goal in [`docs/roadmap.md`](docs/roadmap.md) § Inbound-findings registry and [`docs/design-notes/2026-06-harvesting-reusable-code.md`](docs/design-notes/2026-06-harvesting-reusable-code.md). No spec/AC/contract change.

### Realization index — a derived, cross-design map of *who realizes each AC, where* (toolkit tool)

- **`tools/realization-index.py` (new) + `just realization-index` → [`docs/realization-index.md`](docs/realization-index.md)** — the
  asset-dual of the field notes: a generated table mapping each AC to the accepted designs that realize it,
  the harvested `path:symbol` code pointer, the verifying test, the status, and the design's **archived
  commit / `swhid_dir`** (study the realization at the pin, not drifting `main`). Stdlib only; derived
  entirely from the bundled `reference_designs/<name>/Architecture.md` attestation tables + `design.toml`
  pins, so it can't drift from the evidence it summarizes. The build flow consults it to find proven code
  *per AC* across all designs; the coverage summary names the ACs realized by more than one design (the
  prime patterns to compare).
- **Drift gate + self-test.** `just ci` runs `realization-index --check` (lockfile-style: a stale committed
  index fails CI); a new `lint_selftest.py` case pins the extraction contract (no HTTP route, `*.md` doc
  link, or unstitched `::name` continuation leaks into a pointer) and the drift gate. `just ci` green (43/43).
- **Pointer-coverage as a tracked goal.** The index reports per-design *realization-pointer coverage*
  (today fellows_local_db 13/23, prm 11/14); the standing goal is **100%**. To make attestations
  deterministically harvestable, **`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`** now asks for
  `path:symbol` realizations and full `path/to/test.py::name` verifications (no bare `::name`). Raising the
  two reference designs to full coverage is cross-repo follow-on work tracked in [`docs/roadmap.md`](docs/roadmap.md).
- **Docs:** `docs/users-guide.md` gains the recipe + a *The realization index* section (and back-fills the
  missing `just rearchive` row); the rationale lives in
  [`docs/design-notes/2026-06-harvesting-reusable-code.md`](docs/design-notes/2026-06-harvesting-reusable-code.md)
  (indexed in [`docs/PriorArt.md` § Design notes](docs/PriorArt.md)).
- No spec/AC/contract change; no new obligation on any design (a toolkit fix). The template's
  citation-form guidance is a recommendation that sharpens harvestability, not a new conformance bar.

### `just rearchive` — one-step reference-design re-archival (toolkit tool)

- **`tools/rearchive.py` (new) + `just rearchive <name> <ref> <clone>`** — re-archiving an accepted design at
  a new commit (a new release, or a re-pin after upstream spec changes land) was a multi-step, drift-prone
  chore. The helper does the deterministic part end-to-end: it calls `tools/swh-save.sh` (Save Code Now POST +
  git-compatible SWHIDs), rewrites the design's `design.toml` pin (`commit`/`swhid_rev`/`swhid_dir` +
  `archival = "archived"`, comments and alignment preserved), refreshes the bundled `Architecture.md` +
  `evaluate-report.json` copies from the clone *at the ref* (`git show <ref>:…` — no checkout), and re-runs
  `tools/lint-spec-ids.py`. It deliberately leaves prose (the README archival bullet, the index line, the
  CHANGELOG) and cross-repo actions (tagging the design repo, the PR) to the human — printing paste-ready
  stubs for each — and warns when a bundled report's `candidate.commit` lags the pinned commit (with the exact
  regenerate recipe). `--no-save` runs it offline.
- **`tools/tests/lint_selftest.py`** — a new offline case builds a throwaway design clone, re-pins the prm
  design inside a repo copy, and asserts the manifest pin + the Architecture refresh + the stale-report warning
  + a lint-clean result (`--no-save` / `SWH_SAVE_NO_REQUEST` keeps `just ci` offline). `tools/rearchive.py`
  added to the versioned-artifact set in `tools/lint-spec-ids.py`; `CONTRIBUTING.md § acceptance` documents it.
  `just ci` green (39/39).
- No spec/AC/contract change; no new obligation on any design (a toolkit fix).
### PRM: re-archived at `pnt-ref-0.1.1` (`1551896`) — Software Heritage SWHIDs refreshed (reference design)

- `reference_designs/prm/` re-pinned from `a70d35b` (the v0.1 attestation, prm #35) to **`pnt-ref-0.1.1`**
  (`1551896`) — the prm [#59](https://github.com/richbodo/prm/pull/59) merge to `main` landing the loopback-daemon
  trust-surface work (`AC-PRM-H`), now that the spec changes it rides are accepted. New annotated tag pushed on the
  prm side. New SWHIDs `swh:1:rev:1551896025307ac4b08ba621c02f4e0d77eb9391`,
  `swh:1:dir:39637a1ff96f77e7df47e87ac53a7c6d8fc61b62` (git-compatible, via `tools/swh-save.sh`); Save Code Now
  re-ingest requested (request id 2367638, accepted — async).
- Bundled **`Architecture.md`** + **`evaluate-report.json`** copies refreshed from canonical (the
  `private.db`→`relationships.db` rename + the new AC-PRM-H "no ungoverned data tap" contribution prose). The
  `evaluate-report.json` was **regenerated at the accepted commit** by prm's deterministic emitter, so its
  `candidate.commit` pins `1551896` (mirroring the a70d35b re-sync); the 18-AC attestation table is unchanged
  (12 conformant / 2 partial / 4 not-applicable).
- `reference_designs/prm/README.md` "Contributions to the spec" gains the **`AC-PRM-H`** bullet (the design now
  rides five spec changes). `design.toml` + the `reference_designs/` index re-pinned to the tag. `just lint` green.

### Capture-lessons practice: AC-keyed field notes (adopted; dogfooded on AC-PRM-H)

- **`docs/field-notes/` (new)** — the consumable, AC-keyed store for generalizable lessons harvested from reference designs (pitfalls + negative-invariant checklists). First entry **`AC-PRM-H.md`**, dogfooded from the loopback-surface work (PRM #59).
- **`pna-toolkit/SKILL.md`** — the build and evaluate flows now read an AC's field note *before* implementing/judging it; a new § *Capturing a conformance lesson* documents the procedure (and the `/capture-lesson` command), with the **PR-checklist standing rule** (AC-driven + test-backed change → link a field note or honestly decline).
- **`.github/pull_request_template.md`** — the standing-rule checkbox. **`docs/design-notes/2026-06-capturing-conformance-lessons.md`** flipped proposal → **adopted** (ideas 1–3); indexed in [`docs/PriorArt.md` § Design notes](docs/PriorArt.md).

### Loopback-surface auth lands: `AC-PRM-H` + the "no ungoverned data tap" principle (with its demonstrator, PRM #59)

- **`spec/axes.md` § Workspace shell — new flavor-derived `AC-PRM-H`** (replacing the prior RFC pointer): a same-host-reachable surface a PNA opens over its own data (a loopback HTTP daemon, a local socket) MUST be loopback-bound + authenticated to the user's own session. Triggered by a server-backed local shell × a non-`web-bundle` distribution. Authenticating the transport relaxes no guarantee, so it does **not** flip `pna-active`.
- **Principle prose by [`AC-2`](spec/axes.md#ac-2)** — AC-2 (the web-bundle delivery server) and AC-PRM-H (the loopback daemon) are named as two **realizations of one rule**: a server a PNA stands up must not become an ungoverned tap on its own data. The principle generalizes (future surface types → further flavor-derived ACs) while each obligation stays narrowly checkable.
- **`docs/design-notes/2026-06-loopback-surface-auth.md`** flipped proposed → **landed**, citing the durable demonstrator commit (PRM `main` `1551896`). **`docs/PriorArt.md` § Design notes** — already indexed.
- Demonstrator: **PRM [#59](https://github.com/richbodo/prm/pull/59) merged** — daemon session-auth (token + Host/Origin guard + loopback-pin) + the L1/L2 loopback lint run `--strict` in its own gate. The deterministic toolkit lint shipped in #80; the acceptance-process clarification in #79.

### Loopback-surface lint: deterministic check for an app-opened transport (toolkit tool)

- **`tools/loopback-surface-lint.py` (new)** — the static "checked, not asserted" companion for the one surface a PNA opens over its *own* data (an app-stood-up HTTP daemon; candidate `AC-PRM-H`, RFC). **L1** (a literal non-loopback bind) **gates**; **L2** (a handler module with no recognized auth guard) is **advisory** by default and gates only under `--strict` — so a heuristic can't rot into alarm-fatigued CI noise (the deliberate severity split). `--json` folds into an evaluate report (`source=deterministic`). Clean/dirty/noauth fixtures + `lint_selftest` cases; added to the versioned-artifact set and `just loopback-lint`. A standalone evaluator tool (like `egress-lint`); the `AC-PRM-H` *obligation* lands with its demonstrator (PRM) per CONTRIBUTING.

### Acceptance-process clarification: demonstrating commit vs. acceptance (toolkit fix)

- **`CONTRIBUTING.md` § Acceptance process** — names the **demonstrating-commit vs. acceptance** distinction (two repos, two merges): the demonstrator is a *pushed, working, cited commit* — **not** a design-repo merge; the only gating merge is the toolkit PR ("the merge is the acceptance"); pin the demonstrator at a durable (merged / tagged) commit *before* acceptance, for SWHID / `Toolkit-Version` stability. No new obligation. (Split out of the loopback-surface RFC, [PR #78](https://github.com/richbodo/personal_network_toolkit/pull/78), to land first on its own.)

### Same-UID research folds into the Harden countermeasure rows (toolkit fix)

- **`spec/exceptions.md` § Countermeasure library** — deep research into the desktop sandbox/encryption
  primitives (Linux · macOS · Windows, with the mobile contrast) refined the **environmental** rows:
  **"Run the PNA under a separate OS user" is elevated as the cleanest convenient desktop answer** — a
  distinct UID denies a same-user agent at the file-permission / `/proc` / `ptrace` checks at once
  (recreating mobile's per-app-UID isolation) — and **"Sandbox the automation agent" is annotated** with
  the same-UID insufficiency (a mount-namespace alone is defeated by the `/proc/<pid>/root` wormhole + a
  filesystem-wide encryption unlock + `ptrace`; it needs `PR_SET_DUMPABLE=0` + `ptrace_scope` + a
  per-process MAC). A new note records that **confining a same-UID agent is an access-control, not an
  encryption, problem** — reinforcing the at-rest deprecation.
- Advisory / environmental only — no AC, Exception, Constraint, or obligation added; the strength classes
  are unchanged (`best-effort`, bounded by adoption).
### Skill renamed `pna-build-eval-contrib` → `pna-toolkit` (toolkit fix)

- **`pna-toolkit/` (was `pna-build-eval-contrib/`)** — the skill directory and its frontmatter
  `name:` are renamed to a stable domain label. The old name enumerated three flows
  (`build · eval · contrib`) and silently omitted the fourth, **harden**; enumerating flows in the
  name goes stale on every new flow. `pna-toolkit` follows Claude Code skill-naming convention — a
  brief kebab-case domain label — and never needs to change as flows are added. Auto-discovery is
  unaffected: it keys on the `description` field (unchanged), not the name.
- **Swept all 55 references across 26 files** (spec, README, users-guide, CONTRIBUTING, roadmap,
  plans, tool/contract comments, sample reports, `CLAUDE.md`, `.claude/commands/prime.md`) to the new
  path so every cross-link stays live. `just ci` green (34/34).
- No new obligation on any design — a rename of the agent-consumption artifact; no AC, contract, or
  version change. `VERSION` stays `0.1`.
### Recorded the *conditional* at-rest-encryption variants we declined (toolkit fix / docs)

- **`docs/PriorArt.md` § Design notes** — the at-rest scope-decision entry now records the three
  *conditional* at-rest-encryption variants weighed in the 2026-06-14 direction session
  (scoped-to-"MCP-on", per-field "encrypt when MCP-accessed", hazard-triggered) and why each was
  **declined** — so the reasoning isn't lost outside the brainstorm. Detail lives in the design note;
  no spec, contract, or behavior change.

### `just validate <candidate>` — one-command deterministic-baseline evaluate-report (toolkit fix)

- **`tools/validate.py` (new) + `just validate <dir>`** — the assembly layer from
  [`docs/design-notes/2026-06-validate-command-and-strength-tiers.md`](docs/design-notes/2026-06-validate-command-and-strength-tiers.md):
  runs the **Tier-S deterministic lints** (`egress-lint` → AC-1; `attestation-evidence-lint`
  when the candidate self-attests; `export-readable-lint` with `--export`) against a candidate and
  folds them into one typed `evaluate-report.json` (the Visual Validator's render contract),
  detecting — and reporting, not running — a cooperating design's Tier-F `[verify].entrypoint`.
  Stdlib-only; shells out to the existing lints' `--json` mode.
- **Honesty is enforced, not hoped:** a deterministic check that *finds* a violation →
  `non-conformant`; a *clean* check → `unable-to-determine` (necessary, not sufficient). The tool
  **never** emits a green `conformant` verdict on its own, so a clean run is an honest triage
  baseline, not a trust certificate (the design note's "lite-as-full" guardrail, closed in code).
- **`tools/tests/lint_selftest.py`** — six new assertions pin the contract on the egress fixtures:
  exit code (dirty → 1, clean → 0), the emitted report passes the render contract, and the
  clean→`unable-to-determine` / dirty→`non-conformant` AC-1 mapping. `just ci` green (31/31).
- **`docs/users-guide.md`** — new `just validate` row, audit-flow usage, and tool listings;
  `tools/validate.py` added to the version-stamped artifact set.
- No new obligation on any design — this is evaluative *tooling* (it consumes the spec, realizes
  no AC). `/pna-evaluate` (#55) becomes a thin wrapper over this baseline + the LLM pass.
- **`docs/PriorArt.md` § Design notes** — pointer recorded; the `just validate` design note's
  status flips to "Tier-S landed".

### Harden flow added to the skill — the advisory 4th flow (toolkit fix)

- **`pna-toolkit/SKILL.md`** — adds **Harden** as the fourth flow the skill packages
  (`build · evaluate · contribute · harden`), writing the advisor procedure whose *concept* landed
  earlier with the Countermeasure library. Harden secures the *operating environment* a PNA runs in —
  runtime adversaries the app's own code can't reach (an OS-level AI agent or another local process) —
  maps each hazard to the **environmental** rows of the Countermeasure library ([`spec/exceptions.md`](spec/exceptions.md))
  with their strength classes, and reports an honest Protect / Detect / Respond posture. It is
  **advisory**: it recommends, adds no AC, and awards no pass/fail.
- **`README.md` / `docs/users-guide.md` / `spec/PNA_Spec.md` § Composition** — the "three flows / three
  modes" descriptions become four: a Harden mode bullet (README), a Harden how-to + Quick-reference row
  (users-guide), and a Harden reference in § Composition. Per `CLAUDE.md`, the skill-flow change updates
  the User's Guide in the same change.
- **`README.md` § Status refresh** (same pass) — corrects stale notes surfaced while auditing the README
  against the 2026-06-14 direction work: `prm` is now *realized* (not "draft") and archived, `tools/swh-save.sh`
  ships, both reference designs carry Architecture docs with AC attestation tables; retired the old
  "Phase 5 / 7" framing in the success criteria.
- **No new obligation on any design** — Harden is advisory; no AC, Exception, or Constraint added.

### Goals restructured 5 → 4, app-framed at outcome altitude (toolkit fix)

- **`spec/PNA_Spec.md`** — the goal layer is re-pitched as **four** outcome-altitude goals, each with a
  per-goal template (outcome → example mechanism → why it matters → the plain-language ACs it requires):
  **G1 Take ownership of the root · G2 Protect the root's integrity, by validation · G3 Protect the root
  from egress · G4 Protect the root from entropy & accidents.** Old G2 (local root) → G1; old G5
  (diagnosability) folds into G2; old G1 (privacy) + old G3 (communication) merge into G3 (egress); old G4
  (durability) → G4. Usability is named as a preamble assumption *above* the goals. **No AC's requirement
  changes** — a re-presentation, no new obligation on any design.
- **AC ↔ Goal is many-to-many, rendered primary-grouped.** A new **cardinality note** ("How the pieces fit
  together") states how every spec component relates, and the AC table's `Serves` column is re-mapped from
  the goal categorization (AC-1 → Goal 1, Goal 3; AC-10 → Goal 1, Goal 4; AC-17 → Goal 2 [provenance =
  data-validation]; AC-MCP-A → Goal 2, Goal 3). Cross-cuts are capped at two.
- **§ Vocabulary** gains *Architectural commitment, Constraint, Exception, Goal, Sub-contract* glosses
  (definition-before-first-use, now a rule in **`CLAUDE.md`**) so the Goals + cardinality table are grounded.
- **`tools/lint-spec-ids.py` (check 9, + 2 fault-injection self-tests)** — validates every `Goal N`
  reference (the AC `Serves` column, constraints' `Bounds:`, exceptions' `Stresses:`) resolves to a
  `### Goal N` the spec defines, and enforces the two-goal cardinality cap. Guards the renumber against
  silent rot.
- **Ripples carried through** `exceptions.md` (`Stresses`), the `evaluate-report.schema.json` goal range
  (max 5 → 4), `SKILL.md` / `users-guide.md` (the Goals-1–N enumeration), the Visual Validator's
  `GOAL_NAMES`, the three sample reports' `goals` arrays, both reference-design Architecture copies
  (`stresses Goal 1` → `Goal 3`), `conformance-scope-and-lifecycle.md`, `PriorArt.md`, the data-floor note,
  the `roadmap.md` labels, the egress-lint docstring, and `README.md` positioning. Downstream Architecture
  re-syncs are tracked in fellows #284 / prm #38. `just ci` green (28/28).
- Toolkit-Version stays **0.1-draft** (a re-presentation; no new obligation). Deferred to a fast-follow:
  demoting § Vision below the Goals + the deeper preamble rework.
- **`docs/PriorArt.md` § Design notes** — rationale entry recorded.

### Countermeasure library + the Harden sibling: the mitigation side of Exceptions (toolkit fix)

- **`spec/exceptions.md`** — expands **EX-H6** ("recommended solution") into a reusable **Countermeasure
  library**: a hazard-keyed catalog where each row carries a *hazard*, a *strength class* (reusing the
  EX-H8 vocabulary, so the existing strength lint covers it), a *locus* (**PNA-intrinsic** vs
  **environmental**), and a *demonstrator*. Seeded from the data-protection-vs-OS-automation research
  (R3): consent-at-own-surface, surface minimization, the data-floor, human-presence gating (intrinsic);
  sandbox-the-agent/`denyRead`, separate-OS-user, MCP per-request/JIT broker, honeytoken+watchdog
  (environmental).
- Adds the **environmental-threats / Harden** concept — a *sibling* of Exceptions (a detected hazard the
  user mitigates with toolkit advice, vs. a user-raised deviation the app handles) — and the four-source
  taxonomy of pressure on the guarantees (Constraints · Exceptions · Environmental threats ·
  User-mediation), plus the line *app-security = build/evaluate/contribute; environment-security =
  harden/advise*. The **Harden** flow's procedure (the advisor skill) is sequenced separately; this
  establishes the concept and its home beside Exceptions.
- **At-rest encryption stays deprecated** (re-confirmed by R3): the catalog favors mediating the access
  path / detecting the intrusion while preserving the PNA's tool-readability promise
  (`CST-PWA-SANDBOX-SEALED`), not scoped at-rest encryption.
- **`tools/tests/lint_selftest.py`** — new fault-injection case pins the strength-class check (which had
  none) against the new catalog's Strength column, closing the same dead-check gap that bit the
  `Reversible:` check in PR #18. `just ci` green (26/26).
- **No new obligation on any design** — EX-H6 stays a SHOULD; the catalog is a menu and the Harden flow
  is advisory. The RFC predicate-split / EX-H7 fail-closed / un-relaxable-floor proposals are
  **unchanged** (still demonstrator-gated; promotion to normative is tracked separately as a follow-up).
- **`docs/PriorArt.md` § Design notes** — rationale entry recorded.

### Fix `swh-save.sh` annotated-tag SWHID + add a regression self-test (toolkit fix)

- **`tools/swh-save.sh` derived the commit with `git rev-parse "$REF"`** — which returns the *tag
  object* hash for an **annotated** tag, not the commit it points to. Archiving from a `git tag -a`
  ref therefore printed a wrong `commit` / `swhid_rev` (the tag-object hash — a SWH *release* — where a
  *revision* belongs), and the manifest lint still accepted it because `swhid_rev` matched the (wrong)
  `commit`. Now peels `^{commit}` (a no-op for branches / lightweight tags / raw SHAs, unwraps an
  annotated tag); `swhid_dir` was already correct via `^{tree}`. Surfaced while archiving the **prm**
  reference design from an annotated tag (#65).
- **`tools/tests/lint_selftest.py`** — new offline regression case builds a throwaway repo with an
  annotated tag and asserts the emitted `swh:1:rev:` is the commit, not the tag object. The Save Code
  Now POST is skipped via a new `SWH_SAVE_NO_REQUEST=1` env so `just ci` stays offline and never spams
  the archive. `just ci` green (25/25).
- **`docs/users-guide.md`** notes that annotated and lightweight tags both pin the commit.
- No spec/AC/contract change; no new obligation on any design.
### PRM: archival completed — Software Heritage SWHIDs recorded (reference design)

- `reference_designs/prm/` flips `archival = "pending"` → `"archived"` now that prm
  [#35](https://github.com/richbodo/prm/pull/35) is squash-merged to `main`. Source pinned at
  `prm@pnt-ref-0.1` (commit `a70d35b`): `swh:1:rev:a70d35bcf5765001322b29d0acdc14b1ae14ae11`,
  `swh:1:dir:9d73887ae6a3b277a9232a5267be359387edb00f`. Save Code Now ingest requested
  (request id 2354495, accepted — async). `evaluate-report.json`'s commit pin re-synced from the
  mid-branch `37806aa` to the accepted commit `a70d35b` (regenerated by prm's deterministic emitter).
  `just ci` green.

### PRM: second reference design + `comms:none` pick + AC-PRM-B/C out of draft (reference design)

- Adds **prm** ([richbodo/prm](https://github.com/richbodo/prm)) as the **2nd PNT reference design**
  (Personal Relationship Manager use case), validated against Toolkit-Version 0.1. Flavor:
  `never-distributed-single-user × native-sqlite-via-filesystem × multi-source-merge-with-dedup ×
  vanilla-js-spa × comms:none × mcp-exposure:shared-only`. New `reference_designs/prm/` (README,
  Architecture.md, design.toml, evaluate-report.json).
- **`spec/axes.md`** — new **`comms:none`** pick (a PNA whose loop stops at *recording* relationship data;
  AC-16/18/19/MCP-B become not-applicable), demonstrated by prm.
- **AC-PRM-B (multi-source dedup) + AC-PRM-C (native-sqlite file-lock) promoted out of `[draft]`** — prm is
  the first design to exercise them (`spec/axes.md`, `spec/use_cases.md`, `spec/PNA_Spec.md` § Scope).
- **PRM use case realized** — `spec/use_cases.md` + `spec/PNA_Spec.md` § Use cases flip from `[draft]` to
  realized-in-prm; the speculative "likely flavor" is replaced with prm's actual picks.
- First never-distributed / build-from-verifiable-source distribution; demonstrates the
  propose→review→apply mutation-mediation loop. Two `partial-conformance` rows (AC-PRM-A, AC-MCP-A) are
  honestly handled — an MCP server cannot identify the consuming LLM. Validated: prm suite **131 passed**;
  toolkit lints (`lint-spec-ids`, `report-fixtures-lint`, `attestation-evidence-lint` vs the live repo) green.
- `archival = "pending"` — SWHIDs recorded post-merge via `tools/swh-save.sh` against the attested commit
  (`37806aa`). Deferred riders (AC-PRM-E/F, the UM-1/2/3 framework, the distribution-verifiability split)
  are a planned follow-up, not part of this PR.

### Docs: name the canonical evaluate-report artifact + recognize a deterministic emitter (toolkit fix)

- An audit of `fellows_local_db` mistook its design-internal `docs/conformance/report.json` (a
  fellows-format ship-gate readout) for the toolkit's render-contract artifact, which is
  `evaluate-report.json`. Clarified across the docs so the two can't be confused:
  - **`CONTRIBUTING.md` § PR contents** now names the **canonical filename (`evaluate-report.json`)**,
    states that a design's *other* conformance readouts are not this artifact, and recognizes **two
    equally-valid producers** — the skill's LLM evaluate flow *or* a design's deterministic
    `[verify].entrypoint` emitter (e.g. `just evaluate-report`).
  - **`pna-toolkit/SKILL.md`** — evaluate-flow step 7 tells the agent to confirm which file
    is a schema instance when a candidate ships several, and to prefer a cooperating design's
    deterministic emitter; PR-authoring step 6 now lists `evaluate-report.json` among the required PR
    artifacts (it was previously omitted there, though § PR contents already required it).
  - **`docs/users-guide.md`** audit step notes the canonical filename and the internal-readout trap.
- No new obligation on any design — the artifact was already required by `CONTRIBUTING.md` § PR
  contents; this is purely a naming/discoverability clarification. `just ci` green.

### Visual Validator: clearer end-user caveat + link to the spec Goals (toolkit fix)

- **`tools/report-viewer/index.html`** — the end-user posture caveat now states what the test
  *is* ("a measurement of the application's architecture") and what a **good** result means
  ("its architecture matches the PNA spec closely, and is architecturally aligned with the
  **goals of a PNA**"), with "goals of a PNA" linked to [`spec/PNA_Spec.md` § Goals](spec/PNA_Spec.md#goals).
  Rendered as a real `<a>` via the existing `safeLink()` helper (no `innerHTML`); the viewer stays
  static / zero-dep / engine-agnostic. No render-contract or schema change; the broader plain-language
  rework of the end-user register is tracked in #62.

### Tier-0 keystone complete: `fellows_local_db` archived with a live `[verify]` entrypoint (toolkit fix)

- **`reference_designs/fellows_local_db/design.toml` flipped `archival = "pending" → "archived"`**,
  re-pinned to fellows `main` @ **`dc3e0cf`** (the post-#267 state) with `swhid_rev`/`swhid_dir`
  recomputed by `tools/swh-save.sh` (SH *Save Code Now* request `2352911`, 2026-06-09; SWHIDs are
  git-content-addressed, so valid independent of async ingest). The `[verify].entrypoint` is now
  **`just evaluate-report`** — fellows PR #267's deterministic, stdlib emitter that derives a
  schema-valid `evaluate-report.json` from the attestation table (byte-stable, CI-able). This is the
  first archived reference design with a reproducible verify command, **activating conformance-suite
  Phase 4** and satisfying README success criteria 1/4/6.
- **`reference_designs/fellows_local_db/Architecture.md` re-synced** to the archived commit — picks up
  fellows' **User-mediation attestation** (UM-1/2/3 + the mediated-boundary registry, #265), the
  EAR-is-a-non-goal / encrypt-**in-transit** note, and the updated `CST-PWA-*` rows. README SWHIDs
  reconciled to match the manifest. Authoritative `attestation-evidence-lint` against the fellows
  checkout is green (every `conformant` row cites live, non-deferred evidence).
- **`tools/tests/lint_selftest.py`** — re-anchored the two `design.toml` fault-injection cases
  (archived-without-pin; malformed SWHID) to the new archived manifest, in the same change (lint
  discipline: a check's self-test moves with the artifact it anchors on). `just ci` green (24/24).
- No spec/AC/contract change; no new obligation on any design. Manifest *values* changed, not fields,
  so no `docs/users-guide.md` change is required (the archival flow it documents is unchanged).

### CI: bump GitHub Actions off Node 20 (toolkit fix)

- Bumped the pinned action majors ahead of GitHub forcing Node 24 on **2026-06-16**:
  `actions/checkout@v4 → @v6`, `actions/setup-python@v5 → @v6` (and `actions/cache@v4 → @v5` where used).
  Applies to `spec-lint.yml` + `conformance.yml`; the new `viewer-e2e.yml` is bumped in its own
  (unmerged) PR so it lands Node-24-correct. CI behavior unchanged — `just ci` is local-only and uses
  no actions.

### Plan: Visual Validator browser-render testing (Playwright) (toolkit fix)

- **New `plans/viewer-e2e-testing-plan.md`** — a phased plan to add real-browser render tests for the
  viewer (`tools/report-viewer/`), mirroring `fellows_local_db`'s Python-Playwright setup shrunk to a
  static-file viewer (stdlib `http.server` fixture; no app server). Records the **scoped convention
  exception**: an opt-in `pytest` + `pytest-playwright` suite (`just test-viewer`, deps in a new
  `requirements-dev.txt`) running in its **own** CI job — the toolkit's sole sanctioned third-party /
  pytest dependency, scoped to browser-UI rendering and **never** part of the stdlib-only `just ci`.
  Planning artifact only — no deps added yet, no spec/AC/contract change.

### Visual Validator Phase 5: report-set flip-through + `just view-reports` (toolkit fix)

- **`tools/report-viewer/index.html`** now loads a **set** of reports and flips through them with
  **‹ Prev / Next ›**, **← / →**, or a jump dropdown (with a position indicator) — the view mode
  (developer / end-user / side-by-side) is preserved across flips. Load a set via multi-file
  drag-drop / file-picker, `?reports=a,b,c`, or `?dir=<path>` (fetches `<path>/index.json`, an array
  of filenames). A single report renders with no nav, as before.
- **`just view-reports [dir]`** — serves the viewer (stdlib `http.server`, port 8009) and opens it
  pointed at a directory of reports; no arg flips through the three bundled samples. (`tools/report-viewer/_reports`
  is a transient symlink it creates for a custom dir, gitignored + cleaned up on exit.)
- **e2e:** the Playwright suite grows to **13 tests** — adds flip-through via `?reports=` and a
  `?dir=` manifest, mode-preserved-across-flip, and single-report-has-no-nav. Verified: 13 passed in
  headless Chromium; screenshot confirmed the nav + side-by-side. Implements
  [`plans/visual-validator-plan.md`](plans/visual-validator-plan.md) Phase 5. `just ci` unchanged (24/24).

### Visual Validator e2e CI job — `viewer-e2e` (e2e plan Phase 3) (toolkit fix)

- **`.github/workflows/viewer-e2e.yml`** — a dedicated GitHub Actions job that installs Playwright +
  Chromium (browser cache keyed on `requirements-dev.txt`) and runs the viewer render suite
  (`python -m pytest tools/report-viewer/tests/`) on every PR that touches the viewer or its deps.
  It is the **one** non-stdlib CI job, deliberately a separate workflow from the bare-`python3`
  `spec-lint.yml` jobs — `just ci` is unaffected. Completes
  [`plans/viewer-e2e-testing-plan.md`](plans/viewer-e2e-testing-plan.md) Phase 3; the viewer is now
  gated in CI. `docs/users-guide.md` Status block updated.

### Visual Validator Phase 3: end-user register + side-by-side (toolkit fix)

- **`tools/report-viewer/index.html`** now renders a report in **two registers from the same JSON**:
  the developer (A0) view (Phase 2) and a plain-language **end-user (A1)** view — good / at-risk /
  how-to-be-safer, organized by Goal, with the liability-safe caveat ("measured against this spec's
  promises; the app may not be trying to be a PNA"). A segmented **view-mode control** — `end-user` ·
  `side-by-side` (finding-aligned) · `developer` — persists in `localStorage` and is deep-linkable via
  `?mode=`. Side-by-side pairs each finding's plain-language and technical cells in one aligned grid
  row — the educational payoff. Still static / zero-dep / engine-agnostic; DOM built with `textContent`.
- **e2e:** the Playwright suite grows to **9 tests** covering both registers, the side-by-side
  alignment, and the live mode toggle (`just test-viewer`); a captured screenshot confirmed the
  rendering. Implements [`plans/visual-validator-plan.md`](plans/visual-validator-plan.md) Phase 3.
  `just ci` unchanged (24/24).

### Visual Validator browser-render tests — Playwright (e2e plan Phases 1–2) (toolkit fix)

- **`tools/report-viewer/tests/`** — an opt-in Playwright suite that render-tests the viewer in a real
  browser (6 tests: the three samples render with the right posture / finding count / `ac_id`s /
  evidence-source badges / title and no console errors, plus the empty-state and malformed-report
  error paths). Closes the VV Phase-2 "render unverified" gap; verified load-bearing (making
  `broken.json` valid turns the error-path test red).
- **Harness:** a stdlib `http.server` fixture serves `tools/report-viewer/` on port **8791** (distinct
  from fellows 8765 / PRM 8770); `just setup-test` installs the deps (`requirements-dev.txt`: pytest,
  playwright, pytest-playwright) + Chromium; `just test-viewer` runs the suite.
- **Scoped convention exception** (the toolkit's first third-party / pytest dep) recorded in
  `CLAUDE.md` § Conventions + Worktrees: it runs in its **own** CI job and is **never** part of
  `just ci`, which stays bare `python3` (24/24, unaffected). `docs/users-guide.md` updated. Implements
  [`plans/viewer-e2e-testing-plan.md`](plans/viewer-e2e-testing-plan.md) Phases 1–2; Phase 3 (the
  dedicated CI job) is a follow-up.

### Visual Validator Phase 2: single-report renderer (toolkit fix)

- **`tools/report-viewer/index.html`** — a static, zero-dependency, engine-agnostic vanilla-JS
  viewer (no build / framework / network / Chromium-only APIs; DOM built with `textContent` so report
  strings can't inject HTML). Loads a report via drag-drop, file picker, `?report=<path>`, or the
  bundled-sample buttons, and renders the **developer register**: candidate header + axis picks,
  summary posture + status counts + leading concerns, and a card per finding (status, goals,
  requirement, rationale, citations, evidence tagged `deterministic`/`llm`/`human`,
  `needs_human_review`). Implements [`plans/visual-validator-plan.md`](plans/visual-validator-plan.md)
  Phase 2; Phase 3 adds the end-user register + the side-by-side view. Drag-drop / file-picker work
  over `file://`; `?report=` and the sample buttons need `python3 -m http.server`.

### Visual Validator Phase 1: sample reports + render-contract lint (toolkit fix)

- **`tools/report-viewer/sample-reports/`** — three valid `evaluate-report.schema.json` instances
  (a `conformant` Minimum-Viable-PNA; a `non-conformant` leaky app with an undeclared `EX-CLOUD-LLM`
  deviation; a `mixed` report modeled on fellows with EX-/CST-handling referenced *inside* the AC
  findings, and evidence from all three sources). The Visual Validator's render fixtures + render
  contract. **EX-*/CST- note:** the v0.1 report schema is AC-keyed (`ac_id` matches `^AC-…$`), so
  exceptions and constraints are referenced within the AC findings they bear on, not as top-level
  keys (a SKILL ↔ schema reconciliation tracked separately).
- **`tools/report-fixtures-lint.py`** — stdlib render-contract lint (required keys, summary posture,
  and the per-finding `ac_id`/`status` + status-conditional rules the viewer relies on). `just
  report-lint <path>` runs it against the samples or any report directory. Fault-injection self-test
  wired into `tools/tests/lint_selftest.py` (clean samples pass; a `conformant`-without-`citations`
  dirty fixture fails) per the lint-discipline rule. `docs/users-guide.md` command table + tools list
  updated. Implements [`plans/visual-validator-plan.md`](plans/visual-validator-plan.md) Phase 1.

### Worktree note + per-wave instance ownership (toolkit fix)

- **`CLAUDE.md`** gains a **Worktrees** section: worktrees are cheap and fully isolated here (no
  server/port/DB/build artifacts; `just ci` runs against a tempdir copy), so concurrent worktrees
  need no setup or serialization — unlike the app reference designs, which gate on a shared workspace
  port. Supports the one-Claude-Code-instance-per-repo working model.
- **`docs/roadmap.md`** annotates each cross-repo execution wave with its **owning instance**
  (Wave 1 → fellows, 2–3 → toolkit, 4 → prm, 5 → fellows→toolkit) so work dispatches as "do Wave N."
  Also records a second gate on the Wave-2 keystone: the `[verify].entrypoint` needs fellows to emit
  a schema-shaped `evaluate-report.json` (its own `conformance_report_and_gate.md`), separate from
  the Wave-1 merges.

### Consolidated roadmap + inbound-findings registry (toolkit fix)

- **New `docs/roadmap.md`** — the prioritization/sequencing layer above the per-plan phases:
  dependency-ordered priority tiers (Tier 0 = finalize the fellows attestation keystone, which is
  ~80% done; Tier 1 = PRM as the second reference design carrying the distribution-axis split; then
  the value-driven surfaces and the tracked inbound findings), a dependency graph, an
  **inbound-findings registry** that tracks reference-design findings as demonstrator-gated
  spec-change candidates, a **cross-repo execution order** (Waves 1–5) over every open issue/PR
  across fellows_local_db / prm / the toolkit with an open-work utility classification, and a
  **deprecations map** (encryption-at-rest for the live store retired — the "lock my data" lineage,
  fellows #154/#155/#256/PR #258 — reframed to encrypt-in-transit). dwebcamp dropped as a forcing
  function this cycle (sequence by dependency, not calendar). `README.md` § Status now links it.
  Planning artifact only — no spec/AC/contract change.
- **Cross-repo sync (GitHub):** the three recent `fellows_local_db` findings now have toolkit tracking
  issues under the new `inbound-finding` label — #40 (workspace user-mediation invariant → candidate
  3rd general mechanism, ⇄ fellows#252), #41 (EAR rejected for the live store; encrypt-the-export
  kernel, ⇄ fellows#256), #42 (cross-device over commodity channels, ⇄ fellows#257) — and the
  distribution-axis finding is bidirectionally linked (#39 ⇄ prm#8).

### Visual Validator plan + Chromium-only capability-gap note (toolkit fix)

- **New plan `plans/visual-validator-plan.md`** — a phased plan for a static, zero-dependency,
  engine-agnostic HTML/JS viewer (under `tools/report-viewer/`) that renders
  `tools/evaluate-report.schema.json` instances in a developer **and** an end-user register —
  shown toggled or **finding-aligned side by side** (the educational payoff) — building to a
  directory-of-reports ←/→ flip-through (the home doubling as a cron-job reports drop on a dev
  box). Planning artifact only — no spec/AC/contract change, no behavior change.
- **`spec/constraints.md`** — added a non-normative *Chromium-only capability gap* implementation
  note consolidating that user-visible durable local file/folder access (the File System Access
  API: `showDirectoryPicker` / `showOpenFilePicker` / `showSaveFilePicker`) is Chromium-only, and
  linking the existing `CST-PWA-PRIVATE-SNAPSHOT` / `CST-PWA-SANDBOX-SEALED` ceilings for the
  consequences. Clarification only — no `CST-*`/AC/EX ID added or changed; lint + self-tests green.

### Mission-forward Preamble + new vocabulary: personal network / contact data / relationship data (toolkit fix)

- **Rewrote the `spec/PNA_Spec.md` Preamble** to lead with the spec's role ("defines what an application must *prove*"), define a **personal network** as the egocentric, you-at-the-center graph, frame the highest-leverage claim explicitly as a *wager*, add the AI-OS "*where* does software act over your relationships" framing, and carry the social-network-health "why" in one sober sentence + an evidence-safe footnote (correlate, not cause; mental-health pathway). Added three first-class **Vocabulary** terms mapped onto the existing shared/private split — **contact data** (→ Shared DB), **personal network**, **relationship data** ("private relationship memory" → Private DB). Prose/definitions only — no Toolkit-Version bump, no AC/EX/CST/sub-contract ID changed.

### Project renamed to "PNA Toolkit"; "PNT" acronym retired (toolkit fix)

- **Project name changed from "Personal Network Toolkit (PNT)" to "PNA Toolkit".** The "PNT" acronym is retired across the docs, spec prose, skill, templates, plans, and code comments in favor of "PNA Toolkit" (first mention / headings / titles) and "the toolkit" (subsequent in-prose mentions). Cosmetic rename only — **no Toolkit-Version bump**, no AC/EX/CST/sub-contract ID changed, no behavior changed. The **repo slug `personal_network_toolkit` and all `github.com/...` URLs are unchanged**, so existing clones, links, and cross-repo references (including `fellows_local_db`'s) still resolve. The predecessor "Personal Relationship Toolkit" (PRT) name is untouched.

### Proposed (RFC, separate follow-up to #32): architectural data-floor — disclosure tiers

> **Status: RFC stub, not in this repo's normative tables yet.** Lands with the PRM reference design
> that demonstrates it (per `CONTRIBUTING.md` § Contribution types). Companion to PR #32. Full stub:
> `docs/design-notes/2026-06-data-floor-disclosure-tiers.md`.

- Proposes bounding *what* an exception can disclose (not just the act of disclosing): a per-field
  Private-DB `disclosure_tier` (**`PR-7`**, default `private-sealed`, workspace-only mutable, enforced
  at the query layer), a projection-bound cloud MCP surface that structurally cannot return a sealed
  field even with consent (**`AC-MCP-C`**, the data twin of AC-MCP-B's action-floor), and a
  blast-radius strength dimension (**`EX-H9`**) — verified by a static disclosure-tier lint + a dynamic
  egress probe. Came out of the moderated tournament of alternate solutions recorded in the existential
  review. Doc-only in this PR; no normative table changed (lint + self-tests green).
### Proposed (RFC — not yet accepted): honest-exit amendments to the Exceptions mechanism

> **Status: RFC, opened for maintainer consideration — not merged behavior.** Changes (2) and (3)
> impose new obligations on designs, so per `CONTRIBUTING.md` § Contribution types they require a
> demonstrating reference design before acceptance. Rationale:
> `docs/design-notes/2026-06-exceptions-existential-review.md`.

- **(1) Predicate split (clarification).** `spec/exceptions.md` § Concept + `spec/PNA_Spec.md`
  (`vocab-pna`, § Vision, § Composition): the overloaded "conformant PNA in non-PNA mode" is split
  into two reported predicates — **`pna-active`** (the mode bit; `false` while any exception is
  active; the categorical "is it a PNA right now?" claim a relying party keys on) and
  **`exception-handling`** reported *per handler clause* (`pass`/`partial`/`cannot-tell`, EARL-style).
  Discipline (refined): **`pna-active` is the only conferred verdict and the only interop key**;
  handling is never aggregated into a "conformant" badge, and `tools/evaluate-report.schema.json`'s
  `summary.posture` is redefined to report PNA membership only (so a cleanly-handled `EX-CLOUD-LLM`
  app can never surface `posture: conformant`). The interop future-direction gates on `pna-active`,
  not on exception-handling conformance.
- **(2) EX-H7 fail-closed.** `spec/exceptions.md` § Handler contract: consent for a Private-DB
  exception MUST be obtained on a PNA-controlled surface (`enforced`), the PNA SHOULD relay a
  best-effort "confirm in the app" notice to cooperating clients via the MCP `instructions` handshake,
  and where it cannot confirm a human consented it MUST fail closed (AC-MCP-A's "either refuse" arm)
  rather than raise on a proxy's say-so. Refined: the gate is **workspace-bound** (a cloud client
  can't forge a workspace-side human action, so it is genuinely `enforced`) and is a real but
  **secondary** control governing the *act* of disclosure — bounding *what* may be disclosed is the
  data-floor (4).
- **(3) Un-relaxable floor.** `spec/exceptions.md` § Scope discipline: AC-18, AC-19, and AC-MCP-B are
  a floor no exception may relax even with consent (a user may consent to *disclose data they read*,
  never to remove the human-in-the-loop on action taken on their behalf, which reaches third parties).
  This is the *action*-floor; the symmetric *data*-floor is the separately-tracked correction (4).
- **(4) Architectural data-floor (separate follow-up, demonstrated by PRM).** Out of a follow-up
  review: bound *what* an exception can disclose, not just the act. A per-field Private-DB disclosure
  tier (`PR-7`, default most-protective), a projection-bound cloud surface that structurally cannot
  return a sealed field even with consent (`AC-MCP-C`), and a blast-radius strength dimension
  (`EX-H9`). Drafted as its own proposal (`docs/design-notes/2026-06-data-floor-disclosure-tiers.md`);
  not part of this PR's diff — it lands with the PRM reference design that demonstrates it.
- Lint + self-tests stay green (prose-only; no machine-parsed table changed).

### Slots optionality + the Minimum Viable PNA use case (normative clarification)

- **Required vs optional slots clarified.** Only **Ingestion, Storage, and Workspace** are required; **Communications and Distribution are optional** (previously only Distribution was marked optional). A PNA that never reaches out omits Communications — its comms ACs (AC-16/18/19) are then vacuous, mirroring how the MCP ACs are vacuous when no MCP server is exposed. This is a **relaxation**: every existing design (which has all slots) stays conformant; it just lets a smaller app qualify. See `spec/PNA_Spec.md` § Slots, Interfaces, and Sub-contracts.
- **New use case — Minimum Viable PNA ("Personal Vault").** The smallest conformant shape: Ingestion + Storage + a minimal Workspace, no Communications, no Distribution — a local mirror of your contacts plus a private overlay you add via a CLI; nothing leaves the device. Added to `spec/use_cases.md` and the PNA_Spec use-cases list (README / SKILL / llms.txt summaries updated to match).
- **Workspace stays required — MCP can't replace it (v0.1).** The Workspace bundles three roles: render, write-private-data, and the human-in-the-loop consent boundary. MCP servers can *add* an AI-driven surface but can't replace the Workspace in v0.1, because the data-ops MCP servers are read-only (no private writes via MCP) and AC-MCP-A/B make the Workspace the mandatory consent surface (the MCP server proposes; the Workspace disposes). A **headless / MCP-native PNA** is recorded as a v0.2+ direction in `use_cases.md`.

### Design note — existential review of the Exceptions mechanism (toolkit fix)

- Records the deliberation behind the honest-exit RFC ([PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32)): *should the spec allow `EX-*` exceptions at all?* Conclusion — **keep them**; the mechanism isn't the corruption, an unverifiable purity claim would be. New full note at `docs/design-notes/2026-06-exceptions-existential-review.md`, indexed by a dated entry in `docs/PriorArt.md § Design notes`. **Establishes `docs/design-notes/` as the home for full-length notes** that the PriorArt log indexes (short entry in the log; long deliberations as their own files). Doc-only; the spec lint + self-tests are unaffected.

### ID columns moved to the right + header-aware lint + deep-link anchors (toolkit fix)

- **The ID column now sits last** in every ID-bearing spec table — the Universal AC table (`Commitment | Serves | ID`), the axes "Extra commitments these picks add" tables (`Commitment | Applies when you pick | AC`), and the constraints + exceptions registries — so a human reads the commitment before the ID. **No AC/EX/CST ID changed and every `<a id>` deep-link anchor is preserved** (verified), so PR #27's external references (which `fellows_local_db` relies on) still resolve.
- **`tools/lint-spec-ids.py` is now header-aware.** It locates each ID column by *header name* (not position) via a shared `iter_tables()` helper, so column order no longer matters; `parse_constraint_table` is likewise keyed by header. Self-tests stay green (22/22).
- **Deep-link anchors extended.** Slots (`#slot-storage`), interfaces (`#iface-shared-schema`), and all 58 sub-contracts (`#ws-1` … `#db-9`) now carry `<a id>` anchors so conformance reports can link to them the way they already link to ACs (`fellows_local_db` cites `PR-6` etc. by name with no link today).
- **Editing notes.** Each spec file with a machine-parsed table carries a top-of-file note that its tables are read by the lint *and* external report writers, and must be updated in lockstep if their columns / headers / IDs change.
- **Note for report writers:** because the table column *order* changed, any *positional* parser of these tables (e.g. a conformance-report builder) must be updated; the IDs and anchors themselves are unchanged.

### Spec readability pass — PNA_Spec.md + axes.md (toolkit fix)

- **`spec/PNA_Spec.md` restructured for readability**, with no change to any AC, anchor, or ID (the lint and the external `#ac-*`/`#vocab-*` deep links from #27 are untouched): merged Vision into the Preamble; relocated "Building a PNA" into Composition and tied it to the skill's three flows; demoted the misnamed "Target environments for one PNA" to an informal "Common axis clusters" note; renamed "Slot map" → "**Slots, Interfaces, and Sub-contracts**" (old `#slot-map` anchor preserved) with a "reference — skip unless implementing" signpost; alphabetized the Vocabulary.
- **`spec/axes.md` plain-English pass**: each per-axis "Triggered flavor-derived ACs" table is now "**Extra commitments these picks add**"; the cryptic "Triggered by" `[dist:server-backed]` column becomes a plain-English "**Applies when you pick**" column, and the tables now lead with the commitment (the AC ID stays in column 1 for the lint). "flavor-derived AC" is **glossed** as a *conditional commitment*, not renamed (the term is load-bearing in the skill and artifacts).
- **Editor notes** added above every lint-parsed table (`PNA_Spec.md` AC table; `axes.md` AC tables; `constraints.md` registry) warning that the table is machine-parsed — a column reorder must be matched by a `tools/lint-spec-ids.py` update plus a `tools/tests/lint_selftest.py` case. IDs/columns are kept consistent precisely because the lints depend on them.

### Stable per-ID anchors for AC / CST / EX (additive)

- **Every AC, CST, and EX now carries a stable HTML anchor** so a reference design's conformance report (and any cross-reference) can deep-link to the *specific* commitment/constraint/exception instead of dumping the reader at the top of a multi-section spec. The anchor id is the lowercased ID: `#ac-1`, `#ac-prm-a`, `#cst-pwa-sandbox-sealed`, `#ex-cloud-llm`, etc. Added as `<a id="…"></a>` inside the ID cell of each AC table row (`spec/PNA_Spec.md` ×16, `spec/axes.md` ×9) and on the line above each `### CST-…` / `### EX-…` detail heading (`spec/constraints.md` ×7, `spec/exceptions.md` ×1) — 33 anchors, no prose change.
- **`tools/lint-spec-ids.py`** — the `AC_RE` / `EX_RE` / `CST_RE` registry-row regexes now tolerate the optional `<a id="…"></a>` cell prefix (shared `_CELL_ANCHOR`), so ID extraction is unchanged. The clean tree (which now carries the anchors) exercises this, and `tools/tests/lint_selftest.py` stays 22/22.
- Motivated by `richbodo/fellows_local_db`'s conformance report, which links each attested row back to its toolkit definition; doc-level links to a 50-section spec were too much cross-repo context to hold.

### Attestation-evidence lint + deferral discipline (additive)

- **`tools/attestation-evidence-lint.py` (new).** The portable attestation checker the `ARCHITECTURE_TEMPLATE.md` § "Mechanical check" only *described* in prose is now a real stdlib lint, with `tools/attestation-evidence-lint-fixtures/{clean,dirty}` and three new `tools/tests/lint_selftest.py` cases (21/21). It parses a design's AC/CST attestation table and fails when a `conformant` row's evidence isn't real. Beyond the prose checker's existence-only rule, it adds the **marker-state** check: a `conformant` row may not cite an `xfail` or unconditional `skip` test — a declared-false/unrun invariant is not evidence (a conditional `skipif` guard is exempt). Closes the seam where a reference design cited `xfail(strict=True)` as proof and every gate stayed green. Emits `--json` evaluate-report evidence like the sibling lints.
- **`ARCHITECTURE_TEMPLATE.md` — deferral discipline + validation timing.** Deferrals now carry a machine-readable `tracking: #NNN` **issue** anchor (issue, not PR — issues close when the work is done); the **asymmetry** of `strict=True` is named (trips on accidental success, never on abandoned deferral) with two reinforcements (abandoned-deferral check when the tracker reports issue state; a low deferral cap). A new **Validation timing** note states the load-bearing principle — *non-conforming code must not reach users* — and that the suite runs at the user-exposure boundary (ship / per-PR / release), with feature add/remove as the re-check trigger; the cap is secondary hygiene, the gate is the mechanism.
- **`SKILL.md`.** Evaluate-flow attestation audit points at the real lint and names the deterministic-vs-runtime layering ("exists" is the lint; "passes" is the suite); deferral guidance switched to the issue anchor; contribute-flow preflight blockers gain the xfail/skip-as-evidence and unanchored-deferral findings.
- **`docs/PriorArt.md § Design notes`.** Records the finding and its reusable lesson (a portable existence checker created false confidence the passing check was covered; the deterministic/runtime seam was unowned). Distilled from `richbodo/fellows_local_db#249`. (Filed via the toolkit-fix contribution path.)
### Command consistency — contributor docs use `just` (toolkit fix)

- The contributor-facing checklists and skill now reference the `just` entry point introduced in the docs work, instead of bare `python tools/lint-spec-ids.py`: `just lint` in the PR template's reference-design checklist, `just ci` (lint + self-tests) in `CONTRIBUTING.md` § Contribution types and the skill's Toolkit-fix flow. (CI still calls the tools directly; this is human-facing prose only.) Mechanical consistency fix — the first contribution authored through the newly first-classed *Toolkit fix* path.

### Contribution types — toolkit fix vs reference design (process, additive)

- **The toolkit-fix path is now first-class and discoverable.** A "Toolkit fix" PR type already existed in `.github/pull_request_template.md` and was acknowledged in passing under `CONTRIBUTING.md § Versioning`, but the **skill** (the LLM entry point) documented only the heavyweight reference-design flow, and the template shipped no toolkit-fix checklist — so an agent contributing a lint/docs/scope change had no path to follow and would wrongly force it through reference-design preflight. Since most PRs to the toolkit are toolkit fixes, the dominant case was the undocumented one.
- **`pna-toolkit/SKILL.md`.** The Contribute flow now opens with a **routing heuristic** — *does the change impose a new contract a conformant design must satisfy?* — splitting into *Reference-design contribution* (the existing flow) and a new *Toolkit fix* sub-flow (normal PR; `tools/lint-spec-ids.py` + fixture self-tests; CHANGELOG entry; a `docs/PriorArt.md § Design notes` entry for decisions; check the Type box). [PR #19](https://github.com/richbodo/personal_network_toolkit/pull/19) (a scope decision that declined an AC) is cited as the canonical toolkit fix.
- **`CONTRIBUTING.md`.** New *Contribution types* section near the top with the same routing question; *What we don't accept* nuanced so a spec note that clarifies/declines a commitment is correctly a toolkit fix, not a forbidden undemonstrated spec change.
- **`.github/pull_request_template.md`.** Adds a lightweight **Toolkit-fix checklist** (no new design obligation; CHANGELOG; Design-notes entry for decisions) alongside the reference-design one, with a routing comment in the Type section.

### Documentation — `CLAUDE.md`, task-ordered users-guide, doc-currency rule (process, additive)

- **New `CLAUDE.md`.** Repo conventions plus a **documentation map** — one source of truth per fact (spec = normative, `pna-toolkit/SKILL.md` = agent procedure, `docs/users-guide.md` = task-ordered how-to, `CONTRIBUTING.md` = policy; docs link rather than restate) — the stdlib-only / RFC 2119 / versioned-as-a-unit conventions, and the lint-discipline rule (every check needs a fault-injection self-test in `tools/tests/lint_selftest.py`).
- **`docs/users-guide.md` re-architected** to be task-ordered: `Install the skill` + `Using the skill` (Build / Audit / Contribute) + `Working in this repo` (the `just` menu, one plain line per recipe) + `Contributing beyond reference designs`. The incoherent Goal 4 (archival) and Goal 5 (versioning) dissolved into the Contribute flow's tail (pointing to `CONTRIBUTING` for policy rather than restating it); the Goal 6 attestation steps folded into Build. Stale facts fixed (`swh-save` shipped; `just` commands replace bare `python3`; Constraints, Exceptions, and `design.toml` now documented).
- **Doc-currency rule.** Any PR that changes a developer-visible behavior updates `docs/users-guide.md` in the **same PR** — stated in `CLAUDE.md` and enforced by a checkbox in the PR template's new **Every PR** section. The docs had drifted behind the code (justfile, self-tests, export lint, Constraints/Exceptions, manifests all undocumented); this stops the recurrence.

### Conformance suite — toolkit self-tests + machine-readable design records (additive)

- **Tier A — toolkit self-tests.** `tools/tests/lint_selftest.py` (stdlib-only) asserts the clean tree passes the lints, then applies a catalog of named fault injections and asserts each makes the right lint fail with the expected message — pinning the lints' own behavior so a check can't silently rot (cf. the dead `Reversible:` check found in PR #18). A `justfile` (`just` shows the menu; `just ci` runs lint + self-tests; `just egress-lint`/`export-lint`/`swh-save` wrap the other tools) and a `lint-selftest` CI job run it.
- **Tier B groundwork — machine-readable design records.** `reference_designs/templates/design.toml` + `reference_designs/fellows_local_db/design.toml`: the conformance suite's source of truth (repo, `[flavor]` axis picks, `[verify]` entrypoint, and the git-compatible SWHID pin). `tools/lint-spec-ids.py` validates every manifest: required keys, status/archival vocab, flavor picks resolving per-axis against `axes.md`, and an **honest-deferral rule** — an `archived` design must carry a 40-hex commit + well-formed `swhid_rev`/`swhid_dir` (with `swhid_rev` matching the commit) + a verify entrypoint, while a `pending` (in-flight) design may defer those. A design dir with an `Architecture.md` must carry a manifest. (Also broadened the axis-pick regex to admit `+` in `mcp-exposure` picks like `shared+private+comms`.)
- **Skill + contribution instrumentation.** `SKILL.md` contribute flow authors/refreshes `design.toml` and writes the SWHIDs into it at archival; `CONTRIBUTING.md` lists the manifest as a required PR artifact and as part of the archival step; `tools/swh-save.sh` prints paste-ready `design.toml` fields.
- **Phase 4 scaffold (inert).** `.github/workflows/conformance.yml` (manual + reusable triggers; schedule commented out) and a `just test-design` stub — the fetch-verify-build-run harness, activated when a design declares a runnable `[verify]` entrypoint.
- **Design docs.** [`docs/conformance-scope-and-lifecycle.md`](docs/conformance-scope-and-lifecycle.md) (the utility line — three evaluate output modes; the active/archival reference-design lifecycle; roadmap; the general application-class-blueprint framing) and [`plans/conformance-suite-plan.md`](plans/conformance-suite-plan.md) (the four-phase implementation plan).

### Constraints concept (additive)

- **`spec/constraints.md` (new).** Introduces **Constraints** — the dual of Exceptions: stable-ID'd (`CST-*`) platform/substrate-imposed ceilings, inherited automatically by axis picks, that bound a capability a PNA would otherwise offer. No one raises a Constraint (the platform imposes it); the PNA must *detect* it honestly and *handle* it by per-platform capability reduction. Handling a Constraint does **not** exit PNA mode — the failure mode is over-reach (false durability). Carries the `Triggered-by:`/`Bounds:`/`Frontier:`/`Detectability:` header conventions, two meta-principles (capability presence ≠ usefulness ≠ permanence; reduce at the data layer, not UI-only), and the seven-entry `CST-PWA-*` registry for the `web-bundle` × `opfs-sqlite-wasm` flavor.
- **`tools/lint-spec-ids.py`.** Extended to collect `CST-*` IDs and validate constraint declarations: `Triggered-by:` tokens resolve to the pick set of the *named axis* (per-axis resolution, exact ID or pick-family prefix from `axes.md`); `Bounds:` tokens are valid `AC-*`/`Goal-N`/`PNA-DEFINITION`; `Frontier:` is well-formed (`Open`/`Mitigated`/`Solved-on-<platform>`/`Inherent`) with `Mitigated`/`Solved-*` requiring a `Workaround:`; `Detectability:` is one of `feature-detect`/`empirical-probe`/`ua-sniff`. The summary registry table is validated to the same rules as the detail blocks, and the two are cross-checked for consistency (same set of `CST-*` IDs; matching Triggered-by/Bounds/Frontier/Detectability per entry) so the human-facing table cannot silently drift from the authoritative blocks.
- **`spec/PNA_Spec.md` + `spec/axes.md`.** A Constraints pointer near Goal 4 and in the "Validation, not certification" callout; the triggering picks (`storage:opfs-sqlite-wasm`, `web-bundle-*`) now cross-reference the constraints they inherit. The forced worker-owned single-connection architecture (formerly a separate `CST-PWA-DURABLE-SQL-ARCH` constraint that bounded no user-facing guarantee) is folded into AC-3's prose, where the same worker-owned realization already lives.
- **`pna-toolkit/SKILL.md`.** Build flow gains "enumerate inherited Constraints" after axis selection; evaluate flow gains "detect and verify Constraints" after the exceptions pass (reporting by `CST-*` ID, with over-reach as the backstop).
- **Reference design.** `reference_designs/fellows_local_db/` adds the Constraints contribution note and a § Constraint attestation table demonstrating the handling (the private-data capability gate, folder mode, data-layer browse-only enforcement). Distilled from a real MCP-handoff fragility finding on that design.

### Private-DB portability (PR-6)

- **PR-6: human-readable export (SHOULD).** New Private-schema sub-contract: implementations SHOULD export the Private DB to a flat, tool-free format (CSV per table, schema-embedded JSON, or a Markdown vault) *in addition to* the canonical SQLite file, readable with a generic CSV/JSON/Markdown reader and no PNA tooling. Closes the practical-ownership gap in Goal 4 — owning the bytes is not the same as being able to read them without a SQLite browser. The export is explicitly **one-way**: implementations MUST NOT treat it as a guaranteed re-import surface; re-import stays on the PR-5 SQLite path. Sub-contract count: `PR-` (6), 58 total.
- **`tools/export-readable-lint.py`.** Deterministic PR-6 checker (mirrors `egress-lint.py`): every file in a human-readable export must parse with a Python stdlib reader and require no project code. Clean/dirty fixtures + a CI self-test job. The canonical `.sqlite` binary in an export is the textbook failure it catches. Motivated by mapping the spec against the Ink & Switch "local-first software" ultimate-ownership ideal; see `richbodo/fellows_local_db#216`. Demonstrating reference-design attestation (fellows_local_db) is the companion follow-up.

### Threat-model scope clarification (at-rest encryption)

- **At-rest encryption is not a universal AC — by decision.** `spec/PNA_Spec.md` § Scope and versioning now records that defending against *local device access* (lost/stolen/seized/shared machine) is out of v0.1's threat model: OS full-disk encryption is the right layer, and a boolean "encrypted at rest" AC would invite false assurance and tension with Goal 4 (lost key = lost data). At-rest encryption remains the `native-sqlcipher` flavor with deferred key-management ACs and a required strength profile. Full rationale captured as the first entry in a new **§ Design notes** in `docs/PriorArt.md`, alongside the Ink & Switch local-first ideal-mapping that motivated both this and PR-6. Resolves `richbodo/fellows_local_db#216` proposal 1.

### Lint fix: dead Exceptions `Reversible:`/`Reversal:` check (standalone)

- **`tools/lint-spec-ids.py`.** The `exceptions.md` `Reversible:`/`Reversal:` validation was not actually enforcing anything, for two compounding reasons: (1) `REVERSIBLE_RE` lacked the markdown-bold tolerance (`**Field:**`) that the version-stamp regex has, so it captured *no* value from the `**Reversible:** yes` form the file actually uses — leaving both the `yes|no` well-formedness check and the coupling check dead; and (2) the coupling test was a bare `"Reversal:" not in ex_text` substring check, which the header-conventions prose (which mentions `` `Reversal:` ``) satisfied unconditionally. Fixed `REVERSIBLE_RE` to tolerate the bold form and replaced the substring test with a line-anchored `**Reversal:**` *field* detector. Both checks are now non-vacuous (verified by fault injection). Surfaced while adding the Constraints checks; called out separately because it hardens the pre-existing Exceptions lint, independent of Constraints.

### Formalization pass (Phase 3 of the reorg plan)

- **RFC 2119 normative language.** Every AC and every sub-contract in `spec/PNA_Spec.md` and `spec/axes.md` was reworded so that conformance-bearing statements use MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. Readable prose around the keywords preserved (motivation, examples, why-it-matters). A short "Normative language" note added at the top of each AC-bearing section.
- **Bidirectional traceability (AC ↔ contract).** Every typed contract file in `contracts/` now carries a `Realizes: AC-X, AC-Y` header (as a `$comment` field in JSON Schemas; as a top-of-file comment in YAML / SQL / TypeScript). AC IDs are now the load-bearing join key between spec prose and typed contracts.
- **Spec ID lint.** `tools/lint-spec-ids.py` checks (a) every AC has a stable ID, (b) every contract names at least one AC, (c) every claimed AC exists in the spec. Wired into CI via `.github/workflows/spec-lint.yml`.
- **Software Heritage SWHID declared in the spec.** Added to the reference-design vocabulary entry: v0.1 commits to SWHIDs as the canonical permanent identifier for accepted reference designs.
- **Vision future-direction note.** Added a paragraph about conformance evaluation as a potential precondition for runtime interop between PNAs in a multi-PNA ecosystem (a systems-level test requiring spec rethinking; flagged direction for a later version).
- **Variable-language pass.** Numeric axis counts ("six Axes") replaced with variable language ("the Axes", "these Axes", "the independent Axes") so the spec doesn't drift if the axis set evolves.

### v0.1 baseline

Initial release of the toolkit (PNA Spec + typed contracts). Establishes:

- Vocabulary (Use case, Axis, Axis pick, Flavor, Composition model, MCP server, Universal vs flavor-derived AC).
- Goals (1-5: private data sovereignty, mirror centralized sources locally, secure communication options, portable/durable/recoverable user data, locally diagnosable).
- Use cases attested: Directory Archive (realized in fellows_local_db), Personal Relationship Manager [draft], Multi-PNA ecosystem [target v0.2+].
- Axes: distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure.
- Two target environments for a single PNA (Browser PNAs and CLI / native PNAs) plus one runtime cooperation pattern across PNAs (the ecosystem reference design, mediated by canonical MCP servers).
- Universal ACs: AC-1, AC-4, AC-6, AC-7, AC-9, AC-10, AC-11, AC-15, AC-16, AC-17, AC-18, AC-19, AC-PRM-A, AC-PRM-D, AC-MCP-A, AC-MCP-B (16 in v0.1).
- Flavor-derived ACs: AC-2, AC-3, AC-5, AC-8, AC-12, AC-13, AC-14 from the original set; AC-PRM-B and AC-PRM-C as [draft] PRM-flavor commitments.
- Slot map: five slots (Ingestion, Storage, Workspace, Communications, Distribution) + three interfaces (Shared schema, Private schema, Debug contract).
- Sub-contract decomposition: each slot and interface decomposes into named sub-contracts under a per-slot two-letter prefix — `WS-` (10), `ST-` (11), `IN-` (4), `CO-` (6), `DI-` (6), `SH-` (6), `PR-` (5), `DB-` (9). 57 sub-contracts total in v0.1. Cross-slot threads (build-label discipline, opt-in directory update, restore data flow, capability-failure surfacing, …) are formalized in the same section. The spec is now self-contained: builders can cite sub-contracts by ID without consulting the working triage.
- Five canonical MCP server contracts: Shared Data Ops, Private Data Ops, Ingestion, Communications, Diagnostics. The original "Data operations" server was split along the Shared / Private privacy boundary so AC-MCP-A's cloud-client consent rule targets exactly the Private Data Ops surface — a user can wire a cloud client to Shared Data Ops alone without crossing the boundary. v1 reference implementations of Shared Data Ops, Private Data Ops, and Comms ship in `fellows_local_db/mcp_servers/`; JSON Schemas live alongside this CHANGELOG in `contracts/mcp-shared-data-ops.schema.json`, `mcp-private-data-ops.schema.json`, and `mcp-comms.schema.json`. Ingestion and Diagnostics remain spec stubs (no reference implementation yet).
- MCP-exposure axis picks restructured from {`none`, `data-ops-only`, `data-ops+comms`, `full`} to {`none`, `shared-only`, `shared+private`, `shared+private+comms`, `full`} to reflect the split; fellows_local_db's attested pick is `shared+private+comms`.

Spec scaffolding (`_pna_triage.md` working triage doc + `_pna_spec_format_landscape.md` format-choice notes) retired in v0.1 after all spec-side and repo-side migrations landed. The spec is now self-contained: `spec/PNA_Spec.md`, `spec/axes.md`, `spec/use_cases.md`, and the typed contracts under `contracts/`.

Items deliberately deferred to future versions: privacy reclassification migration mechanics, multi-source dedup migration (beyond AC-PRM-B's draft form), per-database transport requirements, cross-device sync, federated p2p, formal verification.
