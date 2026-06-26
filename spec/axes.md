# Axes

<!-- EDITING NOTE — machine-parsed tables: the per-axis "Extra commitments these picks add" tables are read by tools/lint-spec-ids.py AND by external report writers (reference-design conformance reports), and their `<a id>` row anchors are deep-linked from those reports. Treat each such table's columns, headers, and IDs as an API: if you change one, update those consumers — and the lint's self-tests (tools/tests/lint_selftest.py) — in the same change. The lint finds columns by header name, so the AC ID may sit in any column; it currently lives in the last column. -->

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).

This document catalogs the Axes a PNA picks along, the attested picks on each Axis, the **conditional** architectural commitments each pick entails (Layer 1; defined in [`PNA_Spec.md`](PNA_Spec.md#conditional-architectural-commitments)), and the Layer-2 **realizations** (the `RZ-*` family) it brings.

The Axis concept is defined in [`PNA_Spec.md` § Vocabulary](PNA_Spec.md#vocabulary). The Axes overview in `PNA_Spec.md` lists picks at a glance; this file is the authoritative catalog with full descriptions and the commitments each pick adds.

For each Axis below: a description of what the Axis decides, the attested picks (each with a short note on what it implies, where it's attested, and which other axis-picks it commonly correlates with), and — when a pick adds commitments beyond the universal set — an **Extra commitments these picks add** subsection — the *conditional* ACs the pick entails (defined in [`PNA_Spec.md` § Conditional architectural commitments](PNA_Spec.md#conditional-architectural-commitments)) and the Layer-2 *realizations* it brings (the `RZ-*` family, defined here).

**Normative language.** Conformance-bearing statements in the AC tables below use RFC 2119 / RFC 8174 keywords — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY — when, and only when, capitalized. Surrounding prose is plain English. Same convention as `PNA_Spec.md`.

---

## Distribution

How the PNA reaches a user's device. The distribution pick shapes whether the PNA has a server at all, whether that server gates installs, and whether the bundle ships as a PWA — choices that ripple into several conditional ACs and realizations.

> **Verifiability is a universal commitment, not a distribution pick.** Whether a user (or their tools) can read and check the running code before trusting it is [AC-23](PNA_Spec.md#ac-23) (Goal 2), which applies to *every* PNA regardless of how it is delivered. The picks below describe **delivery mechanics only** — server / no server, PWA / native / CLI, app-store / sideload — not a trust posture. So a `never-distributed-single-user` PNA shipped build-from-verifiable-source and the same pick shipped as an opaque binary are the *same* distribution pick; they differ on AC-23, and that difference lives in the commitment, not the axis. (This supersedes the earlier proposal to split the distribution axis on verifiability — [toolkit#39](https://github.com/richbodo/personal_network_toolkit/issues/39) / #64 rider 1.)

### Picks

- **`web-bundle-with-magic-link`** *(server-backed, auth-gated, PWA)* — An HTTP origin serves the bundle behind email-allowlist auth. The user receives an unlock link, exchanges it for a session, and installs the PWA. Multiple users install from the same source. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md). Triggers AC-2, AC-5, AC-8; brings realization RZ-4 (and, combined with `storage:opfs-sqlite-wasm`, RZ-3). **Inherits constraints** `CST-PWA-NO-BACKGROUND`, `CST-PWA-SERVER-FLOOR` — and, combined with `storage:opfs-sqlite-wasm`, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)).
- **`never-distributed-single-user`** — The PNA is built or installed by the user themselves; no per-user delivery story. No server, no auth, no service worker. PRT-inspired. Entails no conditional AC and brings no realization on this axis.
- **`web-bundle-open`** *(server-backed, no auth, PWA)* — Same delivery shape as magic-link but with no auth gate; anyone with the URL can install. Triggers AC-2; brings realization RZ-4 (and, combined with `storage:opfs-sqlite-wasm`, RZ-3). **Inherits constraints** `CST-PWA-NO-BACKGROUND`, `CST-PWA-SERVER-FLOOR` — and, combined with `storage:opfs-sqlite-wasm`, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)).
- **`app-store-native`** — Packaged native app distributed via a platform store (Mac App Store, Google Play, etc.). The store is the install path; no PNA-operated server. None of this axis's conditional ACs or realizations fire.
- **`sideloaded-native`** — Packaged native app distributed directly (download a binary, install). Same: no PNA-operated server; none of this axis's conditional ACs or realizations fire.

