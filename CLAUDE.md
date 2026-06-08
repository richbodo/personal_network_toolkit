# CLAUDE.md

PNA Toolkit — a machine-readable, goal-anchored spec (plus typed
contracts, lints, an agent skill, and reference designs) that an AI agent uses to
**build** conformant Personal Network Applications (PNAs) and **evaluate** candidate
apps against the PNA Goals. This is a spec/lint/docs repo, **not** an application.

**Read in this order:** [`README.md`](README.md) (overview + status) →
[`spec/PNA_Spec.md`](spec/PNA_Spec.md) (the spec) →
[`pna-build-eval-contrib/SKILL.md`](pna-build-eval-contrib/SKILL.md) (the agent flows) →
[`docs/users-guide.md`](docs/users-guide.md) (step-by-step how-to). Run `just` for the
command menu and `just ci` before pushing.

## Keep the docs current

The toolkit's users are developers, and [`docs/users-guide.md`](docs/users-guide.md) is the
developer-facing source of truth. **Any PR that changes a behavior a developer would
notice — a `just` recipe, a lint check or its message, a skill flow, a contract / AC /
manifest field, or a contribution step — MUST update `docs/users-guide.md` in the same
PR.** Accepting the PR accepts the doc change with it. (The PR template carries a
matching checkbox.) This rule exists because the docs fell behind the code once already;
don't let it happen again.

## Documentation map — one source of truth per fact

Restating a fact in a second doc creates a drift surface. Each doc *owns* a category and
the others *link* to it rather than re-explaining:

- **`spec/*.md`** — normative content: Goals, ACs, axes, sub-contracts, Exceptions
  (`EX-*`), Constraints (`CST-*`). Owns *what conformance means*.
- **`pna-build-eval-contrib/SKILL.md`** — how the agent executes the build / evaluate /
  contribute flows. Owns *agent procedure*.
- **`docs/users-guide.md`** — task-ordered how-to for humans; mostly numbered action
  sequences. Owns *what a developer does, step by step*. Links to the spec / SKILL /
  CONTRIBUTING for definitions and policy; does not restate them.
- **`CONTRIBUTING.md`** — contribution *policy*: what's accepted, versioning (SemVer),
  archival. Owns *policy*.
- **`CHANGELOG.md`** — version history.

When you add a fact, put it in the doc that owns its category and link from the others.

## Conventions

- **Stdlib-only `python3` (3.10+).** No third-party runtime deps — no `pytest`, no
  `tomllib` (hand-roll a small parser if needed). CI runs bare `python3`.
- **RFC 2119 language in spec files** — `MUST`/`SHOULD`/`MAY` only when capitalized;
  plain English (motivation, examples) otherwise.
- **The toolkit is versioned as a unit** — every artifact carries a `Toolkit-Version:`
  stamp matching `/VERSION`, enforced by `tools/lint-spec-ids.py`.
- **The AC is the unit of identity**; conformance is *checked, not awarded*; use variable
  language about axis counts ("the axes", never "the six axes").
- Run `just ci` after changes; put manual test/QA steps in the **PR description**.

## Worktrees (multiple agents on one host)

Worktrees are **cheap and fully isolated** here — this is a stdlib-only `python3` spec/lint/docs
repo with **no server, port, database, or build artifacts** to share, and `just ci` runs against a
tempdir copy, so concurrent `just ci` across worktrees can't collide. When more than one Claude
Code / agent works on this host's checkout at once, give each its own worktree so a `git checkout`
in one can't pull the branch (or uncommitted work) out from under another:

```
git worktree add ../pnt-wt-<branch> -b <branch>     # ready immediately — no setup
git worktree remove ../pnt-wt-<branch>              # when done
```

No `wt` recipe or env-share script is needed (unlike the app reference designs, which gate on a
shared workspace port). See [`docs/roadmap.md`](docs/roadmap.md) for which Claude Code instance owns
which wave of work.

## Lint discipline — fail loudly

- **Every check in `tools/lint-spec-ids.py` needs a fault-injection case in
  `tools/tests/lint_selftest.py`, added in the *same* change.** A check with no self-test
  can silently rot — exactly what happened to the dead `Reversible:`/`Reversal:` check
  (PR #18, green while enforcing nothing). `just lint-selftest` runs them; the clean tree
  must pass and each injected fault must fail with its expected message.
- **Deferrals are honest** — an in-artifact status (`archival = "pending"`, an attestation
  `partial`/`Open`, a CHANGELOG "deferred" note), never a bare `TODO`/`INERT` comment that
  *claims* a property the code doesn't deliver.
- **Convert an absent guarantee into a red test (or a lint failure), never a silent pass.**
