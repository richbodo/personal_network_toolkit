# PNA Toolkit User's Guide

The PNA (Personal Network Application) Spec is the canonical specification; this guide is the canonical **how-to**. It is task-ordered: each section is a numbered sequence of actions to accomplish one thing. Where a step needs a rule or definition, it links to the authoritative document rather than restating it.

The PNA Toolkit is built to be consumed by AI coding agents, and its users are developers. Most of this guide assumes you have an agent (Claude Code, Cursor, an equivalent) you can ask things like *"use the toolkit skill to validate my design."* The skill at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) is the agent-consumption view of the build / audit / contribute flows below.

**The fastest way in is auditing.** If you just want to know whether a contact app is safe before you install it — without building or contributing anything — go straight to [Audit a candidate PNA](#audit-a-candidate-pna-before-installing-it). Point an agent at the app's source and get back an AC-keyed safety report.

> **Status (June 2026).** The toolkit's deterministic tooling is tested and CI-enforced; the agent-driven flows are being exercised for real.
>
> **Tested / CI-enforced** (run on every PR, reproducible locally with `just ci`):
> - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract / exception / constraint / manifest / toolkit-version traceability lint.
> - [`tools/tests/lint_selftest.py`](../tools/tests/lint_selftest.py) — the lints' own self-tests (each check is proven to fail on an injected fault).
> - [`tools/egress-lint.py`](../tools/egress-lint.py) — the deterministic AC-1 off-device-egress check, with clean/dirty fixtures.
> - [`tools/export-readable-lint.py`](../tools/export-readable-lint.py) — the deterministic PR-6 export-readability check, with clean/dirty fixtures.
> - [`tools/attestation-evidence-lint.py`](../tools/attestation-evidence-lint.py) — the deterministic attestation-evidence check (a `conformant` row must cite a live, non-`xfail`/`skip` test or a declared review kind), with clean/dirty fixtures.
> - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — the audit-report schema.
>
> **Exercised end-to-end:** the **contribute** flow — `fellows_local_db`'s Exceptions, Constraints, and conformance-suite contributions were all authored through it. The **build** and **audit** flows are still being dogfooded against `fellows_local_db`; the agent prompts and output shapes below describe the intended behavior per [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md), and continue to be refined.

---

## Install the skill

The flows below are driven by the toolkit skill at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md). If you haven't used Claude Code skills before: they're modular agent capabilities that live in a `.claude/skills/<skill-name>/SKILL.md` layout. You install one once, then use it through natural language in any chat.

### How Claude decides to use the skill

At session start Claude Code loads every installed skill's **name and `description`** into context — not the full body, which loads only when the skill actually runs. Claude then **auto-discovers** the skill: when your prompt matches the triggers in its `description`, it invokes the skill on its own, without you naming it. The toolkit skill's description is written to fire on phrases like *"is this app safe to install?"*, *"does my app conform?"*, or "build a local-first contact app", so a request like *"audit this contact app before I install it"* trips it automatically.

You don't have to rely on that, though. You can always invoke it explicitly — `/pna-build-eval-contrib`, or just *"Use the toolkit skill to…"*. Auto-discovery is a match against prose, so it's a strong default but not a guarantee; for a deliberate task like validating that a repo conforms, naming the skill (or the flow) is the most reliable path — and that's how the prompts in this guide are phrased.

