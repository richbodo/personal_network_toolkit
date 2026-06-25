# PNA Exceptions

<!-- EDITING NOTE — machine-parsed tables: the exception registry table, the strength-profile tables, and the Reversible:/Reversal: fields are read by tools/lint-spec-ids.py AND by external report writers (reference-design conformance reports), and the `<a id>` row anchors are deep-linked from those reports. Treat the registry's columns, headers, and IDs (and the strength-class vocabulary) as an API: if you change one, update those consumers — and the lint's self-tests (tools/tests/lint_selftest.py) — in the same change. The lint finds columns by header name, so the EX ID may sit in any column; it currently lives in the last column. -->

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This file defines **Exceptions**: stable-ID'd conditions (`EX-*`) under which a PNA deliberately
> departs from a baseline guarantee — a named AC, or the core PNA definition ("runs local-only,
> never as SaaS"; see [`PNA_Spec.md` § Vocabulary](PNA_Spec.md), `vocab-pna`).

> **⚠ Proposed amendments (RFC — not yet accepted).** This file carries **two** still-proposed changes,
> opened for maintainer consideration (rationale in the companion design note
> `docs/design-notes/2026-06-exceptions-existential-review.md`): **(1)** split the overloaded
> "conformant" predicate into **`pna-active`** (the mode bit a relying party keys on) and
> **`exception-handling`** conformance — a reporting *clarification* (§ Concept); **(2)** harden
> **EX-H7** from best-effort to *fail-closed* when human consent cannot be confirmed at a
> PNA-controlled surface (§ Handler contract). Change (2) imposes a **new obligation** on designs, so
> per [`CONTRIBUTING.md`](../CONTRIBUTING.md) § Contribution types it requires a **demonstrating
> reference design** before acceptance — the **PRM v0.2** *hardened model* (consent enforced at the
> PNA's own surface); `fellows_local_db` ships only best-effort today, so it does not yet demonstrate
> fail-closed. The separately-tracked *architectural data-floor* (`AC-MCP-C` / `PR-7`) — which bounds
> *what* an exception may disclose, not just the act — rides the same **PRM v0.2** demonstrator
> ([data-floor note](../docs/design-notes/2026-06-data-floor-disclosure-tiers.md)) and **complements**
> these. The two remaining proposals are inline-tagged *(Proposed, RFC)*.
>
> **Accepted (normative).** The **un-relaxable floor** (§ Scope discipline) — guarantees no exception
> may relax even with consent (**AC-18 / AC-19 / AC-MCP-B**) — is now normative: demonstrated by
> `EX-CLOUD-LLM` (which relaxes no floor AC) and **enforced** by `tools/lint-spec-ids.py` (a `Relaxes:`
> naming a floor AC fails CI). *(Formerly proposal (3).)*

This file also catalogs the **mitigation side** of exceptions — a reusable
[Countermeasure library](#countermeasure-library) — and names its sibling for adversary-in-the-runtime
hazards, the advisory [Harden flow](#environmental-threats-and-the-harden-flow). Both are **additive and
impose no new obligation**: they organize the recommended solutions an exception already names (EX-H6),
and are **not** part of the RFC above.

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
  same refusal-to-collapse the toolkit already applies in the strength profile (EX-H8) and that EARL applies
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
flow](pna-toolkit/SKILL.md) reports both, by `EX-*` ID.

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

The PNA Toolkit **validates behaviors against the Goals; it does not certify.** There is no pass/fail badge and
no certifying body (see `CONTRIBUTING.md` and the skill's § Principles, "Conformance is checked, not
awarded"). The evaluate flow *detects* exceptions and *verifies how each is handled*, reporting by
`EX-*` ID. "This app raises `EX-CLOUD-LLM` and handles it to contract" is a finding, not a grade.

### Scope discipline

Exceptions are bounded so they stay a PNA-class mechanism rather than a general deviation framework:

- **Goal-anchored.** Every exception MUST name, via `Relaxes:`, the specific `AC-*` (or
  `PNA-DEFINITION`) it departs from. The toolkit defines exceptions ONLY for deviations from its own
  Goals/ACs — not for other application classes. A proposed "exception" that relaxes no named PNA
  guarantee is not a PNA exception.
- **Composition, not enumeration.** Non-PNA mode is binary (in / out). The active-set explainer
  (EX-H4) renders the *currently-active* exceptions at runtime, each with its own entry and strength
  profile. The toolkit never pre-enumerates combinations; cost scales linearly in the number of defined
  exceptions, not combinatorially.
- **Un-relaxable floor.** *(Normative — generalizes a per-exception fact into a standing rule; a new
  obligation on future exceptions. Demonstrated by `EX-CLOUD-LLM` (relaxes no floor AC) and enforced by
  `tools/lint-spec-ids.py`: a `Relaxes:` naming a floor AC fails CI.)* Some guarantees are a floor that
  **no exception may relax, even with consent.** Charter members: **AC-18** (a transport's mechanism cannot read message
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
  demonstrated by a reference design. Recommended solutions are drawn from the
  [Countermeasure library](#countermeasure-library) below — a reusable, hazard-keyed catalog — and an
  exception's entry composes the catalog rows it relies on. The library is a *menu*, not a new
  obligation: EX-H6 stays a SHOULD.
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

> **Sub-contract IDs.** `EX-H1..EX-H8` follow the toolkit's existing sub-contract convention
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
  strictly relaxing a single AC. Example: `Stresses: Goal 3`.

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

## Countermeasure library

EX-H6 asks an exception to name a *recommended solution*. Those solutions are not one-off: the same
hazard — an AI client over-reaching the Private DB, another process reading the store, a proxy
consenting on the human's behalf — recurs across exceptions and across designs. This section collects
the recommended solutions into a reusable, **hazard-keyed catalog**: the **mitigation side** of the
Exceptions mechanism. An exception's `Recommended solution` (EX-H6) composes one or more catalog rows;
a reference design demonstrates the PNA-intrinsic ones.

A countermeasure is described by four fields, three of which reuse machinery this file already defines:

- **Hazard addressed** — the threat the countermeasure reduces.
- **Strength** — the honest assurance class, drawn from the **same fixed vocabulary as the strength
  profile** (EX-H8): `enforced` / `verifiable` / `best-effort` / `provider-asserted` /
  `recoverable-only` / `none`. A countermeasure that only *reduces* risk says so here; the catalog
  refuses a collapsed "secure" label exactly as EX-H8 does. (Lint-checked for membership; the evaluate
  flow judges accuracy.)
- **Locus — PNA-intrinsic vs environmental.** *Intrinsic* countermeasures are realized by the PNA's own
  code and tie to a named AC — the toolkit can require them and a design can demonstrate them.
  *Environmental* countermeasures live in the user's operating environment (the OS, an agent sandbox, a
  broker process); the PNA's code has no reach there, so the toolkit can only **advise** their adoption
  — that advice is the [Harden flow](#environmental-threats-and-the-harden-flow). The Locus is why a
  single hazard can carry both an `enforced` intrinsic row and a `best-effort` environmental row.
- **Demonstrator** — the reference design (or proposed demonstrator) that exercises the countermeasure,
  per the toolkit's reference-driven model. Environmental countermeasures are demonstrated by the Harden
  flow's advice, not by a conformance attestation.

> **On the strength of *environmental* rows.** An environmental countermeasure may be strongly enforced
> *by the OS* once in place (a separate user account, an honoured `denyRead`), but the toolkit cannot
> compel a user to deploy it; end-to-end, the assurance the toolkit can stand behind is bounded by
> adoption, so those rows read `best-effort`. The Locus column carries the nuance the single Strength
> value can't.

<!-- machine-parsed: the Strength column is validated against the EX-H8 vocabulary by tools/lint-spec-ids.py; keep every value a bare class word. -->
| Countermeasure | Hazard addressed | Strength | Locus | Demonstrator |
|---|---|---|---|---|
| **Consent enforced at the PNA's own surface, fail-closed** — disclosure needs a human action on a surface the PNA controls; refuse when a comprehending human can't be confirmed | A proxy / agent self-consents to a cloud disclosure on the user's behalf | enforced | PNA-intrinsic (AC-MCP-A; EX-H7 fail-closed, *RFC*) | `fellows_local_db` consent gate; fail-closed direction *RFC* |
| **Surface minimization** — the cloud-facing private surface exposes only the tools a use needs; the most sensitive (notes, comms history) are simply not on it | A connected client reads more of the Private DB than the task needs | verifiable | PNA-intrinsic (AC-MCP-A) | `fellows_local_db` (`private_data_ops` = groups only) |
| **Data-floor — sealed-by-default disclosure tiers** — most-sensitive fields are unreachable by any cloud-facing surface *by construction*, even with consent | Over-broad disclosure once consent is given | enforced | PNA-intrinsic (AC-MCP-C / PR-7, *proposed*) | PRM v0.2 (proposed; [data-floor note](../docs/design-notes/2026-06-data-floor-disclosure-tiers.md)) |
| **Human-presence gating** — a fresh human-presence signal is required before private rows are returned | A headless / automated agent drains the Private DB with no human present | best-effort | PNA-intrinsic | none yet (proposed) |
| **Sandbox the automation agent / `denyRead` the store** — the user confines an OS-automation agent so it cannot read the PNA's data files (against a *same-UID* agent a namespace alone is **insufficient** — see *On confining a same-UID agent* below) | An OS-level AI agent with broad filesystem access reads the store out-of-band | best-effort | environmental (Harden) | advisory — Harden flow |
| **Run the PNA under a separate OS user** — file-permission isolation so an agent running as the primary user cannot read the store; **the cleanest convenient desktop answer** — a distinct UID denies the agent at the file-permission, `/proc`, and `ptrace` checks at once (see the note below) | An OS-automation agent reading the store as the primary user | best-effort | environmental (Harden) | advisory — Harden flow |
| **MCP access broker with per-request / JIT grants** — an intermediary mediates each tool call with a just-in-time, scoped grant the user approves | A connected client over-pulls across a long-lived session | best-effort | environmental (Harden); intrinsic analog AC-MCP-A | advisory — Harden flow |
| **Honeytoken + watchdog ("claw trap")** — a canary record plus a monitor that detects an unexpected read and raises an alert / triggers a response | An intrusion or rogue process reading the store goes unnoticed | recoverable-only | environmental (Harden) | advisory — Harden + watchdog-advisor skill |

**At-rest encryption is deliberately *not* in this catalog.** Scoping at-rest encryption to "MCP-on"
windows was considered (and revisited) as a countermeasure; the toolkit's standing decision —
re-confirmed by the data-protection-vs-OS-automation research that seeded this catalog — is that
**at-rest encryption stays deprecated** for the live store: it is dominated by full-disk encryption, and
it contradicts the **tool-readability** the PNA promises (the user can open their own Private DB with
ordinary SQLite tools; see [`constraints.md`](constraints.md), `CST-PWA-SANDBOX-SEALED`). Every
countermeasure above was chosen because it **mediates the access path or detects the intrusion while
preserving readability**, rather than encrypting the data away from its owner.

**On confining a *same-UID* agent — why "separate OS user" leads.** The hardest case for the environmental
rows is an OS-automation agent running under the **same user** as the PNA. Deep research into the desktop
primitives (Linux · macOS · Windows, with the mobile contrast) found that confining a same-UID reader is
an **access-control problem, not an encryption one**: at-rest encryption keyed to the login (Linux
`fscrypt`, Windows EFS, DPAPI) releases the key to the logon session, so a same-user process is already
inside the trust boundary — the kernel itself defers to "file mode bits, ACLs, LSMs, or namespaces." Two
consequences for the rows above:

- A **mount-namespace sandbox alone is insufficient** against a same-UID agent: it reaches the decrypted
  view through the `/proc/<pid>/root` "wormhole" (gated only by same-UID `PTRACE_MODE_READ_FSCREDS`, which
  it passes — Yama `ptrace_scope` gates *attach*, not *read*) and can `ptrace` the live process. Hardening
  it takes `PR_SET_DUMPABLE=0` (closes the wormhole) **+** `ptrace_scope ≥ 1` (blocks live-memory reads)
  **+** a **per-process MAC** (SELinux/AppArmor; Landlock can only self-restrict the app, never confine a
  peer agent).
- **Running the PNA under a separate OS user** sidesteps the whole problem cheaply — a distinct UID fails
  the agent at the file-permission, `/proc`, and `ptrace` checks at once. It is the **cleanest convenient
  desktop countermeasure**, and it recreates by hand what **mobile platforms do by construction**: each app
  gets its own UID/sandbox **+** per-app key by default, so the same-UID-agent threat is largely a *desktop*
  problem. (On Windows the convenient equivalent is a VM boundary — a WSL2 instance hosting the composite;
  a same-user *VM* is the isolation a shared-UID desktop otherwise lacks.)

All of this stays **"raise the bar," not hardware-grade**: a determined root, or an agent that *spawns* the
app (making it a `ptrace` descendant), still wins — consistent with the [Harden flow](#environmental-threats-and-the-harden-flow)'s
advisory posture. (The at-rest decision this elaborates: [`docs/PriorArt.md` § Design notes](../docs/PriorArt.md).)

## Environmental threats and the Harden flow

*Advisory — this section adds no AC and imposes no new obligation on a conforming PNA. It names a
category of pressure the toolkit responds to by **advising**, not by requiring.*

An Exception is **raised by the user** and **handled by the app** — the software analogy is
`raise` / `try-except`. Some hazards don't fit that shape: an adversary in the runtime (an OS-automation
AI agent reading the store, another process opening the DB) is not something the user *raises* and not
something the app's control flow *catches*. It arrives from outside, like a **signal or interrupt**, and
defending against it lives mostly in the user's **operating environment**, where the PNA's code has no
reach — so the toolkit's role is to **advise** which countermeasures work and are appropriate, not to
mandate one.

That makes **environmental threats a sibling of Exceptions**, not a kind of them. The two share the
[Countermeasure library](#countermeasure-library) and the strength vocabulary, but differ on who acts:

| Pressure | Raised / detected by | Handled by | Toolkit's role |
|---|---|---|---|
| **Exception** (`EX-*`) | the user — a deliberate action | the app — the handler contract | require + a design demonstrates |
| **Environmental threat** | detection — a hazard appears in the runtime | the user — mitigates in their environment | **advise** — the Harden flow |

This completes a small taxonomy of **the four sources of pressure** on a PNA's guarantees:

- **Constraints** (`CST-*`, [`constraints.md`](constraints.md)) — a *platform* ceiling the PNA inherits.
- **Exceptions** (`EX-*`, this file) — a *user* relaxation, app-handled.
- **Environmental threats** (this section) — an *adversary in the runtime*, detected → user-mitigated with toolkit advice.
- **[User-mediation](user_mediation.md)** (`UM-*`) — the *actuation* invariant: the proposer stages, the principal disposes. Now its own first-class mechanism (the **third**, with Constraints and Exceptions) — a standing invariant the architecture upholds, not a pressure to handle.

Constraints and Exceptions are duals (a ceiling imposed vs. a guarantee relaxed); environmental threats
are the third party at the table — neither imposed by the platform nor chosen by the user, but brought
by an adversary. The toolkit draws a clean line through them:

> **App security is `build` / `evaluate` / `contribute`; environment security is `harden` / advise.**
> What a *built PNA* must do lives in the ACs (and is checked by the first three flows). Securing the
> *operating environment the PNA runs in* — compensating controls, monitoring, detect-and-respond — is
> the **Harden** flow: a fourth, **advisory** toolkit flow that tells the user which environmental
> countermeasures apply to their hazard and environment, which are in place, and what is still exposed.
> (Compensating controls and monitor-and-respond echo NIST CSF *Identify → Protect → Detect → Respond*.)

The Harden flow's procedure (the advisor skill) is sequenced separately — see [`roadmap.md`](../docs/roadmap.md);
this section establishes the **concept** and its place beside Exceptions. The environmental rows of the
[Countermeasure library](#countermeasure-library) are its catalog.

## Exception registry

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. -->
| Name | Relaxes | Stresses | Reversible | Recommended solution | EX |
|---|---|---|---|---|---|
| Cloud-hosted AI over PNA data | PNA-DEFINITION, AC-MCP-A | Goal 3 | yes (mode only) | consent gate + persistent dismissable "not a PNA" signal + active-set explainer + return-to-PNA-mode — demonstrated by `fellows_local_db` | EX-CLOUD-LLM |

<a id="ex-cloud-llm"></a>
### EX-CLOUD-LLM — Cloud-hosted AI over PNA data

**Relaxes:** PNA-DEFINITION, AC-MCP-A
**Stresses:** Goal 3
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
Demonstrated by `fellows_local_db` (`reference_designs/fellows_local_db/`). These compose
[Countermeasure library](#countermeasure-library) rows — consent enforced at the PNA's own surface and
surface minimization (both PNA-intrinsic, demonstrated by `fellows_local_db`), with the proposed
data-floor (PRM v0.2) as the bounding twin.

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
[un-relaxable floor](#scope-discipline), so even a fully-consented exception keeps
the human-in-the-loop-before-send seam intact. Keeping the `Relaxes:` set tight is part of honest
handling — an exception names the *minimum* set of guarantees it actually departs from.

## Origin

The Exceptions concept was distilled from operating the `fellows_local_db` reference design with a
~500-user base: users wanted cloud-LLM integration, local models were impractical for them, and the
spec had no first-class way to deviate *honestly*. See that design's `docs/architectural_findings.md`
(upstream) and `reference_designs/fellows_local_db/`. Per the toolkit's reference-driven model, this concept
ships alongside the working design that demonstrates it.
