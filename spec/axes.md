# Axes

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).

This document catalogs the Axes a PNA picks along, the attested picks on each Axis, and the flavor-derived ACs each pick triggers.

The Axis concept is defined in [`PNA_Spec.md` § Vocabulary](PNA_Spec.md#vocabulary). The Axes overview in `PNA_Spec.md` lists picks at a glance; this file is the authoritative catalog with full descriptions and AC triggers.

For each Axis below: a description of what the Axis decides, the attested picks (each with a short note on what it implies, where it's attested, and which other axis-picks it commonly correlates with), and a `Triggered flavor-derived ACs` subsection when any picks on that axis fire flavor-derived ACs (Architectural Commitments).

**Normative language.** Conformance-bearing statements in the AC tables below use RFC 2119 / RFC 8174 keywords — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY — when, and only when, capitalized. Surrounding prose is plain English. Same convention as `PNA_Spec.md`.

---

## Distribution

How the PNA reaches a user's device. The distribution pick shapes whether the PNA has a server at all, whether that server gates installs, and whether the bundle ships as a PWA — choices that ripple into several flavor-derived ACs.

### Picks

- **`web-bundle-with-magic-link`** *(server-backed, auth-gated, PWA)* — An HTTP origin serves the bundle behind email-allowlist auth. The user receives an unlock link, exchanges it for a session, and installs the PWA. Multiple users install from the same source. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md). Triggers AC-2, AC-5, AC-8, AC-14; combines with `storage:opfs-sqlite-wasm` to trigger AC-13. **Inherits constraints** `CST-PWA-NO-BACKGROUND`, `CST-PWA-SERVER-FLOOR` — and, combined with `storage:opfs-sqlite-wasm`, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)).
- **`never-distributed-single-user`** — The PNA is built or installed by the user themselves; no per-user delivery story. No server, no auth, no service worker. PRT-inspired. Triggers no flavor-derived ACs on this axis.
- **`web-bundle-open`** *(server-backed, no auth, PWA)* — Same delivery shape as magic-link but with no auth gate; anyone with the URL can install. Triggers AC-2 and AC-14; combines with `storage:opfs-sqlite-wasm` to trigger AC-13. **Inherits constraints** `CST-PWA-NO-BACKGROUND`, `CST-PWA-SERVER-FLOOR` — and, combined with `storage:opfs-sqlite-wasm`, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)).
- **`app-store-native`** — Packaged native app distributed via a platform store (Mac App Store, Google Play, etc.). The store is the install path; no PNA-operated server. None of this axis's flavor-derived ACs fire.
- **`sideloaded-native`** — Packaged native app distributed directly (download a binary, install). Same: no PNA-operated server; none of this axis's flavor-derived ACs fire.

### Triggered flavor-derived ACs

| AC | Triggered by | Commitment |
|---|---|---|
| <a id="ac-2"></a>AC-2 | `[dist:server-backed]` (any `web-bundle-*` pick) | **No SaaS surface.** The server, when present, MUST be a delivery channel, not a service. The server MUST NOT expose per-user RW endpoints, MUST NOT persist private data, MUST NOT host an admin console, and MUST NOT operate cross-device sync. |
| <a id="ac-5"></a>AC-5 | `[dist:auth-gated]` (`web-bundle-with-magic-link`) | **Stale session never locks users out of cached data.** A 401/403 from any shared-side fetch MUST fall through to the local cache. Fresh data MUST require explicit user action. |
| <a id="ac-8"></a>AC-8 | `[dist:auth-server]` + `[debug:has-error-sink]` | **Anti-enumeration on auth + abuse-bounded analytics.** Distribution-channel auth endpoints MUST always return neutral payloads. Per-IP rate limits MUST be enforced. The sanitized error sink MAY double as the analytics pipe (`kind=install`, `kind=worker`, …) but MUST NOT widen the privacy boundary. |
| <a id="ac-14"></a>AC-14 | `[dist:pwa]` (any `web-bundle-*` PWA pick) | **Service worker never owns SQLite.** The SW MUST be app-shell + update detection only — SW lifecycle (idle eviction, multi-instance, restart on push) is hostile to data ownership. The Shared store URL MUST be bypassed in the SW fetch handler. |

---

## Storage substrate

What backs the data layer — the bytes on disk or in OPFS that hold the Shared and Private DBs. The storage substrate pick shapes ownership of file handles, concurrent-access detection, and what cross-origin headers (if any) the distribution must serve.

### Picks

