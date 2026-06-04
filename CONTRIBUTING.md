# Contributing to PNT

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](VERSION).

PNT (the Personal Network Toolkit) evolves through reference-driven specification: a spec change that imposes a new obligation on designs is accepted only with a working reference design that demonstrates it in code. But most contributions are lighter — **toolkit fixes** (tooling, docs, the skill, a scope or clarification spec note) that impose no such obligation. This document covers both; see *Contribution types* below for which path yours takes.

## Philosophy

The spec is generative + evaluative. AI agents read it to build conformant PNAs (Personal Network Applications), and to evaluate whether a candidate application is safe to use as one. Both modes are first-class. PNT is a thin canonical repo: spec, typed contracts, reference design records, skill, tooling. It does not host runnable application code.

A reference design is the bridge between abstract spec and working software. Spec changes that impose a new obligation on designs without a demonstrating design are not accepted; designs without a discussion of what they contribute to the spec are not accepted either. The two co-evolve.

## Contribution types

A contribution is a PR against the versioned toolkit, in one of two shapes. **Route yours first** — they carry very different weight:

- **Reference design** — a new or updated reference design, or a spec/contracts change that imposes a new obligation on designs (a new or changed AC, a new sub-contract, a new axis pick). Accepted only with a working design that demonstrates it. This is the heavyweight path the rest of this document specifies: an Architecture document with an AC attestation table, an evaluate-flow report, archival. The skill's *Reference-design contribution* flow drives it.
- **Toolkit fix** — a change to the toolkit's own artifacts that imposes **no** new contract a design must satisfy: tooling/lints, templates, the skill, docs, a CHANGELOG entry, or a spec note that *clarifies* or *declines* a commitment. No reference-design attestation. **Most PNT PRs are toolkit fixes.** Open a normal PR, run `python tools/lint-spec-ids.py`, add a CHANGELOG entry, record rationale in [`docs/PriorArt.md` § Design notes](docs/PriorArt.md) if it's a decision, and check the *Toolkit fix* box in the PR template. The skill's *Toolkit fix* flow drives it. [PR #19](https://github.com/richbodo/personal_network_toolkit/pull/19) is the canonical example: an at-rest-encryption scope decision that *declined* to add an AC.

