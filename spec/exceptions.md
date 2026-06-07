# PNA Exceptions

<!-- EDITING NOTE — machine-parsed tables: the exception registry table, the strength-profile tables, and the Reversible:/Reversal: fields are read by tools/lint-spec-ids.py AND by external report writers (reference-design conformance reports), and the `<a id>` row anchors are deep-linked from those reports. Treat the registry's columns, headers, and IDs (and the strength-class vocabulary) as an API: if you change one, update those consumers — and the lint's self-tests (tools/tests/lint_selftest.py) — in the same change. The lint finds columns by header name, so the EX ID may sit in any column; it currently lives in the last column. -->

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This file defines **Exceptions**: stable-ID'd conditions (`EX-*`) under which a PNA deliberately
> departs from a baseline guarantee — a named AC, or the core PNA definition ("runs local-only,
> never as SaaS"; see [`PNA_Spec.md` § Vocabulary](PNA_Spec.md), `vocab-pna`).

> **⚠ Proposed amendments (RFC — not yet accepted).** This file carries three proposed changes,
> opened for maintainer consideration (rationale in the companion design note, landing at
> `docs/design-notes/2026-06-exceptions-existential-review.md`): **(1)** split the overloaded
> "conformant" predicate into **`pna-active`** (the mode bit a relying party keys on) and
> **`exception-handling`** conformance — a reporting *clarification* (§ Concept); **(2)** harden
> **EX-H7** from best-effort to *fail-closed* when human consent cannot be confirmed at a
> PNA-controlled surface (§ Handler contract); **(3)** add an **un-relaxable floor** of guarantees no
> exception may relax (§ Scope discipline). Changes (2) and (3) impose **new obligations** on designs,
> so per [`CONTRIBUTING.md`](../CONTRIBUTING.md) § Contribution types they require a **demonstrating
> reference design** before acceptance (`fellows_local_db` would demonstrate fail-closed; a PRM the
> hardened model). A **fourth, separately-tracked** correction came out of a follow-up review — an
> *architectural data-floor* (`AC-MCP-C` / `PR-7`) that bounds *what* an exception can disclose, not
> just the act of disclosing — drafted as its own proposal
> ([`docs/design-notes/2026-06-data-floor-disclosure-tiers.md`](../docs/design-notes/2026-06-data-floor-disclosure-tiers.md)),
> to be demonstrated by the PRM reference design; it **complements, not replaces**, the three here.
> Inline changes are tagged *(Proposed, RFC)*.

## Concept

An Exception is modeled on a software exception. It is **raised** by a specific user action, must
be **caught** (never raised silently), and must be **handled** by a defined **solution**.

| Software exception | PNA Exception |
|---|---|
| A condition that interrupts normal control flow | A condition under which a PNA departs from a baseline guarantee |
| `raise` / `throw` | **Raised** by a specific user action (e.g. connecting a cloud MCP client) |
| Uncaught exception crashes / leaks | A *silent* deviation is the failure mode — exceptions MUST be **caught** |
| `try/except` handler | A defined **solution** (consent + signal + explainer + reversal path) |
| Stack trace identifies the exception | Every exception has a stable `EX-*` ID and a registry entry |

**An app is in PNA mode when no exceptions are active.** Raising any exception exits PNA mode. Two
*separate* predicates then describe the app, and fusing them is the mistake the rest of this section
exists to prevent: *(Proposed, RFC — predicate split; a reporting clarification.)*

- **`pna-active`** — the mode bit. `true` only while **no** exception is active. This is the
  categorical claim the word *PNA* carries: *the architecture is holding the local-only guarantee
  right now.* A relying party — a user reading the screen, or another PNA deciding whether to expose
  its Private DB (see [`PNA_Spec.md` § Vision](PNA_Spec.md), interop) — keys on this bit, and on
  nothing else.
- **`exception-handling`** — how honestly the app handles each active exception, **reported per
  handler clause** (EX-H1..EX-H8) as `pass` / `partial` / `cannot-tell` (à la EARL). A statement
  about *process*, not about the guarantee: the app is deviating *honestly*. It is deliberately
  **never aggregated into a single conferred "conformant" status, and is never an interop
  credential** — only `pna-active` is conferred and gated on (see *Discipline* below). This is the
  same refusal-to-collapse PNT already applies in the strength profile (EX-H8) and that EARL applies
  per-assertion: a rolled-up "handled conformantly" bit would hide exactly the `partial` /
  `cannot-tell` the per-clause report exists to surface.

This reframes conformance:

- **Old framing:** conformant = *never deviates from any AC or the PNA definition.*
- **New framing:** *in PNA mode (`pna-active = true`) honor every applicable AC; in non-PNA mode the
  app is **not a PNA right now** (`pna-active = false`, the guarantee is suspended) yet
  **exception-handling conformant** if it catches and handles every active deviation honestly.*

A tool that lets a user point a hosted model at their Private DB is neither "non-conformant garbage"
nor "secretly fine." The honest report names **both** predicates: *not a PNA while `EX-CLOUD-LLM` is
active (`pna-active = false`), and exception-handling conformant.* The earlier shorthand — "a
conformant PNA operating in a declared non-PNA mode" — fused the two and is **retired**: *PNA* is the
guarantee, and the guarantee is suspended while an exception is active. The [evaluate
flow](pna-build-eval-contrib/SKILL.md) reports both, by `EX-*` ID.

**Discipline — confer the membership bit, report the rest.** *(Proposed, RFC — sharpens this change
with the "detect, don't bless" rule.)* `pna-active` is the **only conferred conformance verdict** and
the **only thing a future interop gate keys on** ([`PNA_Spec.md` § Vision](PNA_Spec.md)); a peer MUST
refuse Private-DB access to an app whose `pna-active` is false *regardless* of how well it handles its
exceptions. The per-clause handler report is description a *human* reads — never a badge a vendor can
wave or a gate a machine can pass. Concretely: the evaluate report's `summary.posture`
([`tools/evaluate-report.schema.json`](../tools/evaluate-report.schema.json)) MUST be redefined so its
conferred value reports **PNA membership only** (exception handling living solely in the per-`EX-*`
findings), so that a cleanly-handled `EX-CLOUD-LLM` app can never surface a top-line
`posture: conformant`. (That schema edit lands with acceptance; it is named here so acceptance accepts
it.)

### Validation, not certification

PNT **validates behaviors against the Goals; it does not certify.** There is no pass/fail badge and
no certifying body (see `CONTRIBUTING.md` and the skill's § Principles, "Conformance is checked, not
awarded"). The evaluate flow *detects* exceptions and *verifies how each is handled*, reporting by
`EX-*` ID. "This app raises `EX-CLOUD-LLM` and handles it to contract" is a finding, not a grade.

### Scope discipline

Exceptions are bounded so they stay a PNA-class mechanism rather than a general deviation framework:

- **Goal-anchored.** Every exception MUST name, via `Relaxes:`, the specific `AC-*` (or
  `PNA-DEFINITION`) it departs from. PNT defines exceptions ONLY for deviations from its own
  Goals/ACs — not for other application classes. A proposed "exception" that relaxes no named PNA
  guarantee is not a PNA exception.
- **Composition, not enumeration.** Non-PNA mode is binary (in / out). The active-set explainer
  (EX-H4) renders the *currently-active* exceptions at runtime, each with its own entry and strength
  profile. PNT never pre-enumerates combinations; cost scales linearly in the number of defined
  exceptions, not combinatorially.
- **Un-relaxable floor.** *(Proposed, RFC — generalizes a per-exception fact into a standing rule; a
  new obligation on future exceptions.)* Some guarantees are a floor that **no exception may relax,
  even with consent.** Charter members: **AC-18** (a transport's mechanism cannot read message
  contents), **AC-19** (the user sees the full payload before any send, and can edit or cancel), and
  **AC-MCP-B** (the workspace — not an MCP/AI client — launches the send; AC-19 "MUST NOT be
  bypassable by AI clients"). The principle that fixes the line: a user MAY consent to **disclosing
  data they read** — that is what `EX-CLOUD-LLM` is — but MUST NOT be able to consent away the
  **human-in-the-loop on an action taken on their behalf**, because that action reaches *other
  people*, the contacts in their graph, who consented to nothing. Disclosure is a bounded harm to
  one's own data; unreviewed delegated action is an open-ended harm to third parties. An exception
  that lists a floor AC among the guarantees it departs from is **malformed**, not merely strong.
  This is the *action*-floor (no unreviewed action on the user's behalf). A symmetric *data*-floor —
  the most-sensitive Private-DB fields structurally unreachable by a cloud surface, even with consent
  — is proposed as a separate follow-up (`AC-MCP-C` / `PR-7`; see the banner) and demonstrated by PRM;
  together they bound both *what is done* and *what is disclosed*.

## Handler contract

Normative language uses RFC 2119 / RFC 8174 keywords (MUST, MUST NOT, SHOULD, MAY) only when
capitalized, consistent with [`PNA_Spec.md` § Universal architectural commitments](PNA_Spec.md). For
each exception it can raise, a conforming PNA:

- **EX-H1 — Stable identity.** MUST define and reference the exception by its stable `EX-*` ID.
- **EX-H2 — Consent before raise.** MUST obtain explicit informed consent BEFORE raising the
  exception (no silent raise). The consent surface MUST link to an explanation of that specific
  exception.
- **EX-H3 — Persistent non-PNA-mode signal.** While the exception is active, MUST present a
  persistent user-facing signal that the app is not in PNA mode. The signal MUST name the active
  exception and MUST link to an explanation of the active exception set. The signal MAY be
  dismissable, but dismissal MUST NOT clear the exception (dismissal acknowledges; it does not
  resolve).
- **EX-H4 — Active-set explainer.** MUST provide a user-reachable explanation of the
  CURRENTLY-ACTIVE exception set. Because active combinations are installation-specific and cannot
  be enumerated in a static document, this explainer MUST be generated at runtime from the active
  set and MUST link out to each active exception's registry entry in this file.
- **EX-H5 — Declared reversibility.** MUST declare whether returning to PNA mode is supported
  (reversible) or not (irreversible). If it declares reversible, it MUST provide a practical,
  user-reachable path back to PNA mode that the validation flow can confirm from code/UX.
  Reversibility refers to **MODE ONLY**: a handler MUST NOT imply that returning to PNA mode undoes
  consequences already incurred (e.g. data already disclosed to a third party).
- **EX-H6 — Recommended solution.** SHOULD name a recommended solution in its registry entry,
  demonstrated by a reference design.
- **EX-H7 — Consent reaches the ultimate human; fail closed when it cannot.** *(Proposed, RFC —
  tightens EX-H7 from pure best-effort to fail-closed; a new obligation.)* Where the consuming actor
  is an agent/proxy rather than the ultimate human (e.g. an orchestrator agent invoking the PNA on a
  person's behalf), the handler MUST make a best-effort attempt to propagate the notice and
  acceptance (EX-H2) to the ultimate human interface, and MUST NOT treat an intermediary agent's
  acceptance as the human's. **Consent for an exception that discloses Private DB rows MUST be
  obtained on a surface the PNA itself controls** (its own workspace), where the act of consenting is
  `enforced`, not relayed. *Best-effort up:* the PNA SHOULD use the MCP `instructions` handshake (and
  tool-result messages) to tell a cooperating client *"ask the user to open the app and confirm
  before I return private data — then come back."* *Hard refuse down:* where the PNA **cannot
  establish** that a comprehending human consented at its own surface (a non-cooperating client, a
  headless / agent-mediated call), the Private Data Ops surface MUST refuse — exercising AC-MCP-A's
  "either refuse" arm — rather than raise on a proxy's say-so. This moves the consent dimension from
  `best-effort` toward `enforced` for the case the PNA controls, while staying honest that a
  non-cooperating client cannot be compelled to relay anything. (Cf. macaroon attenuation: delegated
  authority only narrows down a chain, never amplifies.) The gate is genuinely `enforced` because the
  consent artifact lives on the PNA's **own** surface — a cloud client cannot forge a workspace-side
  human action — but note its *role*: it governs the **act** of disclosing the user-shareable view,
  not **which data is eligible** to cross. Bounding the latter is the proposed *data-floor*
  (`AC-MCP-C`; see the banner's fourth correction), which is why this gate is a real but
  **secondary** control, not the load-bearing protection for sensitive fields.
- **EX-H8 — Per-dimension strength disclosure.** MUST publish a **strength profile** for the
  exception (see [Strength profiles](#strength-profiles)): for each dimension of the guarantee, the
  *kind* of assurance offered, drawn from the fixed vocabulary. The profile MUST be user-reachable
  from the active-set explainer (EX-H4). A single collapsed "assurance level" MUST NOT be used in
  place of the per-dimension profile.

> **Sub-contract IDs.** `EX-H1..EX-H8` follow PNT's existing sub-contract convention
> (`<prefix>-<integer>`). They are deliberately prose/list items, not `| EX-… |` registry rows, so
> the lint collects them as handler clauses, not as registry exceptions. The evaluate flow cites
> them ("fails EX-H3 — no persistent signal").

## Header conventions

These mirror the `Realizes: AC-…` header that contract files carry (see `tools/lint-spec-ids.py`).
They appear in an exception's registry entry and in a reference design's handler declaration.

- **`Relaxes:`** — the baseline guarantee(s) the exception departs from; the inverse of `Realizes:`.
  Each token is an `AC-*` ID or the literal `PNA-DEFINITION` (for departures from "local-only, never
  SaaS"). Comma-separated. Example: `Relaxes: PNA-DEFINITION, AC-MCP-A`.
- **`Reversible:`** — whether returning to PNA mode is supported. `yes` or `no`. If `yes`, a
  `Reversal:` field MUST follow naming the mechanism (a route, control, or code reference the
  validation flow can confirm). See EX-H5.
- **`Stresses:`** *(optional, non-normative)* — a Goal the exception puts under pressure without
  strictly relaxing a single AC. Example: `Stresses: Goal 1`.

## Strength profiles

The strength of an exception's handling is disclosed **per dimension, not as a single graded level.**
A collapsed level (à la Common Criteria EAL or OWASP ASVS L1/2/3) would fold "the boundary is
enforced" together with "the provider's data handling is unverifiable" into one misleading number.
The honest frame: **once data crosses to a third party, the PNA can guarantee nothing about the data
itself; every real guarantee is about the *boundary* (consent, signaling, reversibility,
auditability) and *local recoverability*.**

Each dimension's class is one of the fixed vocabulary (lint-checked for membership; the evaluate
flow judges accuracy):

| Class | Meaning |
|---|---|
| `enforced` | The app's own code makes it true; locally testable/auditable. |
| `verifiable` | A claim an auditor can confirm from open code (not enforced at runtime, but checkable). |
| `best-effort` | The app requests it of an untrusted party; cannot compel. |
| `provider-asserted` | Depends entirely on a third party's own, app-unverifiable policy. |
| `recoverable-only` | The app cannot prevent the harm but can undo/restore it. |
| `none` | No guarantee is possible. |

## Exception registry

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. -->
| Name | Relaxes | Stresses | Reversible | Recommended solution | EX |
|---|---|---|---|---|---|
| Cloud-hosted AI over PNA data | PNA-DEFINITION, AC-MCP-A | Goal 1 | yes (mode only) | consent gate + persistent dismissable "not a PNA" signal + active-set explainer + return-to-PNA-mode — demonstrated by `fellows_local_db` | EX-CLOUD-LLM |

<a id="ex-cloud-llm"></a>
### EX-CLOUD-LLM — Cloud-hosted AI over PNA data

**Relaxes:** PNA-DEFINITION, AC-MCP-A
**Stresses:** Goal 1
**Reversible:** yes
**Reversal:** mode only — the user disconnects the cloud MCP client and returns to PNA mode.
Returning to PNA mode does NOT undo any disclosure already made to the cloud provider (EX-H5).

**Raised when:** the user connects a cloud-hosted MCP client (e.g. Claude Desktop on a hosted
model, a desktop AI app on a hosted API) to a PNA's MCP servers that can return Private DB rows. The
canonical trigger is the Private Data Ops server (see [`PNA_Spec.md` § Vocabulary](PNA_Spec.md), MCP
server).

**Recommended solution:** pre-raise consent gate (EX-H2) naming the exception and linking the
explainer; persistent dismissable "not a PNA right now" signal (EX-H3); runtime active-set explainer
(EX-H4) surfacing the strength profile below; declared, reversible return-to-PNA-mode path (EX-H5);
best-effort consent-propagation notice to cloud clients via the MCP `instructions` handshake (EX-H7).
Demonstrated by `fellows_local_db` (`reference_designs/fellows_local_db/`).

**Strength profile (EX-H8):**

| Dimension | Strength | Why |
|---|---|---|
| Consent precedes the raise | enforced | Setup is blocked until the user accepts the agreement. |
| Non-PNA-mode signal while active | enforced | A persistent banner shows until the user returns to PNA mode. |
| Mode is reversible | enforced | A return-to-PNA-mode control clears the exception. |
| Servers read-only, two files only | verifiable | Databases opened `mode=ro`; auditable in open source. |
| Local data damage from a bad AI step | recoverable-only | Not prevented — restorable from a backup/export. |
| Consent reaches the human, not a proxy | best-effort | EX-H7 — cloud clients are asked to relay it; cannot be compelled. *(RFC: the proposed EX-H7 fail-closed rule moves the PNA-controlled-surface case toward `enforced`; this row stays `best-effort` until a design demonstrates it.)* |
| Provider won't train on / retain the data | provider-asserted | The provider's policy; unverifiable by the app. |
| Data already sent to the provider | none | Irreversible once it has crossed the boundary. |

#### What it does and does not relax

`EX-CLOUD-LLM` relaxes the *delivery* guarantee (data leaves the device to a cloud model) and
AC-MCP-A's consent posture. It does **not** relax AC-MCP-B (the workspace still launches
transports), AC-1, or any other AC — and **cannot**: AC-18, AC-19, and AC-MCP-B are the
[un-relaxable floor](#scope-discipline) (*Proposed, RFC*), so even a fully-consented exception keeps
the human-in-the-loop-before-send seam intact. Keeping the `Relaxes:` set tight is part of honest
handling — an exception names the *minimum* set of guarantees it actually departs from.

## Origin

The Exceptions concept was distilled from operating the `fellows_local_db` reference design with a
~500-user base: users wanted cloud-LLM integration, local models were impractical for them, and the
spec had no first-class way to deviate *honestly*. See that design's `docs/architectural_findings.md`
(upstream) and `reference_designs/fellows_local_db/`. Per PNT's reference-driven model, this concept
ships alongside the working design that demonstrates it.
