# What the PNA Toolkit can learn from CLI Printing Press

*Design note · 2026-06-21 · status: **analysis captured; nothing adopted yet** —
checkpoints a 2026-06-21 session (Rich + Claude Code) studying the sibling repo
`../cli-printing-press` (github.com/mvanhorn/cli-printing-press) as a model for the PNA
Toolkit's **build and validation flows**. Three read-only explorations mapped its build
pipeline, its validation/quality machinery, and its contribution/catalog/website mechanism.
This note records the transferable mechanisms and a staged recommendation; the companion
follow-on is a mapping of these onto
[`../../plans/conformance-suite-plan.md`](../../plans/conformance-suite-plan.md). Indexed in
[`../PriorArt.md` § Design notes](../PriorArt.md).*

> **Not a commitment, and not a spec change.** This records an analysis, the transferable
> mechanisms, and a staged recommendation. It imposes no obligation on any design, adds no AC,
> and changes no developer-visible behavior (so no `users-guide.md` change rides with it). The
> point is to write the thinking down so we can pilot, adopt, or reject each piece on the record.

## The occasion

**CLI Printing Press (CPP)** is a generator that turns the name of an API or website into a
shipped Go CLI **plus** an MCP server **plus** a Claude Code skill. It picked one narrow,
hot, easily-automatable output type and built an aggressive, many-step, *executing* pipeline
around it: research → ecosystem-absorb → generate → "build the GOAT" → **shipcheck** → publish,
with a public library repo + a `registry.json` + a web catalog (printingpress.dev) on the far
end. Rich's read, which frames this note: PNA will never have CPP's traction (it's a blueprint
for a whole *class* of apps, deliberately human-AI-composed, not a one-tool-class generator in
the hottest market) — but **its build process and validation flows are worth learning from.**

This note is deliberately about *mechanisms*, not about CPP's market focus. The asymmetry is
the whole point: CPP could fully automate because it builds one thing; PNA borrows the *gates
and flows*, not the codegen.

## The core insight — same philosophy, different operationalization

CPP and PNA rest on the **same conviction**: a behavior only counts when its conformance can be
*mechanically checked*, not merely asserted. CPP's pitch ("a well-designed CLI is muscle memory
for an agent") and the PNA Spec's Preamble ("a behavior counts as *specified* only when its
conformance can be **checked** … never merely asserted in prose") are the same sentence.

The difference is **how hard each operationalizes it.** CPP *runs* the artifact's evidence in a
layered pipeline — cheap deterministic gates first and blocking, expensive LLM review second and
mostly advisory, every gate executing against the real (or mocked) thing. PNA's checking is, by
contrast, mostly **static** (stdlib lints read source) plus **LLM reading** plus
**trust-the-attestation** — and the toolkit's own [`SKILL.md`](../../pna-toolkit/SKILL.md) names
the resulting weakness out loud:

> "a static lint cannot prove the test *passes* … Confirm passing by running the design's suite."

The [`attestation-evidence-lint`](../../tools/attestation-evidence-lint.py) proves a cited test
*exists and is live* — never that it *passes*. So PNA's behavioral tier is **declared but
unbuilt** ([`test-design`](../../plans/conformance-suite-plan.md) is an inert Phase-4 scaffold).

**The throughline of every recommendation below: close the gap between what PNA already says it
believes ("checked, not asserted") and what it currently mechanizes (mostly static + attestation
trust) — by *running* things, the way CPP does. Take CPP's discipline; leave its narrow focus
and its letter grade.**

## What CPP actually does (the transferable mechanisms)

- **Layered validation, deterministic-first.** ~12 deterministic checks (build, `go vet`,
  `gosec`, golden tests, `dogfood`, `verify`, `verify-skill`, `workflow-verify`, `tools-audit`,
  `pii-audit`, path-validity, auth-protocol) run **first and blocking**; the LLM layer
  (`output-review`, code-review) runs **second and advisory**, reserved for what rules can't do
  (substring-relevance, silent source drops, ranking failures). *If a property is mechanizable,
  there is a deterministic probe for it; the LLM does judgment, not bookkeeping.*
- **`shipcheck`** folds every leg into one verdict (`ship` / `ship-with-gaps` / `hold`), run as
  one block before publishing.
- **A scorecard** scores 0–100 across two weighted tiers (infrastructure vs. domain correctness),
  grades A/B/C — and crucially **does not gate the build.** Hard gates gate; the score *informs.*
  N/A dimensions drop out of the denominator so the number stays honest.
