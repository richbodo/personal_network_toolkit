# Capturing the lessons reference designs teach us

*Design note · 2026-06 · status: **adopted — minimum viable built.** The AC-keyed
field-notes store ([`../field-notes/`](../field-notes/)) + the build/evaluate
consumption hooks in [`../../pna-toolkit/SKILL.md`](../../pna-toolkit/SKILL.md) + the
PR-checklist standing rule + the `/capture-lesson` procedure — ideas 1–3 below,
dogfooded with the first field note on `AC-PRM-H`
([`../field-notes/AC-PRM-H.md`](../field-notes/AC-PRM-H.md)). Checkpoints a
2026-06-18 collaborative discussion (Rich + Claude Code) about how to stop losing
the hard-won, conformance-driven knowledge that surfaces while building and
hardening reference designs; builds on the design-notes habit (this folder) and the
raw-capture habit (`grillme` + `brainstorms/`). Indexed in
[`../PriorArt.md` § Design notes](../PriorArt.md).*

> **Not a commitment, and not a spec change.** This records a problem and five candidate
> mechanisms with a recommendation. It imposes no obligation on any design and adds no
> AC. The point is to write the thinking down so we can pilot, adopt, or reject it on the
> record — itself an instance of the very habit under discussion.

## The problem

When we learn something while making a reference design conform — especially when we
*harden* an existing slot (the prompting example: `prm` PR #59 hardening `server.py`,
many components, tests written and passing) — that learning is mostly captured in the
**collaborative conversation** between Rich and Claude Code. We take design notes *some*
of the time. We don't capture everything. The reasoning is genuinely educational and
genuinely load-bearing, and most of it evaporates — so future **validators** and
**builders** re-derive it from scratch, which is exactly the time-cost the toolkit
exists to remove.

The trigger Rich identified is precise and worth honoring: **a feature written
specifically to satisfy a conformance AC, whose tests are now passing.** The green test
proves the lesson is real and load-bearing; the moment it goes green, the reasoning is
still fresh. That is a well-bounded, sustainable scope — *not* "capture everything."

## The core insight

1. **The AC is the natural index.** PR #59's hardening isn't generic wisdom — it's "what
   AC-2 / AC-8 / DI-4 / DI-5 actually demand in practice, the gotchas, and the negative
   test that proves each." Validators and builders already work AC-by-AC, so a lesson only
   pays off if it lands where those flows already look: **keyed by AC**. A note buried in
   one design's repo does nothing for someone auditing a *different* candidate.

2. **Consumption is what makes capture worth it.** Capture is write-only unless the
   evaluate and build flows are pointed at it. The payoff is a line in `SKILL.md`:
   *"before judging/implementing AC-X, read its field notes for known pitfalls and the
   harvested negative-invariant checklist."*

3. **There is a value ladder, and we already own both ends.** A lesson can climb:

   > tacit reasoning (chat) → raw checkpoint (`brainstorms/`) → distilled design note →
   > **AC-keyed field note (in the toolkit, consumable)** → negative test that pins it →
   > deterministic lint (if generalizable *and* mechanical)

   `grillme`/`brainstorms/` already capture the raw bottom; `egress-lint` /
   `attestation-evidence-lint` already are the top. **The gap is the middle rungs — and
   the *habit* of climbing them.**

### Two cross-cutting principles (these are what keep it from rotting)

This repo's recurring failure mode is rot: the dead `Reversible:` check that was green
while enforcing nothing; deferrals that live only in comments. A lessons practice that
relies on goodwill will rot the same way (we already observed it does). So:

- **Split generalizable from design-specific.** The design's note keeps "how *we* hardened
  *our* server"; the toolkit's field note keeps "what AC-2 demands of *any* PNA." Same
  routing logic as the contribute flow (new obligation → reference-design contribution;
  everything lighter → stays local).
- **Honest decline beats empty notes.** Some conformance tests yield no general lesson. The
  rule must allow "no generalizable lesson — one line why," in the same spirit as honest
  deferrals and `strict=True` xfails. Without this escape, the rule manufactures noise.

## The five candidate mechanisms

