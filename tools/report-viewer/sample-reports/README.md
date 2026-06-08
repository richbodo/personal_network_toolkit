# Visual Validator — sample reports (render contract)

Valid instances of [`../../evaluate-report.schema.json`](../../evaluate-report.schema.json) — the
typed artifact the toolkit's **evaluate** flow emits ([`pna-build-eval-contrib/SKILL.md`](../../../pna-build-eval-contrib/SKILL.md)).
They serve two jobs (per [`plans/visual-validator-plan.md`](../../../plans/visual-validator-plan.md) Phase 1):

1. **The Visual Validator's render fixtures** — the inputs `tools/report-viewer/index.html` renders
   while it's built (Phase 2+). They exercise every field a viewer must handle.
2. **The render contract** — what a report must carry for the viewer to render it. Guarded
   deterministically by [`../../report-fixtures-lint.py`](../../report-fixtures-lint.py)
   (`just report-lint tools/report-viewer/sample-reports`), wired into `tools/tests/lint_selftest.py`,
   so a schema change or a malformed report **fails loudly** instead of rendering blank.

> All three are **illustrative** — not real evaluations. The first *real* report (fellows_local_db,
> from roadmap Wave 2) will join or replace a synthetic sample once the keystone is finalized.

## The samples

| File | Posture | Exercises |
|---|---|---|
| `01-conformant-minimal-pna.json` | `conformant` | a Minimum-Viable-PNA; `conformant` + `not-applicable` findings (with rationale), `goals`, inferred picks, empty `leading_concerns` |
| `02-non-conformant-leaky-app.json` | `non-conformant` | a Goal-1 leak + an **undeclared `EX-CLOUD-LLM` deviation**; `requirement` text, `deterministic`(egress-lint) + `llm` evidence, populated `leading_concerns`, `needs_human_review` |
| `03-mixed-exceptions-and-constraints.json` | `mixed` | EX-/CST-handling referenced inside AC findings; all three evidence sources (`deterministic` / `llm` / `human`); `unable-to-determine`; declared picks + full candidate metadata |

Together they cover all four finding statuses, three of the four postures, both `picks_source` values,
and all three evidence sources.

## Why EX-* and CST-* are not top-level keys

The v0.1 report schema is **AC-keyed**: `finding.ac_id` matches `^AC-[A-Z0-9-]+$`, so an `EX-*`
exception or a `CST-*` constraint **cannot** be a finding's id. They are referenced *inside* the AC
findings they bear on — e.g. `EX-CLOUD-LLM` (and its `EX-H*` handler clauses) within the **AC-MCP-A**
finding's evidence; `CST-PWA-PRIVATE-SNAPSHOT` within the **AC-1** finding — which mirrors how
`reference_designs/fellows_local_db/Architecture.md` attests them. (Whether a future report schema
should key findings by `EX-*` / `CST-*` directly is a separate question; SKILL.md § Evaluate flow
speaks of reporting "by AC or EX ID", so the schema and the skill may want reconciling — tracked
separately, not in this Phase-1 change.)
