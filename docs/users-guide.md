# PNT User's Guide

The PNA (Personal Network Application) Spec is the canonical specification; this guide is the canonical how-to. It gives step-by-step instructions corresponding to each of the success criteria listed in [`README.md` § Status](../README.md#status).

PNT (Personal Network Toolkit) is built to be consumed by AI coding agents. Most of this guide assumes you have an agent (Claude Code, Cursor, an equivalent) you can ask things like *"use the PNT skill to validate my design."* The skill at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) is the agent-consumption view of everything in this guide.

**The fastest way in is auditing.** If you just want to know whether a contact app is safe before you install it — without building or contributing anything — go straight to [Goal 2](#goal-2--audit-a-candidate-pna-before-installing-it). It's the lowest-friction front door to PNT: point an agent at the app's source and get back an AC-keyed safety report.

> **Status note (May 2026).** PNT's deterministic tooling is tested; the agent-driven flows are now being exercised for real.
>
> **Tested / CI-enforced:**
> - [`tools/egress-lint.py`](../tools/egress-lint.py) — the deterministic AC-1 egress check, with clean/dirty self-test fixtures run in CI.
> - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract / exception / toolkit-version traceability lint, run in CI.
> - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — the audit-report schema, validated against its meta-schema and conditional rules.
>
> **Exercised end-to-end:** the **contribute** flow — `fellows_local_db`'s Exceptions contribution and this Toolkit-Version work were both authored through it, with the build and evaluate flows informing that work. The **build** and **audit** flows are still being dogfooded; Phase 5 continues to validate them against `fellows_local_db`. The agent prompts and output shapes below describe the intended behavior per [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md); expect continued refinement.

---

## Install the skill

The flows below are driven by the PNT skill at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md). If you haven't used Claude Code skills before: they're modular agent capabilities that live in a `.claude/skills/<skill-name>/SKILL.md` layout and load automatically when a prompt matches the skill's `description` field. You install a skill once, then invoke it through natural language in any chat.