### Extra commitments these picks add

**Conditional ACs these picks entail** (Layer 1; defined in [`PNA_Spec.md` § Conditional architectural commitments](PNA_Spec.md#conditional-architectural-commitments)): a server-backed `web-bundle-*` distribution *operates a server* → <a id="ac-2"></a>[AC-2](PNA_Spec.md#ac-2); an auth-gated `web-bundle-with-magic-link` additionally *gates data behind an authenticated refresh* → <a id="ac-5"></a>[AC-5](PNA_Spec.md#ac-5) and *operates an authentication server* (with a configured error sink) → <a id="ac-8"></a>[AC-8](PNA_Spec.md#ac-8).

**Realizations these picks bring** (Layer 2):

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. The RZ traceability lint reads the RZ + Realizes columns. -->
| Realization | Realizes | Substrate (axis pick) | RZ |
|---|---|---|---|
| **Service worker never owns SQLite.** The SW MUST be app-shell + update detection only — SW lifecycle (idle eviction, multi-instance, restart on push) is hostile to data ownership. The Shared store URL MUST be bypassed in the SW fetch handler. | AC-1 | Any PWA (`web-bundle-*`) distribution. | <a id="rz-4"></a><a id="ac-14"></a>RZ-4 |

> **A general rule, two realizations.** [AC-2](PNA_Spec.md#ac-2) is the *distribution-server* form of a broader principle: **a server a PNA stands up over its own data must not become an ungoverned tap on it.** AC-2 keeps the delivery server a *channel, not a service* (no per-user RW endpoints, no private-data persistence, no sync); the *loopback-daemon* form — where a local daemon legitimately serves the single user RW — is [AC-PRM-H](PNA_Spec.md#ac-prm-h) (§ Workspace shell), which requires that surface be loopback-bound and session-authenticated. The principle generalizes (a future surface type — a local socket, a gRPC endpoint — adds its own conditional AC) while each obligation stays narrowly checkable. They differ on `pna-active`: AC-2 guards *off-device egress*; AC-PRM-H guards *same-host access* and, once authenticated, relaxes no guarantee (so it does not flip the bit).

---

## Storage substrate

What backs the data layer — the bytes on disk or in OPFS that hold the Shared and Private DBs. The storage substrate pick shapes ownership of file handles, concurrent-access detection, and what cross-origin headers (if any) the distribution must serve.

### Picks

- **`opfs-sqlite-wasm`** — sqlite-wasm running in a dedicated worker, with OPFS-SAH-Pool VFS as the underlying storage. Browser-only. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md). Brings realizations RZ-1, RZ-2; combined with `dist:web-served`, brings RZ-3. **Inherits constraints** `CST-PWA-SANDBOX-SEALED`, `CST-PWA-STORAGE-EVICTABLE`, `CST-PWA-SINGLE-OWNER` — and, combined with a `web-bundle` distribution, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)). (The forced worker-owned single-connection architecture is captured directly in RZ-1 above.)
- **`native-sqlite-via-filesystem`** — Native SQLite library (libsqlite3) opens database files directly via OS filesystem APIs. WAL mode + advisory file locks recommended. CLI / native PNAs only. PRT-inspired; attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md). Brings realization RZ-5.
- **`idb-only-browser`** — IndexedDB without SQLite. Less expressive (no SQL); mostly hypothetical for PNA. No conditional ACs or realizations in v0.1 (the relevant ACs assume sqlite); a future toolkit version may add IDB-specific ones if a reference design picks this.
- **`native-sqlcipher`** — Encrypted-at-rest variant of `native-sqlite-via-filesystem`. Inherits RZ-5 plus additional commitments about key storage and rotation that v0.1 doesn't yet name. Those deferred key-management ACs land when a SQLCipher-flavored reference design is built.

