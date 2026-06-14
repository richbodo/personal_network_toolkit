# Data-floor: per-field disclosure tiers for exceptions (`AC-MCP-C` / `PR-7` / `EX-H9`)

*Design note / spec stub · 2026-06 · status: **proposed (RFC), demonstrated-by: PRM v0.2**. Companion
to the honest-exit RFC ([PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32)) and the
[existential review](2026-06-exceptions-existential-review.md) it came out of. Indexed from
[`../PriorArt.md` § Design notes](../PriorArt.md).*

> **This is a stub, not a normative change.** It proposes new spec objects (`AC-MCP-C`, `PR-7`,
> `EX-H9`) but deliberately does **not** add them to the live AC table, sub-contract list, or handler
> contract — doing so would assert an obligation no accepted design yet demonstrates (and would make
> `fellows_local_db` retroactively non-conformant). Per [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)
> § Contribution types, an obligation-imposing AC lands **with the reference design that demonstrates
> it**. The intended demonstrator is the **PRM** reference design at v0.2; this note is the design on
> record so the demonstrator has a target.

## The gap this closes

PR #32 makes the exit honest (labeling), hardens the consent gate (EX-H7 fail-closed), and protects
the human-in-the-loop on *action* (the un-relaxable action-floor). All three govern the **act** of
disclosure. None touches the **blast radius** — *how much, and how sensitive, the data that crosses
is*. The `EX-CLOUD-LLM` strength profile says this part out loud: "Data already sent to the provider →
`none`", "Provider won't train on / retain → `provider-asserted`". You cannot raise `none` after the
fact. You **can** bound the antecedent — *which data is eligible to cross at all* — entirely before the
irreversible step, in the zone where the PNA's own code is sovereign and `enforced` applies.

This was the strongest single result of the moderated tournament of alternates (see the existential
review): consent hardening polishes a control the review proved is structurally unverifiable in the
adversarial case; a **data-floor** puts a `verifiable` floor *underneath* it, so that even a defeated
consent gate leaks only a bounded, user-curated subset rather than the whole Private DB. It is the
*symmetric twin* of PR #32's action-floor: **you may consent to disclose data you read; the
most-sensitive data is not even reachable to be disclosed.**

## The proposal

### Disclosure tiers (fixed, lint-checked vocabulary)

| Tier | Meaning at a cloud-facing MCP surface |
|---|---|
| `private-sealed` | **Default.** Never reachable by any MCP surface an exception can expose to a non-local client. Not selectable into a projection; does not appear in any tool output, full stop. |
| `private-shareable-on-consent` | Reachable through a cloud-facing surface **only** while an exception is active **and** the field is in the user's curated projection. The only tier consent governs. |
| `shared` | Already in the Shared DB (contact PII the user accepts external systems hold). Out of scope for this tier — governed by AC-1. |

### `PR-7` (proposed Private-schema sub-contract)