**Recommended — symlink globally** (run from your PNT working directory):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/pna-build-eval-contrib" ~/.claude/skills/pna-build-eval-contrib
```

Symlinking keeps the skill in sync with your PNT clone — a `git pull` here updates the skill everywhere it's used.

**Alternatives:**

- **Copy instead of symlink** — replace `ln -s` with `cp -r` to pin the skill to a specific version. You'll re-copy when you want updates.
- **Run Claude Code from PNT itself** — no install required; the skill is discoverable from this directory. Adequate for one-off auditing.

### Per-repo install (for a design that contributes to PNT)

When a PNA repo actively contributes back (it's a reference design, or you drive the contribute flow from it), scope the skill to that repo at `<your-project>/.claude/skills/pna-build-eval-contrib` so collaborators on it pick the skill up. Two forms:

- **Symlink** (dev convenience, no drift):
  ```bash
  ln -s <path-to-pnt>/pna-build-eval-contrib <your-project>/.claude/skills/pna-build-eval-contrib
  ```
  Stays in sync with your PNT clone, but the absolute path is machine-specific — **don't commit a machine-specific symlink.**
- **Vendored copy** (portable, committable):
  ```bash
  cp -r <path-to-pnt>/pna-build-eval-contrib <your-project>/.claude/skills/pna-build-eval-contrib
  ```
  Commit it **with a provenance note pinning the PNT commit** it was copied from (e.g. an `INSTALLED_FROM.md` beside `SKILL.md`). Collaborator-friendly and reproducible, but it **drifts** from upstream — re-sync (re-copy + bump the pinned commit) before relying on it for a contribution.

Pick the symlink for local iteration; pick the vendored copy when the design repo should carry the skill for everyone working on it.

**Verify.** Start Claude Code and try one of the prompts below; if the skill triggers, you're set. You can also ask *"what PNT skills do you have available?"*. **Note:** skills load at **session start** — if you just installed the skill, restart Claude Code (or open a fresh session) before it becomes invocable; a mid-session install is not picked up.

---

## Goal 1 — Build a conformant PNA

You're starting (or extending) a personal network application.

**Quick steps:**

1. Skim the spec for vocabulary, then pick a use case.
2. Walk through axis picks with the agent (via the skill).
3. Study the reference design closest to your axis picks.
4. Stub an Architecture document declaring Toolkit-Version + axis picks.
5. Build code that satisfies the typed contracts for your picks.
6. Fill in the AC attestation table as you build.
7. Self-check via Goal 2 before declaring done.

**Details:**

**1. Skim the spec and pick a use case.** You don't need to memorize [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) to start — but read enough to know its vocabulary (*slot*, *axis*, *flavor*, *AC*) and that the universal ACs are non-negotiable. Then browse [`spec/use_cases.md`](../spec/use_cases.md) for the attested classes of PNA (Directory Archive realized; Personal Relationship Manager [draft]; Multi-PNA ecosystem [target]) and pick one. A use case suggests default axis picks but doesn't determine them.

**2. Walk through axis picks with the agent.** Open Claude Code in your new project's directory and ask:

   > "Use the PNT skill to walk me through axis picks for a [Directory Archive | Personal Relationship Manager | …] PNA."

   The agent walks each Axis (distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure) and the attested picks per Axis. An *Axis* is an area of functionality with a small set of pre-attested choices; your full set of picks is your *flavor*. Some picks trigger flavor-derived ACs — see [`spec/axes.md`](../spec/axes.md).

**3. Study the closest reference design.** Each [`reference_designs/<name>/`](../reference_designs/) directory has a design record naming its flavor and a Software Heritage SWHID (Persistent IDentifier) pointing to archived source. Pick the design whose flavor has the most overlap with your picks. Read its code; treat it as the seed your PNA grows from. Adapting from an existing design is faster than starting from scratch — most of the cross-slot integration work is already done.

**4. Stub an Architecture document.** Copy [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md) to `docs/Architecture.md` (or equivalent) in your design's own repo. Fill in: Toolkit-Version, axis picks and their versions, and per-axis implementation notes. Leave the AC attestation table empty for now — you'll fill it in as you build (step 6).

**5. Build against the typed contracts.** [`contracts/`](../contracts/) holds the load-bearing interfaces — JSON Schema for the worker init handshake and RPC (Remote Procedure Call) protocol, OpenAPI for distribution auth, SQL DDL for the two database schemas, TypeScript for the Communications transport, JSON Schema for each canonical MCP server's tool surface. Every contract opens with `Realizes: AC-X, AC-Y` naming the ACs it serves; your code conforms to these contracts. If you find you need to deviate from a contract, propose a spec change via Goal 3 (Contribute) rather than just diverging.

**6. Fill in the AC attestation table as you build.** For every applicable AC (universal in `PNA_Spec.md` + flavor-derived from your axis picks in `axes.md`), record three fields in your Architecture document:
   - **Realization** — how your code realizes it, with `file:line` references
   - **Verification** — the test, LLM evaluation rubric, or human-review note that verifies it for your design
   - **Status** — `conformant` / `partial-conformance` (with known gap) / `not-applicable` (with reason)

   The Verification field is load-bearing for Goal 3 (Contribute). See Goal 6 for what makes a good Verification entry.

**7. Self-check.** Run Goal 2 (Audit) on your own in-progress code before declaring the design done. The agent walks every applicable AC and flags non-conformances. For the AC-1 (private-data-sovereignty) row in particular, add an `egress-allow.json` to your repo listing the remote origins your flavor legitimately uses, and run [`tools/egress-lint.py`](../tools/egress-lint.py) against your source — it's the deterministic half of that check and makes a ready-made Verification entry (see Goal 6). Wire it into your own CI so a future change can't silently introduce an off-device data path.

---

## Goal 2 — Audit a candidate PNA before installing it

You have a PNA in front of you (someone else's, or your own in-progress one) and you want an LLM (Large Language Model) to check whether it actually honors the PNA Spec — whether it's safe with your data.

**Quick steps:**

1. Get the candidate's source.
2. Open Claude Code in your PNT directory, with the candidate accessible.
3. Ask the agent to run the audit.
4. Read the AC-keyed report.
5. Decide: any Goal 1–5 non-conformances? → not safe to trust.

**Details:**

**1. Get the candidate's source.** Clone the repo. If you only have a bundle, ask for the source — you can't audit a black box.

**2. Open Claude Code in your PNT directory.** This guide assumes you have PNT cloned alongside the candidate, or that PNT is reachable from the agent's working directory. The skill lives at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) and the agent reads it when the prompt matches.

**3. Ask the agent to run the audit.** Use natural language:

   > "Use the PNT skill to audit `<path-to-candidate>` for PNA-spec conformance. Is this app safe for me to install?"

   If the candidate ships its own Architecture document with an AC attestation table, the agent validates the document against the code (do cited code locations match the claimed realization? do declared verification mechanisms actually pass?). If there's no Architecture document, the agent infers axis picks from the source and walks every applicable AC from scratch.

   As part of the audit the agent also runs the deterministic checks in `tools/` — notably [`tools/egress-lint.py`](../tools/egress-lint.py), which scans for off-device data leaks (the AC-1 sovereignty concern) — and folds their results into the matching AC findings as `source: deterministic` evidence, alongside its own reading. The deterministic layer catches the one violation that's easy to miss in a large tree; the LLM layer reasons about everything the lint can't.

**4. Read the AC-keyed report.** The agent produces a structured report keyed by AC ID, emitted as a typed artifact ([`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)) with a human-readable rendering over it. Per-AC status is one of:
   - `conformant` — design honors this AC; cited code locations included
   - `non-conformant` — design violates this AC; report names the AC requirement and the offending code
   - `not-applicable` — design's flavor doesn't trigger this AC
   - `unable-to-determine` — needs human review

   Because the report is typed, two runs over the same candidate are diffable. Ask the agent to save the artifact (e.g. `eval-report.json`); when the app ships an update, re-audit and diff the two JSON files — the per-AC status changes are your drift/regression signal (the "did anything quietly stop conforming?" check). The human-readable summary you read is just a rendering over this artifact.

