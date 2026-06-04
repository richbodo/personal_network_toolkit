# PNA Spec

<!-- EDITING NOTE — machine-parsed tables: the ID-bearing tables in this file (the architectural-commitment tables) are read by tools/lint-spec-ids.py AND by external report writers (reference-design conformance reports), and their `<a id>` row anchors are deep-linked from those reports. Treat each such table's columns, headers, and IDs as an API: if you change one, update those consumers — and the lint's self-tests (tools/tests/lint_selftest.py) — in the same change. The lint finds columns by header name, so the ID may sit in any column; it currently lives in the last column. -->

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This document is the universal specification for personal network applications (PNAs). Reference designs declare conformance to a specific Toolkit-Version and to a specific application flavor (defined by a constellation of feature axis picks). A PNA conforms to this spec if it satisfies the universal architectural commitments and the axis-derived contracts for each of its declared axis picks, listed herein.  Each reference design's specialization lives in its own repo (ex: fellows_local_db's specialization is at [`docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md)).

---

## Preamble

Two shifts are arriving at the same time that make [PNAs](#vocab-pna) necessary.  First, data is still flowing into SaaS, but trust is flowing out: users are increasingly unwilling to trust SaaS vendors (Facebook, Google, Apple, etc.) at all, nevermind with knowing who they talk to about politics or mental health. At the same time, edge compute and AI agents capable of running serious work locally are arriving fast. The first shift creates demand for tools that keep user data sovereign; the second makes such tools practical to build, run, and recompose at the user's own pace.

A personal network application is a tool for users to manage and use contact and relationship data that makes up their personal networks. A PNA handles a user's contact data and personal-relationship data with strong, declared contracts about how that data is treated (see the [Goals](#goals) and Architectural Committments below). The PNA separates the concerns of editing data that is shared with other systems from data that is created and held locally and privately.

v0.1 PNAs all operate downstream of SaaS systems of record — they do not modify contact data, although a contact manager might well exist as a [plugin](#vocab-plugin) to a PNA, or vice-versa. What distinguishes the niche is the architectural promise: [shared data](#vocab-shared-data) is local-first and replaceable; [private data](#vocab-private-data) is sovereign and protected; the user can reclassify a record's privacy at any time, and the PNA honors it durably; communication transports are user-chosen to meet the user's privacy and other requirements; the user can reason about where their data lives without trusting a vendor.

With PNAs, we have **credible interop** between SaaS systems and user-owned software.  Contact and relationship data is the **root** of personal networks and personal social network graphs - we have to get that local before we can take control of the whole graph.

And taking control is the point, not the endpoint. Once that root is local and the private layer over it stays sovereign, local AI can finally do serious work over your own relationship graph — search, recall, reaching out — and you compound a private store of relationship knowledge that grows more valuable over time, even as the SaaS services it was sourced from stay replaceable. The goals below are the preconditions; *working your own graph* is the payoff they make possible.

Without PNAs, or something like them, we often go to a list of contacts in linkedin or facebook and are overwhelmed by the noise.  The number of non-relationships in the contact list, manipulation through feeds, and notifications keep us on those sites as long as possible, often never solving any relational need, even if it is extremely urgent and sensitive.  This makes it much harder for many to improve individual and community health.

### Vision

One longer-arc target is an ecosystem of cooperating PNAs on a single user's device — a [Personal Relationship Manager](#vocab-use-case) (PRM - where private relationship data lives) running alongside one or more Directory Archives, a Contact Manager, and a Calendar app, each in its own bundle and sharing data as per their contracts.

The PRM acts as the [meta-workspace](#vocab-workspace): relationship data layered on top of a deduplicated read-only meta-view composed from the other apps' shared stores (Bob's cell from Google + work history from a fellowship directory + email from a Facebook export, resolved into one coherent contact view; the PRM's private overlay attached through stable IDs). The user can also work in clean per-app workspaces when they want a single context. Composing the meta-view requires per-source connectors, dedup with conflict resolution, and disciplined provenance — work for later toolkit versions. The eventual *ecosystem [reference design](#vocab-reference-design)* is the goal; v0.1 ships one PNA (fellows_local_db) and the spec it conforms to, along with [MCP servers](#vocab-mcp-server) (MCP = Anthropic's Model Context Protocol), with the architectural seams sized to let the ecosystem grow into place.

PNAs that participate in such an ecosystem need to be reachable not just to humans but to AI agents acting on the user's behalf. The spec therefore defines MCP server interfaces at five canonical connection points, split along the Shared / Private privacy boundary so an AI client can be wired to one without the other:

- A **Shared Data Ops server** — read access over the [Shared DB](#vocab-shared-db-private-db) (mirrored contact data).
- A **Private Data Ops server** — read access over the [Private DB](#vocab-shared-db-private-db) (user-owned relationship data); AC-MCP-A applies.
- An **Ingestion server** — drives imports, dedup, orphan preview.
- A **Communications server** — stages outreach for workspace-mediated user confirmation per AC-19 (the workspace launches the transport, not the MCP server — AC-MCP-B).
- A **Diagnostics server** — read-only access to the Debug contract.

An AI client (Claude Desktop, Cursor, a local-Ollama-backed agent, or any MCP-capable runtime) can drive a PNA through these servers without modifying its core; canonical implementations will ship with the personal_network_toolkit. Cloud AI clients (anything that sends Private DB rows off-device) require explicit per-call consent — see AC-MCP-A in [§ Universal architectural commitments](#universal-architectural-commitments). v1 surfaces are read-only on both data-ops servers; tool-side write contracts (Private DB CRUD — Create, Read, Update, Delete; message-send confirmation on Comms) land in a later toolkit version.

*Future direction — conformance evaluation as a precondition for ecosystem interop.* As the ecosystem grows, conformance evaluation may become a precondition for runtime interop between PNAs. Today an AI client wires two PNAs together by trusting each implements the canonical contracts; tomorrow, in a larger ecosystem with PNAs the user hasn't personally audited, a *systems-level conformance test* — does this candidate PNA honor the architectural commitments before I let it touch my Private DB? — becomes a natural precondition. This requires rethinking the spec at the systems level: the test isn't whether one PNA conforms in isolation but whether the cooperation across PNAs preserves the spec's guarantees. v0.1 doesn't define this; the present-day evaluation surface (PNA-by-PNA conformance check, performed by an LLM (Large Language Model) consuming this spec) is the closest analog. A later toolkit version may formalize the runtime-interop variant.

---

## Vocabulary

Worked examples below cite `fellows_local_db` as the first reference design — its concrete choices live in [`fellows_local_db/docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).

