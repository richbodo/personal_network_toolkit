# Contributing to PNT

PNT (the Personal Network Toolkit) evolves through reference-driven specification: spec changes are accompanied by a working reference design that demonstrates the change in code. This document describes how to contribute a reference design — and how a spec change rides along with it.

## Philosophy

The spec is generative + evaluative. AI agents read it to build conformant PNAs (Personal Network Applications), and to evaluate whether a candidate application is safe to use as one. Both modes are first-class. PNT is a thin canonical repo: spec, typed contracts, reference design records, skill, tooling. It does not host runnable application code.

A reference design is the bridge between abstract spec and working software. Spec changes without a demonstrating design are not accepted; designs without a discussion of what they contribute to the spec are not accepted either. The two co-evolve.

## How to contribute

The step-by-step procedure for a contribution — preflight your design via the skill, iterate, open the PR, address maintainer feedback, final validation after merge — lives in [`docs/users-guide.md` § Goal 3](docs/users-guide.md#goal-3-submit-your-design-as-a-reference-design). The rest of this document is the policy layer that procedure operates against: what we accept, what we don't, what artifacts your PR must include, and how acceptance, versioning, and archival work after merge.

## What we accept

- Reference designs derived from working applications.
- Under any OSI-approved license.
- With an Architecture document (the design's "Security Target") that:
  - declares the PNA Spec version the design conforms to,
  - declares per-axis picks and their versions,
  - documents per-axis implementation choices, and
  - includes an **AC (Architectural Commitment) attestation table** mapping every applicable AC to (a) how the design realizes it, with code references, and (b) the specific test(s), LLM (Large Language Model) evaluation rubric, or human-review record(s) that verify it for this design. Rows without a Verification reference are not accepted.
- With reproducibility notes sufficient for a future reader to build the archived source.

See [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](reference_designs/templates/ARCHITECTURE_TEMPLATE.md) for the full structure.

## What we don't accept

- Spec changes without a demonstrating reference design.
- Designs whose license prevents Software Heritage archival.
- Architecture documents missing the AC attestation table or its Verification field.
- Designs that maintainers can't get to build at all from the documentation provided.

## PR contents required

The skill's contribute flow (driven by [`docs/users-guide.md` § Goal 3](docs/users-guide.md#goal-3-submit-your-design-as-a-reference-design), backed by [`pna-build-eval-contrib/SKILL.md`](pna-build-eval-contrib/SKILL.md)) assembles all of these for you end-to-end. Manually-authored PRs are also fine — the artifacts a PR must contain:

- **Spec diff (if any)** — changes to `spec/PNA_Spec.md`, `spec/axes.md`, `spec/use_cases.md`, or `contracts/` files
- **A design record** at `reference_designs/<design-name>/README.md` per [`reference_designs/templates/TEMPLATE.md`](reference_designs/templates/TEMPLATE.md)
- **A copy of the design's Architecture document** at `reference_designs/<design-name>/Architecture.md` per [`reference_designs/templates/ARCHITECTURE_TEMPLATE.md`](reference_designs/templates/ARCHITECTURE_TEMPLATE.md)
- **The design's canonical repo URL and the commit SHA being submitted**

## Acceptance process

Maintainer review focuses on the judgment-and-review layer of conformance verification (the layer that deterministic lints and LLM evaluation can't handle on their own):

- Is the spec change motivated by the design, and well-formed?
- Is the Architecture document complete? Does its AC attestation table map every applicable AC to a verification mechanism?
- Does the reference design actually demonstrate the claimed contribution? Maintainers clone the design's source, inspect it, and optionally run the skill's evaluate flow against it.
- Is the license OSI-approved?

On merge:

- Spec changes land (including any new AC IDs, sub-contracts, or axis-pick additions)
- Maintainer triggers Software Heritage archival (planned tooling: `tools/swh-save.sh <repo-url> <commit-sha>`, landing in Phase 5; until then, archival is performed manually via Software Heritage's Save Code Now) and records the returned SWHID (Software Heritage Persistent IDentifier) in the design record
- Maintainer decides whether the design warrants an additional `archive/<design-name>` fork in the `pnt-archive` GitHub organization (high-signal designs only; SWHID alone is sufficient for the archival promise)
- Spec version bumped per the versioning rules below

## Versioning

The PNA Spec uses linear SemVer:

- **Patch** — clarifications, typo fixes, non-substantive edits
- **Minor** — additive changes (new ACs, new axes, new picks, new sub-contracts)
- **Major** — breaking changes (semantically altered ACs, removed picks, contract-shape changes)

Individual axes carry their own version (declared per-axis in each design's Architecture document). A breaking change to an axis bumps that axis's version and the PNA Spec major.

## Archival

Software Heritage SWHIDs are the canonical permanent identifier for accepted reference designs (v0.1 — see `spec/PNA_Spec.md § Vocabulary` under "reference design"). PNT may additionally fork high-signal designs to a `pnt-archive` GitHub organization at maintainer discretion; these forks are frozen at the accepted commit and not maintained.

PNT does not host runnable application code or maintain forks.

## Acceptance is not certification

Acceptance of a reference design signals "this design contributed something to the spec, and demonstrably conforms against it." It is not a recommendation or a certification. There is no certifying body. Conformance is something you check (via [the evaluate flow](docs/users-guide.md#goal-2-audit-a-candidate-pna-before-installing-it)), not something you are awarded.