**5. Decide.** Goals 1–5 are the load-bearing user-facing concerns — private-data sovereignty (Goal 1), sourced-data honesty (Goal 2), user-controlled communication (Goal 3), durability (Goal 4), local diagnosability (Goal 5). If any of those are non-conformant, the design is not safe to trust with your data. Non-conformances against architectural details that don't touch Goals 1–5 are still worth fixing but aren't immediate red flags.

**Optional: emphasize a specific concern.** E.g.: *"Focus on Goal 1 — make sure my Private DB rows can't leave my device."* This shapes the summary, not the underlying check.

---

## Goal 3 — Submit your design as a reference design

You've built (or are operating) a PNA against the spec and want to contribute it back to PNT. This is the most-used flow and gets the most space.

**Quick steps:**

1. Decide if your design is worth submitting (see "Should I submit?" below).
2. Preflight your design via the skill — iterate fix → re-preflight until clean.
3. Ask the agent to open the PR.
4. Address maintainer feedback.
5. Run preflight once more against the merged state.

### Should I submit?

Three patterns are valuable enough to justify a submission:

- **New architectural commitment.** Your design surfaced a constraint the spec doesn't yet capture. Your PR will include a spec diff.
- **Existing patterns on a new platform.** Your design exercises existing ACs on a substrate or use-case not yet attested in the reference set. No spec change needed; your design expands the ecosystem.
- **Ecosystem value-add.** Your design fills a use-case gap, brings accessibility, or makes something easier that no existing design demonstrates.

If your design is *identical* to an existing reference with no novelty, reach out before authoring — the PR may not be worth the maintenance overhead.

**Details:**

**1. Preflight your design via the skill.** Open Claude Code in your design's repo (or in PNT, with a path to your design). Ask:

   > "Use the PNT skill to validate this design for submission to PNT."

   The agent will:

   1. **Locate your Architecture document.** If it exists, validate it against the code. If it doesn't, walk you through creating one interactively (Toolkit-Version, axis picks, per-axis notes, AC attestation rows).
   2. **Ask what's interesting architecturally** about your design (one of the three patterns above).
   3. **Report what's broken or missing** as a structured list — files, sections, Verification fields, cited-but-absent code, failing tests, license problems.

   Iterate: fix things, re-run preflight, keep going until the report is clean.

**2. Ask the agent to open the PR.** Once preflight is clean, ask:

   > "Use the PNT skill's contribute flow to open a PR adding this design at `<path-to-design>` (commit `<sha>`)."

   The agent will read [`CONTRIBUTING.md`](../CONTRIBUTING.md), author a design record at `reference_designs/<design-name>/README.md`, copy your Architecture document to `reference_designs/<design-name>/Architecture.md`, add a spec diff if you're proposing one, and open the PR via `gh pr create`.

