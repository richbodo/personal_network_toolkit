# PNT User's Guide

The PNA (Personal Network Application) Spec is the canonical specification; this guide is the canonical how-to. It gives step-by-step instructions corresponding to each of the success criteria listed in [`README.md` § Status](../README.md#status).

PNT (Personal Network Toolkit) is built to be consumed by AI coding agents. Most of this guide assumes you have an agent (Claude Code, Cursor, an equivalent) you can ask things like *"use the PNT skill to validate my design."* The skill at [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) is the agent-consumption view of everything in this guide.

---

## Goal 1 — Build a conformant PNA

You're starting (or extending) a personal network application.

1. **Read the spec.** Start with [`spec/PNA_Spec.md`](../spec/PNA_Spec.md) end-to-end. The universal architectural commitments (ACs) are non-negotiable; the axes in [`spec/axes.md`](../spec/axes.md) are where you make choices.

2. **Pick your axes with an agent.** Open Claude Code in your project directory and ask:

   > "Use the PNT skill to walk me through axis picks for a [Directory Archive | Personal Relationship Manager | …] PNA."

   The agent walks each axis (distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure — where MCP = Anthropic's Model Context Protocol) and the attested picks per axis.

3. **Find a reference design that shares as many of your picks as possible.** Each [`reference_designs/<name>/`](../reference_designs/) directory has a design record naming its flavor. Study the design closest to what you want. Its archived source is linked via the Software Heritage SWHID (Persistent IDentifier) in the record.

4. **Pull the typed contracts.** [`contracts/`](../contracts/) has them. Each contract opens with a `Realizes: AC-X, AC-Y` header naming the ACs it serves. Treat the contracts as load-bearing; your code conforms to them.

5. **Author your Architecture document.** Use [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](../reference_designs/templates/ARCHITECTURE_TEMPLATE.md) and put the result at `docs/Architecture.md` (or equivalent) in your design's own repo. Fill in PNA Spec version, axis picks and versions, per-axis implementation notes, and — most importantly — the AC attestation table. For every applicable AC, record (a) how your code realizes it and (b) what test/rubric/review-note verifies it.

6. **Build.** Implement the design against the contracts.

7. **Self-check.** Run the audit flow (Goal 2 below) on your own code before declaring the design done.

---

## Goal 2 — Audit a candidate PNA before installing it

You have a PNA in front of you (someone else's, or your own in-progress one) and you want an LLM (Large Language Model) to check whether it actually honors the PNA Spec — whether it's safe with your data.

1. **Get the candidate's source.** Clone the repo. If you only have a bundle, ask for the source.

2. **Open Claude Code in your PNT working directory** (this guide assumes you have PNT itself cloned alongside the candidate, or that PNT is reachable from the agent's working directory).

3. **Ask the agent to run the audit.** Use natural language:

   > "Use the PNT skill to audit `<path-to-candidate>` for PNA-spec conformance. Is this app safe for me to install?"

4. **Read the report.** The agent walks every applicable AC (universal + flavor-derived) and produces a structured AC-ID-keyed report:
   - `conformant` — design honors this AC; cited code locations included.
   - `non-conformant` — design violates this AC; the report names the AC requirement and the offending code.
   - `not-applicable` — design's flavor doesn't trigger this AC.
   - `unable-to-determine` — needs human review.

5. **Read the summary.** Non-conformances against Goals 1–5 (private-data sovereignty, source-mirroring honesty, transport security, durability, local diagnosability) are the load-bearing concerns. If any of those are non-conformant, the design is not safe to trust with your data.

6. **You may emphasize a specific concern.** E.g.: *"Focus on Goal 1 — make sure my Private DB rows can't leave my device."* This shapes the summary, not the underlying check.

---

## Goal 3 — Submit your design as a reference design

You've built (or are operating) a PNA and want to contribute it back to PNT. This is the most-used flow and gets the most space.

### Should I submit?

Three patterns are valuable enough to justify a submission:

- **New architectural commitment.** Your design surfaced a constraint the spec doesn't yet capture. Your PR will include a spec diff.
- **Existing patterns on a new platform.** Your design exercises existing ACs on a substrate or use-case not yet attested in the reference set. No spec change needed; your design expands the ecosystem.
- **Ecosystem value-add.** Your design fills a use-case gap, brings accessibility, or makes something easier that no existing design demonstrates.

If your design is *identical* to an existing reference with no novelty, reach out before authoring — the PR may not be worth the maintenance overhead.

### Step 1: Preflight your design with the skill

Open Claude Code in your design's repo (or in PNT, with a path to your design). Ask:

> "Use the PNT skill to validate this design for submission to PNT."

The agent will:

1. **Locate your Architecture document.** If it exists, validate it against the code. If it doesn't, walk you through creating one interactively, asking about each section (PNA Spec version, axis picks, per-axis notes, AC attestation rows).
2. **Ask what's interesting architecturally** about your design (one of the three patterns above).
3. **Report what's broken or missing** as a structured list — files, sections, Verification fields, cited-but-absent code, failing tests, license problems.

Iterate: fix things, re-run preflight, keep going until the report is clean.

### Step 2: Open the PR

Once preflight is clean, ask the agent:

> "Use the PNT skill's contribute flow to open a PR adding this design at `<path-to-design>` (commit `<sha>`)."

The agent will:

- Read `CONTRIBUTING.md`.
- Author the design record at `reference_designs/<design-name>/README.md`.
- Copy your Architecture document to `reference_designs/<design-name>/Architecture.md`.
- Add the spec diff if you're proposing one.
- Open the PR via `gh pr create`.

### Step 3: Maintainer review

A maintainer reviews at the judgment-and-review layer (does the spec change make sense? does the Architecture document accurately describe the design? is the AC attestation table complete?). They may ask for changes — fix, push, repeat.

### Step 4: After merge — final validation

Once the PR is merged, run preflight one more time against the merged state. It should come out clean.

---

## Goal 4 — Archival via Software Heritage

You don't do anything here — it happens after your PR is accepted.

When the maintainer accepts your PR, they trigger Software Heritage archival on your repo at the accepted commit. The planned tooling is `tools/swh-save.sh <your-repo-url> <commit-sha>` (landing in Phase 5 of the reorganization plan); until then, archival is performed manually via Software Heritage's Save Code Now. The resulting SWHID (a `swh:1:dir:...` content-addressed identifier) is recorded in your design record at `reference_designs/<design-name>/README.md`.

This means your design's source survives even if your upstream repo is deleted or relocated. You don't need to do anything; the maintainer handles it. If they forget, remind them.

For high-signal designs, the maintainer may additionally mirror the design to a `pnt-archive` GitHub organization as a frozen fork. SWHID alone is sufficient for the archival promise; the fork is belt-and-braces.

---

## Goal 5 — Influence spec evolution

If you find a spec gap, ambiguity, or contradiction while building or operating your PNA, your PR includes a spec diff. The maintainer reviews the diff in the context of your demonstrating reference design.

After merge, the PNA Spec version is bumped per linear SemVer:

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

1. **Deterministic test** — a script or test file decides conformance mechanically. Example: a script that scans the codebase for any `fetch(...)` call to a non-localhost URL on the Private DB code path.
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
- [`tools/`](../tools/) — validators
- [`plans/reorganization-plan.md`](../plans/reorganization-plan.md) — the live plan tracking PNT's own evolution