- **`opfs-sqlite-wasm`** — sqlite-wasm running in a dedicated worker, with OPFS-SAH-Pool VFS as the underlying storage. Browser-only. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md). Triggers AC-3, AC-12; combines with `dist:web-served` to trigger AC-13. **Inherits constraints** `CST-PWA-SANDBOX-SEALED`, `CST-PWA-STORAGE-EVICTABLE`, `CST-PWA-SINGLE-OWNER` — and, combined with a `web-bundle` distribution, `CST-PWA-PRIVATE-SNAPSHOT` and `CST-PWA-NO-SYNC` (see [constraints.md](constraints.md)). (The forced worker-owned single-connection architecture is captured directly in AC-3 above.)
- **`native-sqlite-via-filesystem`** — Native SQLite library (libsqlite3) opens database files directly via OS filesystem APIs. WAL mode + advisory file locks recommended. CLI / native PNAs only. PRT-inspired (not yet against this spec). Triggers AC-PRM-C **[draft]**.
- **`idb-only-browser`** — IndexedDB without SQLite. Less expressive (no SQL); mostly hypothetical for PNA. No flavor-derived ACs in v0.1 (the relevant ACs assume sqlite); a future toolkit version may add IDB-specific ACs if a reference design picks this.
- **`native-sqlcipher`** — Encrypted-at-rest variant of `native-sqlite-via-filesystem`. Inherits AC-PRM-C **[draft]** plus additional commitments about key storage and rotation that v0.1 doesn't yet name. Deferred ACs land when a SQLCipher-flavored reference design is built.

### Triggered flavor-derived ACs

| AC | Triggered by | Commitment |
|---|---|---|
| <a id="ac-3"></a>AC-3 | `[storage:opfs-sqlite-wasm]` | **Single OPFS owner.** All OPFS handles and SQLite-WASM instances MUST live in one dedicated worker. The workspace MUST act as an RPC client. Parallel main-thread OPFS MUST NOT exist. *Realizes AC-1 + AC-11 for this substrate.* This worker-owned, single-writer architecture is **forced by the substrate**, not a stylistic choice: durable SQL in a browser (sqlite-wasm + OPFS-SAH-Pool) requires `crossOriginIsolated`, one worker owning every OPFS handle, and a single writer connection — a multi-connection or main-thread design is not available. Builders must know this up front; it is a property of the medium, not a defect to fix. |
| <a id="ac-12"></a>AC-12 | `[storage:opfs-sqlite-wasm]` | **Capability detection inside the worker, UA-parsing for messaging only.** Browsers lie about main-thread OPFS support; the worker MUST be the only context that performs capability detection. UA strings MAY inform error messages but MUST NOT gate. |
| <a id="ac-13"></a>AC-13 | `[storage:opfs-sqlite-wasm]` + `[dist:web-served]` | **COOP/COEP required.** OPFS-SAH-Pool needs `crossOriginIsolated`; both dev server and prod reverse proxy MUST send `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`. Without this the storage substrate silently fails to install. |
| <a id="ac-prm-c"></a>AC-PRM-C **[draft]** | `[storage:native-sqlite-via-filesystem]` | **Single-instance file-lock.** Native SQLite demands one writer; a second process MUST refuse cleanly with a specific message naming the holding process. *Realizes AC-11 for this substrate.* **[draft — no reference design yet]** |

---

## Ingestion shape

How the Shared DB is filled and refreshed — whether from a single export, a single live source, multiple merged sources, or federated reads from peers. The ingestion pick determines whether dedup is a concern at all and what re-import semantics look like.

### Picks

- **`single-source-static-mirror`** — One external source produces a complete Shared DB on each refresh; ingestion stages → validates → atomically swaps. No dedup needed. Re-imports are opt-in per AC-10. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) (Knack-JSON ETL). Triggers no axis-specific ACs.
- **`single-source-live-pull`** — One external source queried live (REST API, OAuth, etc.). Same single-source dedup story (none needed). Triggers no axis-specific ACs in v0.1; a future toolkit version may add live-pull contracts (rate limiting, partial-failure handling, etc.).
- **`multi-source-merge-with-dedup`** — Multiple external sources (Google + Apple + Facebook + organizational directories) merged into one Shared DB. Dedup wizard surfaces conflicts; per-field provenance preserved. PRT-inspired (not yet against this spec). Triggers AC-PRM-B **[draft]**.
- **`federated-read`** *(deferred)* — Reading from peer PNAs. Out of scope for v0.1.

### Triggered flavor-derived ACs

