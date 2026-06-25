# PNA Toolkit User's Guide

The PNA (Personal Network Application) Spec is the canonical specification; this guide is the canonical **how-to**. It is task-ordered: each section is a numbered sequence of actions to accomplish one thing. Where a step needs a rule or definition, it links to the authoritative document rather than restating it.

The PNA Toolkit is built to be consumed by AI coding agents, and its users are developers. Most of this guide assumes you have an agent (Claude Code, Cursor, an equivalent) you can ask things like *"use the toolkit skill to validate my design."* The skill at [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md) is the agent-consumption view of the build / audit / contribute flows below.

**The fastest way in is auditing.** If you just want to know whether a contact app is safe before you install it — without building or contributing anything — go straight to [Audit a candidate PNA](#audit-a-candidate-pna-before-installing-it). Point an agent at the app's source and get back an AC-keyed safety report.

> **Status (June 2026).** The toolkit's deterministic tooling is tested and CI-enforced; the agent-driven flows are being exercised for real.
>
> **Tested / CI-enforced** (run on every PR, reproducible locally with `just ci`):
> - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract / exception / constraint / manifest / toolkit-version traceability lint.
> - [`tools/tests/lint_selftest.py`](../tools/tests/lint_selftest.py) — the lints' own self-tests (each check is proven to fail on an injected fault).
> - [`tools/egress-lint.py`](../tools/egress-lint.py) — the deterministic AC-1 off-device-egress check, with clean/dirty fixtures.
> - [`tools/export-readable-lint.py`](../tools/export-readable-lint.py) — the deterministic PR-6 export-readability check, with clean/dirty fixtures.
> - [`tools/attestation-evidence-lint.py`](../tools/attestation-evidence-lint.py) — the deterministic attestation-evidence check (a `conformant` row must cite a live, non-`xfail`/`skip` test or a declared review kind), with clean/dirty fixtures.
> - [`tools/loopback-surface-lint.py`](../tools/loopback-surface-lint.py) — the deterministic loopback-surface check for an app-opened HTTP daemon (candidate `AC-PRM-H`, RFC): an L1 non-loopback bind gates; an L2 unauthenticated-handler is advisory (`--strict` gates it). Clean/dirty/noauth fixtures.
> - [`tools/validate.py`](../tools/validate.py) — `just validate <candidate>`: runs the Tier-S deterministic lints and folds them into one `evaluate-report.json` (the deterministic baseline an agent's LLM pass then enriches); self-tested on the egress fixtures.
> - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — the audit-report schema.
>
> Plus a separate **`viewer-e2e`** CI job (the one non-stdlib job, path-filtered to viewer PRs): opt-in Playwright render tests for the Visual Validator viewer (`tools/report-viewer/tests/`). Reproduce locally with `just test-viewer` (one-time `just setup-test`) — **not** `just ci`.
>
> **Exercised end-to-end:** the **contribute** flow — `fellows_local_db`'s Exceptions, Constraints, and conformance-suite contributions were all authored through it. The **build** and **audit** flows are still being dogfooded against `fellows_local_db`; the agent prompts and output shapes below describe the intended behavior per [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md), and continue to be refined. The **harden** flow is the newest and is **advisory** — it recommends environmental countermeasures rather than checking ACs; its catalog lives in [`spec/exceptions.md`](../spec/exceptions.md).

---

## Install the skill

The flows below are driven by the toolkit skill at [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md). If you haven't used Claude Code skills before: they're modular agent capabilities that live in a `.claude/skills/<skill-name>/SKILL.md` layout. You install one once, then use it through natural language in any chat.

### How Claude decides to use the skill

At session start Claude Code loads every installed skill's **name and `description`** into context — not the full body, which loads only when the skill actually runs. Claude then **auto-discovers** the skill: when your prompt matches the triggers in its `description`, it invokes the skill on its own, without you naming it. The toolkit skill's description is written to fire on phrases like *"is this app safe to install?"*, *"does my app conform?"*, or "build a local-first contact app", so a request like *"audit this contact app before I install it"* trips it automatically.

You don't have to rely on that, though. You can always invoke it explicitly — `/pna-toolkit`, or just *"Use the toolkit skill to…"*. Auto-discovery is a match against prose, so it's a strong default but not a guarantee; for a deliberate task like validating that a repo conforms, naming the skill (or the flow) is the most reliable path — and that's how the prompts in this guide are phrased.

**Recommended — symlink globally** (run from your toolkit working directory):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/pna-toolkit" ~/.claude/skills/pna-toolkit
```

Symlinking keeps the skill in sync with your toolkit clone — a `git pull` here updates the skill everywhere it's used.

**Alternatives:**

- **Copy instead of symlink** — replace `ln -s` with `cp -r` to pin the skill to a specific version. You'll re-copy when you want updates.
- **Run Claude Code from the toolkit itself** — no install required; the skill is discoverable from this directory. Adequate for one-off auditing.

### Per-repo install (for a design that contributes to the PNA Toolkit)

When a PNA repo actively contributes back (it's a reference design, or you drive the contribute flow from it), scope the skill to that repo at `<your-project>/.claude/skills/pna-toolkit` so collaborators on it pick the skill up. Two forms:

- **Symlink** (dev convenience, no drift):
  ```bash
  ln -s <path-to-pnt>/pna-toolkit <your-project>/.claude/skills/pna-toolkit
  ```
  Stays in sync with your toolkit clone, but the absolute path is machine-specific — **don't commit a machine-specific symlink.**
- **Vendored copy** (portable, committable):
  ```bash
  cp -r <path-to-pnt>/pna-toolkit <your-project>/.claude/skills/pna-toolkit
  ```
  Commit it **with a provenance note pinning the toolkit commit** it was copied from (e.g. an `INSTALLED_FROM.md` beside `SKILL.md`). Collaborator-friendly and reproducible, but it **drifts** from upstream — re-sync before relying on it for a contribution.

Pick the symlink for local iteration; pick the vendored copy when the design repo should carry the skill for everyone working on it.

> **Precedence gotcha — a global install shadows the repo copy.** When the same skill name exists at more than one scope, Claude Code resolves in the order **enterprise → personal (`~/.claude/skills`) → project (`<repo>/.claude/skills`)**, and the higher scope wins *silently* — no collision warning. So if you've done the recommended global install **and** vendored a pinned copy into a design repo, the global copy wins, and your pinned, reproducible copy is never used. When a contribution depends on validating against a specific pinned Toolkit-Version, remove or rename the global install for that work.

**Verify.** Start Claude Code and try one of the prompts below; if the skill triggers, you're set. You can also ask *"what PNA Toolkit skills do you have available?"*. **Note:** a restart is only needed the **first** time you create a top-level skills directory that didn't exist when the session started (e.g. the `mkdir -p ~/.claude/skills` above). Once the directory exists, later edits are picked up live.

---

## Using the skill

The skill packages four flows. Each is a numbered sequence below; run whichever fits your task.

### Build a conformant PNA

You're starting (or extending) a personal network application.

1. **Skim the spec and pick a use case.** You don't need to memorize [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) to start — but read enough to know its vocabulary (*slot*, *axis*, *flavor*, *AC*, *Exception*, *Constraint*) and that the universal ACs are non-negotiable. Then browse [`spec/use_cases.md`](../spec/use_cases.md) for the attested classes of PNA and pick one. A use case suggests default axis picks but doesn't determine them.

2. **Walk through axis picks with the agent.** Open Claude Code in your new project's directory and ask:

   > "Use the toolkit skill to walk me through axis picks for a [Directory Archive | Personal Relationship Manager | …] PNA."

   The agent walks each Axis (distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure) and the attested picks per Axis. Your full set of picks is your *flavor*. Some picks entail a **conditional AC** (defined in [`spec/PNA_Spec.md` § Conditional architectural commitments](../spec/PNA_Spec.md#conditional-architectural-commitments)); each pick also brings its own `RZ-*` realizations and constraints — see [`spec/axes.md`](../spec/axes.md).

3. **Enumerate the Constraints your picks inherit.** A [Constraint](../spec/constraints.md) (`CST-*`) is a platform/substrate ceiling that comes attached to an axis pick — e.g. a `web-bundle` × `opfs-sqlite-wasm` PNA inherits the `CST-PWA-*` family. The agent lists them and helps you plan the honest per-platform capability reduction up front (the cross-references in [`spec/axes.md`](../spec/axes.md) name which picks inherit which constraints). If your design will deliberately depart from a guarantee, plan the [Exception](../spec/exceptions.md) (`EX-*`) handling too — but the **un-relaxable floor** (AC-18 / AC-19 / AC-MCP-B, the human-review-before-send seam) may not be relaxed even with consent (the lint rejects an exception that names a floor AC in `Relaxes:`).

4. **Study the closest reference design.** Each [`reference_designs/<name>/`](../reference_designs/) directory has a design record naming its flavor and a Software Heritage SWHID pointing to archived source. Pick the design whose flavor overlaps your picks the most; read its code and treat it as the seed your PNA grows from. Adapting beats starting from scratch — the cross-slot integration work is already done. To find proven code *per AC* across all designs (not just the closest one), consult the [realization index](#the-realization-index) — it maps each AC to the designs that realize it, where, and at which archived commit.

5. **Stub an Architecture document.** Copy [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md) to `docs/Architecture.md` in your design's own repo. Fill in Toolkit-Version, axis picks and their versions, and per-axis implementation notes. Leave the attestation tables empty for now — you fill them as you build (step 7).

6. **Build against the typed contracts.** [`contracts/`](../contracts/) holds the load-bearing interfaces, each opening with `Realizes: AC-X, AC-Y` naming the ACs it serves. Your code conforms to these. If you need to deviate from a contract, propose a spec change (see [Contributing beyond reference designs](#contributing-beyond-reference-designs)) rather than diverging silently.

7. **Fill in the attestation table as you build.** For every applicable AC (universal **and** conditional in `PNA_Spec.md` — the picks that trigger each conditional AC are listed in `axes.md`), every Exception/Constraint your design raises or inherits, and the user-mediation boundaries it attests (UM-1/2/3, per [`spec/user_mediation.md`](../spec/user_mediation.md)), record three fields in your Architecture document:
   - **Realization** — how your code realizes/handles it, with `file:line` references.
   - **Verification** — the test, LLM rubric, or human-review note that verifies it for *your* design. A `conformant` row needs **executable evidence** (a resolvable test) or an explicitly declared review kind — a bare doc pointer is not evidence, and a negative invariant ("X must NOT happen") needs a *negative* test. See the [evaluate flow's attestation-evidence rules](../pna-toolkit/SKILL.md) for the full bar.
   - **Status** — `conformant` / `partial` (with the known gap) / `not-applicable` (with reason).

8. **Self-check.** Run the [Audit](#audit-a-candidate-pna-before-installing-it) flow on your own in-progress code before declaring done, and **save its `evaluate-report.json`** (e.g. under `docs/conformance/`) — the contribution PR commits this artifact, so producing it now is part of building. For the AC-1 (private-data-sovereignty) row, add an `egress-allow.json` to your repo listing the remote origins your flavor legitimately uses, and run `just egress-lint <your-source-dir>` — it's the deterministic half of that check and makes a ready-made Verification entry. Wire it into your own CI so a future change can't silently introduce an off-device data path.

### Audit a candidate PNA before installing it

You have a PNA in front of you (someone else's, or your own in-progress one) and you want an LLM to check whether it actually honors the PNA Spec — whether it's safe with your data.

1. **Get the candidate's source.** Clone the repo. If you only have a bundle, ask for the source — you can't audit a black box.

2. **Open Claude Code in the PNA Toolkit repo, with the candidate's source at a known path.** Run the audit from the toolkit, not the candidate: the skill ([`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md)), the [`evaluate-report.schema.json`](../tools/evaluate-report.schema.json), and the deterministic `just` lints all live here, and the agent reads the skill when the prompt matches. (If you've installed the skill globally you can run from anywhere — but you still need a toolkit checkout reachable for the `just` lints.)

3. **Ask the agent to run the audit:**

   > "Use the toolkit skill to audit `<path-to-candidate>` for PNA-spec conformance. Is this app safe for me to install?"

   If the candidate ships its own Architecture document, the agent validates it against the code (do cited locations match? do declared verifications pass?). Otherwise it infers axis picks from the source and walks every applicable AC from scratch. It also **detects and verifies Exceptions** (`EX-*`), **Constraints** (`CST-*`), and **User-mediation** (`UM-*`, at each mutation/egress boundary) — confirming each declared deviation/boundary is handled honestly and flagging any *undeclared* one. As part of the audit it runs the deterministic checks in `tools/` (`just egress-lint <path>` for AC-1 off-device leaks; `just export-lint <path>` for PR-6 export readability; `just attestation-lint <path>` to confirm the candidate's own `conformant` attestation rows cite live, non-deferred evidence) and folds their results into the matching AC findings as `source: deterministic` evidence. `just validate <path>` runs that deterministic tier in one command and writes the baseline `evaluate-report.json` for the agent to enrich — but mind its honest ceiling: a clean deterministic run is `indeterminate` (necessary, not sufficient), never a conformance verdict, so the LLM and human tiers still do the load-bearing work.

4. **Read the AC-keyed report.** The agent emits a typed artifact ([`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)) with a human-readable rendering over it. Per-finding status is one of `conformant` / `non-conformant` / `not-applicable` / `unable-to-determine`, each keyed by AC, EX, or CST ID. **Save the JSON** (the **canonical filename is `evaluate-report.json`**, e.g. under `docs/conformance/` in the candidate's repo) and validate it against the render contract with `just report-lint <path>` — a schema-valid artifact is what the [Visual Validator](../tools/report-viewer/) renders and what a contribution PR commits ([Contribute](#contribute-your-design-back-as-a-reference-design) step 2). A candidate may *also* ship internal conformance readouts — a generically-named `report.json`, a human-readable summary — which are **not** the render-contract artifact, so validate before trusting one; a cooperating design can emit `evaluate-report.json` deterministically from its own `design.toml` `[verify].entrypoint` (see [`CONTRIBUTING.md` § PR contents required](../CONTRIBUTING.md#pr-contents-required)). Because the report is typed, two runs over the same candidate are diffable — re-audit after an update and diff the JSON for per-finding status changes (the "did anything quietly stop conforming?" signal).

5. **Decide.** Goals 1–4 are the load-bearing user-facing concerns — ownership of the root (Goal 1), integrity-by-validation (Goal 2; absorbs sourced-data honesty and local diagnosability), protection from egress / private-data sovereignty (Goal 3), durability against entropy and accidents (Goal 4). If any of those are non-conformant (and not honestly handled via a declared Exception), the design is not safe to trust with your data. You can emphasize a concern at runtime — *"Focus on Goal 3 — make sure my Private DB rows can't leave my device"* — which shapes the summary, not the underlying check.

### Contribute your design back as a reference design

You've built or are operating a PNA against the spec and want to contribute it back to the toolkit. This is the most-used flow.

**Should I submit?** Three patterns justify a submission: a **new architectural commitment** (your design surfaced a constraint the spec doesn't capture — your PR includes a spec diff); **existing patterns on a new platform** (you exercise existing ACs on a substrate/use-case not yet attested — no spec change needed); or an **ecosystem value-add** (you fill a use-case gap or bring something no existing design demonstrates). If your design is *identical* to an existing reference with no novelty, reach out before authoring.

1. **Preflight via the skill — iterate until clean.** Run this from **your design's repo**, and make sure two things are reachable from there: the skill (install it per [Install the skill](#install-the-skill) — globally, or repo-scoped) **and** a PNA Toolkit checkout (preflight runs the deterministic `just` lints, which live in the toolkit). Then open Claude Code in your design's repo and ask:

   > "Use the toolkit skill to validate this design for submission to the toolkit."

   The agent locates (or interactively creates) your Architecture document, asks what's architecturally interesting, and reports what's broken or missing as a structured list — missing files/sections, attestation rows without Verification, cited-but-absent code, a missing/malformed `design.toml`, failing tests, license problems. Fix things, re-run preflight, repeat until the report is clean.

2. **Switch to the PNA Toolkit repo and ask the agent to open the PR.** The PR adds files under `reference_designs/` *in the toolkit*, so it's authored from the toolkit repo (with your design repo still reachable at a known path), not from your design's repo. Once preflight is clean:

   > "Use the toolkit skill's contribute flow to open a PR adding this design at `<path>` (commit `<sha>`)."

   The agent reads [`CONTRIBUTING.md`](../CONTRIBUTING.md), authors the design record at `reference_designs/<name>/README.md`, copies your Architecture document to `reference_designs/<name>/Architecture.md`, writes the machine-readable manifest `reference_designs/<name>/design.toml` (per [`reference_designs/templates/design.toml`](../reference_designs/templates/design.toml) — repo, `[flavor]` picks, the `[verify]` entrypoint, and the SWHID pin once archived), commits the `evaluate-report.json` you saved during [Build](#build-a-conformant-pna) step 8 / the audit, adds a spec diff if you're proposing one, and opens the PR. The PR template's [reference-design checklist](../.github/pull_request_template.md) lists every required artifact.

3. **Address maintainer feedback.** A maintainer reviews at the judgment layer: does the spec change make sense? Does the Architecture document accurately describe the design? Is the attestation table complete with real Verification evidence? License must be OSI-approved and permit Software Heritage archival. Fix, push, repeat.

4. **After your PR is accepted.** Acceptance is the merge. Then:
   - **The maintainer archives your source to Software Heritage** at the accepted commit — a post-merge maintainer step (you MAY pre-compute the SWHIDs and include them in the PR). The exact command and its one gotcha live in [Working in this repo → Archive a reference design](#archive-a-reference-design-to-the-software-heritage-archive); the maintainer records the printed `commit` / `swhid_rev` / `swhid_dir` into your `design.toml` (flipping `archival = "archived"`) and design record, so your source survives even if your upstream repo is deleted. For high-signal designs they may also mirror to a `pnt-archive` fork; the SWHID alone is sufficient for the archival promise.
   - The Toolkit-Version is bumped per [`CONTRIBUTING.md` § Versioning](../CONTRIBUTING.md#versioning) (Patch for clarifications, Minor for additive changes, Major for breaking ones; an axis carries its own version too).
   - Run preflight once more against the merged state — it should come out clean.

### Harden the environment your PNA runs in

The first three flows check the *app*; **Harden** advises on the *environment* around it — the runtime where an OS-level AI agent, another local process, or a shared machine could reach your data outside the app's control. It is **advisory**: you get a posture report and recommended countermeasures, not a pass/fail or an AC status. (Concept and catalog: [`spec/exceptions.md` § Environmental threats and the Harden flow](../spec/exceptions.md).)

1. **Describe your environment to the agent.** Open Claude Code in the PNA Toolkit repo and tell it where the PNA runs and what could reach it:

   > "Use the toolkit skill to harden the environment my PNA runs in — I run OS-level AI agents that can read my files."

   The agent identifies the *environmental threats* your setup exposes (an automation agent with filesystem/MCP reach, another process opening the DB, a shared machine) — hazards the app's own code can't defend against.

2. **Read the posture report.** For each hazard the agent maps the applicable **environmental countermeasures** from the [Countermeasure library](../spec/exceptions.md) — sandbox the agent / `denyRead`, a separate OS user, an MCP access broker with just-in-time grants, a honeytoken + watchdog, human-presence gating — and reports which are **in place**, which **apply but aren't**, and what is **still exposed**, each tagged with its strength class so "best-effort" isn't read as "solved."

3. **Apply the countermeasures you choose — in your environment.** The toolkit advises; you actuate. Where a hazard already has a PNA-intrinsic guard (e.g. AC-MCP-A's per-call consent is the in-app analog of an external MCP broker) the agent says so, so you don't double-pay. If a countermeasure ought to become a built-in AC, that's a [contribute](#contribute-your-design-back-as-a-reference-design)-flow proposal, not a Harden output.

---

## Working in this repo

For developers working **on the toolkit itself** (the spec, lints, contracts, skill, docs).

**Commands.** Everything is driven through `just` (a `justfile` at the repo root); run `just` for the menu. No setup or virtualenv is needed — the tools are stdlib-only `python3` (3.10+). *(The lone exception is the opt-in browser render tests for the Visual Validator viewer — `just setup-test` creates a `.venv` + installs Playwright; they are never part of `just ci`.)*

| Command | What it does |
|---|---|
| `just` | Show the command menu. |
| `just ci` | Run the full local gate — `lint` + `lint-selftest`. **Run this before pushing.** |
| `just lint` | Spec / contract / version / constraint / manifest traceability lint (`tools/lint-spec-ids.py`). |
| `just lint-selftest` | The lints' own self-tests: assert the clean tree passes and that each check fails on an injected fault (`tools/tests/lint_selftest.py`). |
| `just validate <dir> [args]` | One-command deterministic baseline: run the Tier-S lints against a candidate PNA and fold them into one `evaluate-report.json` (`--out PATH`, `--export PATH` pass through). A clean run is `indeterminate` (necessary-not-sufficient), never a green verdict — the agent's LLM pass and a design's `[verify]` entrypoint enrich the same report. |
| `just egress-lint <dir> [args]` | Scan a candidate PNA's source for off-device egress vectors — the deterministic AC-1 check (args like `--json`, `--allow <origin>` pass through). |
| `just export-lint <path> [args]` | Check a Private-DB human-readable export is readable with no PNA tooling — the deterministic PR-6 check. |
| `just attestation-lint <dir> [args]` | Check a design's Architecture document — every `conformant` attestation row cites a live, non-deferred (`xfail`/`skip`-free) test or a declared review kind. The deterministic half of "exists **and** passes." |
| `just loopback-lint <dir> [args]` | Scan a candidate for an unauthenticated app-opened **loopback surface** (candidate `AC-PRM-H`, RFC): an L1 literal non-loopback bind **gates**; an L2 unauthenticated handler is **advisory** (`--strict` promotes it to a gate). A bounded tripwire — the deterministic half, like `egress-lint`. |
| `just report-lint <path>` | Validate `evaluate-report.json` instance(s) against the render contract the Visual Validator reads — a single file or a reports directory (e.g. a cron drop). |
| `just swh-save <repo-url> [ref] [clone]` | Request Software Heritage archival of a design's repo and print the SWHID fields to paste into its `design.toml`. **Pass the `clone` path (3rd arg) when running from the toolkit** — otherwise it computes the toolkit's own SWHIDs from the cwd. See [Archive a reference design](#archive-a-reference-design-to-the-software-heritage-archive). |
| `just rearchive <name> <ref> <clone> [args]` | Re-archive an accepted design at a ref in one step: `swh-save` + rewrite its `design.toml` pin + refresh its bundled `Architecture.md`/`evaluate-report.json` copies + lint. `--no-save` skips the Save Code Now POST (offline re-pin). After it refreshes the bundled Architecture copy, regenerate the realization index (`just realization-index`) so `just ci` stays green. |
| `just realization-index [args]` | Regenerate the derived cross-design [realization index](realization-index.md) (`docs/realization-index.md`) from the bundled designs' attestation tables — which design realizes each AC, where, at which archived commit. `--check` (run by `just ci`) fails if the committed index is stale; `--json` prints the machine model. See [The realization index](#the-realization-index). |
| `just test-design <name>` | *(Scaffold, inert)* the planned per-design conformance harness — see [`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md) § Phase 4. |
| `just setup-test` | **(Opt-in, one-time)** Create `.venv` and install the browser-test deps (`pytest` + Playwright + Chromium) from `requirements-dev.txt`. Needed only for `just test-viewer`. |
| `just test-viewer` | **(Opt-in; NOT in `just ci`)** Render-test the Visual Validator viewer in a real browser (Playwright). See [`plans/viewer-e2e-testing-plan.md`](../plans/viewer-e2e-testing-plan.md). |
| `just view-reports [dir]` | **(Opt-in)** Serve the Visual Validator and flip through a directory of `evaluate-report.json` files (← / →). No arg flips through the bundled samples. |

### Archive a reference design to the Software Heritage archive

A reference design's source is pinned with a Software Heritage ID (SWHID) — the content-addressed identifier from the [Software Heritage](https://www.softwareheritage.org/) archive's *Save Code Now* service — so it survives even if the upstream repo disappears. Run this when you **accept** a design, or **re-archive an existing one** at a newer commit (e.g. after its attestation changes). It's a maintainer step — `swh-save` needs no PR.

**Run these from the toolkit repo.** `swh-save` is a `just` recipe, so your shell must be in `~/src/personal_network_toolkit` (the `cd` is the first line below). This is a *cross-repo* operation: the 3rd argument points at a **separate** local clone of the design, which is exactly why the working directory matters — `just` resolves from the toolkit, and the SWHIDs are computed from that other clone.

```bash
cd ~/src/personal_network_toolkit                                        # ← run swh-save from HERE (the toolkit)

# Generic form: <design-repo-url> <git-ref> <path-to-a-local-clone-of-the-design>
just swh-save <design-repo-url> <git-ref> <path-to-local-clone>

# Example — re-archive fellows_local_db at its current HEAD:
git -C ~/src/fellows_local_db pull                                       # make the design's local clone current first
just swh-save https://github.com/richbodo/fellows_local_db HEAD ~/src/fellows_local_db
```

- **The 3rd arg (clone path) is required** here: the SWHIDs are computed from that local clone, and without it the script falls back to the toolkit's own repo and prints the *wrong* IDs. *(Shortcut: run the script from inside the design's repo and you can drop it — `~/src/personal_network_toolkit/tools/swh-save.sh <url> <ref>`.)*
- **`<git-ref>`** is the commit/tag whose attestation you're archiving; it must already be **pushed** so Save Code Now can ingest it. Tag first for a stable ref: `git tag v0.1.1 && git push origin v0.1.1`. Either an **annotated** (`git tag -a`) or lightweight tag works — `swh-save` peels the ref to its commit, so `swhid_rev` always names the commit (not the annotated-tag object).
- The command POSTs the Save-Code-Now request (ingest is async — minutes to hours) and prints paste-ready `commit` / `swhid_rev` / `swhid_dir` lines. Put them in the design's `reference_designs/<name>/design.toml` (and its README), then set `archival = "archived"`.

**Conventions** (full list in [`CLAUDE.md`](../CLAUDE.md)):

- Tools are **stdlib-only `python3` (3.10+)** — no third-party runtime deps. *(One opt-in exception: the viewer's browser render tests use `pytest` + Playwright via `just setup-test` → `just test-viewer`, in their own CI job, never in `just ci` — see [`plans/viewer-e2e-testing-plan.md`](../plans/viewer-e2e-testing-plan.md).)*
- **Every lint check needs a fault-injection self-test** in `tools/tests/lint_selftest.py`, added in the same change — a check with no self-test can silently rot.
- **Keep the docs current:** any change a developer would notice (a `just` recipe, a lint check or message, a skill flow, a contract/AC/manifest field, a contribution step) updates this guide in the **same PR**. Put manual test/QA steps in the PR description.

### The realization index

[`docs/realization-index.md`](realization-index.md) is a **generated** cross-design map: for each AC, *which accepted reference design realizes it, where in its code, and at which archived commit*. It's the asset-dual of the [field notes](field-notes/) — a field note says what an AC is easy to get *wrong*; the index says where the proven code that gets it *right* lives. A builder adapting the closest design (see [Build](#build-a-conformant-pna) step 4) uses it to find proven realizations by AC instead of reading every design's source; the **coverage summary** flags the ACs realized by more than one design — the prime patterns to compare.

- **It is derived, not hand-written.** Every row comes from the bundled `reference_designs/<name>/Architecture.md` attestation tables + the `design.toml` SWHID pin. Don't edit it by hand — run `just realization-index` to regenerate, and `just ci` fails (via `--check`) if the committed copy is stale. Regenerate after anything that changes a bundled Architecture copy (notably `just rearchive`).
- **Pointer coverage is a tracked goal.** The index reports a per-design *realization-pointer coverage* number; the standing goal is **100%**. A row below the bar is attestation prose that named a symbol without its file — which is why the [Architecture template](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md) now asks for `path:symbol` realizations and full `path/to/test.py::name` verifications. Improving a design's attestations toward full coverage is ongoing cross-repo work tracked in [`docs/roadmap.md`](roadmap.md).

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
| Harden the environment your PNA runs in | PNA Toolkit (with your environment described) | "Use the toolkit skill to harden the environment my PNA runs in." |

Working on the toolkit itself: `just` for the command menu, `just ci` before pushing.

---

## Where to find things

- [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) — the canonical spec (vocabulary, Goals, ACs, slot map, sub-contracts)
- [`spec/axes.md`](../spec/axes.md) — axes, attested picks, and the constraints each pick inherits
- [`spec/use_cases.md`](../spec/use_cases.md) — attested classes of PNA
- [`spec/exceptions.md`](../spec/exceptions.md) — Exceptions (`EX-*`): declared, handled departures from a guarantee
- [`spec/constraints.md`](../spec/constraints.md) — Constraints (`CST-*`): platform/substrate ceilings inherited by axis picks
- [`spec/user_mediation.md`](../spec/user_mediation.md) — User-mediation (`UM-*`): the third general mechanism — the actuation invariant (proposer stages, principal disposes; UM-1/2/3)
- [`contracts/`](../contracts/) — typed contracts, each with a `Realizes:` header
- [`reference_designs/`](../reference_designs/) — accepted designs + templates (record, Architecture, `design.toml`)
- [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md) — the agent-consumption view of the flows above
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — full contribution rules and versioning policy
- [`CLAUDE.md`](../CLAUDE.md) — repo conventions and the documentation map
- [`justfile`](../justfile) — the command runner (`just` for the menu)
- [`tools/`](../tools/) — the validators and the audit-report schema:
  - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract / exception / constraint / manifest / version traceability lint
  - [`tools/tests/lint_selftest.py`](../tools/tests/lint_selftest.py) — the lints' own self-tests
  - [`tools/egress-lint.py`](../tools/egress-lint.py) — deterministic AC-1 off-device-egress check
  - [`tools/export-readable-lint.py`](../tools/export-readable-lint.py) — deterministic PR-6 export-readability check
  - [`tools/attestation-evidence-lint.py`](../tools/attestation-evidence-lint.py) — deterministic attestation-evidence check (every `conformant` row cites a live, non-deferred test or a declared review kind)
  - [`tools/loopback-surface-lint.py`](../tools/loopback-surface-lint.py) — deterministic loopback-surface check for an app-opened HTTP daemon (candidate `AC-PRM-H`, RFC; L1 bind gates, L2 no-auth advisory, `--strict` gates L2)
  - [`tools/validate.py`](../tools/validate.py) — `just validate <candidate>`: the one-command Tier-S deterministic baseline, emitting an `evaluate-report.json`
  - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — typed schema for the audit report
  - [`tools/report-fixtures-lint.py`](../tools/report-fixtures-lint.py) — deterministic render-contract check for `evaluate-report.json` instances (the Visual Validator's input); samples at [`tools/report-viewer/sample-reports/`](../tools/report-viewer/sample-reports/)
  - [`tools/report-viewer/`](../tools/report-viewer/) — the Visual Validator viewer (static HTML/JS): open `index.html` and load an `evaluate-report.json` (drag-drop / file picker / `?report=`)
  - [`tools/swh-save.sh`](../tools/swh-save.sh) — Software Heritage archival + SWHID computation
  - [`tools/realization-index.py`](../tools/realization-index.py) — derives the cross-design [realization index](realization-index.md) from the bundled attestation tables (`just realization-index`; `--check` gates `just ci`)
- [`docs/realization-index.md`](realization-index.md) — generated cross-design map: which design realizes each AC, where, at which archived commit (the asset-dual of the field notes); rationale in [`docs/design-notes/2026-06-harvesting-reusable-code.md`](design-notes/2026-06-harvesting-reusable-code.md)
- [`docs/conformance-scope-and-lifecycle.md`](conformance-scope-and-lifecycle.md) — what the conformance suite covers, the active/archival lifecycle, and the roadmap
- [`docs/field-notes/`](../docs/field-notes/) — AC-keyed lessons harvested from reference designs (pitfalls + negative-invariant checklists), read before building or auditing that AC; the practice's rationale is [`docs/design-notes/2026-06-capturing-conformance-lessons.md`](design-notes/2026-06-capturing-conformance-lessons.md)
- [`plans/`](../plans/) — live plans tracking the toolkit's own evolution
