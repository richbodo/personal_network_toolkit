# PNA User-Mediation

<!-- EDITING NOTE — machine-parsed: the user-mediation contract table (the `UM` ID column) and the `Unifies:` header are read by tools/lint-spec-ids.py, and the `<a id>` anchors are deep-linked from reference-design conformance reports. Treat the table's `UM` column, the property IDs, and the `Unifies:` AC list as an API: changing one means updating that consumer AND the lint's self-tests (tools/tests/lint_selftest.py) in the same change. -->

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This file defines **User-mediation** (`UM-*`): the standing invariant that **the human is the
> actuator** — the proposer (an AI, the network, an importer) only **stages**; the principal
> **disposes** through a user-controlled surface, and nothing mutates the sovereign store or egresses
> its data except through that gate. It is the **third general mechanism** of the toolkit, alongside
> Exceptions ([exceptions.md](exceptions.md)) and Constraints ([constraints.md](constraints.md)).

## Concept

Exceptions and Constraints each name a way a PNA's guarantees come under pressure and must be handled
honestly — a deviation the **user raises** (Exception) and a ceiling the **platform imposes**
(Constraint). User-mediation names the third: not a pressure to handle but a **positive invariant the
architecture upholds** at every point where data is mutated in the sovereign store or leaves the
device. The proposer computes and **stages**; the principal **disposes**. Nothing reaches the store or
the wire except through that gate.

| The actor | Its capability |
|---|---|
| **Proposer** — an AI over MCP, a network fetch, an importer, a dedup detector | **Stages only.** Computes a candidate change or outbound payload; has *no* actuation capability. |
| **Principal** — the user, acting through the workspace | **Disposes.** Reviews the staged change in a user-controlled surface and is the sole party that commits it or launches the send. |

Unlike an Exception, user-mediation does **not** exit PNA mode — it is the always-on shape of a PNA's
write and egress paths, present whenever the app is a PNA at all. Unlike a Constraint, no platform
imposes it; the architecture commits to it.

### A third general mechanism

The toolkit names three mechanisms, each kept in its own file so it stays a single mental model:

- **[Exception](exceptions.md) (`EX-*`)** — a *user-raised* departure from a guarantee; raising one
  **exits PNA mode**; handled to the handler contract.
- **[Constraint](constraints.md) (`CST-*`)** — a *platform-imposed* ceiling inherited by an axis pick;
  handled by capability reduction; does **not** exit PNA mode.
- **User-mediation (`UM-*`)** — the *architecture-upheld* actuation invariant beneath the action /
  egress ACs; an always-on property, not a deviation.

### The bounded claim

User-mediation guarantees **separation, legibility, and attribution — not comprehension.** It ensures
the actuation is *decoupled* from the proposer, *rendered legibly* before it commits, and *attributable*
to a dispose event the principal triggered. It does **not** guarantee the principal *understood* what
they approved: an automation acting for the user can drive the dispose surface and click Approve,
exactly as it can for an Exception's consent — the same honest limit as [EX-H7](exceptions.md). The
claim is the **shape of the path**, not the cognition of the actor. Over-claiming comprehension —
implying the gate proves understanding — is a silent conformance failure, the dual of an undeclared
deviation.

### Validation, not certification