- **`verify` actually runs the CLI** — every command against a mock or read-only live API
  (GET-only, `--limit 1`, 10s timeout, stop on 401) — catching behavioral bugs static checks miss.
- **A mechanized contribution skill** (`publish`): resolve → validate → **fresh live gate re-run
  at submit time** (so a stale acceptance proof can't sneak through) → secret-scan → collision
  detection (open PRs / merged / your own) → structured **auto-filled PR body** (validation table,
  manuscript-evidence links, novel-commands table) → CI/Greptile review loop → a conventions-lint
  that hard-fails any PR hand-editing the bot-generated files. The target is a **separate public
  library repo**, not the generator repo.
- **`registry.json` → website.** Post-merge a bot regenerates `registry.json`; printingpress.dev
  renders it (19 categories, search, install commands). The data layer is generated, never
  hand-edited.
- **Provenance + immutable manuscripts.** Every published CLI carries `.printing-press.json`
  (generator version, run id, spec checksum, creator, accruing contributors, novel features) and
  a frozen `.manuscripts/<run-id>/` (research + proofs + discovery).
- **A learning flywheel back into the machine:** `retro` files systemic improvements to the Press
  after a run; `amend` turns dogfood friction into a library PR; `reprint`/`emboss` regenerate
  under a newer Press.
- **Golden tests** pin generator output so intentional changes get reviewed and silent drift is
  caught.

## The recommendations, mapped to PNA's grain (R1–R7)

Each: **CPP mechanism → the PNA gap → the recommendation.** Ranked by leverage.

- **R1 — Build the behavioral conformance harness (run the designs).** *CPP:* `verify`/`dogfood`/
  `shipcheck` execute the artifact and re-run the live gate at submit time. *PNA gap:* conformance
  is never executed; `just test-design` is inert; `attestation-evidence-lint` proves *exists*, not
  *passes*. *Recommendation:* make `test-design` real — fetch a design at its SWHID, build, run its
  `design.toml` `[verify].entrypoint`, fold pass/fail into `evaluate-report.json` as
  `source: deterministic` evidence. The toolkit shells out to the **design's own** toolchain (the
  `[verify]` block already models this), so the stdlib-only-no-deps charter holds. *This is exactly
  Phase 4 of the conformance-suite plan — CPP is a working reference implementation of it.*
- **R2 — Grow the per-AC deterministic floor.** *CPP:* a deterministic probe for every mechanizable
  property; the LLM only does what rules can't. *PNA gap:* ~6 lints cover ~3 ACs (AC-1 egress, PR-6
  export, candidate AC-PRM-H loopback); ~20 ACs are LLM/human-only. *Recommendation:* publish a
  **coverage map** (per AC: deterministic-probe / LLM-only / human-only), and convert mechanizable
  ACs into lints one at a time — each with its fault-injection self-test (the existing CLAUDE.md
  rule). Near-term candidates: AC-15 (build label format), AC-9/ST-6 (backup ring rotates), AC-4/ST-2
  (handshake refuses mutation on skew), DI-4/AC-8 (anti-enum 200/204), DB-4 (sink 204 + cap).
- **R3 — Separate gates from posture; add a per-Goal rollup — *no grade*.** *CPP:* hard gates and the
  (non-gating) scorecard are distinct; N/A drops from the denominator. *PNA gap:* `validate` folds
  lints into one report, but the aggregate posture isn't legible, and PNA *refuses a grade* by design
  ("checked, not awarded"). *Recommendation:* keep refusing the grade; borrow only the *dimension
  decomposition and N/A-honesty* — a per-Goal (and universal-vs-flavor-derived) **coverage vector** in
  `evaluate-report.json` + the Visual Validator ("Goal 3: 6/7 ACs conformant"). A posture vector, not
  a badge — which is what "checked, not awarded" actually wants, and what makes two runs comparable.
- **R4 — Generate a `registry.json` of accepted designs; stage a web catalog.** *CPP:* bot-generated
  registry → website. *PNA gap:* the data exists (`design.toml` + `evaluate-report.json` + the
  [realization index](../realization-index.md)) and a viewer exists (Visual Validator), but no rolled-up
  registry and no public design catalog. *Recommendation, staged:* generate `registry.json` now (a cheap
  join over existing artifacts, drift-gated like the realization index); build the website **only when
  design count justifies it** — an empty showcase undersells, and PNA won't have CPP's traction. The
  registry doubles as the "is this PNA safe to install?" front door and as contribution gravity.
