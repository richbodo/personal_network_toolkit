# PNA Spec

<!-- EDITING NOTE — machine-parsed tables: the ID-bearing tables in this file (the architectural-commitment tables) are read by tools/lint-spec-ids.py AND by external report writers (reference-design conformance reports), and their `<a id>` row anchors are deep-linked from those reports. Treat each such table's columns, headers, and IDs as an API: if you change one, update those consumers — and the lint's self-tests (tools/tests/lint_selftest.py) — in the same change. The lint finds columns by header name, so the ID may sit in any column; it currently lives in the last column. -->

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This document is the universal specification for personal network applications (PNAs). Reference designs declare conformance to a specific Toolkit-Version and to a specific application flavor (defined by a constellation of feature axis picks). A PNA conforms to this spec if it satisfies the universal architectural commitments and the axis-derived contracts for each of its declared axis picks, listed herein.  Each reference design's specialization lives in its own repo (ex: fellows_local_db's specialization is at [`docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md)).

---

## Preamble

This specification does not build an application. It defines what an application must *prove* to be trusted with your personal network.

It is written to be **machine-followable**. As people increasingly compose software by prompting AI agents, the spec — not the codebase — becomes the durable artifact, and a behavior counts as *specified* only when its conformance can be **checked** (by a typed contract, a lint, or an evaluator), never merely asserted in prose. The PNA is the first worked instance of a general method — a *generative + evaluative application-class blueprint* (see [`docs/PriorArt.md`](../docs/PriorArt.md)).

A **[personal network](#vocab-personal-network)** is the egocentric graph of the people you are connected to — you at the center — together with the private memory that decorates those connections: who they are, how you know them, what you've said, who you'd call. A **[personal network application (PNA)](#vocab-pna)** brings that graph onto the user's own device, under the user's own control, and makes architecturally enforced promises about how it is kept and used. This spec is the set of those promises; a PNA conforms when an agent or a reviewer can check that it keeps them.

**Why now.** Two shifts are arriving together. Data still flows into SaaS, but trust flows out: users are increasingly unwilling to let a vendor hold who they talk to about politics, health, or money. At the same time, edge compute and AI agents able to do serious work locally are arriving fast. The first shift creates demand for software that keeps a personal network sovereign; the second makes it practical to build, run, and recompose at the user's own pace. And as OS-level AI agents become the way people operate their devices, the question stops being *whether* software will act over your relationships and becomes *where* it does so — inside a vendor's cloud, or on a sovereign local layer an AI works over only with your consent. A PNA is the latter.

**The wager.** We hold that the personal-network root — your contacts and the private memory layered on them — is the highest-leverage, least-served place in local-first software: the field has concentrated on sync, storage, and conflict resolution, while the everyday problem of *keeping, finding, and reaching the people who matter* has gone largely unaddressed. That is a bet this spec exists to be tested against, not a settled fact.

**What a PNA holds.** A PNA separates two kinds of data (full definitions in [§ Vocabulary](#vocabulary)): **[contact data](#vocab-contact-data)** — the shared, externally-mirrored facts about a person (name, email, organization), local-first and replaceable — and **[relationship data](#vocab-relationship-data)** — the private memory the user creates over those contacts (notes, tags, groups, communication history), sovereign and protected. The architectural promise is the bright line between them: [shared data](#vocab-shared-data) is mirrored and disposable; [private data](#vocab-private-data) never leaves the device on its own; the user can reclassify a record's privacy at any time and the PNA honors it durably; communication transports are user-chosen; and the user can reason about where their data lives without trusting a vendor. v0.1 PNAs operate *downstream* of SaaS systems of record — taking local custody of contact data without modifying it at the source.

**Earning complexity — an evolutionary stance.** This spec is deliberately opinionated and *incomplete*. A specification for an application *class* earns its recommendations only by building and validating real applications — which forces a practical question ahead of any elegant one: *what is simple enough to implement, yet usable and safe enough to put in front of users for real feedback?* v0.1 answers with deliberate first moves — the [shared](#vocab-shared-data)/[private](#vocab-private-data) privacy-class split (canonically two stores), and operating *downstream* of SaaS systems of record rather than synchronizing with them. It forgoes live multi-device sync not because sync is unwanted but because the rules that would keep a user's private layer *safe* across every sync scenario are not yet known — and a class spec cannot honestly mandate what it cannot yet make safe. Harder capabilities — cross-device sync, federation, a richer storage substrate — are explicit future work (see [§ Scope and versioning](#scope-and-versioning)), taken on only once the simpler systems are proven usable and safe, most likely under a separately-controlled tool bound by these same architectural commitments. The spec **earns** complexity; it does not assume it. (Developed as the PNA's deliberately-staged position within a small cross-domain *composite group* in [`docs/papers/paper1-pna-positioning.md`](../docs/papers/paper1-pna-positioning.md).)

**Taking control is the point — and only the start.** Getting the root local is credible interop between SaaS and user-owned software, and it is the precondition for everything above it. Once the root is local and the private layer over it stays sovereign, local AI can finally do real work over your own relationship graph — search, recall, reaching out — and you compound a private store of relationship knowledge that grows more valuable over time, even as the SaaS sources it was drawn from stay replaceable. The [Goals](#goals) below are those preconditions; *working your own graph* is the payoff they unlock.

**Why it matters.** This is not only a privacy concern: the ability to find and reach the people you rely on is itself at stake — social connection is among the most robust correlates of mental health,¹ and the relationship data most worth keeping (who to call when you have nothing left; which family member to make peace with) is exactly what it is unreasonable to entrust to a profit-motivated platform whose board can change overnight. Today that data lives nowhere, or only in memory, buried under the noise, non-relationships, and engagement-maximizing feeds of the systems that hold it. A PNA is one small tool aimed squarely at that gap.

<sub>¹ Social connection and isolation are strongly associated with mental-health outcomes and all-cause mortality (Holt-Lunstad et al., *PLoS Medicine*, 2010; U.S. Surgeon General, *Our Epidemic of Loneliness and Isolation*, 2023; WHO Commission on Social Connection, 2025). The association is robust; recent genetic evidence narrows the *causal* claim for physical disease, leaving the mental-health pathway as the part that holds — which is the pathway this work targets.</sub>

**How this spec is organized — three layers.** This spec is built in three layers, and keeping them distinct is what lets a PNA be rebuilt on any technology without losing what it *is*: the **Goals** — the human-facing (increasingly agent-facing) outcomes a PNA delivers; the **architectural commitments** — the promises that make the Goals real, stated so they hold *regardless of programming language, operating system, database engine, or how the app is delivered*; and the **realizations and constraints** — how each commitment is met on a *specific* technology stack, and what that stack will and won't permit. The line between them is a single test: **an architectural commitment survives a total technology swap.** Rewrite the PNA in another language, on another OS, with another database, delivered another way, and a commitment still binds; anything that names or depends on a specific stack lives one layer down. [§ How the pieces fit together](#how-the-pieces-fit-together) makes this precise.

---

## Vocabulary

Worked examples below cite `fellows_local_db` as the first reference design — its concrete choices live in [`fellows_local_db/docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).

- <a id="vocab-ac"></a>**Architectural commitment (AC).** A specific, stable-ID'd architectural promise a PNA must keep, derived from the [Goals](#goals). The AC is the **unit of conformance**: each carries an ID (`AC-1`, `AC-MCP-A`, …), every typed contract names the AC(s) it realizes, and a design attests AC-by-AC. An AC is a **Layer 1** commitment — it survives a total technology swap (see [§ How the pieces fit together](#how-the-pieces-fit-together)). A *universal* AC applies to every PNA; a *conditional* AC applies only when the PNA has a specific **behavioral property** — see [Universal, conditional, and realized commitments](#vocab-universal-ac).

- **Axes.** Axes are areas of functionality that need to be defined when building a PNA. These are the high level categories of app functionality that you must build.

Each Axis offers a pre-defined, limited number of choices to the builder — internally we call these the builder's "Axis picks", although they can be changed later, they are the first set of decisions that need to be made before building, and some thought should be put into them.

  An example of an Axis is the **distribution** axis, which offers the Axis picks `web-bundle-with-magic-link` (fellows_local_db's pick), `never-distributed-single-user` (PRM's likely pick), `web-bundle-open`, `app-store-native`, `sideloaded-native` — the builder picks one.

  v0.1 names these Axes: distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure. The full catalog of attested picks per Axis lives in [`axes.md`](axes.md).

- **Axis pick.** One value on one Axis. Written `axis:value` — for instance `storage:opfs-sqlite-wasm`, `distribution:web-bundle-with-magic-link`. The set of attested picks per Axis is enumerated in [`axes.md`](axes.md).

- <a id="vocab-contact-data"></a>**Contact data.** The shared, externally-sourced facts that identify a person in the user's network — name, email, phone, photo, organizational membership. A species of [shared data](#vocab-shared-data): some external system (Google, Apple, a directory) holds a copy, the PNA mirrors it locally, and it is local-first and replaceable. Stored in the [Shared DB](#vocab-shared-db-private-db); read-only inside the PNA (written only by Ingestion).

