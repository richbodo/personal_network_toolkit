# Conformance suite — implementation plan

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> The *how/when* of building the PNA Toolkit's test machinery. The *why/where's the line*
> reasoning lives in
> [`docs/conformance-scope-and-lifecycle.md`](../docs/conformance-scope-and-lifecycle.md).

## Two lanes, never conflated

- **Tier A — toolkit self-tests.** Tests of the toolkit's *own* checkers (the lints).
  Fast, hermetic, deterministic, run on every PR. No external repos. Pins the
  toolkit's honesty so a check can't silently rot (cf. the dead
  `Reversible:`/`Reversal:` check found in PR #18 review).
- **Tier B — reference-design conformance regression.** Pull a design's real
  source (pinned by SWHID), build it, run its attested verification, report by
  AC/EX/CST. Heavy, flaky-by-nature, run on a schedule / on demand — **never** a
  blocking per-push gate.

A pin (SWHID) tells you *what* source; it does not tell you *how* to replicate a
test. The other half is a **uniform verify entrypoint** every accepted design
exposes. SWHID + verify-entrypoint + a machine-readable record is what makes the
whole thing mechanical.

## Phasing (cheapest-first; 80/20 = Phases 1–3)

### Phase 1 — Toolkit self-tests *(in repo; no SWHID; highest ROI)*
- `tools/tests/lint_selftest.py` — copies the repo to a tempdir, asserts the
  clean tree passes, then applies a catalog of **named fault injections** and
  asserts each makes the relevant lint exit nonzero with the expected message.
  Encodes the PR-18 review probes permanently (constraint table↔block drift,
  cross-axis `Triggered-by`, orphan rows, the dead `Reversible:` coupling, a
  broken contract `Realizes:` header, …). Also exercises egress-lint and
  export-readable-lint against their existing clean/dirty fixtures.
- `justfile` — `just lint`, `just test` (self-tests), `just` default → `test`.
- CI: a `lint-selftest` job in `.github/workflows/spec-lint.yml` (calls the
  Python directly; no `just` dependency in CI).
- **Done-when:** clean → green; every injected fault → red with its message; CI
  job green. Dependency-free (stdlib only, py3.11).

### Phase 2 — Machine-readable design record + SWHID lint *(in repo; "demand SWHIDs")*
- `reference_designs/templates/design.toml` — the manifest template: `name`,
  `repo`, `commit`, `swhid_dir`, `swhid_rev`, `toolkit_version`, `status`
  (active|archived|superseded), `archival` (pending|archived), `[flavor]` (axis
  picks), `[verify]` (`runner`, `entrypoint`).
- `lint-spec-ids.py` gains a constraint-style check over every
  `reference_designs/<name>/design.toml`:
  - required keys present; `status`/`archival` from their fixed vocab; `[flavor]`
    axes + picks resolve against `axes.md`; `[verify].entrypoint` non-empty.
  - **honest-deferral rule:** when `archival = "archived"`, all of `commit`,
    `swhid_dir`, `swhid_rev`, `[verify].entrypoint` MUST be present and
    well-formed, and `swhid_rev` MUST equal `swh:1:rev:<commit>`. When
    `archival = "pending"`, those MAY be empty (an in-flight design) — but any
    non-empty value MUST still be well-formed. SWHIDs are git-compatible, so
    `swhid_dir` is recomputable later via `git rev-parse <commit>^{tree}`.
  - any `reference_designs/<name>/` containing an `Architecture.md` MUST carry a
    `design.toml` (an accepted design needs a manifest).
- `reference_designs/fellows_local_db/design.toml` — a *truthful* manifest:
  `status = "active"`, `archival = "pending"` (its SWHID backfill is Phase-5
  pending per the repo README), real `repo`/`flavor`/`toolkit_version`, and
  TODO-marked empties for `commit`/SWHIDs/verify until the maintainer fills them.
- **Done-when:** lint validates the manifest shape + consistency; fellows passes
  as a pending design; self-tests gain manifest fault injections.

### Phase 3 — Instrument the skill for submission *(text; lint-verifiable)*
- `SKILL.md` contribute flow: a step to **author/refresh `design.toml`**, run
  `swh-save.sh` at archival, and write the returned `swh:1:dir`/`swh:1:rev` +
  `commit` into the manifest (flip `archival` to `archived`).
- `CONTRIBUTING.md`: the design record now includes `design.toml`; the archival
  step records the SWHID *into the manifest* (not just prose).
- `swh-save.sh`: a closing hint pointing at the manifest fields to fill.
- **Done-when:** the contribute flow produces a manifest, and submission is one
  guided path; lint green.

### Phase 4 — Build-and-test harness *(scaffold now; activates with first design)*

**Purpose — this is the step that turns "exists" into "passes."** The
[`attestation-evidence-lint`](../tools/attestation-evidence-lint.py) proves a cited
test *exists and is live*; only *running* it proves it *passes* — the gap
[`SKILL.md`](../pna-toolkit/SKILL.md) names ("a static lint cannot prove the test
passes … Confirm passing by running the design's suite"). Phase 4 is that runner. A
working reference implementation of exactly this shape — fetch the artifact, run its
evidence read-only, fold the result into one typed report — is CLI Printing Press's
`verify`/`shipcheck`; the borrows below (and several of the hard parts) trace to that
study: [`docs/design-notes/2026-06-printing-press-build-validation-flows.md`](../docs/design-notes/2026-06-printing-press-build-validation-flows.md)
(R1, R5, R7).

- `just test-design <name>` / `just test-designs`: read the manifest, fetch
  (`git clone --depth 1 <repo>` + checkout `commit`; SH vault as fallback),
  verify `git rev-parse HEAD^{tree} == swhid_dir`, run `[verify].entrypoint`
  inside its container, emit an `evaluate-report.json` instance.
- **Re-validate against the *pinned* source, never a contributor's saved report
  (design-note R5 gate).** At acceptance *and* on every sweep, regenerate the report
  from the SWHID-pinned commit rather than trusting the `evaluate-report.json` a
  contributor committed — a stale saved proof MUST NOT be able to pass. The
  reusable-workflow seam below is what makes "green at submit" and "green on
  re-validate" mean the same thing (design-side CI and the toolkit-side gate run
  identical logic).
- **Diff each emitted report against a committed golden baseline (design-note R7).**
  A report nobody compares wastes the typed, diffable artifact. Each active design
  carries a golden `evaluate-report.json`; the sweep diffs the fresh report against it
  and a **per-finding status flip is the regression signal** ("did anything quietly
  stop conforming?"). An intentional change is reviewed and the golden updated —
  exactly the discipline of the realization-index drift gate and CLI Printing Press's
  golden tests. (Depends on the harness above producing a report; sequenced right
  after it.)
- `.github/workflows/conformance.yml` — `workflow_dispatch` + `schedule:` matrix
  over **active** designs; structured to also be a **reusable workflow** a design
  repo can call so design-side CI and toolkit-side sweep run identical logic.
- Ships **inert** (the matrix is empty until a design declares a real verify
  entrypoint + container). Documented activation checklist.
- **Hard parts to resolve at activation (see scope doc):** running contributed
  code = RCE → ephemeral least-privilege network-restricted runner, no secrets;
  arbitrary toolchains → containers; non-executable verifications
  (`human-review`/inspection) → reported `not-executed`, never counted as passed;
  flakiness → infra-failure vs conformance-failure distinction; SH ingest is
  async → verify-by-recompute locally, verify-retrievable on a slow cadence.
  *Precedent worth mining (design note, R1):* CLI Printing Press's `verify` already
  solves several of these for its one tool-class — read-only least-privilege live
  execution (GET-only, `--limit 1`, short timeout, stop-on-401), a typed
  infra-failure-vs-conformance-failure exit-code distinction, and mock-vs-live modes
  for evidence that can't be run live.

## Decisions (locked for this pass)
- **Manifest format:** TOML (`tomllib`, py3.11 stdlib; human-friendly; comments).
- **Fetch path:** git clone + verify SWHID locally; SH vault is the *fallback*
  when upstream is gone (not the primary, for speed).
- **Execution model:** each active design ships a container/verify entrypoint;
  the toolkit orchestrates. (Toolkit-provided per-stack base images is a possible
  later convenience, not required.)
- **Self-tests are dependency-free** so CI needs no pytest/just.

## Open decisions (deferred to Phase 4 activation)
- SH-vault-primary vs git-primary fetch once a design's upstream is gone.
- Toolkit-provided base images vs design-shipped Dockerfiles.
- Active-set cap + promotion/demotion policy (roadmap R3).
