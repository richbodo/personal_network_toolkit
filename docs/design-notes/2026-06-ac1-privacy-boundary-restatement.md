# AC-1 restated: "Sovereign, sealed private layer" — the two-store split is a realization, not the commitment

*2026-06-27. A spec change to the wording (not the meaning) of the unit-of-conformance AC-1,
plus a recategorization of the two-store split from commitment to canonical realization. Routed as
a **clarification** (it imposes no new obligation; both reference designs stay conformant unchanged) —
the lighter [toolkit-fix lane](../../pna-toolkit/SKILL.md), not a reference-design contribution — with the
single-store path it opens left explicitly **demonstrator-gated**. Surfaced by the Signal Desktop
evaluation; it also completes a seed already in the
[2026-06-14 direction grill](../../brainstorms/2026-06-14-pnt-direction-grill.md) ("Goals were mis-designed
— mechanism mistaken for goal; 'two databases' is a mechanism, the concept is privilege separation").*

## The problem

AC-1's old wording — **"Two-store ownership split. … The two stores MUST occupy separate storage
namespaces with separate privacy postures"** — bundled a goal-entailed commitment together with one
*mechanism* for delivering it. Held to the spec's own [Layer-1 dividing test](../../spec/PNA_Spec.md#how-the-pieces-fit-together)
("a statement belongs to Layer 1 iff it survives a total technology swap"; and Rule 1: "a commitment that
names a [structure] is mis-filed — its technology-independent core is the AC, its stack-specific form is a
realization"), AC-1 carried **four claims**, only three of which survive the swap:

| Claim inside old AC-1 | Goal-entailed? (survives the swap) | Layer |
|---|---|---|
| (i) **Classification** — data divides into *shared* (externally mirrored, replaceable) vs *private* (locally created, sovereign) | Yes — Goal 3's "private layer sealed by default" is meaningless without "which data is private" | **L1 (required)** |
| (ii) **Private sovereignty** — private data is locally owned, user-writable, device is sole authority | Yes — this *is* Goal 1 + the Goal 3 seal restated as a checkable property | **L1 (required)** |
| (iii) **Enforced boundary** — the classes carry distinct privacy postures, enforced at the data layer (a shared-class accessor cannot reach private; not UI-only) | Yes — a nominal/bypassable boundary seals nothing | **L1 (required)** |
| (iv) **"two stores … separate storage namespaces"** | **No** — the same boundary is expressible with one store + per-row/-field class + data-layer enforcement | **L2 (a realization, mis-filed as a commitment)** |

So the two-store split is **sufficient and canonical, not necessary.** (i)–(iii) are forced by the Goals;
the *number of physical stores* that delivers them is not. The vocabulary the critique reached for is the
right one: **privacy posture** = (ii); **privilege separation** = (iii); the split = (iv) one realization of
both. This is the "required vs. opinionated" test the spec asks of every commitment, finally applied to AC-1.

## The restatement

**Name:** "Two-store ownership split" → **"Sovereign, sealed private layer."** The name should be the
property, not the mechanism. The Layer-1 commitment is (i)–(iii); the two-store split moves to **canonical
realization**, and a single-store realization is admitted in principle. The normative drop-in is the new
AC-1 row in [`spec/PNA_Spec.md` § Universal architectural commitments](../../spec/PNA_Spec.md#ac-1).

**What stays mandatory (and why it isn't opinion):** classification, private sovereignty, and a
data-layer-enforced boundary are each *entailed by the Goals* — you cannot have "the private layer is sealed
by default" without a notion of which data is private and an enforcement that actually holds. Mandatory only
to the degree the Goal forces; the swap test is exactly the line.

**What was deliberately NOT added:** "legibility" (the Preamble's "reason about where your data lives") was
*not* promoted to a top-level MUST, to keep this a true clarification with no new obligation on existing
designs. It stays a property the canonical realization gives for free and the single-store path must attend
to. AC-1 was also kept as **one** two-goal cross-cut (not split into a Goal-1 half and a Goal-3 half) — that
matches the spec's existing cardinality design; splitting is a future option only if the evaluate flow ever
needs to score ownership and sealing on separate axes.

## The cost of loosening — and why the single-store path stays demonstrator-gated

The two-store split was not arbitrary. It is **privilege separation by construction**: "are there two
namespaces?" a lint or a 30-second read can verify, where "is private unreachable from every shared-class
accessor?" needs whole-program judgment — exactly the verification the toolkit pushes to its LLM/human
tiers. The five-server MCP architecture leans on it directly: the Shared Data Ops server is "cloud-safe"
*because it physically cannot see private rows* (AC-MCP-A). Allow a single store and that guarantee rests on
in-process query filtering — weaker, and easy to get subtly wrong.

So the loosening **moves the burden from structure to enforcement**, and the honest move — the same one the
spec already uses for native-sqlcipher's deferred key-management ACs ("land when a reference design
demonstrates them") — is:

- **The reframing lands now as a clarifying edit.** It imposes no new obligation: both reference designs use
  the canonical split, which trivially satisfies (i)–(iii); nothing must change to stay conformant; no tool
  breaks (the lints key on the `AC-1` ID, not the bold name).
- **The single-store path stays "admissible in principle, not yet demonstrated."** It becomes a *blessed*
  route when a real single-store PNA demonstrates the enforced classification — including the **negative test
  that pins privilege separation**: a shared-class accessor (or a raw MCP/console handle) provably *cannot*
  read a private row. That negative test is what the split gives for free and what a single-store design must
  buy explicitly. The door is open and honest, without pretending a path is proven that no design has walked.

## Worked example — the restatement reads Signal *better*, not just looser

The Signal Desktop evaluation ([`../../Signal-Desktop/evaluate-report.json`](../../Signal-Desktop/evaluate-report.json),
2026-06-27) is what surfaced this. Under old AC-1 the verdict was the blunt "no two stores → non-conformant."
A naive loosening ("does it let me own my data? yes → pass") would be too generous. The restatement
discriminates — it separates the two facets AC-1 was fusing:

- **Ownership / sovereignty (ii): substantially met.** Signal doesn't *block* local custody — encrypted local
  store, local + exportable backups, the device holds your copy.
- **Sealed-by-default (iii, the Goal-3 facet): not met — and not because of store count.** Signal's
  relationship layer leaks by design: contact notes/nicknames sync to `storage.signal.org` and back to the
  phone (`ts/services/storageRecordOps.preload.ts:337-344`), and graph/metadata sync in the background, not
  by explicit user action.

So the restatement relocates the real finding from "wrong structure" to "unsealed relationship layer +
SaaS-backed" — the genuine PNA-definition tension, stated precisely instead of via a proxy. It convicts
Signal of the right thing rather than acquitting it. That gain in *discrimination* is the strongest argument
the restatement is correct, not merely permissive.

## Ripple / rename audit (what this change touched, and what it deliberately left)

**Reworded** (the split as *commitment* → the property, with the split named as canonical realization):
the AC-1 row; the Goal 1 and Goal 3 constraint lists; the Goal↔AC cardinality note; the required-slots and
Storage-slot descriptions; the "Shared DB / Private DB" and MCP-server vocabulary; the Preamble's
"earning complexity" first-move; AC-MCP-A's "cloud-safe" wording (now: the separation is structural under the
split and MUST be data-layer-enforced under a single store); `spec/axes.md`'s MCP-exposure distinction; the
Architecture template's AC-1 label; `docs/conformance-scope-and-lifecycle.md`; and `tools/validate.py`'s AC-1
requirement string.

**Deliberately left unchanged** (and why):
- **The two-store machinery** — the `contracts/*.sql` schemas, the slot sub-contracts (ST-4 "two-database
  management", the `SH-`/`PR-` schema contracts), the `Realizes: AC-1` headers. These are Layer-2 and *are*
  the canonical realization; the reframe doesn't disturb them.
- **The bundled design attestations + the generated realization index + the sample reports.** Both designs
  attest AC-1 via the two-store split, which remains canonical — their attestations stay valid, and a sample
  report saying "the two-store split holds" is still accurate. The realization index is regenerated from the
  designs' (pinned) tables, so it correctly keeps the label the designs use.
- **The papers / PriorArt history.** They already frame it as a "contact-vs-relationship privilege split" and
  record the goal-vs-mechanism history; no normative weight, left as-is.

## Status & version

`/VERSION` stays `0.2.0`. This is a clarifying restatement that changes no existing design's obligations
(precedent: the RZ-relabel "clarity only — no bump" Unreleased entry). The single-store path it opens is
marked *not yet demonstrated*, so no new checkable capability is added today; **a future single-store
demonstrator is the additive event that would merit a minor bump** and would carry the negative-test
discipline above. `just ci` green.
