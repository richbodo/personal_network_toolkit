<!-- PNT pull-request template. Delete the sections that don't apply. -->

## What this PR does

<!-- One-paragraph summary. -->

## Type

- [ ] Reference design (new or updated), or a spec/contracts change → complete the checklists below
- [ ] Toolkit fix / docs / tooling (no reference-design attestation needed)

## Every PR

- [ ] **Docs current** — if this changes a developer-visible behavior (a `just` recipe, a lint check or its message, a skill flow, a contract/AC/manifest field, or a contribution step), [`docs/users-guide.md`](../docs/users-guide.md) is updated in this PR. *(See `CLAUDE.md` § Keep the docs current.)*
- [ ] **Local gate green** — `just ci` passes (lint + self-tests); any new lint check has a fault-injection self-test.
- [ ] **Manual test/QA steps** for the reviewer are in the PR description (when applicable).

## Reference-design / spec contribution checklist

<!-- Only if this PR adds or updates a reference design, or changes spec/contracts. See CONTRIBUTING.md. -->

- [ ] **Architecture document** present (in the design's own repo) declaring its **`Toolkit-Version`**, axis picks + versions, and an **AC attestation table** with a **Verification** entry on *every* applicable AC. *(A row missing Verification is grounds for rejection.)*
- [ ] **Exceptions** — if the design raises any, each is declared with `Relaxes:` / `Reversible:` and a per-dimension strength profile (`spec/exceptions.md`).
- [ ] **Evaluate flow run.** The evaluate flow (`pna-build-eval-contrib/SKILL.md`) was run against the design and the typed report is committed at `reference_designs/<name>/evaluate-report.json` (an instance of `tools/evaluate-report.schema.json`), or linked here.
- [ ] **Lint green** — `python tools/lint-spec-ids.py` passes (CI-enforced).
- [ ] **License** is OSI-approved and permits Software Heritage archival.

## Maintainer acceptance

<!-- Filled by the maintainer at merge. The merge itself is the acceptance; this records what was validated. -->

- [ ] **Validation attested.** The evaluate-flow report and the AC attestation table were reviewed and check out against the cited code, at **Toolkit-Version `<x.y>`**.
- [ ] **Acceptance recorded** in `reference_designs/<name>/README.md` (date · accepted-by · Toolkit-Version validated against).
- [ ] **Post-merge:** Software Heritage archival triggered (`tools/swh-save.sh <repo-url> <tag>`) and the returned **SWHID recorded** in the design entry.