- **R5 — Mechanize the contribute-flow gates.** *CPP:* `publish` re-runs the live gate at submit time,
  auto-fills the PR body, detects collisions, and protects bot files. *PNA gap:* the contribute flow is
  skill-guided prose; "a final preflight run against the merged state should come out clean" is advice,
  not an enforced gate. *Recommendation:* (a) make **submit-time re-validation a hard gate** — regenerate
  the report against the *pinned commit*, don't trust the contributor's saved one; (b) **auto-fill the PR
  body** from the report (validation table + per-AC posture + evidence links); (c) adopt **honest-marker
  preconditions** (the PR step refuses to run without a clean preflight artifact) — the CLAUDE.md
  "fail loudly" ethos, mechanized.
- **R6 — Make a "toolkit retro" a first-class per-run step.** *CPP:* `retro` files Press improvements
  after every run. *PNA gap:* the *concept* exists (field notes + `/capture-lesson` + the manual
  inbound-findings registry in [`roadmap.md`](../roadmap.md)) but capture-lesson is AC-keyed only; there's
  no mechanized "what should the *spec/lint/skill* learn from building/evaluating this design?" step.
  *Recommendation:* generalize capture-lesson so build/evaluate/contribute each end by emitting either a
  field note *or* a toolkit-fix issue. Borrow the *cadence and mechanization*, not the concept.
- **R7 — Golden `evaluate-report`s as a regression gate.** *CPP:* golden tests pin output; intentional
  changes are reviewed, silent drift caught. *PNA gap:* `lint_selftest.py` and the realization-index
  `--check` already apply this to lints, but **nothing catches a spec/lint edit that silently flips a
  *design's* conformance posture.** *Recommendation:* once R1 lands, pin a golden `evaluate-report.json`
  per design with a deterministic emitter, and diff each conformance sweep against it — the
  "did anything quietly stop conforming?" signal the typed, diffable report was built to give but isn't
  yet wired to gate on.

## What *not* to copy (so PNA stays PNA)

- **No single grade / pass-fail badge.** Take the dimension decomposition; leave the letter grade.
  "Checked, not awarded" is a deliberate identity (R3 honors it).
- **No "PNA Press" auto-generator.** PNA is a spec for a *class*, human-AI-composed by design, and
  won't get CPP's traction. The build flow stays agent-guided; borrow the *gates*, not codegen.
- **No third-party tooling creep.** CPP is Go + `gosec` + Greptile + GoReleaser. PNA is stdlib-only
  by charter — the toolkit's own checks stay stdlib Python. R1's harness shells out to the *design's*
  toolchain (via `[verify]`), never importing deps into the toolkit.
- **Don't chase market narrowing.** CPP's focus is its superpower *and* its ceiling; PNA's
  breadth/sovereignty is the bet. Different game.

## Where these land

The recommendations split cleanly by home, which is what keeps each in the doc that owns its category:

- **The conformance-suite plan** ([`conformance-suite-plan.md`](../../plans/conformance-suite-plan.md))
  owns *executing* conformance. **R1** is its Phase 4; **R7** is the regression-diff Phase 4 is missing;
  **R5's re-validate-at-pinned-commit gate** reinforces its Phase 3→4 seam; **R2's coverage map** is
  conformance-scope reasoning. (Detailed mapping is the companion follow-on to this note.)
- **`validate.py` + the report schema + the Visual Validator** own the *shape* of the emitted report —
  home for **R3**.
- **Realization-index / a new ecosystem-catalog tool** owns discovery — home for **R4**.
- **`SKILL.md` contribute flow + `CONTRIBUTING.md` + the PR template** own contribution mechanics —
  home for **R5's PR-body/collision/marker** pieces.
- **Field notes + `/capture-lesson` + the roadmap inbound-findings registry** own the learning flywheel —
  home for **R6**.

## Status and next step

Analysis captured (this note). The immediate follow-on is folding the conformance-relevant pieces —
**R1** (foreground Phase 4's exists→passes goal; cite CPP as the reference implementation that de-risks
its "hard parts"), **R7** (add a golden-report regression diff), and **R5's pinned-commit gate** — into
the conformance-suite plan; the per-AC **R2 coverage map** belongs alongside in
[`conformance-scope-and-lifecycle.md`](../conformance-scope-and-lifecycle.md). **R3/R4/R6** are tracked
against their own homes above. Nothing here is adopted until piloted; honest decline beats a half-built
borrow.
