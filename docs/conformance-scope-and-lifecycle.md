# Conformance suite — scope, the utility line, and the reference-design lifecycle

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> A design note, not a normative spec file. It records *why* the conformance
> suite is bounded the way it is, where the line of useful output sits, and how
> reference designs age out of continuous testing without losing their value.
> The *how/when* of building the suite lives in
> [`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md).

## Why this note exists

Two forces pull on any conformance suite, and both are seductive:

1. **Expand what it evaluates.** "If we can check a PNA, why not any local-first
   app? Why not any app?" The validation skill *would* return something for any
   input — so where does useful information stop and noise begin?
2. **Test everything forever.** "If we pin the source with a SWHID, why not keep
   every accepted design under continuous test for all time?" — until the
   browsers and phones a 2026 design needs no longer exist in 2028.

Left unchecked, the first turns a sharp tool into a vague "privacy score
generator"; the second turns a tractable suite into an unmaintainable museum of
dead environments. This note draws both lines.

## The utility line: the Goals are the measuring stick, and the only one

The PNA Toolkit **validates behaviors against the Goals; it does not certify** (see
[`CONTRIBUTING.md`](../CONTRIBUTING.md) § "Acceptance is not certification"). The
key realization for scope is that **the line is not between "PNA" and "not a
PNA." It is between "evaluated against the toolkit's Goals" and "evaluated against goals
the toolkit does not define."** The Goals (Goal 1–4 in
[`PNA_Spec.md`](../spec/PNA_Spec.md)) are a fixed measuring stick. Pointing that
stick at a non-PNA is legitimate and useful; *inventing new marks on the stick*
to opine on general "privacy" or "software quality" is the creep that destroys
the suite's meaning.

So the evaluate surface has **three honest output modes**, chosen by how much
nexus the candidate has with the personal-network root:

### Mode 1 — Conformance evaluation (membership)
For an app that *claims* to be a PNA, or is architecturally shaped like one
(two-store split, local-first, downstream of SaaS). The full machinery applies:
every applicable AC, every conditional AC, the Exceptions
([`exceptions.md`](../spec/exceptions.md)) and Constraints
([`constraints.md`](../spec/constraints.md)) passes, reported by `AC-*`/`EX-*`/
`CST-*` ID. Output: *is this a conformant PNA, and where does it deviate or hit a
ceiling?* This is the home turf and the only place a design *attests*
conformance.

### Mode 2 — Goal-impact read (any app that touches the personal-network root)
For an app that is **not** trying to be a PNA but does touch contact/relationship
data — Signal, a SaaS CRM, a calendar, a contact manager. We do **not** report
"you fail 14 ACs" (meaningless — it never claimed them; those ACs are
`not-applicable`). We report the app's **relationship to each Goal** on a
fixed scale:

> **protects · neutral · diminishes · out-of-scope** — per Goal.

The high-value signal is *diminishes*: an app that erodes the user's control of
their personal-network root (harvests the contact graph to a server, makes
private notes un-exportable, forces an insecure transport). A user genuinely
wants this, and the toolkit is uniquely positioned to say it precisely, because the toolkit has
crisply *defined* what "control of the personal-network root" means.

Worked example — Signal: Goal 3 (user-controlled, content-blind transport) is
**exemplary**; Goal 1 (a local sovereign root store of your contact graph) is
**out-of-scope** (Signal isn't a root store); contact-graph metadata posture is a
named, bounded *neutral/diminishes* note. That read is useful and honest. A
PNA-membership verdict on Signal would be noise — it never claimed membership.

### Mode 3 — Out-of-scope (no nexus)
For an app with no personal-network root to protect or diminish (a photo editor,
a game). The honest output is **"out of scope — the toolkit has nothing useful to say
here,"** not a contrived number. **The willingness to say this is what keeps the
suite credible.** The temptation to expand is, precisely, the temptation never to
say "out of scope." We say it.

### Why this is the right line
- It preserves "validate against the Goals, nothing else" *verbatim* — Mode 2
  scores Goals, never new criteria.
- It keeps the stick small and fixed, so the output stays interpretable.
- It degrades gracefully: membership → goal-impact → refusal, by nexus. That
  **graceful-degradation curve is itself the reusable artifact** (see § General
  field, below).

### A note on "evaluating Signal would be a huge build"
It would — but evaluation does not build the app. The evaluate flow **reads
source and data flows and reasons**; it does not compile a dozen platform apps.
For a multi-platform app you read the shared core's data posture once and note
per-platform deltas. The huge-build problem only bites **continuous testing**,
which is why continuous testing is reserved for a small *active reference set*
(below) and never aimed at arbitrary candidate apps. **Candidate evaluation is
read-and-reason (cheap); reference-design regression is build-and-run
(expensive, curated).** Keep the two lanes separate.

## The lifecycle line: active vs. archival reference designs

You cannot keep every accepted design runnable forever — the browsers, phones,
and OSes a 2026 design targets will not all exist in 2028, and a container image
extends that window but does not bring an old mobile Safari back to life. So the
reference set is explicitly two-tier (the `Status:` field already in
[`reference_designs/templates/TEMPLATE.md`](../reference_designs/templates/TEMPLATE.md)
becomes load-bearing):

- **Active** — a *small, deliberately curated* set the suite tests continuously
  (containerized, environment kept current). Roughly one per use-case × major
  flavor; intentionally few. These are the load-bearing exemplars.
- **Archival** — pinned by SWHID, source permanently retrievable, attestation
  table and architectural learnings preserved as **knowledge**, but **not**
  continuously tested. The SWHID + `Architecture.md` is the durable artifact;
  re-running its tests is best-effort and may lapse when its environment dies.
- **Superseded** — an archival design replaced by a newer one at the same flavor.

**The transition is explicit and curated.** A design moves active → archival when
(a) its environment becomes impractical to reproduce, (b) it is superseded at its
flavor, or (c) its maintainer stops supporting it. Being choosy about what stays
active is what keeps the suite tractable.

**Archival is not worthless.** This is the honest answer to "how do you retest to
the beginning of time?" — *you don't.* The toolkit does **not** promise eternal
re-testability. It promises:

- eternal **retrievability** (the SWHID-pinned source survives upstream
  deletion), and
- documented **conformance-at-acceptance** (the attestation table + the
  `Toolkit-Version` it was validated against), plus
- continuous testing of the **small active set** only.

This aligns with the existing rule that **a toolkit version bump does not
retroactively re-validate a design** ([`CONTRIBUTING.md`](../CONTRIBUTING.md)
§ Versioning). "Was conformant at acceptance, source preserved" is an honest
claim; "is conformant today, forever" is not one any project can keep, and
pretending otherwise is the museum-of-dead-environments failure.

## Future phases of reference-design testing (roadmap)

The 80/20 for v0.1 is Phases 1–3 of
[`plans/conformance-suite-plan.md`](../plans/conformance-suite-plan.md)
(toolkit self-tests, SWHID-pinned machine-readable records, skill-instrumented
submission). The *living, continuously-tested* suite is deliberately roadmap:

- **R1 — Containerized verify (Phase 4).** Each active design ships (or the
  toolkit provides per-stack) a container + a uniform `verify` entrypoint;
  `just test-design` and a scheduled CI matrix run them. Activates when the first
  real design adopts a verify entrypoint.
- **R2 — Version-bump re-attestation sweep.** On a toolkit bump, re-run the
  *active* set against the new spec and surface which conformance claims break —
  the executable form of "the spec evolves based on a design's findings"
  (README success-criterion #5). Archival designs are explicitly excluded.
- **R3 — Active-set curation policy.** A written cap and promotion/demotion rule
  for what stays active, so the suite never grows past what one maintainer can
  keep current. (Likely: one per use-case × major flavor.)
- **R4 — Environment-pinning beyond containers.** For designs whose value
  outlives their runnable environment (old mobile browsers), record the
  *environment* alongside the source (browser/OS versions, a recorded test
  transcript) so the archival entry documents *what passed where*, even when it
  can no longer be re-run.
- **R5 — Mode 2 (goal-impact read) as a first-class evaluate output.** Extend the
  skill + `evaluate-report.schema.json` to emit per-Goal protects/neutral/
  diminishes/out-of-scope for non-PNA candidates — useful to developers who just
  want to know how their app sits in the local-first, privacy-preserving world.
  Bounded strictly to the Goals.

## General field: application-class blueprints for agents

The PNA Toolkit is one instance of a broader pattern worth naming: **a machine-readable,
goal-anchored spec that an AI agent uses to (a) build conformant instances of an
application class and (b) evaluate arbitrary candidates against the class's
goals.** Two pieces of what we are building here generalize beyond PNAs:

1. **The graceful-degradation evaluator** (membership → goal-impact → refusal),
   with the class's goals as the immovable boundary of what the evaluator will
   opine on. Any application-class blueprint can adopt the same three-mode output
   to stay useful without scope-creeping.
2. **The active/archival curation discipline** with SWHID-pinned retrievability
   and conformance-at-acceptance — a tractable answer to "a living conformance
   suite for software that outlives its runtime environment."

These are a plausible contribution to the field, *separable* from PNAs. We note
them here as direction; v0.1 stays scoped to PNAs and the 80/20. The futurism
informs the seams we leave, not the features we ship now.