| AC | Triggered by | Commitment |
|---|---|---|
| <a id="ac-prm-b"></a>AC-PRM-B **[draft]** | `[ingestion:multi-source-merge-with-dedup]` | **Multi-source dedup contract.** A stable `record_id` MUST survive merge across sources. The dedup flow MUST surface conflicts via a wizard. Per-source provenance MUST be recorded *per field*, not just per record. Lifts the deferred "multi-source dedup contract" from § Scope into v0.1 for PRM-flavor PNAs. **[draft — no reference design yet]** |

---

## Workspace shell

What the user sees and clicks — the surface that renders the data and accepts user input. The workspace shell pick is the highest-impact axis on user experience but does not trigger flavor-derived ACs in v0.1; universal ACs (AC-19 in particular) apply regardless of shell.

### Picks

- **`vanilla-js-spa`** — A hand-written JavaScript single-page application, no framework. Routing typically hash-based. Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md).
- **`framework-spa`** — A SPA built on React / Vue / Svelte / etc. No reference design in v0.1.
- **`tui-textual`** — A terminal UI built with Textual / Bubbletea / a similar TUI library. PRT-inspired (not yet against this spec).
- **`cli-subcommands`** — Bare CLI subcommands; the workspace is the shell prompt itself. Useful for scripting and headless use.
- **`native-shell-tauri`** — Tauri (Rust-backed) wrapping a web SPA in a native shell. Bridges browser UI with native OS access.
- **`native-shell-native`** — Fully native GUI (SwiftUI, Qt, GTK, etc.). No reference design in v0.1.

No flavor-derived ACs are triggered by picks on this axis in v0.1. The universal AC-6 (always-reachable diagnostic escape) takes shell-specific *forms* — URL parameter for SPAs (`?gate=1`), CLI flag for terminal apps (`--reset`), key chord for native — but the contract itself is universal.

---

## Comms transport set

Which outreach mechanisms the workspace offers — what shows up in the user's "reach out" picker.

### Picks

- **`mailto-only`** — Just `mailto:` (plus `tel:` for phone). Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md); Signal planned.
- **`mailto-plus-signal`** — Adds Signal protocol (encrypted-in-protocol; passes AC-18).
- **`mailto-plus-matrix`** — Adds Matrix (encrypted-room mode; passes AC-18).
- **`shell-out-to-cli-clients`** — CLI / native PNAs that invoke `signal-cli`, IMAP libraries, or other transports via subprocess. PRT-inspired (not yet against this spec).

No flavor-derived ACs are triggered by picks on this axis in v0.1. The universal comms ACs — AC-16 (user-driven selection), AC-18 (mechanism cannot read content), AC-19 (user-visible payload before send), AC-PRM-A (LLM-as-transport), AC-MCP-B (MCP comms stage; workspace launches) — apply regardless of pick.

---

## MCP-exposure

Which canonical MCP servers (Shared Data Ops / Private Data Ops / Ingestion / Comms / Diagnostics) the PNA hosts — and therefore which capabilities an AI client can drive without modifying the PNA's core. The MCP-exposure pick determines whether the MCP-related universal ACs apply at all (they're universal, but each is vacuous when no server that triggers it is exposed).

The picks are structured as a progression: each adds one canonical server to the previous pick's set. The Shared / Private split is the load-bearing distinction — `shared-only` is cloud-safe (no Private DB rows flow); anything that includes `private` brings AC-MCP-A into force.

### Picks

- **`none`** — No MCP servers exposed. The PNA is reachable only to humans. AC-MCP-A and AC-MCP-B are vacuous.
- **`shared-only`** — Only Shared Data Ops exposed. AI clients can read mirrored contact data but never see Private DB rows. AC-MCP-A is vacuous (no Private DB tools); AC-MCP-B is vacuous (no Comms). The cloud-safe pick — wire a hosted LLM to this without crossing the privacy boundary.
- **`shared+private`** — Shared Data Ops + Private Data Ops; no outreach surface. AC-MCP-A applies; AC-MCP-B is vacuous. The "ask about my data but don't email anyone" posture.
- **`shared+private+comms`** — Adds Communications. AC-MCP-A and AC-MCP-B both apply. **Attested in [fellows_local_db](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md)** — its `mcp_servers/` ships shared-data-ops, private-data-ops, and comms as stdio servers wired into Claude Desktop.
- **`full`** — All five canonical servers exposed: Shared Data Ops, Private Data Ops, Ingestion, Communications, Diagnostics. Maximum AI-client reachability. All MCP ACs apply.

No axis-specific flavor-derived ACs are introduced here. The MCP-related ACs are universal — AC-MCP-A and AC-MCP-B in [`PNA_Spec.md` § Universal architectural commitments](PNA_Spec.md#universal-architectural-commitments) — and apply whenever the pick includes a server that triggers them.
