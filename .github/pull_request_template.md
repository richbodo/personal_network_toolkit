<!-- PNT pull-request template. Delete the sections that don't apply. -->

## What this PR does

<!-- One-paragraph summary. -->

## Type

- [ ] Reference design (new or updated), or a spec/contracts change that imposes a new obligation on designs → complete the Reference-design checklist
- [ ] Toolkit fix / docs / tooling, or a spec note that clarifies/declines a commitment (no reference-design attestation) → complete the Toolkit-fix checklist

<!-- Routing: does a design have to do anything new to stay conformant after this change? Yes → reference design. Nothing does → toolkit fix. See CONTRIBUTING.md § Contribution types. -->

## Every PR

- [ ] **Docs current** — if this changes a developer-visible behavior (a `just` recipe, a lint check or its message, a skill flow, a contract/AC/manifest field, or a contribution step), [`docs/users-guide.md`](../docs/users-guide.md) is updated in this PR. *(See `CLAUDE.md` § Keep the docs current.)*
- [ ] **Local gate green** — `just ci` passes (lint + self-tests); any new lint check has a fault-injection self-test.
- [ ] **Manual test/QA steps** for the reviewer are in the PR description (when applicable).

## Toolkit-fix checklist

<!-- Only if this PR is a toolkit fix / docs / tooling change (no reference design). Delete if not applicable. -->

- [ ] **No new design obligation** — this change imposes no new contract a conformant design must satisfy. *(If it does, it's a reference-design contribution — use the checklist below instead.)*
- [ ] **CHANGELOG entry** added.
- [ ] **Design note** appended to `docs/PriorArt.md § Design notes` if this PR embodies a decision (added or declined a direction, with rationale worth preserving). Mechanical/typo fixes don't need one.

## Reference-design / spec contribution checklist

<!-- Only if this PR adds or updates a reference design, or changes spec/contracts. See CONTRIBUTING.md. -->

- [ ] **Architecture document** present (in the design's own repo) declaring its **`Toolkit-Version`**, axis picks + versions, and an **AC attestation table** with a **Verification** entry on *every* applicable AC. *(A row missing Verification is grounds for rejection.)*
- [ ] **Exceptions** — if the design raises any, each is declared with `Relaxes:` / `Reversible:` and a per-dimension strength profile (`spec/exceptions.md`).
- [ ] **Evaluate flow run.** The evaluate flow (`pna-build-eval-contrib/SKILL.md`) was run against the design and the typed report is committed at `reference_designs/<name>/evaluate-report.json` (an instance of `tools/evaluate-report.schema.json`), or linked here.
- [ ] **Lint green** — `just lint` passes (CI-enforced).
- [ ] **License** is OSI-approved and permits Software Heritage archival.

## Maintainer acceptance

<!-- Filled by the maintainer at merge. The merge itself is the acceptance; this records what was validated. -->

- [ ] **Validation attested.** The evaluate-flow report and the AC attestation table were reviewed and check out against the cited code, at **Toolkit-Version `<x.y>`**.
- [ ] **Acceptance recorded** in `reference_designs/<name>/README.md` (date · accepted-by · Toolkit-Version validated against).
- [ ] **Post-merge:** Software Heritage archival triggered (`tools/swh-save.sh <repo-url> <tag>`) and the returned **SWHID recorded** in the design entry.