**3. Address maintainer feedback.** A maintainer reviews at the judgment-and-review layer: does the spec change make sense? Does the Architecture document accurately describe the design? Is the AC attestation table complete? They may ask for changes — fix, push, repeat. License must be OSI-approved; see [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the full acceptance rules.

**4. Final validation after merge.** Once the PR is merged, run preflight one more time against the merged state. It should come out clean.

---

## Goal 4 — Archival via Software Heritage

You don't do anything here — it happens after your PR is accepted.

When the maintainer accepts your PR, they trigger Software Heritage archival on your repo at the accepted commit. The planned tooling is `tools/swh-save.sh <your-repo-url> <commit-sha>` (landing in Phase 5 of the reorganization plan); until then, archival is performed manually via Software Heritage's Save Code Now. The resulting SWHID (a `swh:1:dir:...` content-addressed identifier) is recorded in your design record at `reference_designs/<design-name>/README.md`.

This means your design's source survives even if your upstream repo is deleted or relocated. You don't need to do anything; the maintainer handles it. If they forget, remind them.

For high-signal designs, the maintainer may additionally mirror the design to a `pnt-archive` GitHub organization as a frozen fork. SWHID alone is sufficient for the archival promise; the fork is belt-and-braces.

---

## Goal 5 — Influence spec evolution

If you find a spec gap, ambiguity, or contradiction while building or operating your PNA, your PR includes a spec diff. The maintainer reviews the diff in the context of your demonstrating reference design.

After merge, the Toolkit-Version is bumped per linear SemVer:

- **Patch** — clarifications, typo fixes
- **Minor** — additive changes (new ACs, new axes, new picks, new sub-contracts)
- **Major** — breaking changes (semantically altered ACs, removed picks, contract-shape changes)

Individual axes carry their own version (declared per-axis in each Architecture document). A breaking change to an axis bumps that axis's version and the spec major.

If you discover a gap after your design is already accepted, file a new PR with the spec diff and an updated Architecture document. Same workflow as the initial submission.

---

## Goal 6 — AC traceability in your design

Every architectural commitment in the spec has a stable ID (`AC-1`, `AC-MCP-A`, etc.). Every typed contract names the ACs it realizes via a `Realizes: AC-X, AC-Y` header. Every Architecture document maps each applicable AC to a verification mechanism.

Your job as a contributor: fill in the **AC attestation table** in your Architecture document. For each applicable AC, three fields:

- **Realization** — how the design's code realizes the AC, with code references (`file:line` or `module/function`).
- **Verification** — the specific test file, LLM evaluation rubric, or human-review note that verifies it for *your* design.
- **Status** — `conformant`, `partial-conformance` (with known gap), or `not-applicable` (with reason).

The Verification field is load-bearing. Three kinds are acceptable:

1. **Deterministic test** — a script or test file decides conformance mechanically. Example: [`tools/egress-lint.py`](../tools/egress-lint.py) scans the source for unsanctioned off-device egress vectors (`fetch`/`sendBeacon`/remote `src`/etc.) against an allow-list of the origins your flavor legitimately uses, and its `--json` output folds straight into the AC-1 finding of an evaluate report.
2. **LLM evaluation rubric** — a prompt or rubric describing what an LLM should look for. Useful for posture/intent ACs that mechanical tests can't reach. Example: *"Read every code path that reads from Private DB and decide whether any of them sends data off-device. Cite specific call sites."*
3. **Human-review note** — a short note explaining why no automated test is feasible, with the review record itself archived in the design's repo (e.g., `docs/conformance-review-2026-05.md`).

Mixed verification per AC is fine.

The lint at [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) checks that every contract names at least one AC and that every claimed AC exists in the spec. CI runs it on every PR. (A future `tools/validate-architecture.py` will additionally lint your Architecture document for missing Verification fields; planned for Phase 6.)

---

## Quick reference

| You want to … | Open Claude Code in … | Ask the agent … |
|---|---|---|
| Build a new PNA | your new project's dir | "Use the PNT skill to walk me through axis picks for a [use case] PNA." |
| Audit someone's PNA before installing | PNT (with candidate at known path) | "Use the PNT skill to audit `<path>` for PNA-spec conformance." |
| Preflight your design for submission | your design's repo | "Use the PNT skill to validate this design for submission to PNT." |
| Open the contribution PR | PNT | "Use the PNT skill's contribute flow to open a PR adding this design." |

The skill description triggers on natural-language requests fitting any of these flows.

---

## Where to find things

- [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) — the canonical spec
- [`spec/axes.md`](../spec/axes.md) — axes and flavor-derived ACs
- [`spec/use_cases.md`](../spec/use_cases.md) — attested classes of PNA
- [`contracts/`](../contracts/) — typed contracts, each with `Realizes:` header
- [`reference_designs/`](../reference_designs/) — accepted designs + templates
- [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) — the agent-consumption view (what you're invoking through the agent above)
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — full contribution rules
- [`tools/`](../tools/) — validators and the audit-report schema:
  - [`tools/egress-lint.py`](../tools/egress-lint.py) — deterministic AC-1 check for off-device data leaks (Goals 1, 2, 6)
  - [`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json) — typed schema for the audit report (Goal 2)
  - [`tools/lint-spec-ids.py`](../tools/lint-spec-ids.py) — AC ↔ contract traceability lint
- [`plans/reorganization-plan.md`](../plans/reorganization-plan.md) — the live plan tracking PNT's own evolution