**The deciding question:** *does a design have to do anything new to stay conformant after this change?* If yes → reference design. If nothing does → toolkit fix. Everything below (*What we accept* / *don't accept* / *PR contents* / *acceptance* / *archival*) is the **reference-design** policy; a toolkit fix only needs the lint, a CHANGELOG entry, and — for a decision — a Design-notes entry.

## How to contribute

The step-by-step procedure for a contribution — preflight your design via the skill, iterate, open the PR, address maintainer feedback, final validation after merge — lives in [`docs/users-guide.md` § Goal 3](docs/users-guide.md#goal-3-submit-your-design-as-a-reference-design). The rest of this document is the policy layer that procedure operates against: what we accept, what we don't, what artifacts your PR must include, and how acceptance, versioning, and archival work after merge.

## What we accept

- Reference designs derived from working applications.
- Under any OSI-approved license.
- With an Architecture document (the design's "Security Target") that:
  - declares the Toolkit-Version the design conforms to,
  - declares per-axis picks and their versions,
  - documents per-axis implementation choices, and
  - includes an **AC (Architectural Commitment) attestation table** mapping every applicable AC to (a) how the design realizes it, with code references, and (b) the specific test(s), LLM (Large Language Model) evaluation rubric, or human-review record(s) that verify it for this design. Rows without a Verification reference are not accepted.
- With reproducibility notes sufficient for a future reader to build the archived source.

See [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](reference_designs/templates/ARCHITECTURE_TEMPLATE.md) for the full structure.

## What we don't accept

- Spec changes that impose a new obligation on designs (a new/changed AC, sub-contract, or axis pick) without a demonstrating reference design. *(A spec note that merely clarifies or declines a commitment imposes no obligation and is a toolkit fix — see Contribution types.)*
- Designs whose license prevents Software Heritage archival.
- Architecture documents missing the AC attestation table or its Verification field.
- Designs that maintainers can't get to build at all from the documentation provided.

## PR contents required

The skill's contribute flow (driven by [`docs/users-guide.md` § Goal 3](docs/users-guide.md#goal-3-submit-your-design-as-a-reference-design), backed by [`pna-build-eval-contrib/SKILL.md`](pna-build-eval-contrib/SKILL.md)) assembles all of these for you end-to-end. Manually-authored PRs are also fine — the artifacts a PR must contain:

- **Spec diff (if any)** — changes to `spec/PNA_Spec.md`, `spec/axes.md`, `spec/use_cases.md`, or `contracts/` files
- **A design record** at `reference_designs/<design-name>/README.md` per [`reference_designs/templates/TEMPLATE.md`](reference_designs/templates/TEMPLATE.md)
- **A copy of the design's Architecture document** at `reference_designs/<design-name>/Architecture.md` per [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](reference_designs/templates/ARCHITECTURE_TEMPLATE.md)
- **A machine-readable manifest** at `reference_designs/<design-name>/design.toml` per [`reference_designs/templates/design.toml`](reference_designs/templates/design.toml) — the source of truth the conformance suite reads (repo, flavor, the `[verify]` entrypoint, and the SWHID pin once archived). `tools/lint-spec-ids.py` validates its shape; a design dir with an `Architecture.md` must carry one.
- **The design's canonical repo URL and the commit SHA (and tag, if any) being submitted**
- **The evaluate-flow report** at `reference_designs/<design-name>/evaluate-report.json` — an instance of [`tools/evaluate-report.schema.json`](tools/evaluate-report.schema.json), produced by running the skill's evaluate flow against the design. It is the typed, diffable record of *what was validated*, and the input the maintainer attests to at acceptance.

## Acceptance process

Maintainer review focuses on the judgment-and-review layer of conformance verification (the layer that deterministic lints and LLM evaluation can't handle on their own):

- Is the spec change motivated by the design, and well-formed?
- Is the Architecture document complete? Does its AC attestation table map every applicable AC to a verification mechanism?
- Does the reference design actually demonstrate the claimed contribution? Maintainers clone the design's source, inspect it, and optionally run the skill's evaluate flow against it.
- Is the license OSI-approved?

On merge:

- Spec changes land (including any new AC IDs, sub-contracts, or axis-pick additions).
- **Maintainer attests validation.** The maintainer confirms the evaluate-flow report and the AC attestation table check out against the cited code, at a specific **Toolkit-Version**, and records an acceptance line in the design record (`reference_designs/<design-name>/README.md`): *date · accepted-by · Toolkit-Version validated against*. The merge is the acceptance; this line is the durable record of *what* was validated. While there is a single maintainer this stays lightweight — and the first reference design, `fellows_local_db`, is accepted *by definition* as the design the toolkit was distilled from.
- Maintainer triggers Software Heritage archival with [`tools/swh-save.sh <repo-url> [<git-ref>] [<clone-path>]`](tools/swh-save.sh) — a thin wrapper over Save Code Now that also prints the git-compatible SWHIDs — and records the returned `swh:1:dir` SWHID (Software Heritage Persistent IDentifier) in the design record **and in `design.toml`** (set `commit`/`swhid_rev`/`swhid_dir` and flip `archival = "archived"`; the lint then requires them and checks `swhid_rev` against `commit`).
- Maintainer decides whether the design warrants an additional `archive/<design-name>` fork in the `pnt-archive` GitHub organization (high-signal designs only; SWHID alone is sufficient for the archival promise).
- Toolkit version bumped per the versioning rules below.

> **Re-validation on a version bump.** A design is validated against a specific Toolkit-Version (recorded above). A later toolkit bump does not retroactively re-validate it; the design's `Toolkit-Version` declares what it was checked against, and re-validation is a fresh evaluate-flow run when the maintainer chooses to re-attest it.

## Versioning

The PNA Spec uses linear SemVer:

- **Patch** — clarifications, typo fixes, non-substantive edits
- **Minor** — additive changes (new ACs, new axes, new picks, new sub-contracts)
- **Major** — breaking changes (semantically altered ACs, removed picks, contract-shape changes)

Individual axes carry their own version (declared per-axis in each design's Architecture document). A breaking change to an axis bumps that axis's version and the PNA Spec major.

**The toolkit is versioned as a unit.** The version in `/VERSION` covers the whole toolkit — spec, contracts, skill, lint, and templates — not just the prose spec; every toolkit artifact carries a matching `Toolkit-Version:` header, enforced by `tools/lint-spec-ids.py`. A contribution is a PR against that versioned toolkit, whatever its shape — (a) a reference design, (b) a new architectural commitment, exception, or solution, or (c) a modification to the spec documents. Releases are git-tagged (`v<MAJOR.MINOR.PATCH>`). A design declares the `Toolkit-Version` it was built and validated against in its Architecture document; that is how a reader knows which toolkit version a design conforms to.

## Archival

Software Heritage SWHIDs are the canonical permanent identifier for accepted reference designs (v0.1 — see `spec/PNA_Spec.md § Vocabulary` under "reference design"). PNT may additionally fork high-signal designs to a `pnt-archive` GitHub organization at maintainer discretion; these forks are frozen at the accepted commit and not maintained.

PNT does not host runnable application code or maintain forks.

## Acceptance is not certification

Acceptance of a reference design signals "this design contributed something to the spec, and demonstrably conforms against it." It is not a recommendation or a certification. There is no certifying body. Conformance is something you check (via [the evaluate flow](docs/users-guide.md#goal-2-audit-a-candidate-pna-before-installing-it)), not something you are awarded.