### Realizations these picks bring

These are Layer-2 *realizations* — how a universal AC is met on this substrate — not ACs (see [`PNA_Spec.md` § How the pieces fit together](PNA_Spec.md#how-the-pieces-fit-together)). Each names the AC it realizes.

<!-- machine-parsed table — see the EDITING NOTE at the top of this file before changing its columns, headers, or IDs. The RZ traceability lint reads the RZ + Realizes columns. -->
| Realization | Realizes | Substrate (axis pick) | RZ |
|---|---|---|---|
| **Single OPFS owner.** All OPFS handles and SQLite-WASM instances MUST live in one dedicated worker. The workspace MUST act as an RPC client. Parallel main-thread OPFS MUST NOT exist. This worker-owned, single-writer architecture is **forced by the substrate**, not a stylistic choice: durable SQL in a browser (sqlite-wasm + OPFS-SAH-Pool) requires `crossOriginIsolated`, one worker owning every OPFS handle, and a single writer connection — a multi-connection or main-thread design is not available. Builders must know this up front; it is a property of the medium, not a defect to fix. | AC-1, AC-11 | `storage:opfs-sqlite-wasm`. | <a id="rz-1"></a><a id="ac-3"></a>RZ-1 |
| **Capability detection inside the worker, UA-parsing for messaging only.** Browsers lie about main-thread OPFS support; the worker MUST be the only context that performs capability detection. UA strings MAY inform error messages but MUST NOT gate. | AC-22 | `storage:opfs-sqlite-wasm`. | <a id="rz-2"></a><a id="ac-12"></a>RZ-2 |
| **COOP/COEP required.** OPFS-SAH-Pool needs `crossOriginIsolated`; both dev server and prod reverse proxy MUST send `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`. Without this the storage substrate silently fails to install. | AC-1 | `storage:opfs-sqlite-wasm` **and** a web-served distribution. | <a id="rz-3"></a><a id="ac-13"></a>RZ-3 |
| **Single-instance file-lock.** Native SQLite demands one writer; a second process MUST refuse cleanly with a specific message naming the holding process. Attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md). | AC-11 | `storage:native-sqlite-via-filesystem`. | <a id="rz-5"></a><a id="ac-prm-c"></a>RZ-5 |

---

## Ingestion shape

How the Shared DB is filled and refreshed — whether from a single export, a single live source, multiple merged sources, or federated reads from peers. The ingestion pick determines whether dedup is a concern at all and what re-import semantics look like.

### Picks

- **`single-source-static-mirror`** — One external source produces a complete Shared DB on each refresh; ingestion stages → validates → atomically swaps. No dedup needed. Re-imports are opt-in per AC-10. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) (Knack-JSON ETL). Triggers no axis-specific ACs.
- **`single-source-live-pull`** — One external source queried live (REST API, OAuth, etc.). Same single-source dedup story (none needed). Triggers no axis-specific ACs in v0.1; a future toolkit version may add live-pull contracts (rate limiting, partial-failure handling, etc.).
- **`multi-source-merge-with-dedup`** — Multiple external sources (Google + Apple + Facebook + organizational directories) merged into one Shared DB. Dedup wizard surfaces conflicts; per-field provenance preserved. PRT-inspired; attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md). Triggers AC-PRM-B.
- **`federated-read`** *(deferred)* — Reading from peer PNAs. Out of scope for v0.1.

### Extra commitments these picks add

