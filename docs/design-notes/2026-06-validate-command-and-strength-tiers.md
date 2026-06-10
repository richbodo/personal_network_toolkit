# A single-command `just validate <path>`, and the validation-strength gradient

*Design note · 2026-06 · status: **exploratory** (no code yet; captures a 2026-06-09 brainstorm). Builds
on the evaluate flow ([`../../pna-build-eval-contrib/SKILL.md`](../../pna-build-eval-contrib/SKILL.md)
§ Evaluate), the deterministic lints in [`../../tools/`](../../tools/), and the Visual Validator
([`../../tools/report-viewer/`](../../tools/report-viewer/)). Add a
[`../PriorArt.md` § Design notes](../PriorArt.md) pointer if/when any of this lands.*

> **Not a commitment, and not a spec change.** This sketches a command and a mental model. It imposes no
> obligation on any design and adds no AC. The point is to write the target down so the pieces we already
> have can be assembled deliberately later — or rejected on the record.

## The aspiration, and the honest limit

The simplest possible end-user experience is one command, one argument: `just validate <path-to-repo>`.
You built (or cloned) some software, you want to know whether to trust it — point the toolkit at it and
read the report.

The version that is *not* feasible is universal **execution-based** validation: spinning up an arbitrary
candidate's environment — its build, services, and data — is not a one-command problem, and pretending
otherwise is exactly how you get a validator that lies. So split the promise: there is a band we can
**always** do (read the source, run static checks, reason over it) and a stronger band we can do **only
when the design cooperates** by declaring how to build and exercise itself.

Two clarifications remove most of the friction the idea seemed to carry:

- **Validation ≠ archival.** Getting a Software Heritage SWHID is part of the *contribute/accept* flow —
  it pins an *accepted reference design's* source in the toolkit's catalog so it survives upstream
  deletion. It is **not** a precondition for validating anything. `just validate <path>` of Signal needs
  zero SWHID work. (The conflation is natural — the keystone did archival and verification in one sitting
  — but they are separate concerns.)
- **One report, many evidence sources.** The output is already designed for this: a single typed
  `evaluate-report.json` ([`../../tools/evaluate-report.schema.json`](../../tools/evaluate-report.schema.json))
  keyed by AC, where each finding's `evidence` is tagged `deterministic` / `llm` / `human` and the status
  vocabulary includes `unable-to-determine`. The command's job is to **fill that one artifact** from
  whatever sources are available — not to make the user pick a mode.

## The strength gradient (what `just validate` dispatches)

Three tiers, composed in a single run; the strongest available source wins per AC:

| Tier | What runs | Strength | Needs |
|---|---|---|---|
| **S — static / deterministic** | the existing lints: `egress-lint` (AC-1/2), `export-lint` (PR-6), and — where the candidate self-attests — `attestation-evidence-lint` | strong, narrow, no false confidence | readable source only |
| **L — lite / LLM architectural** | the evaluate flow: read source, trace the data/control flow each AC constrains, emit AC-keyed findings with honest `unable-to-determine` where it can't run code | broad, weaker, calibrated | readable source; for source-scattered apps, a **research sub-phase** to locate the surface first |
| **F — full / executable** | run the design's declared `[verify]` entrypoint (fellows' `just evaluate-report`, or a real conformance suite) | strongest | the design **cooperates** — declares an entrypoint and is buildable |

`just validate <path>` always runs **S**, runs **L** if source is readable, and runs **F** if a
`[verify]` entrypoint is declared — folding everything into one report. Tier F is the reference-design
path (the keystone, `fellows_local_db`, is the first design with a real entrypoint). Tier S+L is the
"audit a stranger's app" path. The deterministic lints' output folds in as `source: deterministic`
evidence on the AC each bears on, exactly as the SKILL evaluate flow already prescribes.

The tiers are **additive, not exclusive**: a single AC can carry a deterministic finding *and* an LLM
finding *and* (for a cooperating design) an executable result, and the report keeps all three with their
sources visible. That is the whole point of the typed artifact — diffability and honest provenance.

## Honesty is the load-bearing property

The failure mode is not a weak finding — it is a **lite verdict mistaken for a full one**. The defenses
already exist in the design: the evidence `source` tags, `unable-to-determine` as a first-class status,
and the toolkit's standing *validation, not certification* stance. Stated plainly:

> **Lite validation is a disclosure/triage tool, not a trust certificate.** It answers "what does this
> app demonstrably do, and not do?" — not "is this app safe, full stop."

