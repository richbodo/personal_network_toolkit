# Positioning the Personal Network Application class among behavioral specifications

**Status:** Outline + executive summary + section-by-section skeleton (for expansion into a full draft).
**Date:** 2026-06-14.
**Type:** Working paper / pre-draft. This file is a *skeleton an expert can expand* — each section carries its key claims and citations; full prose is left to the drafting pass.
**Companion:** This is **Paper 1** of a planned pair. Paper 2 ("Generative + evaluative application-class blueprints in the AI era — a PNA case study") covers the *method* (how the toolkit is built); it is seeded by [`docs/PriorArt.md`](../PriorArt.md). The two papers share one asset: the directed graph introduced here.
**Provenance:** Synthesized from the R2 multi-agent prior-art investigation recorded in [`brainstorms/2026-06-14-pnt-direction-grill.md`](../../brainstorms/2026-06-14-pnt-direction-grill.md) (§ "R2 SYNTHESIS — the behavioral directed graph"), against the PNA spec's restructured 4-goal shape (Own the root · Integrity-by-validation · Govern egress · Survive entropy/accidents).

---

## Audience & venue framing

- **Audience.** The local-first software community + the software-engineering research community concerned with how systems specifications encode behavior and conformance.
- **Venue.** Onward!/SPLASH (the venue where the Ink&Switch local-first essay was published¹), an arXiv preprint, or a local-first community whitepaper. The framing deliberately echoes the local-first essay's "ideals → scorecard" rhetorical move, then departs from it: we replace *ideals* with a *behavior-rooted directed graph* and *aspirations* with *checked conformance*.
- **Tone (evidence-safe).** Claims are stated as **findings** of a structured prior-art survey, not as proofs. The headline positioning claim — that the personal-network root is the *highest-leverage, most underserved* corner of local-first software — is carried as a **stated wager**, explicitly falsifiable, never as settled fact. (This mirrors the spec's own "The wager" framing in [`spec/PNA_Spec.md` § Preamble](../../spec/PNA_Spec.md).)

¹ Kleppmann, Wiggins, van Hardenberg, McGranaghan, "Local-first software: you own your data, in spite of the cloud," *Onward! 2019* — https://www.inkandswitch.com/essay/local-first/ ; ACM DOI https://dl.acm.org/doi/10.1145/3359591.3359737

---

## Executive summary

Specifications "in the ballpark of local-first software" are usually compared chronologically or by feature list. This paper proposes a different lens: a **behavior-rooted directed graph**. The leaves are concrete specifications and protocols; the roots are *fundamental behaviors that many specifications share*; the edges are *derives-from* relations (an application-class spec inherits root behaviors and adds its own). Reading the field this way produces three findings.

**Finding 1 — the field clusters into four root-behavior families.** The behaviors that recur across local-first, decentralized-social, portability, security/privacy-assurance, and AI-spec-driven-development work group cleanly into four families: **(I) Substrate / data-liveness** (local-primary copy, offline read, background sync, convergence under concurrency); **(II) Sovereignty / portability / interop** (self-controlled identity, owner-decides-access, portable export, migrate-without-losing-identity, federation-via-wire-contract, public/private visibility); **(III) Assurance / protection** (least-authority, privacy-as-default, confidentiality, integrity/tamper-evidence, authenticate-before-access, accountability/auditable record, transparency/consent, threat-modeling); and **(IV) Machine-followable spec & verification** (typed-contract-as-behavior, behavior-as-executable-test, conformance-checked-by-code-not-prose, capability negotiation, code-enforced runtime guards, priority-ordered policy, cross-artifact consistency, layered derive-and-extend). Most named specifications live predominantly in **one** family.

**Finding 2 — privacy, sovereignty, and durability are *additive*, not *inherited* from local-first.** The strongest empirical result of the survey: the canonical local-first manifesto lists ownership, longevity, and privacy among its ideals,¹ but the mainstream *sync engines* people actually build on do not enforce them — those properties are present in manifesto *language* and absent from engine *contracts*. They originate in Families II and III, not Family I. Any application that wants them must **layer them on**; it does not get them for free by being "local-first."

**Finding 3 — the PNA spec is the only surveyed node composing roots from all four families.** Where local-first apps sit in Family I, decentralized-social protocols in II (+ some III), assurance frameworks in III (+ IV's conformance model), and AI-SDD tooling in IV, the **Personal Network Application** spec draws roots from **I × II × III × IV** and then adds personal-network-root-specific leaf behaviors: the **two-store contact-vs-relationship privilege split**, **governed egress of relationship data**, the **Exception + countermeasure ("Harden")** model, and the **personal-network-root domain** itself. On the orthogonal *conformance-model* axis it sits in the **checked / validated** cluster (W3C QA, OWASP ASVS/MASVS, ISO-27560-style receipts) and explicitly **rejects the certified / awarded pole** (Common Criteria, FedRAMP).

**The wager (stated, not proven).** If privacy/sovereignty/durability are additive rather than inherited (Finding 2), then the cross-family composite a PNA requires (Finding 3) is *expensive* to assemble and therefore *rarely assembled* — leaving the personal-network root the highest-leverage, least-served corner of local-first software. We present this as the bet the PNA spec exists to be tested against, with explicit falsification conditions.

**Contribution.** (a) A reusable, goal-agnostic, behavior-rooted directed-graph method for positioning systems specs; (b) the four-family taxonomy and its deepest convergent roots; (c) the "additive-not-inherited" finding with evidence; (d) the placement of the PNA class as a cross-family composite; (e) the conformance-model sub-axis that distinguishes *checked* from *awarded* conformance.

---

## Paper outline (at a glance)

1. Introduction — the positioning problem; why chronology and feature-lists mislead
2. Method — the behavior-rooted directed graph (roots → families → derived app-class nodes → leaves)
3. The four root-behavior families (I substrate · II sovereignty · III assurance · IV machine-followable)
4. The conformance-model sub-axis — checked/validated vs certified/awarded
5. Application-class nodes and the roots they compose (the surveyed leaves)
6. The PNA node — the cross-family composite + its own leaf additions
7. Findings & the wager — additive-not-inherited; highest-leverage-underserved (stated bet)
8. Threats to validity & falsification conditions
9. Related work, limitations, future work
10. Conclusion
- Appendix A — the directed graph (node/edge tables)
- Appendix B — annotated citation map by family

---

## Section-by-section skeleton

### 1. Introduction — the positioning problem

**Purpose.** Motivate a behavior-rooted graph as the right lens for situating the PNA class.

**Key claims.**
- The local-first essay¹ reframed a field around *ideals* and scored implementations against them (Fast, Multi-device, Offline, Collaboration, Longevity, Privacy, User-control). That move is the model we build on — and the thing we critique: ideals are aspirational, not conformance-bearing.
- Two common positioning lenses fail for this question. **Chronology** (who published when) hides shared structure; **feature checklists** flatten *derivation* (which behavior is foundational vs. which is an app-class addition).
- We instead ask, per behavior: *is this a root (shared by many specs) or a leaf (an app-class's own addition)?* — yielding a directed graph whose edges are *derives-from*.
- The method is **goal-agnostic**: roots are identified from what specs actually mandate, independent of the PNA's goals, so the PNA's eventual placement is a *result*, not an assumption. (Method discipline drawn from the R2 investigation.)

**Citations.** Ink&Switch local-first essay (https://www.inkandswitch.com/essay/local-first/, ACM https://dl.acm.org/doi/10.1145/3359591.3359737); Wikipedia "Local-first software" for the canonical 7-ideals list (https://en.wikipedia.org/wiki/Local-first_software); Tonsky, "Local, First, Forever" as a contrasting community articulation (https://tonsky.me/blog/crdt-filesync/).

---

### 2. Method — the behavior-rooted directed graph

**Purpose.** Define the construction precisely so the result is reproducible and the placement claims are checkable.

**Key claims / definitions.**
- **Node types.** *Root behavior* (a mandated behavior recurring across ≥2 specs); *application-class spec node* (e.g., local-first apps, the PNA spec); *leaf behavior* (an app-class's own addition); plus an *above-the-roots "why" layer* of external mandates (GDPR Art. 20, DMA Art. 6(9)) and aspirational manifestos (the 7 ideals) that motivate but do not themselves specify checkable behavior.
- **Edge = derives-from.** An app-class node inherits a root and may *specialize* it; leaves hang off the node.
- **Root admission test.** A behavior is a *root* only if it is **specified** (mandated/checkable) in ≥2 surveyed specs — not merely aspired to. This test is what produces Finding 2: ownership/privacy/longevity fail the test inside Family I's engines and pass it inside Families II/III.
- **Branch points vs roots.** Where specs *contradict* each other on a behavior, it is a **branch point**, not a root (e.g., conflict-resolution: CRDT-convergent vs. server-authoritative/LWW; offline-*write* contested). This keeps the roots low-contradiction.
- **Method lineage.** The "specified = checkable, not asserted" admission test is the same discipline the AI-era spec-driven-development field is converging on (a behavior is only *specified* if conformance is checked by code) — see § 4 and Family IV.

**Citations.** GDPR Art. 20 right to data portability (https://gdprhub.eu/Article_20_GDPR); Data Transfer Initiative on DMA Art. 6(9) ↔ GDPR Art. 20 (https://dtinit.org/blog/2025/12/02/dma-gdpr-joint-guidelines); arXiv "Spec-Driven Development…" 2602.00180 for the executable-spec-vs-prose distinction (https://arxiv.org/abs/2602.00180).

---

### 3. The four root-behavior families

**Purpose.** Present the taxonomy — the paper's backbone.

#### Family I — Substrate / data-liveness
- **Roots:** local-primary copy · offline-read · background-sync · convergence-under-concurrency.
- **Branch points (not roots):** conflict-resolution (CRDT-convergent vs. server-authoritative/LWW); offline-*write* (contested — some sync engines decline it).
- **Key claim:** Family I is where local-first manifestos and sync engines *agree*; it is also where they *stop* — the family does **not** include ownership, privacy, or longevity as checkable behaviors (set up here, paid off in § 7 Finding 2).
- **Citations:** CRDTs — https://crdt.tech/ ; Automerge — https://automerge.org/ ; Yjs — https://yjs.dev/ (GitHub https://github.com/yjs/yjs); Kleppmann et al. on CRDTs as local-first substrate (essay, above); Tonsky "Local, First, Forever" (file-sync substrate, https://tonsky.me/blog/crdt-filesync/).

#### Family II — Sovereignty / portability / interop
- **Roots:** host-independent self-controlled identity · data-ownership / owner-decides-access · portable machine-readable export · migrate-without-losing-identity · federation-via-wire-contract · public/private-visibility distinction.
- **Key claim:** This family is where *ownership* and *portability* become **specified** (not just aspired) — in decentralized-social/identity protocols and in portability law/frameworks.
- **Citations:** Solid (https://solidproject.org/TR/protocol ; repo https://github.com/solid/specification); AT Protocol (https://atproto.com/ ; Kleppmann et al., "Bluesky and the AT Protocol," arXiv 2402.03239, https://arxiv.org/abs/2402.03239); Nostr (https://github.com/nostr-protocol/nips); Matrix spec (https://spec.matrix.org/ ; repo https://github.com/matrix-org/matrix-spec); ActivityPub W3C Rec (https://www.w3.org/TR/activitypub/); W3C DIDs v1.1 (https://www.w3.org/TR/did-1.1/); W3C Verifiable Credentials Data Model v2.0 (https://www.w3.org/TR/vc-data-model-2.0/); Data Transfer Initiative / Data Transfer Project (https://dtinit.org/); GDPR Art. 20 (https://gdprhub.eu/Article_20_GDPR).

#### Family III — Assurance / protection
- **Roots:** least-authority / explicit-grant · privacy-as-default · confidentiality · integrity / sign-on-write / tamper-evidence · authenticate-before-access · accountability / auditable record (consent receipt) · transparency / informed-consent · threat-modeling.
- **Key claim:** This family is where *protection* is **specified as requirements and verification obligations** — and it carries its own *conformance-model* sub-axis (§ 4).
- **Citations:** OWASP ASVS (https://owasp.org/www-project-application-security-verification-standard/); OWASP MASVS (https://mas.owasp.org/MASVS/); NIST Cybersecurity Framework 2.0 (https://www.nist.gov/cyberframework); NIST Privacy Framework (https://www.nist.gov/privacy-framework); LINDDUN privacy threat modeling (https://linddun.org/); object-capability model (https://en.wikipedia.org/wiki/Object-capability_model ; foundational treatment: Miller, "Robust Composition," 2006); ISO/IEC TS 27560:2023 consent records/receipts (W3C DPV implementation guide https://w3c.github.io/dpv/guides/consent-27560 ; arXiv 2405.04528 https://arxiv.org/abs/2405.04528).

#### Family IV — Machine-followable spec & verification
- **Roots:** typed-contract-as-behavior · behavior-as-executable-test · **conformance-checked-by-code-not-prose** · discovery / capability-negotiation · code-enforced runtime guards (least-priv + human-in-loop) · priority-ordered policy (constitution) · cross-artifact consistency · layered derive-and-extend.
- **Key claim:** The whole AI-spec-driven-dev field is independently converging on the thesis that *a behavior is only specified if its conformance is checked by code* — the same discipline the PNA toolkit encodes ("convert an absent guarantee into a red test"). This is strong external validation of the method in § 2.
- **Citations:** Model Context Protocol (https://modelcontextprotocol.io/ ; spec repo https://github.com/modelcontextprotocol/modelcontextprotocol ; Anthropic announcement https://www.anthropic.com/news/model-context-protocol); BDD/Gherkin/Cucumber executable specifications (https://cucumber.io/docs/bdd/ ; https://cucumber.io/docs/gherkin/); GitHub Spec Kit + `constitution.md` (https://github.com/github/spec-kit ; https://github.com/github/spec-kit/blob/main/spec-driven.md); arXiv "Spec-Driven Development…" 2602.00180 (https://arxiv.org/abs/2602.00180).

#### Deepest convergent roots (appear in ≥2 families)
- data-ownership / owner-decides (I+II+III) · crypto-integrity / sign-on-write (I+II+III) · confidentiality / sealed-by-default (I+II+III) · least-authority / access-control (II+III) · authenticate-before-access (II+III) · portability / export (I+II) · human-in-the-loop / consent / user-initiated (II+III+IV) · conformance-checked-by-code (III+IV).
- **Key claim:** These convergent roots are the spine an ambitious app-class spec must touch; the count and spread foreshadow why a *cross-family composite* is rare.

---

### 4. The conformance-model sub-axis — checked vs awarded

**Purpose.** Introduce the orthogonal axis on which the toolkit-as-blueprint takes a position, separate from *which behaviors* a spec mandates.

**Key claims.**
- Conformance models split into two poles: **checked / validated** — published, machine-runnable criteria anyone can apply, no gatekeeper, "checked not awarded" — vs. **certified / awarded** — an accredited human/body confers a credential.
- **Checked cluster:** W3C QA Framework (Specification/Operational/Test Guidelines — conformance is something a spec *defines so anyone can test*); OWASP ASVS/MASVS (a verification standard you run); ISO/IEC TS 27560-style consent **receipts** (machine-readable evidence, not a stamp).
- **Awarded pole (explicitly rejected by the PNA toolkit):** Common Criteria Protection Profiles / ISO 15408 (an evaluation lab issues a certificate); FedRAMP-style authorization (an authority grants ATO). NIST CSF/Privacy Framework corroborate the anti-certification stance (frameworks, not certifications).
- **Adjacent-but-distinct:** OpenSSF-style *badges* — keep the published-criteria-and-linkable-evidence half, drop the badge/award.
- **Placement claim:** The toolkit sits firmly in the **checked** cluster. It borrowed Common Criteria's *structure* (a Protection-Profile-like class document) while dropping its *authority* (no certifying body). (This is the bridge to Paper 2.)

**Citations.** W3C QA Framework: Specification Guidelines (https://www.w3.org/TR/qaframe-spec/), Operational Guidelines (https://www.w3.org/TR/qaframe-ops/), Test Guidelines (https://www.w3.org/TR/2003/WD-qaframe-test-20030516/); OWASP ASVS (https://owasp.org/www-project-application-security-verification-standard/); Common Criteria Protection Profile / ISO 15408 (https://en.wikipedia.org/wiki/Protection_Profile ; https://www.commoncriteriaportal.org/); ISO/IEC TS 27560 (https://w3c.github.io/dpv/guides/consent-27560); NIST CSF (https://www.nist.gov/cyberframework).

---

### 5. Application-class nodes and the roots they compose

**Purpose.** Lay down the leaves (the surveyed specs) and which family each predominantly draws from — the comparison set against which the PNA is positioned.

**Key claim (one table; most nodes are single-family).**

| App-class node | Roots composed (predominant) | Conformance model |
|---|---|---|
| Local-first apps (manifesto) | I; *aspires* to II-ownership/privacy (not enforced) | aspirational scorecard¹ |
| CRDT / sync engines (Automerge, Yjs, …) | I; split on conflict-resolution (branch point) | engine test suites (checked) |
| Decentralized social / identity (Solid, AT Proto, Nostr, Matrix, ActivityPub, DIDs, VCs) | II + III (auth/access/integrity) | mixed; W3C TR-style for the W3C ones |
| Portability frameworks (DTP, GDPR Art. 20, DMA Art. 6(9)) | II (export/migrate) + the "why" layer | legal/compliance |
| Security/privacy assurance (CC-PP, ASVS/MASVS, NIST CSF/PF, LINDDUN, ocap, ISO-27560) | III + IV (conformance model) | spans BOTH poles (the § 4 split lives here) |
| AI spec-driven-dev (MCP, BDD/Gherkin, Spec Kit, eval-driven) | IV | checked (executable) |

- **Key claim:** Reading down the table, *each row is anchored in one family* (with at most a secondary). No surveyed row spans three families, let alone four. This is the empirical setup for § 6.

**Citations:** as enumerated per family in § 3 and § 4.

---

### 6. The PNA node — the cross-family composite

**Purpose.** State the central positioning result and decompose it.

**Key claims.**
- **The PNA spec draws roots from all four families:**
  - From **I:** local-primary copy (the local Shared/Private store the workspace reads offline).
  - From **II:** ownership / owner-decides + portable export — but **not** federation (v0.1 PNAs sit *downstream* of SaaS systems of record).
  - From **III:** privacy-as-default + least-authority + confidentiality + consent + threat-modeling.
  - From **IV:** typed contracts + checked-by-code + **checked-not-awarded** + human-in-the-loop *enforced at the boundary* + layered derive-and-extend (Goals → Constraints → ACs → contracts).
- **The PNA's own leaf additions (its contribution beyond the roots):**
  1. the two-store **contact-vs-relationship privilege split** (shared/mirrored vs. private/sovereign);
  2. **governed egress of relationship data** (the user chooses the channel, sees the payload, is never forced onto a content-reading transport; LLM/MCP calls treated as transports);
  3. the **Exception + countermeasure / "Harden"** model (honest relaxation of a constraint, with a hazard/environment-keyed catalog of mitigations);
  4. the **personal-network-root** domain itself (contacts + the private relationship memory layered on them).
- **Map to the spec's four goals** (so reviewers can trace the graph onto the artifact): Own & build the root (I+II) · Integrity-by-validation (IV) · Protect from egress (II+III) · Survive entropy & accidents (I + durability from II/III). See [`spec/PNA_Spec.md`](../../spec/PNA_Spec.md) and [`spec/axes.md`](../../spec/axes.md).
- **Why this matters:** PNA's value is not inventing new roots; it is **specializing assurance + sovereignty roots to the personal-network root *and* making them machine-checkable (IV) for an AI builder** — which is exactly the composite no surveyed node had assembled.

**Citations:** the PNA spec itself ([`spec/PNA_Spec.md`](../../spec/PNA_Spec.md), [`spec/axes.md`](../../spec/axes.md), [`docs/PriorArt.md`](../PriorArt.md)); plus the per-family roots cited in § 3.

---

### 7. Findings & the wager

**Purpose.** State the three findings crisply, then the wager with falsification conditions.

**Key claims.**
- **Finding 1 (taxonomy).** Behaviors cluster into four families; most specs are single-family. (From § 3, § 5.)
- **Finding 2 (additive-not-inherited) — the empirical centerpiece.** Ownership, longevity/durability, and privacy are present in local-first manifesto *language* but **absent from mainstream sync-engine contracts**; they are roots of Families II/III, not Family I. Therefore a local-first app does **not** inherit them — it must add them. Evidence: contrast the 7 ideals¹ (privacy = "E2E encryption," longevity, user-control) against what sync engines actually mandate (convergence, offline read; engines such as the Rocicorp/Zero line explicitly *decline* CRDT-style offline collaborative writes — a contract boundary, not an oversight). Verifiability/decentralization show up only in the P2P branch (Hypercore/Fireproof/DXOS-style), not the SQL-sync branch — i.e., app-class additions, not roots.
- **Finding 3 (composite).** The PNA node is the only surveyed node at I × II × III × IV (§ 6).
- **The wager (stated, falsifiable — not a proven claim).** *Because* privacy/sovereignty/durability are additive (Finding 2), assembling the cross-family composite (Finding 3) is costly and therefore rare; this is *why* we bet the personal-network root is the highest-leverage, least-served corner of local-first software. **Falsification conditions** (make the bet honest): the wager is wrong if (a) a mainstream local-first stack ships these properties as *enforced contracts* rather than aspirations; or (b) an existing app-class spec is shown to already compose all four families for the personal-network (or an adjacent personal-data) root; or (c) user demand for a sovereign personal-network root proves thin where the tooling exists. We invite the community to attack each.

**Citations:** Ink&Switch essay (7 ideals); CRDT/sync-engine sources (§ 3 Family I); the survey record in [`brainstorms/2026-06-14-pnt-direction-grill.md`](../../brainstorms/2026-06-14-pnt-direction-grill.md).

---

### 8. Threats to validity & falsification conditions

**Purpose.** Pre-empt the obvious objections; keep the tone evidence-safe.

**Key claims.**
- **Survey/selection bias.** The comparison set was assembled by a structured multi-agent survey; it is broad but not exhaustive. Adjacent fields (decentralized storage à la IPFS, secure-messaging-protocol assurance, data-spaces/Gaia-X) are under-sampled and could shift family boundaries.
- **Root-vs-branch judgment calls.** Some behaviors (offline-*write*) sit near the root/branch line; reasonable readers may reclassify. The admission test (≥2 specs mandate it, low contradiction) is stated so disagreements are about *evidence*, not taste.
- **"Predominant family" is a simplification.** Several real specs straddle families; the table reports the center of mass, and the graph (Appendix A) records the secondary edges.
- **The wager is a wager.** Repeat: Finding 3 (composite) is structural and checkable; the *leverage/underserved* claim is a bet with the falsification conditions in § 7.
- **Construct risk.** "Specified" is doing heavy lifting in Finding 2; we anchor it to checkable conformance (Family IV's own criterion) to avoid circularity.

---

### 9. Related work, limitations, future work

**Key claims.**
- **Related work.** The local-first essay¹ (ideals lens we extend); W3C QA's conformance methodology (the "define so anyone can test" stance); SPL/feature-modeling and Common Criteria PP authoring as *method* lineage — but those belong to **Paper 2**; here we cite them only to disambiguate scope.
- **Limitations.** v0.1 PNAs are downstream-of-SaaS (no Family-II federation yet); the graph captures *specified* behavior, not *deployed* behavior; durability claims run into platform Constraints (browser substrate ceilings) the spec handles via its Constraints/Exceptions duals.
- **Future work.** Promote the graph to a maintained artifact; add the under-sampled fields; quantify the "additive cost" of Finding 2 (e.g., count the contracts a sync engine would need to add to enforce the ideals); test the wager against a real PNA's adoption.

**Citations.** Paper 2 seed ([`docs/PriorArt.md`](../PriorArt.md), [`docs/PriorArtReferences.md`](../PriorArtReferences.md)); W3C QA (§ 4); arXiv 2602.00180.

---

### 10. Conclusion

**Key claims (restate, tightly).**
- A behavior-rooted directed graph is a more honest positioning instrument than chronology or feature-lists.
- The field's behaviors fall into four families; most specs are single-family.
- Privacy, sovereignty, and durability are **additive**, not inherited from local-first — the survey's strongest finding.
- The PNA spec is the lone surveyed node composing all four families, plus personal-network-root leaves; on conformance it is *checked, not awarded*.
- The leverage/underserved claim stands as a **wager** with explicit falsification conditions — an invitation to the community, not a verdict.

---

## Appendix A — the directed graph (node/edge tables to build out)

*To be rendered as a figure + backing tables in the full draft. Skeleton:*

- **Above-the-roots ("why") layer:** GDPR Art. 20 · DMA Art. 6(9) · Ink&Switch 7 ideals (aspirational).
- **Root families (nodes):** I {local-primary, offline-read, background-sync, convergence} · II {self-controlled-identity, owner-decides-access, portable-export, migrate-without-losing-identity, federation-via-wire-contract, public/private-visibility} · III {least-authority, privacy-as-default, confidentiality, integrity/tamper-evidence, authenticate-before-access, accountability/receipt, transparency/consent, threat-modeling} · IV {typed-contract-as-behavior, behavior-as-test, checked-by-code, capability-negotiation, runtime-guards, priority-ordered-policy, cross-artifact-consistency, layered-derive-and-extend}.
- **Branch points (not roots):** conflict-resolution (CRDT vs server-authoritative/LWW) · offline-write.
- **Conformance sub-axis (orthogonal):** checked/validated {W3C QA, ASVS/MASVS, ISO-27560} —|— certified/awarded {CC-PP/ISO-15408, FedRAMP}.
- **App-class nodes → edges to roots:** (fill from § 5 table).
- **PNA node → edges:** I.local-primary, II.{ownership, export}, III.{privacy-default, least-authority, confidentiality, consent, threat-model}, IV.{typed-contracts, checked-by-code, checked-not-awarded, human-in-loop-enforced, layered-derive-and-extend}; **leaves:** contact-vs-relationship split, governed-egress, Exception+Harden, personal-network-root.

---

## Appendix B — annotated citation map (verified URLs)

*All URLs web-verified 2026-06-14.*

**Local-first / substrate (Family I)**
- Kleppmann, Wiggins, van Hardenberg, McGranaghan, "Local-first software," Onward! 2019 — https://www.inkandswitch.com/essay/local-first/ · ACM https://dl.acm.org/doi/10.1145/3359591.3359737 · PDF https://www.inkandswitch.com/essay/local-first/local-first.pdf
- "Local-first software" (canonical 7-ideals summary) — https://en.wikipedia.org/wiki/Local-first_software
- Tonsky, "Local, First, Forever" — https://tonsky.me/blog/crdt-filesync/
- CRDT.tech — https://crdt.tech/ · implementations https://crdt.tech/implementations
- Automerge — https://automerge.org/ · Yjs — https://yjs.dev/ (https://github.com/yjs/yjs)

**Sovereignty / portability / interop (Family II)**
- Solid — https://solidproject.org/TR/protocol · https://github.com/solid/specification
- AT Protocol — https://atproto.com/ · Kleppmann et al., "Bluesky and the AT Protocol," arXiv 2402.03239 — https://arxiv.org/abs/2402.03239
- Nostr (NIPs) — https://github.com/nostr-protocol/nips
- Matrix spec — https://spec.matrix.org/ · https://github.com/matrix-org/matrix-spec
- ActivityPub (W3C Rec) — https://www.w3.org/TR/activitypub/
- W3C DIDs v1.1 — https://www.w3.org/TR/did-1.1/
- W3C Verifiable Credentials Data Model v2.0 — https://www.w3.org/TR/vc-data-model-2.0/
- Data Transfer Initiative (Data Transfer Project) — https://dtinit.org/
- GDPR Art. 20 — https://gdprhub.eu/Article_20_GDPR · DMA↔GDPR — https://dtinit.org/blog/2025/12/02/dma-gdpr-joint-guidelines

**Assurance / protection (Family III)**
- OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
- OWASP MASVS — https://mas.owasp.org/MASVS/
- NIST Cybersecurity Framework 2.0 — https://www.nist.gov/cyberframework
- NIST Privacy Framework — https://www.nist.gov/privacy-framework
- LINDDUN — https://linddun.org/
- Object-capability model — https://en.wikipedia.org/wiki/Object-capability_model (Miller, "Robust Composition," 2006)
- ISO/IEC TS 27560:2023 consent records/receipts — https://w3c.github.io/dpv/guides/consent-27560 · arXiv 2405.04528 https://arxiv.org/abs/2405.04528

**Machine-followable spec & verification (Family IV)**
- Model Context Protocol — https://modelcontextprotocol.io/ · spec https://github.com/modelcontextprotocol/modelcontextprotocol · announcement https://www.anthropic.com/news/model-context-protocol
- BDD / Cucumber / Gherkin — https://cucumber.io/docs/bdd/ · https://cucumber.io/docs/gherkin/
- GitHub Spec Kit — https://github.com/github/spec-kit · https://github.com/github/spec-kit/blob/main/spec-driven.md
- arXiv 2602.00180, "Spec-Driven Development: From Code to Contract…" — https://arxiv.org/abs/2602.00180

**Conformance model (the checked-vs-awarded sub-axis)**
- W3C QA Framework — Specification Guidelines https://www.w3.org/TR/qaframe-spec/ · Operational Guidelines https://www.w3.org/TR/qaframe-ops/ · Test Guidelines https://www.w3.org/TR/2003/WD-qaframe-test-20030516/
- Common Criteria Protection Profile / ISO 15408 — https://en.wikipedia.org/wiki/Protection_Profile · https://www.commoncriteriaportal.org/

**PNA spec & internal companions**
- PNA spec — [`spec/PNA_Spec.md`](../../spec/PNA_Spec.md) · axes — [`spec/axes.md`](../../spec/axes.md)
- Prior-art survey (Paper 2 seed) — [`docs/PriorArt.md`](../PriorArt.md) · [`docs/PriorArtReferences.md`](../PriorArtReferences.md)
- Source synthesis — [`brainstorms/2026-06-14-pnt-direction-grill.md`](../../brainstorms/2026-06-14-pnt-direction-grill.md)

---

*Skeleton ends. Expansion notes for the drafter: (1) build Appendix A into a real figure; (2) for Finding 2, add a side-by-side table of "ideal vs. enforced-by-engine?" with per-engine citations; (3) confirm each W3C/ISO URL resolves to the version you cite at submission time; (4) keep every leverage/underserved sentence flagged as a wager.*