- **Axes.** Axes are areas of functionality that need to be defined when building a PNA. Each Axis offers a pre-defined, limited number of choices to the builder — internally we call these the builder's "Axis picks", and they are the first set of decisions that need to be made before building.

  An example of an Axis is the **distribution** axis, which offers the Axis picks `web-bundle-with-magic-link` (fellows_local_db's pick), `never-distributed-single-user` (PRM's likely pick), `web-bundle-open`, `app-store-native`, `sideloaded-native` — the builder picks one.

  v0.1 names these Axes: distribution, storage substrate, ingestion shape, workspace shell, comms transport set, MCP-exposure. The full catalog of attested picks per Axis lives in [`axes.md`](axes.md).

- **Axis pick.** One value on one Axis. Written `axis:value` — for instance `storage:opfs-sqlite-wasm`, `distribution:web-bundle-with-magic-link`. The set of attested picks per Axis is enumerated in [`axes.md`](axes.md).

- **Flavor.** The full constellation of axis picks for a specific PNA. fellows_local_db's flavor: `distribution:web-bundle-with-magic-link + storage:opfs-sqlite-wasm + ingestion:single-source-static-mirror + workspace-shell:vanilla-js-spa + comms:mailto-only + mcp-exposure:shared+private+comms`. Two PNAs of the same use case can have different flavors (a TUI PRM vs. a Tauri-wrapped GUI PRM share the use case but differ on workspace shell and storage). A flavor + a use case together fully identify a PNA's shape.