**Conditional AC this pick entails** (Layer 1; defined in [`PNA_Spec.md` § Conditional architectural commitments](PNA_Spec.md#conditional-architectural-commitments)): `ingestion:multi-source-merge-with-dedup` *mirrors more than one source* → <a id="ac-prm-b"></a>[AC-PRM-B](PNA_Spec.md#ac-prm-b) (a stable `record_id` survives merge, the dedup flow surfaces conflicts, per-source provenance is recorded per field). This pick brings no Layer-2 realization of its own. Attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md).

---

## Workspace shell

What the user sees and clicks — the surface that renders the data and accepts user input. The workspace shell pick is the highest-impact axis on user experience; it triggers a conditional AC only for a **server-backed local shell** ([AC-PRM-H](PNA_Spec.md#ac-prm-h)), and universal ACs (AC-19 in particular) apply regardless of shell.

### Picks

- **`vanilla-js-spa`** — A hand-written JavaScript single-page application, no framework. Routing typically hash-based. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).
- **`framework-spa`** — A SPA built on React / Vue / Svelte / etc. No reference design in v0.1.
- **`tui-textual`** — A terminal UI built with Textual / Bubbletea / a similar TUI library. PRT-inspired (not yet against this spec).
- **`cli-subcommands`** — Bare CLI subcommands; the workspace is the shell prompt itself. Useful for scripting and headless use.
- **`native-shell-tauri`** — Tauri (Rust-backed) wrapping a web SPA in a native shell. Bridges browser UI with native OS access.
- **`native-shell-native`** — Fully native GUI (SwiftUI, Qt, GTK, etc.). No reference design in v0.1.

The universal AC-6 (always-reachable diagnostic escape) takes shell-specific *forms* — URL parameter for SPAs (`?gate=1`), CLI flag for terminal apps (`--reset`), key chord for native — but the contract itself is universal.

### Extra commitments these picks add

A workspace shell served over an **HTTP/loopback daemon the PNA stands up itself** (rather than a browser bundle delivered from a distribution origin) opens a surface over its own data that other local processes on the host can reach. That gives the PNA the behavioral property *exposes a same-host surface over its data*, which entails the conditional AC <a id="ac-prm-h"></a>[AC-PRM-H](PNA_Spec.md#ac-prm-h) (Layer 1; defined in [`PNA_Spec.md` § Conditional architectural commitments](PNA_Spec.md#conditional-architectural-commitments)): the surface MUST be loopback-bound and authenticated to the user's own session, and a non-loopback bind MUST require an explicit, documented opt-out. Triggered when a server-backed local workspace shell (`vanilla-js-spa` / `framework-spa` / `tui-textual` served over a local daemon) is combined with a non-`web-bundle` distribution. Attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md).

The deterministic half is [`tools/loopback-surface-lint.py`](../tools/loopback-surface-lint.py) (`just loopback-lint`): an L1 non-loopback bind gates; an L2 unauthenticated handler is advisory (`--strict` gates it, as PRM does in its own conformance gate).

---

## Comms transport set

Which outreach mechanisms the workspace offers — what shows up in the user's "reach out" picker.

### Picks

- **`none`** — No outreach surface: the workspace offers no "reach out" picker. A contacts-consolidation or directory PNA whose loop stops at *recording* relationship data (no *gathering*-by-outreach). Attested in [prm](https://github.com/richbodo/prm/blob/main/docs/Architecture.md) (v0.1 consolidates + dedups; outreach is a later version). The outreach comms ACs — AC-16, AC-18, AC-19, AC-MCP-B — are vacuous; AC-20 (LLM-as-transport) still applies via the MCP surface.
- **`mailto-only`** — Just `mailto:` (plus `tel:` for phone). Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md); Signal planned.
- **`mailto-plus-signal`** — Adds Signal protocol (encrypted-in-protocol; passes AC-18).
- **`mailto-plus-matrix`** — Adds Matrix (encrypted-room mode; passes AC-18).
- **`shell-out-to-cli-clients`** — CLI / native PNAs that invoke `signal-cli`, IMAP libraries, or other transports via subprocess. PRT-inspired (not yet against this spec).

No conditional ACs or realizations are triggered by picks on this axis in v0.1. The universal comms ACs — AC-16 (user-driven selection), AC-18 (mechanism cannot read content), AC-19 (user-visible payload before send), AC-20 (LLM-as-transport), AC-MCP-B (MCP comms stage; workspace launches) — apply regardless of pick.

---

## MCP-exposure

Which canonical MCP servers (Shared Data Ops / Private Data Ops / Ingestion / Comms / Diagnostics) the PNA hosts — and therefore which capabilities an AI client can drive without modifying the PNA's core. The MCP-exposure pick determines whether the MCP-related universal ACs apply at all (they're universal, but each is vacuous when no server that triggers it is exposed).

The picks are structured as a progression: each adds one canonical server to the previous pick's set. AC-1's shared/private class boundary is the load-bearing distinction — `shared-only` is cloud-safe (no Private DB rows flow); anything that includes `private` brings AC-MCP-A into force.

### Picks

- **`none`** — No MCP servers exposed. The PNA is reachable only to humans. AC-MCP-A and AC-MCP-B are vacuous.
- **`shared-only`** — Only Shared Data Ops exposed. AI clients can read mirrored contact data but never see Private DB rows. AC-MCP-A is vacuous (no Private DB tools); AC-MCP-B is vacuous (no Comms). The cloud-safe pick — wire a hosted LLM to this without crossing the privacy boundary.
- **`shared+private`** — Shared Data Ops + Private Data Ops; no outreach surface. AC-MCP-A applies; AC-MCP-B is vacuous. The "ask about my data but don't email anyone" posture.
- **`shared+private+comms`** — Adds Communications. AC-MCP-A and AC-MCP-B both apply. **Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md)** — its `mcp_servers/` ships shared-data-ops, private-data-ops, and comms as stdio servers wired into Claude Desktop.
- **`full`** — All five canonical servers exposed: Shared Data Ops, Private Data Ops, Ingestion, Communications, Diagnostics. Maximum AI-client reachability. All MCP ACs apply.

No axis-specific conditional ACs or realizations are introduced here. The MCP-related ACs are universal — AC-MCP-A and AC-MCP-B in [`PNA_Spec.md` § Universal architectural commitments](PNA_Spec.md#universal-architectural-commitments) — and apply whenever the pick includes a server that triggers them.

---

## Retired IDs (redirects)
<a id="retired-ids"></a>

The [L1/L2 layering pass](../plans/l1-l2-layering-pass.md) factored two kinds of ID out of the `AC-*` namespace: **realizations** (Layer-2 — how a commitment is met on a specific stack — recategorized to the `RZ-*` family, since [a realization is never an AC](PNA_Spec.md#how-the-pieces-fit-together)) and two **de-branded universals** (a universal AC should not carry the design that first surfaced it in its ID; provenance lives in the [realization index](../docs/realization-index.md) + each design's attestation). Every retired ID keeps a working deep-link anchor on its new row, so existing links still resolve.

| Retired ID | New home | Why |
|---|---|---|
| AC-3 | RZ-1 (this file) | realization of AC-1 + AC-11 on `opfs-sqlite-wasm` |
| AC-12 | RZ-2 (this file) | realization of AC-22 on `opfs-sqlite-wasm` |
| AC-13 | RZ-3 (this file) | realization of AC-1 on web-served OPFS |
| AC-14 | RZ-4 (this file) | realization of AC-1 on a `web-bundle` PWA |
| AC-PRM-C | RZ-5 (this file) | realization of AC-11 on `native-sqlite-via-filesystem` |
| AC-PRM-A | [AC-20](PNA_Spec.md#ac-20) | de-branded universal (LLM calls over user data are transports) |
| AC-PRM-D | [AC-21](PNA_Spec.md#ac-21) | de-branded universal (re-ingestion is always user-initiated) |

The two **accepted reference designs are pinned to Toolkit-Version 0.1** and still attest the retired IDs in their bundled `Architecture.md`; their attestations re-sync to these new IDs at the v0.2 cut (see the [v0.2 cut plan](../plans/v0.2-spec-cut-plan.md)). The realization index is derived from those 0.1-pinned attestations, so it likewise still shows the old IDs until that re-sync.