**Recommended — symlink globally** (run from your toolkit working directory):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/pna-build-eval-contrib" ~/.claude/skills/pna-build-eval-contrib
```

Symlinking keeps the skill in sync with your toolkit clone — a `git pull` here updates the skill everywhere it's used.

**Alternatives:**

- **Copy instead of symlink** — replace `ln -s` with `cp -r` to pin the skill to a specific version. You'll re-copy when you want updates.
- **Run Claude Code from the toolkit itself** — no install required; the skill is discoverable from this directory. Adequate for one-off auditing.

### Per-repo install (for a design that contributes to the PNA Toolkit)

When a PNA repo actively contributes back (it's a reference design, or you drive the contribute flow from it), scope the skill to that repo at `<your-project>/.claude/skills/pna-build-eval-contrib` so collaborators on it pick the skill up. Two forms:

- **Symlink** (dev convenience, no drift):
  ```bash
  ln -s <path-to-pnt>/pna-build-eval-contrib <your-project>/.claude/skills/pna-build-eval-contrib
  ```
  Stays in sync with your toolkit clone, but the absolute path is machine-specific — **don't commit a machine-specific symlink.**
- **Vendored copy** (portable, committable):
  ```bash
  cp -r <path-to-pnt>/pna-build-eval-contrib <your-project>/.claude/skills/pna-build-eval-contrib
  ```
  Commit it **with a provenance note pinning the toolkit commit** it was copied from (e.g. an `INSTALLED_FROM.md` beside `SKILL.md`). Collaborator-friendly and reproducible, but it **drifts** from upstream — re-sync before relying on it for a contribution.

Pick the symlink for local iteration; pick the vendored copy when the design repo should carry the skill for everyone working on it.

> **Precedence gotcha — a global install shadows the repo copy.** When the same skill name exists at more than one scope, Claude Code resolves in the order **enterprise → personal (`~/.claude/skills`) → project (`<repo>/.claude/skills`)**, and the higher scope wins *silently* — no collision warning. So if you've done the recommended global install **and** vendored a pinned copy into a design repo, the global copy wins, and your pinned, reproducible copy is never used. When a contribution depends on validating against a specific pinned Toolkit-Version, remove or rename the global install for that work.

**Verify.** Start Claude Code and try one of the prompts below; if the skill triggers, you're set. You can also ask *"what PNA Toolkit skills do you have available?"*. **Note:** a restart is only needed the **first** time you create a top-level skills directory that didn't exist when the session started (e.g. the `mkdir -p ~/.claude/skills` above). Once the directory exists, later edits are picked up live.

---

## Using the skill

The skill packages three flows. Each is a numbered sequence below; run whichever fits your task.

### Build a conformant PNA

You're starting (or extending) a personal network application.

1. **Skim the spec and pick a use case.** You don't need to memorize [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) to start — but read enough to know its vocabulary (*slot*, *axis*, *flavor*, *AC*, *Exception*, *Constraint*) and that the universal ACs are non-negotiable. Then browse [`spec/use_cases.md`](../spec/use_cases.md) for the attested classes of PNA and pick one. A use case suggests default axis picks but doesn't determine them.

2. **Walk through axis picks with the agent.** Open Claude Code in your new project's directory and ask:

   > "Use the toolkit skill to walk me through axis picks for a [Directory Archive | Personal Relationship Manager | …] PNA."

   The agent walks each Axis (distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure) and the attested picks per Axis. Your full set of picks is your *flavor*. Some picks trigger flavor-derived ACs — see [`spec/axes.md`](../spec/axes.md).

3. **Enumerate the Constraints your picks inherit.** A [Constraint](../spec/constraints.md) (`CST-*`) is a platform/substrate ceiling that comes attached to an axis pick — e.g. a `web-bundle` × `opfs-sqlite-wasm` PNA inherits the `CST-PWA-*` family. The agent lists them and helps you plan the honest per-platform capability reduction up front (the cross-references in [`spec/axes.md`](../spec/axes.md) name which picks inherit which constraints). If your design will deliberately depart from a guarantee, plan the [Exception](../spec/exceptions.md) (`EX-*`) handling too.

4. **Study the closest reference design.** Each [`reference_designs/<name>/`](../reference_designs/) directory has a design record naming its flavor and a Software Heritage SWHID pointing to archived source. Pick the design whose flavor overlaps your picks the most; read its code and treat it as the seed your PNA grows from. Adapting beats starting from scratch — the cross-slot integration work is already done.

5. **Stub an Architecture document.** Copy [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md) to `docs/Architecture.md` in your design's own repo. Fill in Toolkit-Version, axis picks and their versions, and per-axis implementation notes. Leave the attestation tables empty for now — you fill them as you build (step 7).

6. **Build against the typed contracts.** [`contracts/`](../contracts/) holds the load-bearing interfaces, each opening with `Realizes: AC-X, AC-Y` naming the ACs it serves. Your code conforms to these. If you need to deviate from a contract, propose a spec change (see [Contributing beyond reference designs](#contributing-beyond-reference-designs)) rather than diverging silently.

7. **Fill in the attestation table as you build.** For every applicable AC (universal in `PNA_Spec.md` + flavor-derived from your picks in `axes.md`), and every Exception/Constraint your design raises or inherits, record three fields in your Architecture document:
   - **Realization** — how your code realizes/handles it, with `file:line` references.
   - **Verification** — the test, LLM rubric, or human-review note that verifies it for *your* design. A `conformant` row needs **executable evidence** (a resolvable test) or an explicitly declared review kind — a bare doc pointer is not evidence, and a negative invariant ("X must NOT happen") needs a *negative* test. See the [evaluate flow's attestation-evidence rules](../pna-build-eval-contrib/SKILL.md) for the full bar.
   - **Status** — `conformant` / `partial` (with the known gap) / `not-applicable` (with reason).

8. **Self-check.** Run the [Audit](#audit-a-candidate-pna-before-installing-it) flow on your own in-progress code before declaring done. For the AC-1 (private-data-sovereignty) row, add an `egress-allow.json` to your repo listing the remote origins your flavor legitimately uses, and run `just egress-lint <your-source-dir>` — it's the deterministic half of that check and makes a ready-made Verification entry. Wire it into your own CI so a future change can't silently introduce an off-device data path.

### Audit a candidate PNA before installing it

You have a PNA in front of you (someone else's, or your own in-progress one) and you want an LLM to check whether it actually honors the PNA Spec — whether it's safe with your data.

1. **Get the candidate's source.** Clone the repo. If you only have a bundle, ask for the source — you can't audit a black box.

2. **Open Claude Code with the toolkit and the candidate both reachable.** The skill lives at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md); the agent reads it when the prompt matches.

3. **Ask the agent to run the audit:**

   > "Use the toolkit skill to audit `<path-to-candidate>` for PNA-spec conformance. Is this app safe for me to install?"

   If the candidate ships its own Architecture document, the agent validates it against the code (do cited locations match? do declared verifications pass?). Otherwise it infers axis picks from the source and walks every applicable AC from scratch. It also **detects and verifies Exceptions** (`EX-*`) and **Constraints** (`CST-*`) — confirming each declared deviation is handled honestly and flagging any *undeclared* one. As part of the audit it runs the deterministic checks in `tools/` (`just egress-lint <path>` for AC-1 off-device leaks; `just export-lint <path>` for PR-6 export readability; `just attestation-lint <path>` to confirm the candidate's own `conformant` attestation rows cite live, non-deferred evidence) and folds their results into the matching AC findings as `source: deterministic` evidence.

4. **Read the AC-keyed report.** The agent emits a typed artifact ([`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)) with a human-readable rendering over it. Per-finding status is one of `conformant` / `non-conformant` / `not-applicable` / `unable-to-determine`, each keyed by AC, EX, or CST ID. Because the report is typed, two runs over the same candidate are diffable — save the artifact, re-audit after an update, and diff the JSON for the per-finding status changes (the "did anything quietly stop conforming?" signal).

