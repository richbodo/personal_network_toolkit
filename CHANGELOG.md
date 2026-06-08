# PNA Toolkit Changelog

## v0.1 draft (in progress)

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
- **`pna-build-eval-contrib/SKILL.md`.** The Contribute flow now opens with a **routing heuristic** — *does the change impose a new contract a conformant design must satisfy?* — splitting into *Reference-design contribution* (the existing flow) and a new *Toolkit fix* sub-flow (normal PR; `tools/lint-spec-ids.py` + fixture self-tests; CHANGELOG entry; a `docs/PriorArt.md § Design notes` entry for decisions; check the Type box). [PR #19](https://github.com/richbodo/personal_network_toolkit/pull/19) (a scope decision that declined an AC) is cited as the canonical toolkit fix.
- **`CONTRIBUTING.md`.** New *Contribution types* section near the top with the same routing question; *What we don't accept* nuanced so a spec note that clarifies/declines a commitment is correctly a toolkit fix, not a forbidden undemonstrated spec change.
- **`.github/pull_request_template.md`.** Adds a lightweight **Toolkit-fix checklist** (no new design obligation; CHANGELOG; Design-notes entry for decisions) alongside the reference-design one, with a routing comment in the Type section.

### Documentation — `CLAUDE.md`, task-ordered users-guide, doc-currency rule (process, additive)

- **New `CLAUDE.md`.** Repo conventions plus a **documentation map** — one source of truth per fact (spec = normative, `pna-build-eval-contrib/SKILL.md` = agent procedure, `docs/users-guide.md` = task-ordered how-to, `CONTRIBUTING.md` = policy; docs link rather than restate) — the stdlib-only / RFC 2119 / versioned-as-a-unit conventions, and the lint-discipline rule (every check needs a fault-injection self-test in `tools/tests/lint_selftest.py`).
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
- **`pna-build-eval-contrib/SKILL.md`.** Build flow gains "enumerate inherited Constraints" after axis selection; evaluate flow gains "detect and verify Constraints" after the exceptions pass (reporting by `CST-*` ID, with over-reach as the backstop).
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
