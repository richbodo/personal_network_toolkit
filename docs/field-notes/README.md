# Conformance field notes

AC-keyed lessons harvested from building, hardening, and evaluating reference
designs — the **consumable** layer of the capture-lessons practice
([`../design-notes/2026-06-capturing-conformance-lessons.md`](../design-notes/2026-06-capturing-conformance-lessons.md)).

**What this is for.** When a builder implements an AC, or an evaluator audits a
candidate for it, this is where the hard-won, *generalizable* wisdom lives — the
gotchas, the negative invariants you'd otherwise re-derive, and the tests that pin
them. The build and evaluate flows in [`../../pna-toolkit/SKILL.md`](../../pna-toolkit/SKILL.md)
read the relevant note **before** implementing or judging an AC.

**Scope.** One file per AC that has a generalizable lesson:
`docs/field-notes/<AC-ID>.md` (e.g. `AC-PRM-H.md`). Design-*specific* "how we did
it" stays in that design's own repo (its design note / Architecture); these notes
hold what generalizes to *any* PNA. Not every AC has a note — only those a
reference design taught us something non-obvious about. An honest absence is fine;
a manufactured note is not.

## Entry format

Each note is short and **evidence-linked**:

- **Lesson** — the generalizable insight, in a sentence or two.
- **Negative invariants** — the "X must NOT happen" list a candidate is easy to
  pass *by accident*; each links the test that pins it.
- **Pitfalls / look hardest at** — what an evaluator should scrutinize, and the
  bounded claims of any deterministic check involved.
- **Surfaced by** — the design + PR that taught us this.

## Index

- [`AC-PRM-H.md`](AC-PRM-H.md) — authenticated loopback surface (an app-opened HTTP daemon). Surfaced by PRM #59.