- **Interface.** A contract that spans multiple slots. Where a slot is filled by *one* code module, an interface is a shared constraint — either a data shape that multiple slots produce and consume (the Shared and Private DB schemas), or a capability requirement every slot must implement (the Debug contract). v0.1 names three interfaces: **Shared schema**, **Private schema**, **Debug contract**. Catalogued in [§ Slots, Interfaces, and Sub-contracts](#slot-map) alongside the slots they bind.

- <a id="vocab-mcp-server"></a>**MCP server.** A process exposing PNA capabilities as MCP tools (Anthropic's Model Context Protocol — JSON-RPC, a JSON-based Remote Procedure Call format, over stdio or socket). The spec defines five canonical MCP servers per PNA, structured around the Shared / Private privacy boundary so an AI client can be wired to one without the other:

  - **Shared Data Ops** — read access over the Shared DB (mirrored contact data; AC-MCP-A is not triggered, because no Private DB rows flow through this surface).
  - **Private Data Ops** — read access over the Private DB (user-owned relationship data; AC-MCP-A applies — cloud clients require per-call consent).
  - **Ingestion** — drives imports, dedup, orphan preview.
  - **Communications** — stages outreach for workspace-mediated user confirmation (AC-MCP-B; the MCP server proposes, the workspace disposes).
  - **Diagnostics** — read-only access to the Debug contract.

  Splitting Data ops along the Shared / Private boundary mirrors the storage split (AC-1) at the MCP surface: the privacy posture of each tool call is determined by which server it lands on, not by an in-server gate. An AI client (Claude Desktop, Cursor, a local-Ollama-backed agent, etc.) consumes these servers to drive the PNA. v1 reference implementations expose read-only surfaces only; future toolkit versions may add write-side tools (Private DB CRUD, Comms message-send confirmation) as separate contracts. MCP servers are how multiple PNAs cooperate at runtime: a PNA exposing MCP becomes externally reachable so an AI client can wire multiple PNAs together on the user's device even though each is its own bundle.

- **Mirroring.** The act of producing a fresh shared DB from an external source of shared data. A snapshot is created by the Ingestion component. Re-mirrors are atomic from the workspace's view (stage, validate, swap) and never silently orphan private references.

- <a id="vocab-pna"></a>**Personal network application (PNA).** A PNA is an application that helps a user view contact data and work on relationship data over it as a firewalled data layer with higher security needs than the contact data. The PNA runs local-only, never as SaaS - servers are only used for distribution and app updates, and only where appropriate. The PNA bridges SaaS data (which should never contain private relationship data) into a much more functional, customizable user-owned work environment suitable for viewing personal networks, updating private data about them, and interacting with them. A PNA MAY deliberately and temporarily depart from this definition (or from a named AC) by **raising an Exception** — see [`exceptions.md`](exceptions.md). Raising any exception exits "PNA mode"; the PNA stays conformant only while every active exception is handled to the exceptions.md handler contract.

  [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) is one PNA reference design — making a directory archive useful and fast - providing a credible exit from a SaaS directory system. Another PNA reference design would be a PRM - an app that aggregates personal contact data ingested from the big SaaS providers and lets the user operate privately on that data, adding privacy-sensitive notes, searching, and launching tasks from the app. PNAs bridge the old world of SaaS and offer private, custom tools to operate on contact data.

- <a id="vocab-plugin"></a>**Plugin / extension.** Anything that adds a capability to a composed PNA without modifying its core. A memory-assistant view, a calendar overlay, a federated portrait pull, a community-statistics survey tool — all plugins. PNAs themselves will expose MCP server interfaces as well.

- <a id="vocab-private-data"></a>**Private data.** Data that exists only on the user's device(s). The user is *not* OK with any external system holding a copy. *Examples:* notes the user keeps about a contact, tags they apply, groups they assemble, communication history. The PNA's central architectural job is to keep this layer protected, durable, and exclusively local. This data must never be sent across insecure channels, and must only be explicitly sent by the user's command in any form.

- <a id="vocab-reference-design"></a>**Reference design / thematic example.** A working, deployed PNA that demonstrates one valid combination of slot-fills against the spec. fellows_local_db is the first reference design — its load-bearing adjectives are *magic-link distributed PWA (Progressive Web App)* (Distribution choice) + *static network DB archive* (Ingestion choice — the directory is mirrored once with opt-in updates, not linked to a live contact manager) + *single shared directory* (Source choice). New reference designs accumulate adjectives as their slot-fills land. AIs adapting a thematic example start from one of these and ask the user which slot-fills to keep, swap, or extend.

  *Archival (v0.1).* When a reference design is accepted into PNT (Personal Network Toolkit)'s set, its source at the submitted commit MUST be archived with a Software Heritage Persistent IDentifier (SWHID — a `swh:1:dir:...` content-addressed identifier produced by Software Heritage's Save Code Now service). The SWHID is recorded in the design's PNT entry so the source survives even if the upstream repo is deleted or relocated. Future toolkit versions MAY revise the archival mechanism; v0.1 commits to SWHID.

- <a id="vocab-shared-data"></a>**Shared data.** In the context of a PNA, shared data is data that exists in more than one place — typically, a copy held by an external system the user uses (Google Contacts, Apple Contacts, Facebook friends, a fellowship's directory, a school's roster). The user is OK with that external system continuing to hold it, and often has no say in the matter. *Examples:* name, email, photo, organizational membership. The PNA mirrors this data locally so the user can browse and search it without depending on the external system being reachable.

  > "Shared" is the key word — not "public" in the everyday sense. Shared data can be data that the user publicly shared, or shared with Apple Contacts and exported, and is typically maintained outside the user's systems. The contact data in your Google account isn't *publicly visible*; it just isn't *exclusively yours* — it is shared with Google and any controlling governments or Google partners it is sold to. In all cases, some external system has a copy, or once did.

- <a id="vocab-shared-db-private-db"></a>**Shared DB / Private DB.** The two databases that a PNA stores. The Shared DB holds shared data (read-only inside the PNA — written only by the Ingestion component). The Private DB holds private data (read-write from the workspace). Further decomposition and isolation of data according to privacy constraints is reasonable but unnecessary for the first PNAs envisioned.

  In fellows_local_db, the shared DB is `fellows.db` and the private DB is `relationships.db`. The spec uses the generic names; specializations may rename for ergonomics, or change database engines for practical reasons, as long as the data stays local.

- **Slot.** A slot is a part of a PNA — a code module that handles a specific job within the system. v0.1 names five slots:

  - **Ingestion** — loads contact data into the Shared DB
  - **Storage** — owns the data files and serves queries
  - **Workspace** — runs the UI
  - **Communications** — launches outreach
  - **Distribution** — ships the PNA to other users

  Each slot has a contract; any code that satisfies the contract can fill it — a JavaScript module, a Python package, or an OS process, depending on the target environment. The full catalog and contracts are in [§ Slots, Interfaces, and Sub-contracts](#slot-map).

- <a id="vocab-universal-ac"></a>**Universal AC vs flavor-derived AC.** A *universal* commitment applies to every PNA — it derives from the [Goals](#goals) alone. A *flavor-derived* commitment — also called a **conditional** commitment — applies only when the flavor includes a specific pick (e.g. `storage:opfs-sqlite-wasm`). [§ Universal architectural commitments](#universal-architectural-commitments) lists the universal set; the conditional ones live in [`axes.md`](axes.md), grouped under the pick that adds them.

- <a id="vocab-use-case"></a>**Use case.** A user-facing class of PNA — "Directory Archive," "Personal Relationship Manager." A use case names what kind of app this is *from the user's perspective*. v0.1 attests two; future versions will add more. Use case is *not* one of the Axes (above); it's the parent category that a flavor instantiates. A use case typically suggests default axis picks (Directory Archives gravitate toward web-bundle distribution; PRMs toward never-distributed-single-user) but the axes remain independent — a hypothetical Directory Archive shipped as a Tauri shell + native SQLite is conceivable. Full catalog in [`use_cases.md`](use_cases.md).

- <a id="vocab-workspace"></a>**Workspace.** One of the slots in a PNA: the viewer + editor. The thing the user looks at and clicks. fellows_local_db's workspace is a vanilla-JS SPA (Single-Page Application) in the browser; another PNA's might be a native shell, a Tauri app, a TUI (Terminal User Interface), or a separately-distributed mini-app sharing the same data layer.

---

## Goals

### Goal 1 — Private data

The PNA stores two databases: a Shared DB (data the user is OK with external systems mirroring) and a Private DB (data that must stay only on the user's device). The Private DB is protected forever — it never leaves the device, never lands on any server, and is durable across app updates and routine cache clears. The Shared DB doesn't need that lifetime protection. Further decomposition and isolation of data according to privacy constraints is reasonable but unnecessary for the first PNAs envisioned.

> **Why it matters:** The Private DB is the one space where privacy is *guaranteed by the architecture, not merely hoped for*. Private data — who you confide in, your private notes on people, your communication history — is what most exposes you to surveillance, social-graph mining, and platform abuse. Keeping it on the user's device is the only durable defense, and the architectural job of the PNA is to keep the line between shared and private data unmistakably bright.

### Goal 2 — A local root for your personal networks

Take control of your contact data. A PNA brings the root of your personal network — the contact and relationship data everything else hangs off — onto the user's own device, under the user's own ownership, as a local store the workspace can browse offline and work over. Owning that root is the first order of business; it is the foundation the private overlay (Goal 1), durable storage (Goal 4), and outreach (Goal 3) all build on top of.

*How* a PNA fills that root is an implementation choice, not part of the goal. Mirroring an export is the easiest path today and the one v0.1 reference designs take; live pulls, multi-source merges, and federated reads are equally legitimate ingestion shapes (see the Ingestion axis in [`axes.md`](axes.md)). As a v0.1 scope choice, PNAs operate *downstream* of SaaS systems of record — they take local custody of contact data but do not modify it at the source. That is transitional, not permanent: today it is not yet practical to fully repatriate data from centralized platforms, so a PNA mirrors what is there and gives the user a far better place to work over it.

> **Why it matters:** Contact and relationship data is the *root* of your personal network. The pain is current and concrete: your contacts live in someone else's system — scattered across Google, Apple, Facebook, a fellowship's directory — surveilled and outside your control. Pull that root onto your own device and you can finally build on it; leave it where it is and you can't. Everything else a PNA offers — a private overlay, durable storage, your own outreach — assumes you own the root first.

### Goal 3 — User-controlled communication

When the user wants to reach out to a contact, the workspace offers a *choice* of transports — `mailto:` and `tel:`, and more secure / decentralized options like Signal where configured. The user picks per outreach and sees the full payload before anything is sent. The PNA does not promise to encrypt the user's messages — it hands off to whatever channel the user chose — but it guarantees the user is never *forced* onto an insecure or content-reading channel, and that no data is ever sent on the user's behalf without the user seeing it first.

> **Why it matters:** This is the sanctioned-egress counterpart to Goal 1. Goal 1 says private data never leaves the device on its own; communication is the *one* place data deliberately leaves — the user reaching out to someone. A user who holds their local data to a high bar holds the same bar for how that data travels: defaulting every outreach to email, routed through whoever runs their mail server, is inconsistent with that. So transports are pluggable, the user chooses per outreach, and a contact who says "only reach me over a secure channel" can have that honored against their record. Security is something the user can *achieve* by plugging in a secure channel — and that the PNA promises never to undermine.

### Goal 4 — Portable, durable data

Private data travels with the user across devices, browsers, and PNA versions, and survives the routine churn of app updates and cache clears. When loss does happen, the data is recoverable — not merely resisted.

> **Why it matters:** Local-first only delivers on Goal 1 if "local" doesn't mean "trapped on this exact installation forever." Users replace devices, switch browsers, reinstall PNAs. The Private DB has to be exportable, importable, and resilient against accidental wipes — otherwise local-first becomes fragility. Durability *resists* loss; recoverability *remedies* it when it happens anyway; portability keeps the data from being trapped in the first place — the goal needs all three.

> A platform or storage substrate may impose a ceiling that bounds how fully a PNA can honor a Goal or AC on a given platform — a **Constraint** (see [`constraints.md`](constraints.md)). Goal 4 is where this bites hardest: durable, portable private data runs straight into what the browser substrate will and won't keep. A PNA stays conformant by handling each inherited Constraint honestly (capability reduced to what the platform can keep, frontier declared truthfully); handling a Constraint does not exit PNA mode. Constraints are the dual of [Exceptions](exceptions.md) — a Constraint is imposed by the platform, an Exception is raised by the user.

### Goal 5 — Locally diagnosable

When something goes wrong, the issue can be diagnosed without compromising Goal 1. Sanitized error capture, runtime build labels, in-app diagnostic panels, user-controlled bug-report flows — all sized to a privacy posture consistent with the rest of the app. In single-user instances with no remote maintainer, the diagnostics primarily serve the user themselves. It goes without saying that source code must be available to the user to modify as they please for the diagnostics to be useful.

> **Why it matters:** A privacy-sovereign user's threshold for what diagnostic data flows anywhere is the same as for the rest of their data. The diagnostic surface is part of the privacy surface, not an exception to it. Many eventual PNAs will be single-user installations with no maintainer at all; the debug substrate has to work in that mode without sending anything anywhere by default. When a sink *is* configured (fellows_local_db sends to a maintainer mailbox), it has to be sanitized and rate-limited so the user trusts using it.

---

## Use cases

A use case names a coherent class of PNA from the user's perspective. A use case typically suggests default axis picks but does not determine them. v0.1 attests two named use cases plus a longer-arc target:

- **Directory Archive** — a snapshot of some external organization's roster (a fellowship, a school, a cohort, a community) plus the user's private overlay on top. Shared data has a single external source; each distributed user receives the same shared data and accumulates their own private overlay. Realized in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).
- **Personal Relationship Manager** — the user's own contact databases (Google + Apple + Facebook + LinkedIn + organizational directories) mirrored locally, plus rich private overlays (notes, tags, groups, comms history, message recency) and tools (LLM-mediated search, visual recall, eventual P2P (peer-to-peer)). Multi-source ingestion. Typically single-user, not distributed onward. [PRT](https://github.com/richbodo/prt)-inspired (PRT — also "Personal Network Toolkit" — is the graveyard predecessor project from which the current PNT and fellows_local_db grew); no PNA-spec-conforming reference design yet. **[draft]**
- **Multi-PNA ecosystem (target, v0.2+)** — multiple cooperating PNAs on one user's device, wired together at runtime by an AI agent via MCP. The PRM acts as the meta-workspace over a deduplicated read-only meta-view composed from the per-PNA shared stores; per-app workspaces remain available for single-context work. No reference design yet; v0.1's contracts are sized to enable it.

Full catalog with attestation status, default axis picks, and reference-design links: [`use_cases.md`](use_cases.md).

---

## Axes

v0.1 names the independent Axes a PNA picks along. A PNA's *flavor* is the full constellation of picks. Each pick may trigger flavor-derived ACs (the AC-trigger tags appear in [`axes.md`](axes.md), grouped by axis-pick).

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

> **Validation, not certification.** PNT validates behaviors against the Goals; it does not certify. There is no pass/fail badge and no certifying body (see [`CONTRIBUTING.md`](../CONTRIBUTING.md) § "Acceptance is not certification" and the skill's § Principles, "Conformance is checked, not awarded"). Conformance is *checked* — by the user, or by an AI running the evaluate flow — against this spec. Where a PNA deliberately departs from a guarantee it raises an [Exception](exceptions.md); the evaluate flow then detects each exception and verifies how it is handled, **reporting by `AC-*`/`EX-*` ID rather than awarding a grade.** Where the *platform* imposes a ceiling the PNA cannot clear, that is a [Constraint](constraints.md); the evaluate flow detects each ceiling a design's axis picks inherit and verifies it is handled honestly — capability reduced to what the platform can keep, frontier declared truthfully — reporting by `CST-*` ID. Over-reach (promising a capability the platform cannot keep) is a silent conformance failure, the dual of an undeclared Exception.

The agent's job when **building**, per this spec, is to:

1. Identify the **use case** with the user (see [§ Use cases](#use-cases)).
2. Walk the user through the **Axes** (see [§ Axes](#axes)) and make picks that fit the user's goals.
3. Generate or adapt code that fills each **slot** (see [§ Slots, Interfaces, and Sub-contracts](#slots-interfaces-and-sub-contracts)) according to its contract, consistent with the axis picks.
4. Verify the result against the **universal architectural commitments** (see [§ Universal architectural commitments](#universal-architectural-commitments)) and any conditional commitments the picks add (catalogued in [`axes.md`](axes.md)).

Building is one of **three flows** the skill packages — *validate* (audit a candidate against the spec), *build* (the steps above), and *contribute* (feed a finding back into the spec). See [`pna-build-eval-contrib/SKILL.md`](../pna-build-eval-contrib/SKILL.md) and [`docs/users-guide.md`](../docs/users-guide.md).

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

## Universal architectural commitments

Universal ACs are the architectural commitments derived from the goals alone. They apply to every PNA regardless of flavor.

Recall that a *flavor* is the full set of axis picks a builder makes when shaping a PNA (see [§ Vocabulary](#vocabulary)). **Flavor-derived ACs** are architectural commitments triggered by specific axis picks — they apply only when the flavor includes those picks. Because they depend on specific axis-picks, they're catalogued near them in [`axes.md`](axes.md), grouped under the triggering pick.

Universal ACs (in this file) and flavor-derived ACs (in `axes.md`) share a single stable numbering sequence, so cross-references work regardless of which file the AC ended up in. The gaps you'll see in the table below (no AC-2, AC-3, AC-5, AC-8, AC-12, AC-13, AC-14) are the flavor-derived ACs catalogued in `axes.md`.

The wording in the universal table below is substrate-neutral; specific *forms* (URL parameter vs CLI flag, OPFS vs native filesystem) are flavor-derived realizations of universal contracts.

**Normative language.** Conformance-bearing statements in the AC table below (and in the sub-contract definitions that follow, and in the flavor-derived ACs in `axes.md`) use RFC 2119 / RFC 8174 keywords — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY — when, and only when, capitalized. Surrounding prose is plain English (motivation, examples, why-it-matters notes).

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. -->
| Commitment | Serves | ID |
|---|---|---|
| **Two-store ownership split.** Shared data MUST be read-only and externally managed; private data MUST be read-write and locally owned. The two stores MUST occupy separate storage namespaces with separate privacy postures. (Example realizations: two SQLite databases via OPFS in fellows_local_db; two SQLite files on the filesystem in a CLI / native PNA.) | Goal 1 | <a id="ac-1"></a>AC-1 |
| **Versioned cross-boundary handshake.** Every PNA with a storage boundary (worker ↔ workspace in a browser bundle, CLI ↔ DB module in a TUI/CLI tool, native shell ↔ DB process) MUST version-check at init. On version mismatch the boundary MUST refuse mutating operations; read operations MUST continue to work. The build label MUST NOT be used as the gate. | Goal 4 | <a id="ac-4"></a>AC-4 |
| **Always-reachable diagnostic escape.** A force-reset / force-unlock affordance MUST be reachable regardless of stuck app state. The specific form is shell-derived (URL parameter for web SPAs, e.g., `?gate=1`; CLI flag for terminal apps, e.g., `--reset`; key chord for native shells); the substrate is required everywhere. | Goal 5 | <a id="ac-6"></a>AC-6 |
| **Self-service field-debug substrate.** Every PNA MUST provide a field-debug substrate consisting of: a build label (AC-15), sanitized error capture, a diagnostic state-dump, a bug-report flow, the escape hatch from AC-6, a boot watchdog with named phase marks, and slow-boot persistence. Specific affordances are shell-derived (badge in a web UI; `--diag` subcommand in a CLI; native diagnostic menu); the substrate is required everywhere. | Goal 5 | <a id="ac-7"></a>AC-7 |
| **Auto-backup of private data on user-edit cadence.** The PNA MUST snapshot the Private store on a per-boot debounced schedule (not per-deploy). It MUST rotate snapshots to keep a small ring of recoverable points. | Goal 4 | <a id="ac-9"></a>AC-9 |
| **Re-imports of the Shared store are opt-in and non-destructive.** Re-imports MUST be opt-in — whether refreshed from the original source (a directory operator pushes an update) or re-mirrored from a centralized platform (the user re-exports their Google contacts). Before the user commits a re-import, the workspace MUST preview any private references that would be orphaned by the update. | Goal 2, Goal 4 | <a id="ac-10"></a>AC-10 |
| **Storage substrate detects concurrent access.** When another tab or process holds the data layer, the storage substrate MUST detect the conflict and surface it with a specific message (multi-tab in browsers, multi-process in native); a generic "unsupported" message MUST NOT be used. | Goal 4 | <a id="ac-11"></a>AC-11 |
| **Build label tied to source revision, substituted at build *and* serve time.** Each delivered artifact MUST carry a runtime-visible unique label tied to the source revision. The label MUST be substituted at both build time and serve time. Format is implementation-specific (`<YYYY-MM-DD>-<short-sha>` in fellows_local_db; whatever `--version` reports in CLI tools). | Goal 5 | <a id="ac-15"></a>AC-15 |
| **Communication-transport selection is user-driven.** The workspace MUST surface multiple transports — including secure / decentralized options when configured — and the user MUST choose per outreach. No transport MAY be hardcoded as the only available option. | Goal 3 | <a id="ac-16"></a>AC-16 |
| **Sourced provenance.** Every record in the Shared store MUST trace to a specific external source the user has explicitly configured. The toolkit MUST NOT introduce contact data the user hasn't approved. | Goal 2 | <a id="ac-17"></a>AC-17 |
| **Transports cannot read message contents.** A transport's acceptability is determined by the transport mechanism itself, not by the downstream chain it kicks off. `mailto:` passes (hands off to whichever client the user has configured; the downstream provider's behavior — Gmail, Outlook — is outside the toolkit's enforcement). Signal-class protocols pass (encryption-in-protocol). Workspaces MUST NOT offer centralized message-broker SaaS that decodes payloads as part of operating (Slack, Discord) as a PNA-eligible transport. Contact-graph retention by the transport is *not* part of the rule (too hard to enforce uniformly across protocols; varies by user threat model). | Goal 3 | <a id="ac-18"></a>AC-18 |
| **User-visible payload before send.** Any workspace-initiated communication MUST show the user the full payload — recipients, body, and any data merged in from the Shared or Private store — before the transport is launched. The user MUST be able to edit or cancel. This MUST apply even to bulk operations (e.g., "email this group of 50"). Workspaces MUST NOT auto-blast data through transports without the user seeing the composition. | Goal 3 | <a id="ac-19"></a>AC-19 |
| **LLM calls over user data are transports.** Any LLM invocation over Private or Shared data MUST be treated as a transport: a local model is the default; a cloud model MUST be opt-in per call; the user MUST see the prompt and any merged data before send. Extension of AC-18 and AC-19 to a new transport class. | Goal 3 | <a id="ac-prm-a"></a>AC-PRM-A |
| **Re-ingestion is always user-initiated.** Re-ingestion MUST be triggered by an explicit user action; the PNA MUST NOT background-poll source services (Google Contacts, IMAP, organizational directories). Strengthens AC-10: the user always knows when fresh data is being fetched. | Goal 1, Goal 4 | <a id="ac-prm-d"></a>AC-PRM-D |
| **Cloud AI clients require per-call consent for Private DB access via MCP.** Any MCP tool that returns Private DB rows MUST either refuse, or MUST require explicit per-session opt-in, when the consuming MCP client is not locally hosted. Local clients (Claude Desktop with a local model, Cursor + local Ollama) are the default green path; cloud clients (Claude API direct, OpenAI API, etc.) are opt-in per call. In practice this targets the Private Data Ops server; the Shared / Private split at the MCP surface lets a user wire a cloud client to Shared Data Ops alone without triggering this AC. Concrete realization of AC-PRM-A at the MCP surface. | Goal 1, Goal 3 | <a id="ac-mcp-a"></a>AC-MCP-A |
| **MCP Communications tools stage outreach; the workspace launches.** A Communications MCP tool call MUST NOT directly fire a transport. It MUST return a staging ID with the full payload preview; the user MUST confirm via the workspace before the transport launches. The MCP server proposes; the workspace disposes. AC-19 is enforced at the workspace boundary and MUST NOT be bypassable by AI clients. | Goal 3 | <a id="ac-mcp-b"></a>AC-MCP-B |

---

## Slots, Interfaces, and Sub-contracts
<a id="slot-map"></a>

> **Reference material — skip unless you're implementing or auditing a PNA.** This section is the architectural skeleton (the five slots and three interfaces), then the detailed, ID'd **sub-contracts** that decompose each. A first read can stop after the [Slots](#slots) and [Interfaces](#interfaces) tables; the sub-contracts below them are a per-piece checklist for builders and for the evaluate flow, not narrative.

The spec defines **five slots** (positions filled by code) and **three interfaces** (cross-cutting contracts spanning multiple slots). The Slot and Interface vocab terms are defined in [§ Vocabulary](#vocabulary).

Each slot has a code-level contract. The typed contracts — JSON Schema for RPC + handshake, OpenAPI fragments for distribution, SQL DDL (Data Definition Language) for schemas, TypeScript declaration for the Communications transport interface, JSON Schema for each canonical MCP server's tool surface — live in [`contracts/`](../contracts/).

Many Universal ACs (see [§ Universal architectural commitments](#universal-architectural-commitments)) cite specific slots in their wording. The slots and interfaces are the architectural skeleton; the ACs are the load-bearing constraints over it. Each slot decomposes further into named sub-contracts — see [§ Sub-contracts per slot](#sub-contracts-per-slot) below — so a builder can target each piece individually.

### Slots

| Slot | Purpose |
|---|---|
| <a id="slot-ingestion"></a>**Ingestion** | Produces a Shared DB conforming to the Shared schema, from one or many external sources. |
| <a id="slot-storage"></a>**Storage** | Owns both DB files (Shared + Private) and serves queries. Implements AC-1's two-store ownership split and AC-4's cross-boundary version handshake. |
| <a id="slot-workspace"></a>**Workspace** | The user-facing surface — UI, routing, rendering shared + private data, launching communications. Enforces AC-19's user-visible payload before send. |
| <a id="slot-communications"></a>**Communications** | Pluggable transport layer for outreach. Honors AC-16's user-driven selection and AC-18's transport eligibility rule. |
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

- <a id="st-1"></a>**ST-1: Substrate.** The Storage slot MUST use a single dedicated worker, the OPFS-SAH-Pool VFS (Storage Access Handle Pool Virtual File System), and a sqlite-wasm runtime (or the substrate-equivalent for non-browser flavors). The worker MUST be the only context that calls `navigator.storage.getDirectory` or opens a `FileSystemSyncAccessHandle` (per AC-3).
- <a id="st-2"></a>**ST-2: Init handshake.** The first RPC across the boundary MUST be `op='init'`. Init MUST return `{workerRpcVersion, schemaVersion, buildLabel, opfsCapable, hasSharedDb, hasPrivateDb, poolFiles, trace}`. Capability detection MUST happen inside this op (per AC-12). Typed contract: [`contracts/worker-init-handshake.schema.json`](../contracts/worker-init-handshake.schema.json).
- <a id="st-3"></a>**ST-3: RPC protocol.** The RPC envelope MUST be `{id, op, args}` ↔ `{id, ok, result|error}`. Fan-in dispatch MUST be sequence-numbered via a pending Map. On `worker.onerror`, all pending RPCs MUST be rejected so callers can fall back instead of hanging. Typed contract: [`contracts/worker-rpc-protocol.schema.json`](../contracts/worker-rpc-protocol.schema.json).
- <a id="st-4"></a>**ST-4: Two-database management.** The Storage slot MUST manage a Private DB (RW) and a Shared DB (RO). Cross-DB joins MUST use `ATTACH ?mode=ro`, attached once per init in the worker.
- <a id="st-5"></a>**ST-5: Schema bootstrap.** Storage MUST use `CREATE IF NOT EXISTS` for both schemas, MUST set `PRAGMA foreign_keys=ON` per connection, and MUST set `PRAGMA user_version` to the schema version. The bootstrap MUST be idempotent so older backups gain newer tables on restore.
- <a id="st-6"></a>**ST-6: Auto-backup.** Storage MUST take per-boot debounced snapshots of the Private DB to OPFS root (outside the SAH-pool dir, so snapshots survive sqlite-wasm operations). Rotation MUST be by sorted ISO filename. Per AC-9.
- <a id="st-7"></a>**ST-7: Restore.** Restore MUST accept either a user-supplied file or a recent auto-backup. It MUST validate via `PRAGMA quick_check` plus schema check. The pre-restore state MUST be snapshotted to the same rotation. The swap MUST be atomic.
- <a id="st-8"></a>**ST-8: Opt-in update flow.** The update flow MUST be `compareSha → previewSwap → applySwap | cancelSwap`. An opaque per-session `stagingId` MUST be used so a stale page can't accidentally commit. The affected-member preview MUST be computed from joined Private DB references. Per AC-10.
- <a id="st-9"></a>**ST-9: Multi-tab detection.** `OWNERSHIP_CONFLICT` MUST be tagged on `installOpfsSAHPoolVfs()` failure so WS-6 can render a specific multi-tab panel (per AC-11). Non-browser flavors realize the equivalent file-lock detection per AC-PRM-C.
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
- <a id="di-5"></a>**DI-5: Server hardening.** The Distribution server MUST terminate TLS on :443 → 127.0.0.1 origin. It MUST send COOP (Cross-Origin Opener Policy) and COEP (Cross-Origin Embedder Policy) headers (AC-13). POST body MUST be capped at 16KB. The server MUST NOT expose per-user RW endpoints (AC-2). Caching MUST be status-aware (4xx/5xx MUST NOT be long-cached).
- <a id="di-6"></a>**DI-6: PWA-specific gotchas (when distribution medium is a PWA).** The manifest MUST be minimal — no `related_applications`, no `share_target` POST. The service worker MUST be network-first for HTML/JS/CSS/SW + worker file and cache-first for the vendored runtime. A separate asset cache MUST be used. The Shared DB URL MUST be bypassed in the SW fetch handler (AC-14).

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

**This is the PNA Spec, at Toolkit-Version 0.1.** When new demand surfaces or runtime constraints shift, we bump the toolkit version, declare what changed in [`CHANGELOG.md`](CHANGELOG.md), and update the architectural commitments accordingly.

Items deliberately deferred to future toolkit versions:

- **Privacy reclassification migration mechanics.** The Preamble commits PNAs to honoring user-driven privacy reclassification of a record (shared → private). The *implementation pattern* — does the record stay in the Shared DB with a private-side override row that supersedes? Get copied into the Private DB and removed from the Shared DB on next re-mirror? — is not pinned in v0.1. The contract is declared; the migration is left for a future version when the first reference design needs it.
- **Multi-source dedup implementation.** AC-PRM-B (catalogued in [`axes.md`](axes.md) as a draft flavor-derived AC) captures the v0.1 commitment for `ingestion:multi-source-merge-with-dedup` flavors — stable `record_id` survives merge, dedup wizard surfaces conflicts, per-field provenance. The concrete implementation (merge UI, conflict-resolution algorithms) awaits the first multi-source reference design.
- **Per-database (or finer) transport requirements.** A future toolkit version may let each database — Shared, Private, or any custom database in a richer PNA — declare which transport properties it requires for outbound flow. v0.1 handles the data-transport matching implicitly: AC-18 filters out transports that read content; AC-19 ensures the user sees the full payload before launch; the user resolves the matching in the moment. Explicit per-DB rules (workspaces auto-suggesting or auto-filtering transports based on source DB sensitivity) land when a reference design has an auto-send feature that needs them.
- **At-rest encryption against local device access.** v0.1's threat model is *network and platform exposure* — data leaving the device to SaaS, surveillance, or social-graph mining (Goal 1). Defending against an adversary with **local access to the device itself** (a lost, stolen, or seized machine; a shared computer) is deliberately out of scope at the application layer: OS full-disk encryption (FileVault / BitLocker / LUKS) is the right layer for it, and app-level at-rest encryption is largely redundant with FDE where it works and absent where it matters (a running, unlocked machine holds the key in memory regardless). PNT therefore does **not** make at-rest encryption a universal AC — a boolean "encrypted at rest" would invite false assurance and tension with Goal 4 (a lost key is lost data). At-rest encryption remains available as the `native-sqlcipher` storage flavor (see [`axes.md`](axes.md)); its key-storage and -rotation ACs are deferred until a SQLCipher reference design demonstrates them, and any such attestation discloses a per-dimension **strength profile** ([`exceptions.md`](exceptions.md) § Strength profiles) rather than a single graded claim. Full rationale: [`docs/PriorArt.md`](../docs/PriorArt.md) § Design notes.
- **Cross-device sync.** Out of scope for v0.1. Future versions may declare a sync protocol; v0.1 explicitly does not.
- **Federated P2P capabilities.** Signed-repo asset pulls (a community member's photos), community-stats aggregation tools (the CRT vision). Out of scope for v0.1.
- **Formally verifiable code.** A longer-arc goal. v0.1 aims for AI-checkable contracts (markdown prose + JSON Schema / OpenAPI / SQL DDL / TypeScript declarations); formal verification (TLA+ / Alloy / etc.) is reserved for a later version.

When any of these become near-term, they get a v0.2+ spec bump and the relevant architectural commitments are revised.