- <a id="vocab-constraint"></a>**Constraint (`CST-*`).** A ceiling a *platform or storage substrate* imposes that bounds how fully a PNA can honor a Goal or AC on that platform (e.g. the browser's OPFS sandbox). A PNA stays conformant by handling each inherited Constraint honestly — capability reduced to what the platform can keep, frontier declared truthfully. Constraints are the **dual of [Exceptions](#vocab-exception)** (platform-imposed vs. user-raised); catalogued in [`constraints.md`](constraints.md).

- <a id="vocab-exception"></a>**Exception (`EX-*`).** A deliberate, *user-raised* departure from a baseline guarantee — a named AC, or the PNA definition itself. Raising one exits *PNA mode* (`pna-active = false`) while it is active, and it must be consented-to, signalled, and handled to the handler contract in [`exceptions.md`](exceptions.md). The dual of a [Constraint](#vocab-constraint).

- <a id="vocab-user-mediation"></a>**User-mediation (`UM-*`).** The standing invariant that **the human is the actuator**: the proposer (an AI, the network, an importer) only *stages*; the principal *disposes* through a user-controlled surface, and nothing mutates the sovereign store or egresses its data except through that gate. The **third general mechanism** alongside [Exceptions](#vocab-exception) and [Constraints](#vocab-constraint) — an always-on property the architecture upholds (it does **not** exit PNA mode), the named invariant beneath the action / egress ACs (AC-10 / AC-16 / AC-19 / AC-20 / AC-21 / AC-MCP-B). Its contract — UM-1 (no bypass) · UM-2 (separation) · UM-3 (legibility), bounded to separation / legibility / attribution, **not** comprehension — is in [`user_mediation.md`](user_mediation.md).

- **Flavor.** The full constellation of axis picks for a specific PNA. fellows_local_db's flavor: `distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`. Two PNAs of the same use case can have different flavors (a TUI PRM vs. a Tauri-wrapped GUI PRM share the use case but differ on workspace shell and storage). A flavor + a use case together fully identify a PNA's shape.

- <a id="vocab-goal"></a>**Goal.** One of the few top-level, user-facing outcomes a PNA exists to deliver (see [§ Goals](#goals)). The Goals are the *why*; the [architectural commitments](#vocab-ac) are the checkable *how*. Each AC serves one **primary** Goal (occasionally a second where one mechanism genuinely serves two) — see the cardinality note in [§ Goals](#goals).

- **Interface.** A contract that spans multiple slots. Where a slot is filled by *one* code module, an interface is a shared constraint — either a data shape that multiple slots produce and consume (the Shared and Private DB schemas), or a capability requirement every slot must implement (the Debug contract). v0.1 names three interfaces: **Shared schema**, **Private schema**, **Debug contract**. Catalogued in [§ Slots, Interfaces, and Sub-contracts](#slot-map) alongside the slots they bind.

- <a id="vocab-mcp-server"></a>**MCP server.** A process exposing PNA capabilities as MCP tools (Anthropic's Model Context Protocol — JSON-RPC, a JSON-based Remote Procedure Call format, over stdio or socket). The spec defines five canonical MCP servers per PNA, structured around the Shared / Private privacy boundary so an AI client can be wired to one without the other:

  - **Shared Data Ops** — read access over the Shared DB (typically mirrored contact data from SaaS systems; AC-MCP-A is not triggered, because no Private DB rows flow through this surface).
  - **Private Data Ops** — read access over the Private DB (user-owned relationship data; AC-MCP-A applies — cloud clients require per-call consent).
  - **Ingestion** — drives imports, dedup, orphan preview.
  - **Communications** — stages outreach for workspace-mediated user confirmation (AC-MCP-B; the MCP server proposes, the workspace disposes).
  - **Diagnostics** — read-only access to the Debug contract.

  Splitting Data ops along the Shared / Private boundary mirrors AC-1's class boundary at the MCP surface — structural under the canonical two-store realization: the privacy posture of each tool call is determined by which server it lands on, not by an in-server gate. An AI client (Claude Desktop, Cursor, a local-Ollama-backed agent, etc.) consumes these servers to drive the PNA. v1 reference implementations expose read-only surfaces only; future toolkit versions may add write-side tools (Private DB CRUD, Comms message-send confirmation) as separate contracts. MCP servers are how multiple PNAs cooperate at runtime: a PNA exposing MCP becomes externally reachable so an AI client can wire multiple PNAs together on the user's device even though each is its own bundle.

- **Mirroring.** The act of producing a fresh shared DB from an external source of shared data. A snapshot is created by the Ingestion component. Re-mirrors are atomic from the workspace's view (stage, validate, swap) and never silently orphan private references.

- <a id="vocab-personal-network"></a>**Personal network.** The egocentric graph of people a user is connected to — the user at the center (sometimes an *associogram* or ego-network) — together with the [contact data](#vocab-contact-data) that identifies them and the [relationship data](#vocab-relationship-data) the user keeps about them. "Network" here is the personal, person-centered graph — distinct from, but deliberately resonant with, the *social network* of network science and *social-network health*. A PNA is software for holding and working over one user's personal network.

- <a id="vocab-pna"></a>**Personal network application (PNA).** A PNA is an application that helps a user view contact data and work on relationship data over it as a firewalled data layer with higher security needs than the contact data. The PNA runs local-only, never as SaaS - servers are only used for distribution and app updates, and only where appropriate. The PNA bridges SaaS data (which should never contain private relationship data) into a much more functional, customizable user-owned work environment suitable for viewing personal networks, updating private data about them, and interacting with them. A PNA MAY deliberately and temporarily depart from this definition (or from a named AC) by **raising an Exception** — see [`exceptions.md`](exceptions.md). Raising any exception exits "PNA mode": while an exception is active the app is **not a PNA right now** (the `pna-active` bit is false and the local-only guarantee is suspended), even though it stays **exception-handling conformant** as long as every active exception is handled to the exceptions.md handler contract. The two predicates are distinct, and a relying party keys on `pna-active` — see [`exceptions.md` § Concept](exceptions.md). *(The `pna-active` / `exception-handling` predicate split is normative; see [`exceptions.md` § Concept](exceptions.md).)*

  [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) is one PNA reference design — making a directory archive useful and fast - providing a credible exit from a SaaS directory system. Another PNA reference design would be a PRM - an app that aggregates personal contact data ingested from the big SaaS providers and lets the user operate privately on that data, adding privacy-sensitive notes, searching, and launching tasks from the app. PNAs bridge the old world of SaaS and offer private, custom tools to operate on contact data.

- <a id="vocab-plugin"></a>**Plugin / extension.** Anything that adds a capability to a composed PNA without modifying its core. A memory-assistant view, a calendar overlay, a federated portrait pull, a community-statistics survey tool — all plugins. PNAs themselves will expose MCP server interfaces as well.

- <a id="vocab-private-data"></a>**Private data.** Data that exists only on the user's device(s). The user is *not* OK with any external system holding a copy. *Examples:* notes the user keeps about a contact, tags they apply, groups they assemble, communication history. The PNA's central architectural job is to keep this layer protected, durable, and exclusively local. This data must never be sent across insecure channels, and must only be explicitly sent by the user's command in any form.

- <a id="vocab-reference-design"></a>**Reference design / thematic example.** A working, deployed PNA that demonstrates one valid combination of slot-fills against the spec. fellows_local_db is the first reference design — its load-bearing adjectives are *magic-link distributed PWA (Progressive Web App)* (Distribution choice) + *static network DB archive* (Ingestion choice — the directory is mirrored once with opt-in updates, not linked to a live contact manager) + *single shared directory* (Source choice). New reference designs accumulate adjectives as their slot-fills land. AIs adapting a thematic example start from one of these and ask the user which slot-fills to keep, swap, or extend.

  *Archival (v0.1).* When a reference design is accepted into the toolkit's set, its source at the submitted commit MUST be archived with a Software Heritage Persistent IDentifier (SWHID — a `swh:1:dir:...` content-addressed identifier produced by Software Heritage's Save Code Now service). The SWHID is recorded in the design's toolkit entry so the source survives even if the upstream repo is deleted or relocated. Future toolkit versions MAY revise the archival mechanism; v0.1 commits to SWHID.

- <a id="vocab-relationship-data"></a>**Relationship data.** The private memory a user creates over their contacts — notes, tags, groups, communication history, recency — the layer that turns a contact list into a personal network the user can actually work. A species of [private data](#vocab-private-data): it exists only on the user's device(s), is read-write from the workspace, and is the layer the PNA's central architectural job protects. The positioning calls it *private relationship memory*. Stored in the [Private DB](#vocab-shared-db-private-db).

- <a id="vocab-shared-data"></a>**Shared data.** In the context of a PNA, shared data is data that exists in more than one place — typically, a copy held by an external system the user uses (Google Contacts, Apple Contacts, Facebook friends, a fellowship's directory, a school's roster). The user is OK with that external system continuing to hold it, and often has no say in the matter. *Examples:* name, email, photo, organizational membership. The PNA mirrors this data locally so the user can browse and search it without depending on the external system being reachable.

  > "Shared" is the key word — not "public" in the everyday sense. Shared data can be data that the user publicly shared, or shared with Apple Contacts and exported, and is typically maintained outside the user's systems. The contact data in your Google account isn't *publicly visible*; it just isn't *exclusively yours* — it is shared with Google and any controlling governments or Google partners it is sold to. In all cases, some external system has a copy, or once did.

- <a id="vocab-shared-db-private-db"></a>**Shared DB / Private DB.** The two databases of the **canonical two-store realization** of [AC-1](#ac-1)'s shared/private class boundary. The Shared DB holds shared data (read-only inside the PNA — written only by the Ingestion component). The Private DB holds private data (read-write from the workspace). The split is the canonical, recommended realization — a single-store design that enforces the same class boundary at the data layer is admissible (see [AC-1](#ac-1)) — and further decomposition and isolation of data according to privacy constraints is reasonable but unnecessary for the first PNAs envisioned.

  In fellows_local_db, the shared DB is `fellows.db` and the private DB is `relationships.db`. The spec uses the generic names; specializations may rename for ergonomics, or change database engines for practical reasons, as long as the data stays local.

- **Slot.** A slot is a part of a PNA — a code module that handles a specific job within the system. v0.1 names five slots:

  - **Ingestion** — loads contact data into the Shared DB
  - **Storage** — owns the data files and serves queries
  - **Workspace** — runs the UI
  - **Communications** — launches outreach
  - **Distribution** — ships the PNA to other users

  Each slot has a contract; any code that satisfies the contract can fill it — a JavaScript module, a Python package, or an OS process, depending on the target environment. The full catalog and contracts are in [§ Slots, Interfaces, and Sub-contracts](#slot-map).

- <a id="vocab-subcontract"></a>**Sub-contract.** A named, stable-ID'd decomposition of a [slot](#vocab-slot)'s or interface's contract (prefixes `WS-`, `ST-`, `IN-`, `CO-`, `DI-`, `SH-`, `PR-`, `DB-`), so a builder can target each piece individually. Sub-contracts cite the ACs they realize; catalogued in [§ Slots, Interfaces, and Sub-contracts](#slot-map).

- <a id="vocab-universal-ac"></a>**Universal, conditional, and realized commitments.** A *universal* commitment applies to every PNA — it derives from the [Goals](#goals) alone. A *conditional* commitment applies only when the PNA has a particular **behavioral property** (it reaches out to contacts; it mirrors more than one source; it exposes a programmatic surface over private data). Both are **Layer 1** [architectural commitments](#vocab-ac): they survive a total technology swap and carry an `AC-*` ID. A <a id="vocab-realization"></a>**realization** is the **Layer 2** counterpart — *how* a commitment is met on a specific technology stack (a single OPFS-owning worker; a native file-lock). A realization names a technology, does **not** survive the swap, and carries **no** `AC-*` ID; it lives in [`axes.md`](axes.md) beside the axis pick that brings it. The three layers and the swap test are defined in [§ How the pieces fit together](#how-the-pieces-fit-together). [§ Universal architectural commitments](#universal-architectural-commitments) lists the universal set; the conditional ACs and the realizations live in [`axes.md`](axes.md).

- <a id="vocab-use-case"></a>**Use case.** A user-facing class of PNA — "Directory Archive," "Personal Relationship Manager." A use case names what kind of app this is *from the user's perspective*. v0.1 attests three (Minimum Viable PNA, Directory Archive, Personal Relationship Manager); future versions will add more. Use case is *not* one of the Axes (above); it's the parent category that a flavor instantiates. A use case typically suggests default axis picks (Directory Archives gravitate toward web-bundle distribution; PRMs toward never-distributed-single-user) but the axes remain independent — a hypothetical Directory Archive shipped as a Tauri shell + native SQLite is conceivable. Full catalog in [`use_cases.md`](use_cases.md).

- <a id="vocab-workspace"></a>**Workspace.** One of the slots in a PNA: the viewer + editor. The thing the user looks at and clicks. fellows_local_db's workspace is a vanilla-JS SPA (Single-Page Application) in the browser; another PNA's might be a native shell, a Tauri app, a TUI (Terminal User Interface), or a separately-distributed mini-app sharing the same data layer.

---

## Goals

The Goals are the few user-facing outcomes a PNA exists to deliver — the *why* the [architectural commitments](#vocab-ac) (ACs) below serve. Each is stated at **outcome altitude** (what the user gets), with one concrete *example mechanism*, why it matters, and the plain-language set of constraints (ACs) it requires. (Usability is assumed *above* the Goals: an unusable tool protects nothing, so "simple enough for a human to understand and actually use" is a precondition on all of them, not a Goal of its own.) v0.1 names four.

### Goal 1 — Take ownership of the root

A PNA brings the **root of your personal network** — your contact data and the relationship data you build over it — onto your own systems, under your own ownership, and **keeps it there**: it creates and maintains a local store you control, for as long as you want it, independent of any SaaS account.

*Example mechanism:* the **mirror-and-build pattern** — mirror your SaaS contacts into a local store those systems can't reach, then correlate richer private data (notes, tags, history that never touch SaaS) against that legacy data, locally. *How* the root is filled is an implementation choice (mirror an export, live-pull, multi-source merge — see the Ingestion axis in [`axes.md`](axes.md)); v0.1 PNAs operate *downstream* of SaaS systems of record, taking local custody without modifying the source.

> **Why it matters:** your contacts live in someone else's system — scattered across Google, Apple, Facebook, a fellowship's directory — surveilled and outside your control. Pull that root onto your own device and you can finally build on it; leave it where it is and you can't. Every other Goal assumes you own the root first.

*Constraints it requires:* the sovereign, owned private layer that *is* the local root ([AC-1](#ac-1) — which also seals that layer for Goal 3); the platform cannot silently own or evict the store ([RZ-4](axes.md#rz-4)); a rejected server session still serves the local copy ([AC-5](#ac-5)); and the store is built and refreshed only on an explicit user action, never by background polling ([AC-21](#ac-21)).

### Goal 2 — Protect the root's integrity, by validation

You can **verify** that a PNA does what it claims — that its protections are real, and that the data in the root is authentic to its source — rather than taking it on trust. A protection you cannot check is a protection you do not have.

*Example mechanism:* source-available code plus a runtime **build label** and an always-reachable **diagnostic surface**, so you (or an AI acting for you) can confirm *which* code is running and watch it behave — before and during use.

> **Why it matters:** a privacy-sovereign user's threshold for trust is "show me," not "promise me" — this is the toolkit's own identity (it *validates behaviors, it does not certify*). Integrity has two halves, both checkable locally: **code-validation** (does the app behave as claimed?) and **data-validation** (is the contact data authentic to the source it names?).

*Constraints it requires:* an always-reachable diagnostic escape ([AC-6](#ac-6)) and a field-debug substrate ([AC-7](#ac-7)); a build label tied to the source revision so you can verify what is running ([AC-15](#ac-15)), with that revision's source available to inspect and rebuild ([AC-23](#ac-23)); honest capability assessment that never claims more than the platform delivers ([AC-22](#ac-22)); and **provenance** — every shared record traces to a source the user approved ([AC-17](#ac-17)), with stable IDs and per-field provenance under multi-source merge ([AC-PRM-B](#ac-prm-b)).

> **Why it matters (the diagnostic surface):** A privacy-sovereign user's threshold for what diagnostic data flows anywhere is the same as for the rest of their data. The diagnostic surface is part of the privacy surface, not an exception to it. Many eventual PNAs will be single-user installations with no maintainer at all; the debug substrate has to work in that mode without sending anything anywhere by default. When a sink *is* configured (fellows_local_db sends to a maintainer mailbox), it has to be sanitized and rate-limited so the user trusts using it.

### Goal 3 — Protect the root from egress

Nothing about your personal network leaves your systems without you **choosing how, understanding the threat, and seeing exactly what is sent**. The private layer is **sealed by default**; every way out — reaching a contact, or handing data to an AI — is a governed exit you control, and you are never forced onto an insecure or content-reading channel.

*Example mechanism:* **validate-before-egress** — the workspace offers a *choice* of transports and shows the full payload before launch, and an LLM invoked over your data is treated as just another transport (local by default, a cloud model only on per-call consent).

> **Why it matters:** this absorbs two threats that look different but are the same act — *control what leaves the root*. Unauthorized disclosure (a leak; a cloud model quietly fed your notes) and authorized outreach (you emailing a contact) are both data leaving the root, and the user who holds their local data to a high bar holds the same bar for how it travels. Privacy here is something you can *achieve* by plugging in a secure channel — and that the PNA promises never to undermine.

*Constraints it requires:* the sealed-by-default private layer ([AC-1](#ac-1), shared with Goal 1); no server holds, persists, or syncs the private store ([AC-2](#ac-2)); cross-origin isolation ([RZ-3](axes.md#rz-3)) and anti-enumeration with bounded analytics ([AC-8](#ac-8)); the user picks the transport per outreach ([AC-16](#ac-16)), transports cannot read message contents ([AC-18](#ac-18)), and the full payload is visible before send ([AC-19](#ac-19)); an LLM call over user data is a transport ([AC-20](#ac-20)); and at the MCP surface a cloud client needs per-call consent for private rows ([AC-MCP-A](#ac-mcp-a)) and the workspace — not the AI — launches the send ([AC-MCP-B](#ac-mcp-b)).

### Goal 4 — Protect the root from entropy and accidents

Your data **survives** — you never lose your people. The private layer is durable across devices, browsers, and PNA versions, resists the routine churn of app updates and cache clears, and when loss happens anyway it is **recoverable**, not merely resisted.

*Example mechanism:* per-boot debounced **auto-backup** to a rotating ring of recovery points, plus an export/import path that lets the private store move with the user.

> **Why it matters:** local-first only delivers on the other Goals if "local" doesn't mean "trapped on this one installation forever." Users replace devices, switch browsers, reinstall. Durability *resists* loss, recoverability *remedies* it when it happens anyway, and portability keeps the data from being trapped in the first place — the Goal needs all three.

> A platform or storage substrate may impose a ceiling that bounds how fully a PNA can honor this Goal — a [Constraint](#vocab-constraint) (see [`constraints.md`](constraints.md)). Goal 4 is where this bites hardest: durable, portable private data runs straight into what the browser substrate will and won't keep. A PNA stays conformant by handling each inherited Constraint honestly (capability reduced to what the platform can keep, frontier declared truthfully); handling a Constraint does not exit PNA mode. Constraints are the dual of [Exceptions](#vocab-exception) — a Constraint is imposed by the platform, an Exception is raised by the user.

*Constraints it requires:* no corruption across a version-skewed storage boundary ([AC-4](#ac-4)); auto-backup with a recovery ring ([AC-9](#ac-9)); concurrent-access detection ([AC-11](#ac-11)) — realized as a single OPFS owner/writer ([RZ-1](axes.md#rz-1)) or a native file-lock ([RZ-5](axes.md#rz-5)); and non-destructive re-imports that preview any private references they would orphan ([AC-10](#ac-10), shared with Goal 1).

---

## How the pieces fit together

The spec is a small graph of typed components arranged in **three layers**. Naming the layers — and the line between them — is what keeps the spec navigable for a human and *applicable* for an AI building or evaluating against it on a technology stack the authors never saw.

![The PNA Spec in three layers — Layer 0 Goals (the why), Layer 1 architectural commitments (the what; ACs, the unit of conformance), Layer 2 realizations and constraints (the how; per-stack mechanics). Layers 0–1 survive a total technology swap; Layer 2 names a specific stack and does not. Worked example: AC-11 (one writer at a time) is realized by RZ-1 (a single OPFS-owning worker) on a browser stack and by RZ-5 (a native file-lock) on a native stack — one commitment, two realizations.](figures/three-layers.svg)

*The three layers and the line between them; [The dividing test](#the-dividing-test) below states it precisely.*

### The three layers

- **Layer 0 — Goals.** The few human- and agent-facing outcomes a PNA delivers (see [§ Goals](#goals)). Stated at outcome altitude; they name no technology. The *why*.
  
- **Layer 1 — Architectural commitments (ACs).** The checkable promises that make the Goals real (see [§ Universal architectural commitments](#universal-architectural-commitments)). An AC is the **unit of conformance**. Layer 1 has two kinds, both technology-independent:
  - **Universal** — applies to every PNA, derived from the Goals alone.
  - **Conditional** — applies only when the PNA has a particular *behavioral property* (it reaches out to contacts; it mirrors more than one source; it exposes a programmatic surface over private data). Still Layer 1: a conditional AC names a *behavior*, never a technology.
    
- **Layer 2 — Realizations and constraints (the mechanical layer).** Everything that names or depends on a specific technology stack: the **Axes** ([`axes.md`](axes.md)) — the menu of technology choices a builder picks from; the **realizations** of each commitment on a chosen stack (a single OPFS-owning worker; a native file-lock); the **Constraints** (`CST-*`, [`constraints.md`](constraints.md)) a stack imposes; and the per-slot **[sub-contracts](#vocab-subcontract)** that decompose an implementation.

### The dividing test

> **A statement belongs to Layer 1 if and only if it survives a total technology swap.** Rewrite the PNA in another language, on another operating system, with another database, delivered another way — does the statement still make sense and still bind? If yes, it is an architectural commitment. If it names or depends on a specific stack (OPFS, SQLite, a service worker, an iOS sideload, a `mailto:` URL), it is a Layer-2 realization or constraint, not a commitment.

The line this draws: *the source being available so you — or your tools — can verify the app before trusting it* survives the swap, so it is an architectural commitment. *Sideloaded on iOS* does not: sideloading could be forbidden tomorrow and the platform renamed the day after. The first is Layer 1; the second is Layer 2. Conflating them hides the commitment that matters behind a platform detail that does not.

### Three rules that keep the layers clean

1. **The `AC-*` namespace is Layer 1 only.** Every AC passes the swap test. A commitment that names a technology is mis-filed: its technology-independent core is the AC; its stack-specific form is a realization.
2. **Conditional ACs are Layer 1, but tagged.** Each conditional AC is tagged with the *behavioral property* that triggers it, so "applies only to multi-source PNAs" reads differently from "applies to every PNA."
3. **A realization is never an AC.** Realizations are Layer 2, carry no `AC-*` ID (not even a conditional one), and live with the axis pick that brings them. A conditional AC is triggered by a *behavioral property*; a technology pick may *entail* a property (picking multi-source ingestion entails "mirrors more than one source"), and that property triggers the AC — but the pick itself brings only realizations and constraints.

### Cardinalities

Within and across the layers, the typed components relate many-to-many; stating the cardinalities once keeps the graph navigable — for a human skimming and for an AI building or validating against it:

| Relationship | Cardinality | |
|---|---|---|
| **Goal ↔ AC** (an AC *serves* a Goal) | many-to-many, rendered **primary-grouped** | Each AC's `Serves` (in the [universal-AC table](#universal-architectural-commitments)) lists every Goal it bears on; the per-Goal views above group each AC under one *primary* home. A secondary appears only where one mechanism genuinely serves two — e.g. [AC-1](#ac-1), the sovereign sealed private layer, serves both *Take ownership of the root* and *Protect the root from egress*. Cross-cuts are capped at two; most ACs serve exactly one. |
| **Axis → pick → flavor** | one-to-many | An axis offers several picks; a *flavor* is one pick per axis. |
| **Behavioral property → conditional AC** (a property *triggers* an AC) | one-to-many | A property a PNA has (reaches out; multi-source; exposes a private-data surface) may trigger zero or more conditional ACs. A technology *pick* may **entail** a property — and separately brings its Layer-2 realizations and constraints ([`axes.md`](axes.md)). |
| **Slot → sub-contract** | one-to-many | Each slot decomposes into named [sub-contracts](#vocab-subcontract) (`WS-`, `ST-`, …). |
| **Contract / sub-contract → AC** (*realizes*) | many-to-many | A contract may realize several ACs; an AC may be realized by several. |
| **Exception → AC** (*relaxes*), **Constraint → AC/Goal** (*bounds*) | many-to-many | An [`EX-*`](#vocab-exception) / [`CST-*`](#vocab-constraint) names every guarantee it relaxes or bounds. |

The rule of thumb: **Goals are few and crisp; everything beneath them composes many-to-many — but the reading views (per-Goal AC lists, per-slot sub-contracts) stay clean trees by giving each item one primary home and linking the genuine cross-cuts.**

---

## Use cases

A use case names a coherent class of PNA from the user's perspective. A use case typically suggests default axis picks but does not determine them. v0.1 attests three named use cases plus a longer-arc target:

- **Minimum Viable PNA ("Personal Vault")** — the smallest conformant shape: **Ingestion + Storage + a minimal Workspace**, with no Communications and no Distribution. A local mirror of your contact data plus a private overlay (notes, tags) you add through a CLI or other thin surface; nothing leaves the device, nothing is distributed onward. Useful on its own as a personal backup-with-notes, and the floor every richer PNA builds on.
- **Directory Archive** — a snapshot of some external organization's roster (a fellowship, a school, a cohort, a community) plus the user's private overlay on top. Shared data has a single external source; each distributed user receives the same shared data and accumulates their own private overlay. Realized in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).
- **Personal Relationship Manager** — the user's own contact databases (Google + Apple + Facebook + LinkedIn + organizational directories) mirrored locally, plus rich private overlays (notes, tags, groups, comms history, message recency) and tools (LLM-mediated search, visual recall, eventual P2P (peer-to-peer)). Multi-source ingestion. Typically single-user, not distributed onward. [PRT](https://github.com/richbodo/prt)-inspired (PRT — "Personal Relationship Toolkit" — is the graveyard predecessor project from which the current toolkit and fellows_local_db grew). Realized in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md).
- **Multi-PNA ecosystem (target, v0.2+)** — multiple cooperating PNAs on one user's device, wired together at runtime by an AI agent via MCP. The PRM acts as the meta-workspace over a deduplicated read-only meta-view composed from the per-PNA shared stores; per-app workspaces remain available for single-context work. No reference design yet; v0.1's contracts are sized to enable it.

Full catalog with attestation status, default axis picks, and reference-design links: [`use_cases.md`](use_cases.md).

---

## Axes

v0.1 names the independent Axes a PNA picks along. A PNA's *flavor* is the full constellation of picks. Each pick may trigger conditional ACs (via a behavioral property it entails) and brings its own Layer-2 realizations and constraints (the tags appear in [`axes.md`](axes.md), grouped by axis-pick).

- **Distribution** — how the PNA reaches a user's device. Picks: `web-bundle-with-magic-link`, `never-distributed-single-user`, `web-bundle-open`, `app-store-native`, `sideloaded-native`.
- **Storage substrate** — what backs the data layer. Picks: `opfs-sqlite-wasm`, `native-sqlite-via-filesystem`, `idb-only-browser`, `native-sqlcipher`.
- **Ingestion shape** — how the Shared DB is filled and refreshed. Picks: `single-source-static-mirror`, `multi-source-merge-with-dedup`, `single-source-live-pull`, `federated-read` (deferred).
- **Workspace shell** — what the user sees and clicks. Picks: `vanilla-js-spa`, `framework-spa`, `tui-textual`, `cli-subcommands`, `native-shell-tauri`, `native-shell-native`.
- **Comms transport set** — which outreach mechanisms the workspace offers. Picks: `mailto-only`, `mailto-plus-signal`, `mailto-plus-matrix`, `shell-out-to-cli-clients`.
- **MCP-exposure** — which canonical MCP servers (Shared Data Ops / Private Data Ops / Ingestion / Comms / Diagnostics) the PNA hosts. Picks: `none`, `shared-only`, `shared+private`, `shared+private+comms`, `full`.

Notes on Axis independence:

- Some Axes cluster strongly. Browser-based distribution typically goes with `storage:opfs-sqlite-wasm` and a SPA-style workspace shell. CLI (Command-Line Interface) distribution typically goes with `storage:native-sqlite-via-filesystem` and a TUI or CLI workspace shell. [§ Composition](#composition) names these clusters (Browser PNAs, CLI / native PNAs) for shorthand.
- Some Axes are genuinely orthogonal. A Directory Archive use case could in principle ship as a Tauri-wrapped native shell + native SQLite + a browser-style bundle; the use case doesn't determine those picks.

Use case is *not* one of these Axes — it's the parent category from which a flavor is instantiated; see [§ Use cases](#use-cases).

Full per-pick catalog with attestation status, AC triggers, and correlation notes: [`axes.md`](axes.md).

---

## Composition

A PNA is composed by an AI coding agent (Claude Code, Cursor, or similar) working with a user — **the AI agent is the composer.** The agent reads this spec, optionally adapts a reference design like fellows_local_db, uses the canonical MCP servers to interact with existing PNA data, and writes the code with the user. v0.1 does not ship a separate build tool that assembles PNAs from stock modules; the toolkit's three deliverables (specs, reference apps, MCP servers) are the materials, and the agent uses them.

The contracts are written so the agent can pick them up and check its own work, and so both the user and the agent can read the spec. As long as the contracts hold, an agent can rewrite a PNA from scratch while the user is still talking to it without changing the user's sovereignty, durability, or privacy posture. The Goals are the user-facing needs; the architectural commitments (ACs) are the choices that make those needs achievable. (Read any reference design's Architecture document to see the output of this process.)

> **Validation, not certification.** The toolkit validates behaviors against the Goals; it does not certify. There is no pass/fail badge and no certifying body (see [`CONTRIBUTING.md`](../CONTRIBUTING.md) § "Acceptance is not certification" and the skill's § Principles, "Conformance is checked, not awarded"). Conformance is *checked* — by the user, or by an AI running the evaluate flow — against this spec. Where a PNA deliberately departs from a guarantee it raises an [Exception](exceptions.md); the evaluate flow then detects each exception and verifies how it is handled, **reporting by `AC-*`/`EX-*` ID rather than awarding a grade** — and, while an exception is active, reporting the app as **not a PNA right now** (`pna-active = false`) even as it attests honest exception-handling (*the `pna-active` predicate split; see [`exceptions.md` § Concept](exceptions.md)*). Where the *platform* imposes a ceiling the PNA cannot clear, that is a [Constraint](constraints.md); the evaluate flow detects each ceiling a design's axis picks inherit and verifies it is handled honestly — capability reduced to what the platform can keep, frontier declared truthfully — reporting by `CST-*` ID. Over-reach (promising a capability the platform cannot keep) is a silent conformance failure, the dual of an undeclared Exception.

The agent's job when **building**, per this spec, is to:

1. Identify the **use case** with the user (see [§ Use cases](#use-cases)).
2. Walk the user through the **Axes** (see [§ Axes](#axes)) and make picks that fit the user's goals.
3. Generate or adapt code that fills each **slot** (see [§ Slots, Interfaces, and Sub-contracts](#slots-interfaces-and-sub-contracts)) according to its contract, consistent with the axis picks.
4. Verify the result against the **universal architectural commitments** (see [§ Universal architectural commitments](#universal-architectural-commitments)) and any conditional commitments the picks add (catalogued in [`axes.md`](axes.md)).

Building is one of **four flows** the skill packages — *validate* (audit a candidate against the spec), *build* (the steps above), *contribute* (feed a finding back into the spec), and *harden* (advise on securing the operating environment a PNA runs in — the advisory flow defined in [`exceptions.md` § Environmental threats and the Harden flow](exceptions.md)). The first three secure what the built PNA does; harden secures the environment around it. See [`pna-toolkit/SKILL.md`](../pna-toolkit/SKILL.md) and [`docs/users-guide.md`](../docs/users-guide.md).

### Common axis clusters

Axis picks tend to fall into a couple of recognizable shapes. These are **shorthand, not a formal axis** — every pick is still made independently (a given use case could in principle ship as either shape):

- **Browser PNAs** — run in the browser as a web bundle; storage is SQLite-WASM over OPFS in a dedicated worker; distribution through an HTTP origin (with or without an auth gate); multiple users install from one source. **fellows_local_db is a Browser PNA.**
- **CLI / native PNAs** — run as one or more OS processes (a TUI, a CLI subcommand set, or a native GUI); storage is a native SQLite file (optionally SQLCipher); distribution is typically self-install and single-user. **PRT is the inspiration; a CLI / native PRM is the next planned reference design.**

See [`axes.md`](axes.md) for the per-axis picks and how they correlate.

### Cooperation across multiple PNAs

At runtime, multiple PNAs on a user's device can cooperate through their canonical MCP servers. An AI client (Claude Desktop, Cursor, a custom agent) connects to each PNA's exposed MCP servers and orchestrates across them — pull a contact from a Directory Archive, attach a private note from a PRM, schedule a follow-up in a Calendar app. The AI client is the runtime composer here, just as the AI coding agent was the build-time composer above.

This is the longer-arc *ecosystem reference design* described in [§ Vision](#vision). v0.1 doesn't yet have multiple cooperating PNAs to demonstrate the pattern, but the architectural seams that enable it — the five canonical MCP server interfaces (Shared Data Ops, Private Data Ops, Ingestion, Communications, Diagnostics), AC-MCP-A's cloud-client consent rule, AC-MCP-B's workspace-mediated outreach — are part of v0.1.

Cooperation across PNAs is not the same kind of thing as building one PNA. Building is design-time + AI coding agent + writing code that fills slots. Cooperation is runtime + AI client + invoking MCP tools across already-built PNAs. The two kinds of composition are separate concerns.

---

## Vision

One longer-arc target is an ecosystem of cooperating PNAs on a single user's device — a [Personal Relationship Manager](#vocab-use-case) (PRM - where private relationship data lives) running alongside one or more Directory Archives, a Contact Manager, and a Calendar app, each in its own bundle and sharing data as per their contracts.

The PRM acts as the [meta-workspace](#vocab-workspace): relationship data layered on top of a deduplicated read-only meta-view composed from the other apps' shared stores (Bob's cell from Google + work history from a fellowship directory + email from a Facebook export, resolved into one coherent contact view; the PRM's private overlay attached through stable IDs). The user can also work in clean per-app workspaces when they want a single context. Composing the meta-view requires per-source connectors, dedup with conflict resolution, and disciplined provenance — work for later toolkit versions. The eventual *ecosystem [reference design](#vocab-reference-design)* is the goal; v0.1 ships one PNA (fellows_local_db) and the spec it conforms to, along with [MCP servers](#vocab-mcp-server) (MCP = Anthropic's Model Context Protocol), with the architectural seams sized to let the ecosystem grow into place.

PNAs that participate in such an ecosystem need to be reachable not just to humans but to AI agents acting on the user's behalf. The spec therefore defines MCP server interfaces at five canonical connection points, split along the Shared / Private privacy boundary so an AI client can be wired to one without the other:

- A **Shared Data Ops server** — read access over the [Shared DB](#vocab-shared-db-private-db) (mirrored contact data).
- A **Private Data Ops server** — read access over the [Private DB](#vocab-shared-db-private-db) (user-owned relationship data); AC-MCP-A applies.
- An **Ingestion server** — drives imports, dedup, orphan preview.
- A **Communications server** — stages outreach for workspace-mediated user confirmation per AC-19 (the workspace launches the transport, not the MCP server — AC-MCP-B).
- A **Diagnostics server** — read-only access to the Debug contract.

An AI client (Claude Desktop, Cursor, a local-Ollama-backed agent, or any MCP-capable runtime) can drive a PNA through these servers without modifying its core; canonical implementations will ship with the personal_network_toolkit. Cloud AI clients (anything that sends Private DB rows off-device) require explicit per-call consent — see AC-MCP-A in [§ Universal architectural commitments](#universal-architectural-commitments). v1 surfaces are read-only on both data-ops servers; tool-side write contracts (Private DB CRUD — Create, Read, Update, Delete; message-send confirmation on Comms) land in a later toolkit version.

*Future direction — conformance evaluation as a precondition for ecosystem interop.* As the ecosystem grows, conformance evaluation may become a precondition for runtime interop between PNAs. Today an AI client wires two PNAs together by trusting each implements the canonical contracts; tomorrow, in a larger ecosystem with PNAs the user hasn't personally audited, a *systems-level conformance test* — does this candidate PNA honor the architectural commitments before I let it touch my Private DB? — becomes a natural precondition. This requires rethinking the spec at the systems level: the test isn't whether one PNA conforms in isolation but whether the cooperation across PNAs preserves the spec's guarantees. v0.1 doesn't define this; the present-day evaluation surface (PNA-by-PNA conformance check, performed by an LLM (Large Language Model) consuming this spec) is the closest analog. A later toolkit version may formalize the runtime-interop variant. *(Proposed, RFC.)* When it does, the gate MUST key on the candidate's **`pna-active`** bit — *is it a PNA right now?* — not on its exception-handling conformance: a PNA must refuse to expose its Private DB to a peer whose `pna-active` is false, because an app actively raising `EX-CLOUD-LLM` is piping to a cloud model, and "handles its exception nicely" is not a reason to hand it more private data. See [`exceptions.md` § Concept](exceptions.md) for the two predicates.

---

## Universal architectural commitments

Universal ACs are the architectural commitments derived from the goals alone. They apply to every PNA regardless of flavor.

Recall that an AC is a **Layer 1** commitment — it survives a total technology swap (see [§ How the pieces fit together](#how-the-pieces-fit-together)). **Conditional ACs** apply only when the PNA has a particular **behavioral property** (it reaches out to contacts; it mirrors more than one source; it exposes a programmatic surface over private data). Because the picks that *entail* those properties are catalogued in [`axes.md`](axes.md), the conditional ACs live there too, grouped near them.

Universal and conditional ACs share a single stable numbering sequence. The universal set is the table immediately below; the conditional ACs (AC-2, AC-5, AC-8, AC-PRM-B, AC-PRM-H) are in [§ Conditional architectural commitments](#conditional-architectural-commitments) that follows it. The Layer-2 **realizations** that were formerly AC-3 / AC-12 / AC-13 / AC-14 / AC-PRM-C now carry `RZ-*` IDs in [`axes.md`](axes.md) (see its [Retired IDs](axes.md#retired-ids) table); realizations are the Layer-2 *forms* of these contracts and are not themselves ACs.

The wording in the universal table below is substrate-neutral; specific *forms* (URL parameter vs CLI flag, OPFS vs native filesystem) are the Layer-2 **realizations** of these universal contracts.

**Normative language.** Conformance-bearing statements in the AC table below (and in the sub-contract definitions that follow, and in the conditional ACs and realizations in `axes.md`) use RFC 2119 / RFC 8174 keywords — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY — when, and only when, capitalized. Surrounding prose is plain English (motivation, examples, why-it-matters notes).

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. -->
| Commitment | Serves | ID |
|---|---|---|
| **Sovereign, sealed private layer.** A PNA MUST distinguish **shared** data (externally mirrored — some other system holds a copy; local-first but replaceable) from **private** data (created by the user over the shared layer; the device is its sole authority). Private data MUST be locally owned and user-writable; shared data MUST be treated as a refreshable mirror, not authored in place. The two classes MUST carry **distinct privacy postures enforced at the data layer**: the private class is sealed by default — it MUST NOT egress or mutate except through an explicit user action (the egress and user-mediation ACs apply to it) — and a component granted access to the shared class MUST NOT thereby reach the private class. The *mechanism* is a realization, not part of this commitment: the **canonical and recommended realization is the two-store split** — separate storage namespaces (shared read-only / externally-managed; private read-write / locally-owned), which makes the boundary *structural* and mechanically checkable (the five-server MCP split leans on it; example realizations: two SQLite databases via OPFS in fellows_local_db, two SQLite files on the filesystem in prm). A **single-store realization** that enforces the same class boundary at the data layer (per-row / -field classification + least-privilege access by class, pinned by a negative test) MAY satisfy this commitment, but carries a higher verification burden and is, as of this Toolkit-Version, not yet demonstrated. | Goal 1, Goal 3 | <a id="ac-1"></a>AC-1 |
| **Versioned cross-boundary handshake.** Every PNA with a storage boundary (worker ↔ workspace in a browser bundle, CLI ↔ DB module in a TUI/CLI tool, native shell ↔ DB process) MUST version-check at init. On version mismatch the boundary MUST refuse mutating operations; read operations MUST continue to work. The build label MUST NOT be used as the gate. | Goal 4 | <a id="ac-4"></a>AC-4 |
| **Always-reachable diagnostic escape.** A force-reset / force-unlock affordance MUST be reachable regardless of stuck app state. The specific form is shell-derived (URL parameter for web SPAs, e.g., `?gate=1`; CLI flag for terminal apps, e.g., `--reset`; key chord for native shells); the substrate is required everywhere. | Goal 2 | <a id="ac-6"></a>AC-6 |
| **Self-service field-debug substrate.** Every PNA MUST provide a field-debug substrate consisting of: a build label (AC-15), sanitized error capture, a diagnostic state-dump, a bug-report flow, the escape hatch from AC-6, a boot watchdog with named phase marks, and slow-boot persistence. Specific affordances are shell-derived (badge in a web UI; `--diag` subcommand in a CLI; native diagnostic menu); the substrate is required everywhere. | Goal 2 | <a id="ac-7"></a>AC-7 |
| **Auto-backup of private data on user-edit cadence.** The PNA MUST snapshot the Private store on a per-boot debounced schedule (not per-deploy). It MUST rotate snapshots to keep a small ring of recoverable points. | Goal 4 | <a id="ac-9"></a>AC-9 |
| **Re-imports of the Shared store are opt-in and non-destructive.** Re-imports MUST be opt-in — whether refreshed from the original source (a directory operator pushes an update) or re-mirrored from a centralized platform (the user re-exports their Google contacts). Before the user commits a re-import, the workspace MUST preview any private references that would be orphaned by the update. | Goal 1, Goal 4 | <a id="ac-10"></a>AC-10 |
| **Storage substrate detects concurrent access.** When another tab or process holds the data layer, the storage substrate MUST detect the conflict and surface it with a specific message (multi-tab in browsers, multi-process in native); a generic "unsupported" message MUST NOT be used. | Goal 4 | <a id="ac-11"></a>AC-11 |
| **Build label tied to source revision, substituted at build *and* serve time.** Each delivered artifact MUST carry a runtime-visible unique label tied to the source revision. The label MUST be substituted at both build time and serve time. Format is implementation-specific (`<YYYY-MM-DD>-<short-sha>` in fellows_local_db; whatever `--version` reports in CLI tools). | Goal 2 | <a id="ac-15"></a>AC-15 |
| **Communication-transport selection is user-driven.** The workspace MUST surface multiple transports — including secure / decentralized options when configured — and the user MUST choose per outreach. No transport MAY be hardcoded as the only available option. | Goal 3 | <a id="ac-16"></a>AC-16 |
| **Sourced provenance.** Every record in the Shared store MUST trace to a specific external source the user has explicitly configured. The toolkit MUST NOT introduce contact data the user hasn't approved. | Goal 2 | <a id="ac-17"></a>AC-17 |
| **Transports cannot read message contents.** A transport's acceptability is determined by the transport mechanism itself, not by the downstream chain it kicks off. `mailto:` passes (hands off to whichever client the user has configured; the downstream provider's behavior — Gmail, Outlook — is outside the toolkit's enforcement). Signal-class protocols pass (encryption-in-protocol). Workspaces MUST NOT offer centralized message-broker SaaS that decodes payloads as part of operating (Slack, Discord) as a PNA-eligible transport. Contact-graph retention by the transport is *not* part of the rule (too hard to enforce uniformly across protocols; varies by user threat model). | Goal 3 | <a id="ac-18"></a>AC-18 |
| **User-visible payload before send.** Any workspace-initiated communication MUST show the user the full payload — recipients, body, and any data merged in from the Shared or Private store — before the transport is launched. The user MUST be able to edit or cancel. This MUST apply even to bulk operations (e.g., "email this group of 50"). Workspaces MUST NOT auto-blast data through transports without the user seeing the composition. | Goal 3 | <a id="ac-19"></a>AC-19 |
| **LLM calls over user data are transports.** Any LLM invocation over Private or Shared data MUST be treated as a transport: a local model is the default; a cloud model MUST be opt-in per call; the user MUST see the prompt and any merged data before send. Extension of AC-18 and AC-19 to a new transport class. | Goal 3 | <a id="ac-20"></a><a id="ac-prm-a"></a>AC-20 |
| **Re-ingestion is always user-initiated.** Re-ingestion MUST be triggered by an explicit user action; the PNA MUST NOT background-poll source services (Google Contacts, IMAP, organizational directories). Strengthens AC-10: the user always knows when fresh data is being fetched. | Goal 1 | <a id="ac-21"></a><a id="ac-prm-d"></a>AC-21 |
| **Cloud AI clients require per-call consent for Private DB access via MCP.** Any MCP tool that returns Private DB rows MUST either refuse, or MUST require explicit per-session opt-in, when the consuming MCP client is not locally hosted. Local clients (Claude Desktop with a local model, Cursor + local Ollama) are the default green path; cloud clients (Claude API direct, OpenAI API, etc.) are opt-in per call. In practice this targets the Private Data Ops server; AC-1's class boundary at the MCP surface lets a user wire a cloud client to Shared Data Ops alone without triggering this AC — a separation the canonical two-store split makes *structural* (the Shared server physically cannot reach private rows), and which a single-store realization MUST instead enforce at the data layer for this guarantee to hold. Concrete realization of AC-20 at the MCP surface. | Goal 2, Goal 3 | <a id="ac-mcp-a"></a>AC-MCP-A |
| **MCP Communications tools stage outreach; the workspace launches.** A Communications MCP tool call MUST NOT directly fire a transport. It MUST return a staging ID with the full payload preview; the user MUST confirm via the workspace before the transport launches. The MCP server proposes; the workspace disposes. AC-19 is enforced at the workspace boundary and MUST NOT be bypassable by AI clients. | Goal 3 | <a id="ac-mcp-b"></a>AC-MCP-B |
| **Honest capability assessment.** A PNA MUST establish the runtime-substrate capabilities that bear on its commitments by *sound* means — probing the substrate, not trusting an unverified self-report (a feature-presence flag, a platform / UA string) — and MUST report the outcome truthfully, including an explicit *undetermined* where a capability cannot be established. It MUST NOT claim or rely on a capability it has not verified the substrate delivers. (Substrate-specific probes are realizations — e.g. RZ-2's worker-side OPFS detection in `axes.md`; a CLI's "is FTS5 compiled into this `sqlite3`" check.) | Goal 2 | <a id="ac-22"></a>AC-22 |
| **Source available for verification.** The source corresponding to a delivered artifact's build label (AC-15) MUST be available to the user and their tools, so the PNA's behavior and its conformance can be independently checked before it is trusted. The strong form is build-from-verifiable-source (the user clones, builds, and runs the evaluate flow before first use); source published alongside a served or packaged artifact is the baseline. An opaque artifact with no inspectable source does not satisfy this commitment — it is a departure to report (or to declare as an Exception), not a conformant flavor. | Goal 2 | <a id="ac-23"></a>AC-23 |

---

## Conditional architectural commitments

Conditional ACs are **Layer 1** — they survive a total technology swap (see [§ How the pieces fit together](#how-the-pieces-fit-together)) — but apply only when the PNA has a particular **behavioral property**, not when it picks a particular technology. Each is tagged below with the property that triggers it; the axis picks that *entail* each property are catalogued in [`axes.md`](axes.md), which links back here.

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. -->
| Commitment | Serves | Applies when (behavioral property) | ID |
|---|---|---|---|
| **No SaaS surface.** A server a PNA stands up MUST be a delivery channel, not a service: it MUST NOT expose per-user RW endpoints, persist private data, host an admin console, or operate cross-device sync. | Goal 3 | the PNA **operates a server** over its data | <a id="ac-2"></a>AC-2 |
| **Stale session never locks users out of cached data.** A rejected shared-side fetch (e.g. 401/403) MUST fall through to the local cache; fresh data MUST require an explicit user action. | Goal 1 | the PNA **gates data behind an authenticated refresh** | <a id="ac-5"></a>AC-5 |
| **Anti-enumeration + abuse-bounded analytics.** Authentication endpoints MUST return neutral payloads and enforce per-IP rate limits; a sanitized error sink MAY double as the analytics pipe but MUST NOT widen the privacy boundary. | Goal 3 | the PNA **operates an authentication server** (with a configured error sink) | <a id="ac-8"></a>AC-8 |
| **Multi-source dedup contract.** A stable `record_id` MUST survive merge across sources; the dedup flow MUST surface conflicts; per-source provenance MUST be recorded *per field*, not just per record. | Goal 2 | the PNA **mirrors more than one source** | <a id="ac-prm-b"></a>AC-PRM-B |
| **Authenticated same-host surface.** A same-host-reachable surface a PNA opens over its own Private/Shared data (a loopback HTTP daemon, a local socket) MUST be loopback-bound and authenticated to the user's own session, disclosing nothing to an unauthorized same-host reader; a non-loopback bind MUST require an explicit, documented opt-out. | Goal 3 | the PNA **exposes a same-host surface** over its data | <a id="ac-prm-h"></a>AC-PRM-H |

The two `AC-PRM-*` IDs here are frozen legacy identifiers (the suffix records that PRM first demonstrated them — provenance now lives in the [realization index](../docs/realization-index.md), not the ID). The Layer-2 *realizations* of these contracts on specific substrates (and of the universal ACs) live in [`axes.md`](axes.md) as the `RZ-*` family, beside the axis pick that brings them.

---

## Slots, Interfaces, and Sub-contracts
<a id="slot-map"></a>

> **Reference material — skip unless you're implementing or auditing a PNA.** This section is the architectural skeleton (the five slots and three interfaces), then the detailed, ID'd **sub-contracts** that decompose each. A first read can stop after the [Slots](#slots) and [Interfaces](#interfaces) tables; the sub-contracts below them are a per-piece checklist for builders and for the evaluate flow, not narrative.

The spec defines **five slots** (positions filled by code) and **three interfaces** (cross-cutting contracts spanning multiple slots). The Slot and Interface vocab terms are defined in [§ Vocabulary](#vocabulary).

**Required vs optional slots.** Three slots are **required**: **Ingestion** (get shared data in), **Storage** (the sovereign, sealed private layer that *is* the PNA's defining promise — canonically the two-store split), and **Workspace** (the surface where the user writes private data and confirms anything outbound). **Communications** and **Distribution** are **optional**: a PNA that never reaches out omits Communications — its comms ACs (AC-16/18/19) are then vacuous, like the MCP ACs when no MCP server is exposed — and a single-user PNA omits Distribution. The smallest conformant shape is the [Minimum Viable PNA](use_cases.md) (ingest + store + a minimal workspace to add notes). The Workspace is required but can be *minimal*: its form — GUI, TUI, CLI, native shell — is the `workspace-shell` axis. **MCP servers can *add* an AI-driven surface but cannot *replace* the Workspace in v0.1**, because the data-ops MCP servers are read-only (no private writes via MCP yet) and the Workspace is the human-in-the-loop consent boundary that AC-MCP-A/B require — the MCP server proposes, the Workspace disposes. (A headless, MCP-native PNA is a v0.2+ direction; see [`use_cases.md`](use_cases.md).)

Each slot has a code-level contract. The typed contracts — JSON Schema for RPC + handshake, OpenAPI fragments for distribution, SQL DDL (Data Definition Language) for schemas, TypeScript declaration for the Communications transport interface, JSON Schema for each canonical MCP server's tool surface — live in [`contracts/`](../contracts/).

Many Universal ACs (see [§ Universal architectural commitments](#universal-architectural-commitments)) cite specific slots in their wording. The slots and interfaces are the architectural skeleton — the named roles every PNA fills, which survive a [total technology swap](#how-the-pieces-fit-together) — and the Layer-1 ACs are the load-bearing constraints over them. Each slot decomposes further into named sub-contracts — see [§ Sub-contracts per slot](#sub-contracts-per-slot) below — which are **Layer 2** (how a slot is realized on a specific stack); a builder targets each piece individually, keeping the Layer-1 AC and adapting the Layer-2 realization to their stack.

### Slots

| Slot | Purpose |
|---|---|
| <a id="slot-ingestion"></a>**Ingestion** | Produces a Shared DB conforming to the Shared schema, from one or many external sources. |
| <a id="slot-storage"></a>**Storage** | Owns both DB files (Shared + Private) and serves queries. Implements AC-1's sovereign/sealed private-layer boundary (canonically the two-store split) and AC-4's cross-boundary version handshake. |
| <a id="slot-workspace"></a>**Workspace** *(required)* | The user-facing surface — routing, rendering shared data, reading and **writing private data**, and (when Communications is present) **confirming any outbound send**. Its form is the `workspace-shell` axis (GUI/TUI/CLI/native). Enforces AC-19's user-visible payload before send. |
| <a id="slot-communications"></a>**Communications** *(optional)* | Pluggable transport layer for outreach. Honors AC-16's user-driven selection and AC-18's transport eligibility rule. Omitted by a PNA that never reaches out (its comms ACs are then vacuous). |
| <a id="slot-distribution"></a>**Distribution** *(optional)* | Delivers the PNA to other users' devices. When the PNA isn't distributed (single-user CLI / native), this slot is empty. |

### Interfaces

| Interface | Purpose |
|---|---|
| <a id="iface-shared-schema"></a>**Shared schema** | Data contract for the Shared DB — tables, columns, optional FTS (Full-Text Search) structure, optional per-record asset URL conventions. Produced by Ingestion; consumed by Storage and Workspace. |
| <a id="iface-private-schema"></a>**Private schema** | Data contract for the Private DB — `groups`, `group_members`, `record_tags`, `record_notes`, `settings`, opt-in `record_comms_history`. Owned by Storage; accessed by Workspace through Storage. Durability rules (survives app update + Clear App Cache; wiped only by Reset Everything) are part of the contract. |
| <a id="iface-debug-contract"></a>**Debug contract** | Capabilities every slot must implement: build label substitution at build *and* serve time (AC-15), sanitized error capture (with sink endpoint when configured), diagnostic state-dump, bug-report flow, always-reachable escape hatch (AC-6), boot watchdog with named phase marks. |

### Sub-contracts per slot

Each slot's contract decomposes into named sub-contracts so an AI building or rewriting a PNA can target each piece individually. Naming convention: two-letter prefix per slot (`WS-`, `ST-`, `IN-`, `CO-`, `DI-`) and per interface (`SH-`, `PR-`, `DB-`), then dash, then monotonic integer. New sub-contracts get the next integer; numbers don't get reused.

Sub-contracts cite the universal ACs they realize where appropriate; the AC table above remains the single source of truth for the architectural commitments themselves.

**These sub-contracts are Layer 2** (see [§ How the pieces fit together](#how-the-pieces-fit-together)). They decompose *how* each slot is realized on a concrete stack, not *what* the PNA must promise — that is the [Layer-1 ACs](#universal-architectural-commitments) they cite. Most are generalized from `fellows_local_db`'s browser implementation (the toolkit's first reference design) and carry "or substrate-equivalent" hedges for non-browser flavors; a few still name browser specifics outright (e.g. ST-1's OPFS-SAH-Pool VFS, ST-3's exact `{id, op, args}` RPC envelope, WS-7's literal `fellows_authenticated_once` localStorage key). Read them as a builder's checklist *for that lineage* — adapt per stack, do not treat them as universal contracts. As reference designs on other substrates land, the genuinely-universal pieces factor up into ACs and the stack-specific ones stay realizations. (The `RZ-*` family in [`axes.md`](axes.md) is the other half of Layer 2 — realizations a specific *axis pick* brings; these sub-contracts are the per-slot decomposition of the same lineage.)

#### Workspace (`WS-`)

- <a id="ws-1"></a>**WS-1: Boot persona.** The workspace MUST implement a function that decides "directory mode" vs "distribution gate" given standalone-display, persistence marker, and force-gate URL. This function drives the entire boot flow.
- <a id="ws-2"></a>**WS-2: Routing.** Routing MUST be hash-based or equivalent. The workspace MUST support per-route focus modes; URL-shareable filter state SHOULD be supported where applicable.
- <a id="ws-3"></a>**WS-3: Render contracts.** Each view MUST honor a per-route render contract specifying what the view shows. Render contracts MUST include orphan-row rendering after Shared DB updates (per AC-10).
- <a id="ws-4"></a>**WS-4: Data provider abstraction.** The workspace MUST expose a three-tier provider (worker / api+idb / api) with mid-boot hot-swap on auth failure (per AC-5). The active provider MUST be reachable via a single source of truth (`window.__dataProvider` in the JS-specific realization; non-browser PNAs realize this differently).
- <a id="ws-5"></a>**WS-5: Boot orchestration.** The workspace MUST emit named `bootMarks` at meaningful transitions. On watchdog timeout it MUST surface a recovery panel naming the last-completed mark. Slow-boot persistence to localStorage across sessions MUST be implemented.
- <a id="ws-6"></a>**WS-6: Capability-failure panel.** The workspace MUST render a capability-failure panel (`renderLocalDataUnavailablePanel(feature)`-style) for OPFS / version-skew / multi-tab-conflict failures.
- <a id="ws-7"></a>**WS-7: Persistence-marker.** The workspace MUST preserve exactly one localStorage key across Clear App Cache (the "this origin authenticated once" marker; spelled `fellows_authenticated_once` in fellows_local_db).
- <a id="ws-8"></a>**WS-8: Local-search fallback.** The workspace MUST provide search over the cached Shared DB when the network is offline.
- <a id="ws-9"></a>**WS-9: Sanitization discipline.** The workspace MUST escape HTML (`escapeHtml`) for all user-supplied data, MUST use parameterized `?` placeholders for all SQL, and MUST validate image paths against traversal.
- <a id="ws-10"></a>**WS-10: User-visible payload before send (AC-19).** The workspace MUST show the full composition before any communication launches.

Cross-slot: WS-4 sits at the boundary with Storage (the `worker` tier is RPC into ST-3); WS-5 implements the boot side of DB-3.

#### Storage (`ST-`)

- <a id="st-1"></a>**ST-1: Substrate.** The Storage slot MUST use a single dedicated worker, the OPFS-SAH-Pool VFS (Storage Access Handle Pool Virtual File System), and a sqlite-wasm runtime (or the substrate-equivalent for non-browser flavors). The worker MUST be the only context that calls `navigator.storage.getDirectory` or opens a `FileSystemSyncAccessHandle` (per RZ-1).
- <a id="st-2"></a>**ST-2: Init handshake.** The first RPC across the boundary MUST be `op='init'`. Init MUST return `{workerRpcVersion, schemaVersion, buildLabel, opfsCapable, hasSharedDb, hasPrivateDb, poolFiles, trace}`. Capability detection MUST happen inside this op (per RZ-2, realizing AC-22). Typed contract: [`contracts/worker-init-handshake.schema.json`](../contracts/worker-init-handshake.schema.json).
- <a id="st-3"></a>**ST-3: RPC protocol.** The RPC envelope MUST be `{id, op, args}` ↔ `{id, ok, result|error}`. Fan-in dispatch MUST be sequence-numbered via a pending Map. On `worker.onerror`, all pending RPCs MUST be rejected so callers can fall back instead of hanging. Typed contract: [`contracts/worker-rpc-protocol.schema.json`](../contracts/worker-rpc-protocol.schema.json).
- <a id="st-4"></a>**ST-4: Two-database management.** The Storage slot MUST manage a Private DB (RW) and a Shared DB (RO). Cross-DB joins MUST use `ATTACH ?mode=ro`, attached once per init in the worker.
- <a id="st-5"></a>**ST-5: Schema bootstrap.** Storage MUST use `CREATE IF NOT EXISTS` for both schemas, MUST set `PRAGMA foreign_keys=ON` per connection, and MUST set `PRAGMA user_version` to the schema version. The bootstrap MUST be idempotent so older backups gain newer tables on restore.
- <a id="st-6"></a>**ST-6: Auto-backup.** Storage MUST take per-boot debounced snapshots of the Private DB to OPFS root (outside the SAH-pool dir, so snapshots survive sqlite-wasm operations). Rotation MUST be by sorted ISO filename. Per AC-9.
- <a id="st-7"></a>**ST-7: Restore.** Restore MUST accept either a user-supplied file or a recent auto-backup. It MUST validate via `PRAGMA quick_check` plus schema check. The pre-restore state MUST be snapshotted to the same rotation. The swap MUST be atomic.
- <a id="st-8"></a>**ST-8: Opt-in update flow.** The update flow MUST be `compareSha → previewSwap → applySwap | cancelSwap`. An opaque per-session `stagingId` MUST be used so a stale page can't accidentally commit. The affected-member preview MUST be computed from joined Private DB references. Per AC-10.
- <a id="st-9"></a>**ST-9: Multi-tab detection.** `OWNERSHIP_CONFLICT` MUST be tagged on `installOpfsSAHPoolVfs()` failure so WS-6 can render a specific multi-tab panel (per AC-11). Non-browser flavors realize the equivalent file-lock detection per RZ-5.
- <a id="st-10"></a>**ST-10: Reset Everything.** A `wipeAll` RPC MUST be exposed that closes both DBs, calls `removeVfs()`, and iterates the OPFS root removing every entry. The caller MUST reload after.
- <a id="st-11"></a>**ST-11: Diagnostics.** Storage MUST expose `getOpfsInventory`, `getTrace`, `getVersions`, `getSharedDbMeta`. These MUST be read-only — pure reads, no fetches.

Cross-slot: ST-2/3 are the contract WS-4 calls; ST-7's schema re-bootstrap respects PR-3.

#### Ingestion (`IN-`)

- <a id="in-1"></a>**IN-1: Source adapter.** The Ingestion slot MUST produce bytes conforming to the Shared schema (SH-1 through SH-3). The adapter is app-specific.
- <a id="in-2"></a>**IN-2: Output validation.** Output MUST pass `PRAGMA quick_check`. The primary record table MUST have ≥1 row (zero-row guard prevents catastrophic orphaning of every Private DB reference).
- <a id="in-3"></a>**IN-3: Sourced provenance (AC-17).** Every record MUST trace to a specific external source the user has configured.
- <a id="in-4"></a>**IN-4: Re-ingestion mechanics.** Re-ingestion MUST be atomic stage → validate → swap. It MUST be non-destructive of Private DB references. An orphan preview MUST be provided (per AC-10, surfaced via ST-8 + WS-3).

Cross-slot: IN-4 hands off to ST-8 for the actual stage/swap; SH-5 is the Shared-side view of the same transition.

#### Communications (`CO-`)

- <a id="co-1"></a>**CO-1: Transport interface.** Each transport MUST implement `canHandle(action) → bool`, `launch(action, payload) → Promise<launchResult>`, and `descriptor() → {id, name, secureLevel?, …}`. Typed contract: [`contracts/transport-interface.d.ts`](../contracts/transport-interface.d.ts).
- <a id="co-2"></a>**CO-2: Action set.** The action enum MUST include `email_one`, `email_group_cc`, `email_group_bcc`, `direct_message_one`, `share_link_one`, `share_link_group`. New actions MAY be added in future toolkit version bumps.
- <a id="co-3"></a>**CO-3: Transport eligibility (AC-18).** A transport's mechanism MUST NOT read message contents.
- <a id="co-4"></a>**CO-4: User-driven selection (AC-16).** The workspace MUST surface multiple transports; the user MUST pick per outreach.
- <a id="co-5"></a>**CO-5: User-visible payload (AC-19).** The workspace MUST show the full payload (recipients, body, merged data) before launch.
- <a id="co-6"></a>**CO-6: Distinction from distribution-mechanism transports.** A distribution flavor's auth-link transport (e.g., Postmark in fellows_local_db's magic-link distribution) is governed by Distribution slot contracts, not by CO-3.

Cross-slot: CO-4 is observable from WS (the shell renders the picker); CO-5 is the same contract as WS-10, dual-listed because both slots co-implement.

#### Distribution (`DI-`) — optional

- <a id="di-1"></a>**DI-1: Install path.** The Distribution slot MUST provide bundle delivery, a verified initial Shared DB, and a session bootstrap.
- <a id="di-2"></a>**DI-2: Update path.** The update path MUST cover the shell and worker file via the service worker plus cache versioning. Shared DB updates MUST be user-driven (per AC-10), not automatic.
- <a id="di-3"></a>**DI-3: Auth contract.** The Distribution slot MUST expose `GET /api/auth/status`, `POST /api/send-unlock`, `POST /api/verify-token`, and `POST /api/logout`. The session cookie MUST be signed using HMAC (Hash-based Message Authentication Code) and version-prefixed (so prior versions reject cleanly post-deploy). Typed contract: [`contracts/distribution-auth.openapi.yaml`](../contracts/distribution-auth.openapi.yaml).
- <a id="di-4"></a>**DI-4: Anti-enum + rate limit (AC-8).** `send-unlock` and `client-errors` MUST always return 200 / 204. Per-IP and per-email-hash rate limits MUST be enforced. `verify-token` MUST use distinct expired/invalid error strings.
- <a id="di-5"></a>**DI-5: Server hardening.** The Distribution server MUST terminate TLS on :443 → 127.0.0.1 origin. It MUST send COOP (Cross-Origin Opener Policy) and COEP (Cross-Origin Embedder Policy) headers (RZ-3). POST body MUST be capped at 16KB. The server MUST NOT expose per-user RW endpoints (AC-2). Caching MUST be status-aware (4xx/5xx MUST NOT be long-cached).
- <a id="di-6"></a>**DI-6: PWA-specific gotchas (when distribution medium is a PWA).** The manifest MUST be minimal — no `related_applications`, no `share_target` POST. The service worker MUST be network-first for HTML/JS/CSS/SW + worker file and cache-first for the vendored runtime. A separate asset cache MUST be used. The Shared DB URL MUST be bypassed in the SW fetch handler (RZ-4).

Cross-slot: DI-2's update path triggers WS's "New version available — Reload" banner; DI-3 outcomes feed WS-1's persona decision.

#### Shared schema (`SH-`)

- <a id="sh-1"></a>**SH-1: Primary record table.** The Shared schema MUST define a primary record table with `record_id` PK, `slug` UNIQUE, `name`, app-defined display columns, and `extra_json TEXT` overflow. Typed contract: [`contracts/shared-db.schema.sql`](../contracts/shared-db.schema.sql).
- <a id="sh-2"></a>**SH-2: Optional FTS5 virtual table.** Implementations MAY provide an FTS5 virtual table indexing whichever columns the workspace wants searchable.
- <a id="sh-3"></a>**SH-3: Optional per-record asset URL convention.** Implementations MAY use a `/images/<slug>.{jpg,png}` style — cacheable, immutable, slug-keyed.
- <a id="sh-4"></a>**SH-4: Read-only enforcement.** Cross-DB joins MUST use ATTACH `?mode=ro`. Stray writes MUST raise `OperationalError`.
- <a id="sh-5"></a>**SH-5: Atomic re-import semantics with orphan preview (AC-10).** Re-imports MUST be stage → validate → swap. A pre-swap impact preview MUST list Private DB references that would be orphaned.
- <a id="sh-6"></a>**SH-6: Sourced-provenance per record (AC-17).** Multi-source PNAs MUST add a `source` column. Single-source PNAs MAY omit it.

Cross-slot: SH-5 is implemented by ST-8.

#### Private schema (`PR-`)

- <a id="pr-1"></a>**PR-1: Core tables.** The Private schema MUST define `groups`, `group_members`, `record_tags`, `record_notes`, and `settings(workspace_id, key, value)` with composite PK. Typed contract: [`contracts/private-db.schema.sql`](../contracts/private-db.schema.sql).
- <a id="pr-2"></a>**PR-2: Opt-in tables.** `record_comms_history` MAY be present and MUST be disabled by default (`settings['comms_history_enabled']='1'` to enable). The user MUST have full read/edit/delete control.
- <a id="pr-3"></a>**PR-3: Schema metadata.** Implementations MUST set `PRAGMA user_version` and MUST set `PRAGMA foreign_keys=ON` per connection.
- <a id="pr-4"></a>**PR-4: Durability.** The Private DB MUST NOT be replaced on app update. It MUST survive Clear App Cache. Only Reset Everything (ST-10) MAY wipe it.
- <a id="pr-5"></a>**PR-5: Backup/restore conformance.** Implementations MUST use idempotent CREATE IF NOT EXISTS so older backups gain newer tables on restore.
- <a id="pr-6"></a>**PR-6: Human-readable export (recommended).** Implementations SHOULD provide an export of the Private DB to a flat, human-readable format in addition to the canonical SQLite file — for example CSV per table, JSON with the schema embedded, or a Markdown vault keyed by `record_id`. The export MUST be readable without any PNA tooling (a generic CSV / JSON / Markdown reader suffices). The canonical SQLite file remains the authoritative form; the human-readable export is a portability escape hatch, not a sync surrogate — implementations MUST NOT treat it as a guaranteed re-import surface, and re-import stays on the PR-5 SQLite path. *Verification: a deterministic check that every exported file parses with a standard-library reader and requires no project code — see [`tools/export-readable-lint.py`](../tools/export-readable-lint.py).*

Cross-slot: PR-4 is enforced by ST-1 (separate file from Shared DB) and ST-10 (Reset Everything is the only wipe path); PR-5 is exercised by ST-7; PR-6 is produced by Storage (export bytes) and surfaced by the Workspace (export action).

#### Debug contract (`DB-`)

- <a id="db-1"></a>**DB-1: Build label substitution.** Build label substitution MUST happen at both build time and serve time (AC-15). The format `<YYYY-MM-DD>-<short-sha>` is RECOMMENDED; implementations MAY pick another stable format.
- <a id="db-2"></a>**DB-2: Build badge.** The workspace MUST provide an always-visible runtime display showing local + server labels.
- <a id="db-3"></a>**DB-3: Boot phase marks + watchdog.** Implementations MUST emit named `bootMarks`. A watchdog timeout MUST surface a recovery panel. Slow-boot persistence across sessions MUST be implemented.
- <a id="db-4"></a>**DB-4: Sanitized error sink.** A POST endpoint MUST be exposed with: 16KB cap, rate limit, always-204 response, an allowlisted `kind=` enum, and server-side free-text sanitization. Typed contract: [`contracts/client-errors-payload.schema.json`](../contracts/client-errors-payload.schema.json).
- <a id="db-5"></a>**DB-5: Sink-as-analytics.** Adding a new `kind=` enum value MUST be the only widening lever for analytics. No separate analytics endpoint MAY be added; no separate identifier scheme MAY be introduced.
- <a id="db-6"></a>**DB-6: Bug-report dialog.** The workspace MUST provide a bug-report dialog that collects DB-2 + DB-3 + DB-4 ring contents and opens mailto to the configured maintainer.
- <a id="db-7"></a>**DB-7: Force-gate / force-reset escape hatch.** The escape hatch MUST be reachable from `?diag` (or the substrate-equivalent diagnostics affordance) and from a hardcoded URL parameter regardless of cookie / localStorage state (per AC-6).
- <a id="db-8"></a>**DB-8: Configurability.** Every part of the Debug substrate MUST be configurable. Purely-personal PNAs MAY have an empty sink and no maintainer mailbox; the substrate MUST still work.
- <a id="db-9"></a>**DB-9: Test affordance.** The workspace MUST expose the active data provider on a stable global (`window.__dataProvider` in fellows_local_db) so test suites can drive the contracts the same way the workspace does, without a separate test-only seam.

Cross-slot: every component implements DB-1; WS instantiates DB-2, DB-3, DB-6, DB-7, DB-9; DI hosts DB-4 (when present).

### Cross-slot sub-contract threads

Sub-contracts that span slots, formalized:

- **Build-label discipline (AC-15):** every component implements DB-1.
- **Update notification:** DI-2 → SW banner → WS-3 reload affordance.
- **Opt-in directory update (AC-10):** IN-4 → ST-8 → SH-5 → WS-3 (orphan render).
- **Storage RPC boundary:** WS-4 calls ST-3 / ST-4 / etc.; ST-2's handshake gates whether mutations are allowed (AC-4).
- **Restore data flow:** WS (file picker / backup picker UI) → ST-7 → PR-5 (re-bootstrap).
- **Human-readable export (PR-6):** ST produces the export bytes; WS exposes the export action. One-way — re-import stays on the PR-5 SQLite path.
- **User-aware payload (AC-19):** WS-10 ↔ CO-5 — dual-listed because both slots co-implement.
- **Capability-failure surfacing:** ST-2 (`opfsCapable=false`) → WS-6 (panel render); ST-9 (`OWNERSHIP_CONFLICT`) → WS-6 (multi-tab variant).
- **Diagnostic substrate (DB-\*):** every slot logs to DB-4; WS surfaces DB-2/3/6/7/9.

These cross-slot threads are what make the spec describe a *system* rather than a bag of slots.

### Decomposition decisions

- **No slots split.** Each top-level slot keeps a single contract surface; sub-contracts give it texture without fragmenting the toolkit's mental model. The toolkit may internally factor slots further (Storage in particular has eleven internal contracts already), but the spec exposes one slot per concern.
- **Cross-slot ACs land in both slots' sub-contracts.** AC-19 is both WS-10 and CO-5; AC-10 fans out into IN-4 + ST-8 + SH-5 + WS-3; etc. The AC table remains the single source of truth; sub-contracts cite ACs where they land.
- **One naming convention.** `<slot prefix>-<integer>`, monotonic per slot. No renumbering as items are added; new sub-contracts get the next integer.

---

## Scope and versioning

This spec is intentionally narrow. It addresses the user demand and runtime realities we can implement and deploy now. New demand develops further versions of the toolkit; reference designs continue to satisfy whatever Toolkit-Version they were built against.

The deferrals below are **deliberate staging**, not mere omission — the *evolutionary stance* of the [Preamble](#preamble): each is a capability the spec declines to mandate until a reference design demonstrates it is usable *and* safe, at which point it earns a version bump. Several (cross-device sync, federation, a richer storage substrate) are exactly the "harder capabilities" that framing defers.

**This is the PNA Spec, at Toolkit-Version 0.1.** When new demand surfaces or runtime constraints shift, we bump the toolkit version, declare what changed in [`CHANGELOG.md`](CHANGELOG.md), and update the architectural commitments accordingly.

Items deliberately deferred to future toolkit versions:

- **Privacy reclassification migration mechanics.** The Preamble commits PNAs to honoring user-driven privacy reclassification of a record (shared → private). The *implementation pattern* — does the record stay in the Shared DB with a private-side override row that supersedes? Get copied into the Private DB and removed from the Shared DB on next re-mirror? — is not pinned in v0.1. The contract is declared; the migration is left for a future version when the first reference design needs it.
- **Multi-source dedup implementation.** AC-PRM-B (a conditional AC in [`axes.md`](axes.md), triggered when a PNA mirrors more than one source) captures the v0.1 commitment for `ingestion:multi-source-merge-with-dedup` flavors — stable `record_id` survives merge, dedup wizard surfaces conflicts, per-field provenance — now demonstrated by the [prm](https://github.com/richbodo/prm) reference design. The finer implementation choices (merge UI, conflict-resolution algorithms) remain per-design, not pinned by the spec.
- **Per-database (or finer) transport requirements.** A future toolkit version may let each database — Shared, Private, or any custom database in a richer PNA — declare which transport properties it requires for outbound flow. v0.1 handles the data-transport matching implicitly: AC-18 filters out transports that read content; AC-19 ensures the user sees the full payload before launch; the user resolves the matching in the moment. Explicit per-DB rules (workspaces auto-suggesting or auto-filtering transports based on source DB sensitivity) land when a reference design has an auto-send feature that needs them.
- **At-rest encryption against local device access.** v0.1's threat model is *network and platform exposure* — data leaving the device to SaaS, surveillance, or social-graph mining (Goal 3). Defending against an adversary with **local access to the device itself** (a lost, stolen, or seized machine; a shared computer) is deliberately out of scope at the application layer: OS full-disk encryption (FileVault / BitLocker / LUKS) is the right layer for it, and app-level at-rest encryption is largely redundant with FDE where it works and absent where it matters (a running, unlocked machine holds the key in memory regardless). The toolkit therefore does **not** make at-rest encryption a universal AC — a boolean "encrypted at rest" would invite false assurance and tension with Goal 4 (a lost key is lost data). At-rest encryption remains available as the `native-sqlcipher` storage flavor (see [`axes.md`](axes.md)); its key-storage and -rotation ACs are deferred until a SQLCipher reference design demonstrates them, and any such attestation discloses a per-dimension **strength profile** ([`exceptions.md`](exceptions.md) § Strength profiles) rather than a single graded claim. Full rationale: [`docs/PriorArt.md`](../docs/PriorArt.md) § Design notes.
- **Cross-device sync.** Out of scope for v0.1. Future versions may declare a sync protocol; v0.1 explicitly does not.
- **Federated P2P capabilities.** Signed-repo asset pulls (a community member's photos), community-stats aggregation tools (the CRT vision). Out of scope for v0.1.
- **Formally verifiable code.** A longer-arc goal. v0.1 aims for AI-checkable contracts (markdown prose + JSON Schema / OpenAPI / SQL DDL / TypeScript declarations); formal verification (TLA+ / Alloy / etc.) is reserved for a later version.

When any of these become near-term, they get a v0.2+ spec bump and the relevant architectural commitments are revised.