5. **Decide.** Goals 1–5 are the load-bearing user-facing concerns — private-data sovereignty (Goal 1), sourced-data honesty (Goal 2), user-controlled communication (Goal 3), durability (Goal 4), local diagnosability (Goal 5). If any of those are non-conformant (and not honestly handled via a declared Exception), the design is not safe to trust with your data. You can emphasize a concern at runtime — *"Focus on Goal 1 — make sure my Private DB rows can't leave my device"* — which shapes the summary, not the underlying check.

### Contribute your design back as a reference design

You've built or are operating a PNA against the spec and want to contribute it back to the toolkit. This is the most-used flow.

**Should I submit?** Three patterns justify a submission: a **new architectural commitment** (your design surfaced a constraint the spec doesn't capture — your PR includes a spec diff); **existing patterns on a new platform** (you exercise existing ACs on a substrate/use-case not yet attested — no spec change needed); or an **ecosystem value-add** (you fill a use-case gap or bring something no existing design demonstrates). If your design is *identical* to an existing reference with no novelty, reach out before authoring.

1. **Preflight via the skill — iterate until clean.** Open Claude Code in your design's repo and ask:

   > "Use the toolkit skill to validate this design for submission to the toolkit."

   The agent locates (or interactively creates) your Architecture document, asks what's architecturally interesting, and reports what's broken or missing as a structured list — missing files/sections, attestation rows without Verification, cited-but-absent code, a missing/malformed `design.toml`, failing tests, license problems. Fix things, re-run preflight, repeat until the report is clean.

2. **Ask the agent to open the PR.** Once preflight is clean:

   > "Use the toolkit skill's contribute flow to open a PR adding this design at `<path>` (commit `<sha>`)."

   The agent reads [`CONTRIBUTING.md`](../CONTRIBUTING.md), authors the design record at `reference_designs/<name>/README.md`, copies your Architecture document to `reference_designs/<name>/Architecture.md`, writes the machine-readable manifest `reference_designs/<name>/design.toml` (per [`reference_designs/templates/design.toml`](../reference_designs/templates/design.toml) — repo, `[flavor]` picks, the `[verify]` entrypoint, and the SWHID pin once archived), commits the evaluate-report, adds a spec diff if you're proposing one, and opens the PR. The PR template's [reference-design checklist](../.github/pull_request_template.md) lists every required artifact.

3. **Address maintainer feedback.** A maintainer reviews at the judgment layer: does the spec change make sense? Does the Architecture document accurately describe the design? Is the attestation table complete with real Verification evidence? License must be OSI-approved and permit Software Heritage archival. Fix, push, repeat.

4. **After your PR is accepted.** Acceptance is the merge. Then:
   - The maintainer archives your source with `just swh-save <your-repo-url> <tag>` (a wrapper over Software Heritage's Save Code Now that prints the git-compatible SWHIDs), and records the returned `swh:1:dir`/`swh:1:rev` in your `design.toml` (flipping `archival = "archived"`) and design record. Your source then survives even if your upstream repo is deleted. For high-signal designs the maintainer may also mirror to a `pnt-archive` fork; the SWHID alone is sufficient for the archival promise.
   - The Toolkit-Version is bumped per [`CONTRIBUTING.md` § Versioning](../CONTRIBUTING.md#versioning) (Patch for clarifications, Minor for additive changes, Major for breaking ones; an axis carries its own version too).
   - Run preflight once more against the merged state — it should come out clean.

---

## Working in this repo

For developers working **on the toolkit itself** (the spec, lints, contracts, skill, docs).

**Commands.** Everything is driven through `just` (a `justfile` at the repo root); run `just` for the menu. No setup or virtualenv is needed — the tools are stdlib-only `python3` (3.10+).

| Command | What it does |
|---|---|
| `just` | Show the command menu. |
| `just ci` | Run the full local gate — `lint` + `lint-selftest`. **Run this before pushing.** |
| `just lint` | Spec / contract / version / constraint / manifest traceability lint (`tools/lint-spec-ids.py`). |
| `just lint-selftest` | The lints' own self-tests: assert the clean tree passes and that each check fails on an injected fault (`tools/tests/lint_selftest.py`). |
| `just egress-lint <dir> [args]` | Scan a candidate PNA's source for off-device egress vectors — the deterministic AC-1 check (args like `--json`, `--allow <origin>` pass through). |
| `just export-lint <path> [args]` | Check a Private-DB human-readable export is readable with no PNA tooling — the deterministic PR-6 check. |
| `just attestation-lint <dir> [args]` | Check a design's Architecture document — every `conformant` attestation row cites a live, non-deferred (`xfail`/`skip`-free) test or a declared review kind. The deterministic half of "exists **and** passes." |
| `just report-lint <path>` | Validate `evaluate-report.json` instance(s) against the render contract the Visual Validator reads — a single file or a reports directory (e.g. a cron drop). |
| `just swh-save <repo-url> [ref] [clone]` | Request Software Heritage archival of a design's repo and print the SWHID fields to paste into its `design.toml`. |
| `just test-design <name>` | *(Scaffold, inert)* the planned per-design conformance harness — see [`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md) § Phase 4. |

**Conventions** (full list in [`CLAUDE.md`](../CLAUDE.md)):

- Tools are **stdlib-only `python3` (3.10+)** — no third-party runtime deps.
- **Every lint check needs a fault-injection self-test** in `tools/tests/lint_selftest.py`, added in the same change — a check with no self-test can silently rot.
- **Keep the docs current:** any change a developer would notice (a `just` recipe, a lint check or message, a skill flow, a contract/AC/manifest field, a contribution step) updates this guide in the **same PR**. Put manual test/QA steps in the PR description.

---

## Contributing beyond reference designs

Not every contribution is a reference design — most aren't. The routing is owned by [`CONTRIBUTING.md` § Contribution types](../CONTRIBUTING.md#contribution-types) (the deciding question: *does a design have to do anything new to stay conformant after this change?*) and surfaced in the [PR template](../.github/pull_request_template.md)'s two lanes; in brief:

- **Toolkit fix / docs / tooling** — a lint improvement, a new tool, a doc fix, a clarifying spec edit (Patch-level). No reference-design attestation needed; just `just ci` green and (per the rule above) any user-facing doc updated in the same PR.
- **Reference design, or a spec/contracts change** — completes the reference-design checklist. Note the policy in [`CONTRIBUTING.md`](../CONTRIBUTING.md): **new normative content (a new AC, Exception, or Constraint) is not accepted without a demonstrating reference design** — the spec and a working design that exercises it co-evolve. So "a new AC" rides in on a design's PR; "fix a typo in an AC" or "tighten a lint" does not.

If you find a spec gap, ambiguity, or contradiction, your PR includes a spec diff; the maintainer reviews it in the context of the demonstrating design. After merge the Toolkit-Version is bumped per [`CONTRIBUTING.md` § Versioning](../CONTRIBUTING.md#versioning).

---

## Quick reference

| You want to … | Open Claude Code in … | Ask the agent … |
|---|---|---|
| Build a new PNA | your new project's dir | "Use the toolkit skill to walk me through axis picks for a [use case] PNA." |
| Audit someone's PNA before installing | PNA Toolkit (with candidate at known path) | "Use the toolkit skill to audit `<path>` for PNA-spec conformance." |
| Preflight your design for submission | your design's repo | "Use the toolkit skill to validate this design for submission to the toolkit." |
| Open the contribution PR | PNA Toolkit | "Use the toolkit skill's contribute flow to open a PR adding this design." |

Working on the toolkit itself: `just` for the command menu, `just ci` before pushing.

---

## Where to find things

- [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) — the canonical spec (vocabulary, Goals, ACs, slot map, sub-contracts)
- [`spec/axes.md`](../spec/axes.md) — axes, attested picks, and the constraints each pick inherits
- [`spec/use_cases.md`](../spec/use_cases.md) — attested classes of PNA
- [`spec/exceptions.md`](../spec/exceptions.md) — Exceptions (`EX-*`): declared, handled departures from a guarantee
- [`spec/constraints.md`](../spec/constraints.md) — Constraints (`CST-*`): platform/substrate ceilings inherited by axis picks
- [`contracts/`](../contracts/) — typed contracts, each with a `Realizes:` header
- [`reference_designs/`](../reference_designs/) — accepted designs + templates (record, Architecture, `design.toml`)
- [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) — the agent-consumption view of the flows above
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — full contribution rules and versioning policy
- [`CLAUDE.md`](../CLAUDE.md) — repo conventions and the documentation map
- [`justfile`](../justfile) — the command runner (`just` for the menu)
- [`tools/`](../tools/) — the validators and the audit-report schema:
  - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract / exception / constraint / manifest / version traceability lint
  - [`tools/tests/lint_selftest.py`](../tools/tests/lint_selftest.py) — the lints' own self-tests
  - [`tools/egress-lint.py`](../tools/egress-lint.py) — deterministic AC-1 off-device-egress check
  - [`tools/export-readable-lint.py`](../tools/export-readable-lint.py) — deterministic PR-6 export-readability check
  - [`tools/attestation-evidence-lint.py`](../tools/attestation-evidence-lint.py) — deterministic attestation-evidence check (every `conformant` row cites a live, non-deferred test or a declared review kind)
  - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — typed schema for the audit report
  - [`tools/report-fixtures-lint.py`](../tools/report-fixtures-lint.py) — deterministic render-contract check for `evaluate-report.json` instances (the Visual Validator's input); samples at [`tools/report-viewer/sample-reports/`](../tools/report-viewer/sample-reports/)
  - [`tools/report-viewer/`](../tools/report-viewer/) — the Visual Validator viewer (static HTML/JS): open `index.html` and load an `evaluate-report.json` (drag-drop / file picker / `?report=`)
  - [`tools/swh-save.sh`](../tools/swh-save.sh) — Software Heritage archival + SWHID computation
- [`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md) — what the conformance suite covers, the active/archival lifecycle, and the roadmap
- [`plans/`](../plans/) — live plans tracking the toolkit's own evolution