At lite strength you can still say true, useful things: *"egresses to a well-known endpoint owned by
X-corp, for reason Y"* (an `egress-lint` + LLM-trace finding on AC-1/AC-2), and *"no human-readable
export"* (a PR-6 / `export-lint` finding). Those are real disclosures even when the report can't reach a
verdict on execution-gated ACs — **provided it says so**, per AC, with the reason. A silent gap is the
dishonesty; a declared `unable-to-determine` is the integrity.

## Worked example — Signal (why the gradient matters)

Signal is the stress test the band was drawn for. Its source spans many repositories; validating it
"really" is itself a research project — locate the surface, decide what *running* it would even prove,
map its features against the goals. Two honest outputs:

- **Lite (no code run):** an AI research pass yields a *partial* AC-keyed map — egress endpoints, storage
  shape, the absence of a PR-6-style human-readable export. Weak, possibly fatally so, but it discloses
  real behaviors.
- **Full:** infeasible generically (multi-repo build + live services). So the report *says so* —
  `unable-to-determine` on the execution-gated ACs, with the reason — rather than leaving a silent gap.

Two cautions this example forces into the open:

1. **Mapping an arbitrary app against the PNA goals is a weaker, different act than validating a
   self-declared PNA.** Signal does not claim to be a PNA; many ACs are `not-applicable` or only loosely
   meaningful, and its `pna-active` predicate was never asserted. The honest framing is "how this app's
   behaviors land against the PNA goals," **not** "Signal is / isn't a conformant PNA." Without that
   framing the report over-claims, and a reader mistakes `not-applicable` for a pass.
2. **The research sub-phase is the cost center.** A source-scattered app can burn a lot of tokens just
   locating and reading the relevant code. That tier needs an explicit scope/budget and must **`log` what
   it did not read** — a silent "covered everything" over a sampled read is the same dishonesty the lints
   exist to prevent.

## The direction worth chasing — a behavior-based chooser

Generalize the evaluate flow from *audit one app* to *choose / trust among apps by behavior*. The
Creative-Commons license chooser is the right analogy: answer a few questions about what you require, get
pointed at the artifact that matches. Here: *which Goals / ACs do you insist on?* → which candidates honor
them, drilling from goal down to the code that realizes (or violates) it.

This is tractable **because** one class — PNAs — is over-specified. It is also the more *differentiated*
direction: an application *builder* is a crowded race, but a **behavior-based trust/discovery layer** for
a well-specified class is not, and the spec already gestures at it ("conformance evaluation as a
precondition for ecosystem interop", `PNA_Spec.md` § Vision).

> **Wager, not claim.** The chooser's ceiling is the reliability of lite validation — a weak verdict
> feeding a trust decision can be worse than no verdict. The honest version leads with *disclosure*
> ("here is what it does") and states confidence explicitly, rather than emitting a green/red badge it
> cannot back. Whether lite validation is good enough to anchor a chooser is the bet this direction is
> made to test, not a settled fact.

## Buildable now vs. later

- **Now (cheap, mostly assembly):** `just validate <path>` that runs the evaluate flow and folds the
  deterministic lints into one `evaluate-report.json`; the Visual Validator already renders it. This is
  wiring existing pieces, not new mechanism.
- **Later:** the research sub-phase for source-scattered apps (with a token budget + honest
  coverage logging); the chooser UX over a corpus of reports; a re-run/diff convenience (the typed report
  is already diffable — "did anything quietly stop conforming since last time?").
- **Deliberately not (this version):** generic execution-based validation. Tier F stays **opt-in via a
  design's declared `[verify]` entrypoint** — we never try to spin up an arbitrary app's environment, and
  we never imply we did.

## Open questions

- **Lite-as-full risk.** Is `source`-tagging + `unable-to-determine` enough, or does the *command* need to
  refuse a single overall "verdict" at lite strength and only ever emit per-AC findings?
- **Applicability to non-PNAs.** For an app that never asserts `pna-active`, which ACs are even meaningful
  to score? The report likely needs an explicit "this app does not claim to be a PNA" header so
  `not-applicable` is never read as a pass.
- **Research-tier budget.** How is scope bounded for a Signal-class target, and how is partial coverage
  surfaced so a sampled read cannot masquerade as complete?
- **Provenance of a lite verdict.** Should a Tier-S+L report be *prevented* from ever being committed as a
  design's `evaluate-report.json` for a contribution (where Tier F is expected), so the contribute and
  audit uses of the same artifact don't blur?