1. **AC-keyed "Conformance Field Notes" store, wired into the SKILL.** *(The home, and the
   only thing that makes capture pay off.)* `docs/field-notes/<AC-ID>.md` (or one sectioned
   file); each entry: the lesson, the design that surfaced it, the negative invariants
   discovered, links to the pinning test(s) and PR. Add one consumption step to each of the
   evaluate and build flows in `SKILL.md`. Everything below feeds this. *Cost: low — a
   folder + two SKILL steps; the discipline is keeping it AC-keyed.*

2. **A `/capture-lesson` skill that drafts the note from the live session + diff + green
   tests.** *(Kills the friction that is the actual reason capture doesn't happen.)* The
   richest knowledge is already in the chat — don't ask a human to re-type it. On green,
   invoke it; the agent reads the conversation, diff, and AC-tagged tests and drafts the
   field note (generalizable → toolkit) and the design note (specific → design repo),
   pre-split. Human edits and commits. Highest-leverage piece given the diagnosis ("we
   don't capture everything"). *Cost: a skill to author; quality rides on a good template.*

3. **A standing rule + PR-checklist gate, with an honest-decline escape.** *(The "standing
   rule" requested, made reliable.)* Mirror the existing "keep the docs current in the same
   PR" rule: a PR-template item in the reference designs and the toolkit — *"Adds/changes a
   feature to satisfy a conformance AC, tests now passing? → link the field-note / design-
   note entry, or check 'no generalizable lesson' + why."* The bounded trigger keeps it
   sustainable; the decline box keeps it honest. This is what makes capture *happen* rather
   than depend on memory. *Cost: trivial to add; relies on review discipline.*

4. **Co-locate the lesson with the test that proves it (structured docstring → generated
   doc).** *(Anti-rot, evidence-linked, dead-on this repo's grain.)* AC-driven tests carry a
   structured docstring — invariant, why it's easy to miss, what surfaced it, the AC — and a
   small stdlib tool extracts them into the store in (1). The lesson then can't drift from
   the code, and the "negative-invariant catalog" the evaluate flow already asks for becomes
   harvested, not hand-maintained. Fault-injection-self-tested like every other lint here.
   *Cost: an extractor + a docstring convention; more ceremony — add once the habit earns
   it.*

5. **A red→green nudge hook on AC-tagged tests.** *(Automates the exact moment Rich
   identified.)* `prm` already has a conformance-guard stop-hook that nudges when the
   attestation is edited without touching tests. Add the complement: when a commit/PR makes
   an AC-tagged conformance test pass, nudge — *"you just satisfied AC-X; run
   `/capture-lesson` before moving on."* Keep it a **nudge, not a gate** (the gate is (3)'s
   checklist), consistent with "the stop-hook is a nudge, not the gate." *Cost: hook
   plumbing + reliable AC-tagging of tests/files.*

## Recommendation

Build the self-reinforcing minimum, then harden — don't front-load ceremony before knowing
which lessons are worth the weight.

- **Now: 1 + 2 + 3.** The AC-keyed home + the SKILL consumption hook (so it pays off), the
  `/capture-lesson` drafter (so it's cheap), the standing rule with honest-decline (so it
  happens). That trio is a complete loop and is mostly docs/skill work — no rot-prone
  machinery.
- **Later, once the habit has earned it: 4, then 5.** Co-location and the auto-nudge are
  reinforcement. And the genuinely generalizable + mechanical lessons keep climbing into
  deterministic lints (ladder rung 6) — the strongest possible form.

## Status and next step

**Proposal only — nothing built, nothing adopted.** The agreed next step is to **pilot on
`prm` PR #59**: read the PR and draft the field-note + design-note entries for each
hardening component, as the cheapest way to pressure-test whether the format is actually
useful before standing up any infrastructure. Rich is reviewing PR #59 and will report
back; the pilot output should inform whether (and how) we adopt 1 + 2 + 3.

## Worked example (illustrative — pre-pilot, PR #59 not yet read)

What `/capture-lesson` might emit for one component, to show the target shape:

> **AC-8 (anti-enumeration).** Closing enumeration requires *all* of: always-200/204 even
> on failure, per-IP **and** per-email-hash rate limits, and distinct expired-vs-invalid
> strings — any one missing reopens the oracle. Surfaced in `prm` PR #59. Negative test:
> `test_send_unlock_returns_204_on_unknown_email`. Generalizable → AC-8 + DI-4 field note;
> the "how our server does it" detail stays in `prm`'s design note.