The PNA Toolkit **validates behaviors against the Goals; it does not certify** (see `CONTRIBUTING.md`
and the skill's § Principles, "Conformance is checked, not awarded"). The
[evaluate flow](../pna-toolkit/SKILL.md) enumerates a candidate's mutation and egress **boundaries** and
verifies UM-1/2/3 hold at each — reporting per boundary, by `UM-*` ID. "This design routes private-store
restore through the dispose gate, refused at the data layer (UM-1 + UM-2 hold; UM-3 weaker than AC-10's
preview — frontier)" is a finding, not a grade.

## What it unifies

User-mediation is the **named invariant beneath** several architectural commitments that each
instantiate it on one surface; the mechanism states once what they share.

**Unifies:** AC-10, AC-16, AC-19, AC-20, AC-21, AC-MCP-B

Each of these ACs is a *face* of the same invariant — the user picks the transport (AC-16) and sees the
payload before it leaves (AC-19); an LLM call is governed as an egress (AC-20); a re-import previews what
it would orphan and is user-committed (AC-10) and never background-polled (AC-21); an MCP tool stages and
the workspace launches (AC-MCP-B). User-mediation does not replace these ACs; it names the principle they
share, so a builder implements it once and an evaluator checks it as one property.

## The user-mediation contract

Normative language uses RFC 2119 / RFC 8174 keywords (MUST, MUST NOT, SHOULD, MAY) only when
capitalized, consistent with [`PNA_Spec.md`](PNA_Spec.md). At **every** boundary that mutates the
sovereign (Private) store or sends its data off-device, a PNA upholds:

<!-- machine-parsed table — see the EDITING NOTE at the top of this file. -->
| Property | Requirement (summary) | UM |
|---|---|---|
| No bypass | No path mutates the store or egresses its data except through the dispose gate; enforced at the data layer. | <a id="um-1"></a>UM-1 |
| Separation | The proposing surface carries no actuation capability; dispose is a distinct, attributable event. | <a id="um-2"></a>UM-2 |
| Legibility | The dispose surface renders a deterministic, human-readable payload and escapes untrusted proposer strings. | <a id="um-3"></a>UM-3 |

- **UM-1 — No bypass.** Every path that mutates the Private store or egresses its data MUST route
  through the dispose gate. The refusal MUST be enforced at the **data layer** (the storage owner, or
  the egress chokepoint), not UI-only: a surface hidden while the underlying write or send still
  succeeds — driven from a developer console, or by calling the worker directly — is **not** mediated.
  Because this is a **negative invariant**, it MUST be pinned by a **negative test** (the proposer path
  is *refused*, not merely unused).
- **UM-2 — Separation.** The proposing surface MUST carry no actuation capability. A proposal MUST be
  inert until the principal disposes it through a distinct, attributable action. An MCP / AI surface
  that can both propose a change and commit it is not separated. (At the MCP write boundary this is
  AC-MCP-B's "the server proposes; the workspace disposes," generalized to every proposer.)
- **UM-3 — Legibility.** The dispose surface MUST render the staged change or outbound payload
  **deterministically and human-readably** before the principal commits — names, not opaque IDs — and
  MUST treat the proposer's text as **data, never trusted markup** (escape it). Legibility is bounded
  (§ The bounded claim): it makes *what is changing* visible; it does not certify comprehension. Where a
  boundary's legibility is weaker than a related AC requires (e.g. a row-count delta vs. AC-10's
  per-member orphan preview), the design MUST declare the **frontier** honestly rather than over-claim.

## Mediated boundaries

UM-1/2/3 are a property *of each boundary*, not of the app in the abstract. A conforming design
enumerates its **mediated boundaries** — every distinct path that mutates the Private store or egresses
its data (private-data restore, group / tag / note edits, outreach, AI-proposed merges, …) — and
attests UM-1/2/3 at each: the negative test pinning UM-1, and an honest **frontier** where a boundary's
legibility is weaker than its related AC. The spec defines the invariant once; the design maintains the
**mediated-boundary registry** in its own Architecture document (the per-boundary table). This is the
actuation analog of the constraints registry — there a platform-by-platform ceiling, here a
boundary-by-boundary invariant.

## Header conventions

These mirror the `Realizes:` header in `contracts/` and the `Relaxes:` / `Bounds:` headers in the
sibling mechanisms.

- **`Unifies:`** — names the `AC-*` commitments user-mediation is the invariant beneath (above). Every
  token MUST be a defined AC; the lint resolves each, so a renamed or retired AC cannot silently dangle
  the mechanism.
- **`UM-*` IDs** — the three properties are a fixed set (`UM-1` no-bypass, `UM-2` separation, `UM-3`
  legibility); numbers are not reused. A design's per-boundary attestation cites them with a status
  (`conformant` / `partial-conformance` + the declared frontier).

## Demonstrators

User-mediation is reference-driven (per `CONTRIBUTING.md` — a mechanism ships with the designs that
demonstrate it). Two reference designs attest UM-1/2/3 `conformant` at complementary halves of the
invariant:

- **`fellows_local_db` — the egress side.** The worker refuses durable private writes and off-device
  sends except through the gate, enforced at the data layer (refused even via the raw worker RPC); a
  mediated-boundary registry covers restore, group / note edits, and outreach. See
  `reference_designs/fellows_local_db/Architecture.md` § User-mediation attestation.
- **`prm` — the mutation side.** The propose→review→apply loop: an MCP / AI proposer stages an inert
  changeset; the lock-guarded daemon is the sole applier; the workspace renders a per-field,
  provenance-bearing diff. See `reference_designs/prm/Architecture.md` § User-mediation attestation.

## Origin

User-mediation was distilled from a latent invariant already load-bearing across the spec — the
*action-floor* of [`exceptions.md`](exceptions.md) (no unreviewed action on the user's behalf), AC-MCP-B,
AC-19, AC-10 — surfaced while building the `fellows_local_db` workspace-mediation work (fellows#252), and
corroborated by the behavioral-space survey ([`docs/papers/paper1-pna-positioning.md`](../docs/papers/paper1-pna-positioning.md)),
which read the toolkit's honest-deviation machinery as a distinctive contribution. It was promoted from a
proposal to a named mechanism once both reference designs demonstrated it. Per the toolkit's
reference-driven model, this concept ships alongside the working designs that demonstrate it.