Every Private-DB field (and every user-defined custom field) carries a `disclosure_tier`. The default
for any newly defined field is `private-sealed` (most-protective — mirrors PRM's INV-10 default-most-
protective AI-*write* tier). The tier is **mutable only in the workspace**, never via MCP (mirrors
PRM's INV-3 "schema mutable only in the workspace, enforced structurally not by prompt"). Enforcement
is at the **storage/query layer**, not the UI (per [`../../spec/constraints.md`](../../spec/constraints.md)'s
"reduce at the data layer, not UI-only" rule): a cloud-facing private surface issues queries against a
projection/view that physically selects only `private-shareable-on-consent` columns in the active
projection.

### `AC-MCP-C` (proposed universal AC; Serves Goal 3)

*A cloud-facing MCP surface MUST be projection-bound: it MUST expose only `private-shareable-on-consent`
fields that the user has placed in a curated projection, and MUST be incapable — at the tool-schema and
query layer — of returning a `private-sealed` field, even with consent, even while an exception is
active.* This is to `AC-MCP-B` (the action-floor: the workspace, not the AI, launches a send) what the
data-floor is to the action-floor. It composes with `AC-MCP-A` (cloud clients need per-call consent for
Private DB access): AC-MCP-A gates *whether* the shareable projection flows; AC-MCP-C bounds *what is in
it*.

### `EX-H9` (proposed handler clause)

An exception that relaxes a Private-DB delivery guarantee MUST publish, in its strength profile
(EX-H8), a **blast-radius** dimension naming *which tiers can cross*. That dimension MUST be `enforced`
(sealed fields cannot cross by construction) and MUST NOT be satisfied merely by consent over an
unbounded field set.

### Verification (makes the floor checkable, not prose)

- **A static `disclosure-tier` lint** (sibling of `tools/egress-lint.py` / `export-readable-lint.py`,
  with clean/dirty fixtures + a `lint_selftest` case): every Private-DB field declares a tier; default
  is `private-sealed`; no cloud-facing MCP tool output schema references a field whose tier is
  `private-sealed`. A sealed field on a cloud-facing surface is a hard failure — the dual of an
  undeclared exception.
- **A dynamic egress probe** in the evaluate flow (the "runtime egress detection as a metric" direction
  parked in the existential review): drive the cloud-facing surface during an evaluate run and assert no
  sealed field ever crosses. The runtime complement to the static lint.

## Why it's demonstrable (not speculative)

- **`fellows_local_db` already does this coarsely.** Its `private_data_ops` MCP server exposes only
  `list_groups` / `find_group` / `get_group_members` — `record_notes` and `record_comms_history` are
  simply **not on the surface** (`mcp_servers/private_data_ops.py`). That is hand-rolled, all-or-nothing
  minimization. `PR-7` makes it a first-class, per-field, spec-governed dimension instead of an
  implementation accident.
- **PRM already has the machinery.** PRM's plan carries per-field provenance, a user-defined custom
  schema mutable only in the workspace (INV-3), and per-field AI-*write* policies defaulting to the
  most-protective tier (INV-10), enforced structurally (FK + absent-tool). A per-field *disclosure*
  tier is the **read-side mirror** of the write-side tier PRM is already building — same column shape,
  same default, same workspace-only authorship, same structural enforcement. The marginal build is
  small relative to work already scheduled, which is why **PRM v0.2 is the natural demonstrator**
  (candidate AC id for PRM's own attestation: `AC-PRM-G`).

## How it composes with PR #32 (defense in depth)

Three layers, none load-bearing alone — the right posture when the core problem (telling a human from a
machine) is unsolvable:

1. **Architecture bounds what *can* leave** (this note: `AC-MCP-C` / `PR-7`) — `enforced` / `verifiable`.
2. **Consent gates the *act*** (PR #32's workspace-bound EX-H7) — a real but *secondary* control.
3. **Labeling keeps the word honest** (PR #32's `pna-active`, disciplined to confer nothing else).

The payoff is visible in the strength profile: the `EX-CLOUD-LLM` table that today bottoms out at
`none` gains a row — *"most-sensitive Private-DB fields cannot reach the cloud surface → `enforced`;
the user-curated shareable projection, once sent → `provider-asserted` / `none`."* The floor is new;
the honesty about what crosses above it is unchanged.

## Honest caveats (why this is a floor, not a panacea)

- **It relocates, not escapes, comprehension.** Deciding which fields are `shareable` is itself a
  consent/comprehension act. But the *default* protects the passive (and least-technical) user with no
  comprehension required — the veil-of-ignorance floor — and the active widener is the sophisticated
  user the exception path is for. The worst case ("user marks everything shareable") is merely PR #32's
  *every* case; this is never worse and usually much better.
- **Mis-tiering creates bounded false comfort.** `EX-H9`'s honest split ("sealed → `enforced`; what
  *you* shared → `provider-asserted`") is the mitigation; the toolkit already forbids a single collapsed "safe"
  claim (EX-H8). The false comfort is bounded to the chosen projection; PR #32's, with no floor, is
  unbounded.
- **It's a real build, not prose.** That is exactly why it is a follow-up gated on a demonstrating
  design rather than part of PR #32's prose-only diff.

## Sequencing

Ship PR #32 now (prose, demonstrable against the current designs). Land this data-floor with **PRM
v0.2**: add `PR-7` to the Private-schema sub-contracts, `AC-MCP-C` to the universal AC table, `EX-H9`
to the handler contract, and the `disclosure-tier` lint + self-test + dynamic probe — all in the PR
that ships the PRM design demonstrating them, per CONTRIBUTING's reference-driven model.
