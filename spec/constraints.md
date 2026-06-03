# PNA Constraints

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> This file defines **Constraints**: stable-ID'd ceilings (`CST-*`) that a platform or storage
> substrate imposes on a PNA, inherited automatically by one or more axis picks ([axes.md](axes.md)).
> Constraints are the dual of Exceptions ([exceptions.md](exceptions.md)): an Exception is a deviation
> the USER raises and the app handles; a Constraint is a limitation the PLATFORM imposes and the app
> must likewise handle — never silently.

## Concept

An Exception borrows the *runtime* exception metaphor (raise / catch / handle). A Constraint borrows
the *compile-time* one: the platform's type system won't admit the program you intended, so you
restructure to a smaller program that *does* type-check.

| Software | PNA Constraint |
|---|---|
| A compile-time / type error: the platform won't admit the program you intended | A capability the PNA **cannot express** on a given platform, given its axis picks |
| Not caught at runtime — you restructure the program to fit | Handled by **reducing the feature set** to what the platform can actually keep |
| The error names exactly what's unsupported | Every constraint has a stable `CST-*` ID naming the ceiling |
| `#ifdef PLATFORM` / capability shims | **Per-platform capability reduction** ("enough power to be useful, not dangerous") |
| A `// TODO: unsupported on X` with an issue link | The **Frontier** field: `Open` (no known workaround) vs `Solved`/`Mitigated` (here's how) |

A Constraint is **inherited** (by an axis pick — raised by no one), must be **detected** honestly per
platform, and must be **handled** by reducing capability to what the platform can actually deliver
("enough power to be useful, not enough to be dangerous").

**Handling a Constraint does NOT exit PNA mode.** A capability-reduced PNA that handles its inherited
ceilings honestly is fully a PNA — just a smaller one on that platform. The failure mode is
over-reach: promising a capability the platform cannot keep (**false durability**) without
acknowledging the ceiling.

> **Exceptions exit PNA mode; Constraints do not.** The conformance question for a Constraint is not
> "is it active?" (it always is, on the triggering platform) but "is it **handled honestly** —
> capability matched to deliverable durability, frontier declared truthfully, no false promises?"

### Inherited / detected / handled

- **Inherited** — a Constraint attaches automatically to one or more axis picks. Picking
  `storage:opfs-sqlite-wasm` *is* taking on `CST-PWA-SANDBOX-SEALED`; no action raises it.
- **Detected** — the app must determine, per platform/session, whether the ceiling is active, and do
  so **honestly** (see the `Detectability:` field — capability presence ≠ usefulness ≠ permanence).
- **Handled** — the app reduces capability to match what the platform can deliver, and **declares the
  frontier honestly** (it does not claim to Solve what it only Mitigated). A reference design stays
  conformant by handling, not by overcoming.

### Validation, not certification

PNT **validates behaviors against the Goals; it does not certify** (see `CONTRIBUTING.md` and the
skill's § Principles, "Conformance is checked, not awarded"). For Constraints, the
[evaluate flow](../pna-build-eval-contrib/SKILL.md) detects each inherited ceiling and verifies that
the candidate *handles it honestly* — capability reduced to match the platform, frontier declared
truthfully — reporting by `CST-*` ID. "This design inherits `CST-PWA-PRIVATE-SNAPSHOT` and handles it
by dropping durable private writes off-Chromium (frontier: Open)" is a finding, not a grade.

The backstop is the dual of the Exceptions backstop: where the Exceptions pass catches *undeclared
deviations* (the app violates an AC without raising an exception), the Constraints pass catches
*undeclared over-reach* — the app promises a capability the platform cannot keep without acknowledging
the ceiling (**false durability**). Both are silent dishonesty; both are conformance failures.

### Adverse-only registry

The registry is **adverse-only**: it catalogs ceilings that *remove or bound* capability. Some
platform ceilings happen to *serve* a PNA goal (a PWA can't send mail itself, only hand off a
`mailto:` URL — landing the app in exactly the "transports cannot read message contents" shape AC-18
wants). Those are real but are not builder/verifier advice the way an adverse ceiling is; they belong
in a separate, future "what worked well" channel and are out of scope here. (No `valence:` field.)

## Header conventions

These mirror the `Realizes: AC-…` header in `contracts/` and the `Relaxes:`/`Reversible:` headers in
[exceptions.md](exceptions.md). They appear in a constraint's registry entry and in any reference
design's constraint-attestation declaration.

- **`Triggered-by:`** — names the axis pick(s) that inherit this constraint. Each token is an
  axis-pick identifier of the form `<axis>:<pick>` as defined in [axes.md](axes.md) (e.g.
  `storage:opfs-sqlite-wasm`, `distribution:web-bundle`). Multiple tokens are comma-separated and mean
  "any of these picks inherits it" unless the entry says the combination is required. A bare
  `<axis>:<family>` prefix (e.g. `distribution:web-bundle`) means "any pick in that family"
  (`web-bundle-with-magic-link`, `web-bundle-open`, …).
  Example: `Triggered-by: distribution:web-bundle, storage:opfs-sqlite-wasm`
- **`Bounds:`** — names the Goal(s)/AC(s) whose full achievement the ceiling limits. The PNA still
  TRIES to honor them; the constraint bounds how completely it can on the triggering platform. Tokens
  are `AC-*`, `Goal-N`, or the literal `PNA-DEFINITION`. An entry that bounds only the build space
  (not a user-facing guarantee) MAY omit `Bounds:` and say so in prose.
  Example: `Bounds: AC-1, Goal-4`
- **`Frontier:`** — the resolution status. One of `Open` (no viable workaround found this version),
  `Mitigated` (partial handling exists; ceiling not removed), `Solved-on-<platform>` (removed on the
  named platform — e.g. `Solved-on-chromium`), or `Inherent` (cannot be removed; it is the medium).
  If `Mitigated` or `Solved-*`, a `Workaround:` field MUST follow naming the mechanism (a control,
  route, or code reference the validation flow can confirm).
  Example: `Frontier: Solved-on-chromium`
- **`Detectability:`** *(builder-actionable)* — how a builder determines whether the ceiling is active
  on a given platform. One of `feature-detect` (a clean capability check suffices), `empirical-probe`
  (the feature check lies; you must actually exercise it), or `ua-sniff` (no reliable capability
  signal; user-agent inference is the only handle). Example: `Detectability: ua-sniff`

> **`PNA-DEFINITION` token.** Reused from [exceptions.md](exceptions.md) — the PNA definition lives in
> prose (`vocab-pna` in [PNA_Spec.md](PNA_Spec.md)), not in the AC table, so `Bounds:` references it via
> the same literal sentinel the lint already resolves for `Relaxes:`.

## Meta-principles

- **M1 — capability presence ≠ usefulness ≠ permanence.** `showDirectoryPicker in window` is true on
  Android Chrome but only reaches an OS-clearable folder; `persist()` returns true but Safari still
  evicts; `createSyncAccessHandle` exists in a worker but not on the page. Detect USEFUL, DURABLE
  capability — often empirically. This is why every entry carries a `Detectability:` field.
- **M2 — the handling pattern is per-platform capability reduction.** Match each platform's offered
  features to the durability it can actually keep: "enough power to be useful, not enough to be
  dangerous." A capability reduction MUST enforce at the data layer, not UI-only — hiding a surface
  while the underlying write still happens is the cosmetic half, not the reduction.

## Constraint registry

| CST | Name | Triggered-by | Bounds | Frontier | Detectability |
|---|---|---|---|---|---|
| CST-PWA-PRIVATE-SNAPSHOT | Private store read-only off FSA browsers | distribution:web-bundle, storage:opfs-sqlite-wasm | AC-1, Goal-4 | Open | feature-detect |
| CST-PWA-SANDBOX-SEALED | OPFS store invisible + non-interoperable | storage:opfs-sqlite-wasm | AC-1, Goal-4, AC-MCP-A | Solved-on-chromium | feature-detect |
| CST-PWA-STORAGE-EVICTABLE | Script storage is evictable | storage:opfs-sqlite-wasm | Goal-4 | Mitigated | empirical-probe |
| CST-PWA-NO-SYNC | Origin/device-local silos; no built-in portability | distribution:web-bundle, storage:opfs-sqlite-wasm | Goal-4 | Open | feature-detect |
| CST-PWA-SINGLE-OWNER | Multi-tab contention, no OS file lock | storage:opfs-sqlite-wasm | AC-11 | Solved-on-chromium | empirical-probe |
| CST-PWA-NO-BACKGROUND | No reliable scheduled background execution | distribution:web-bundle | Goal-4 | Mitigated | feature-detect |
| CST-PWA-SERVER-FLOOR | Origin + TLS + secure context required | distribution:web-bundle | PNA-DEFINITION | Inherent | feature-detect |

### CST-PWA-PRIVATE-SNAPSHOT — Private store is read-only off File-System-Access browsers

**Triggered-by:** distribution:web-bundle, storage:opfs-sqlite-wasm
**Bounds:** AC-1, Goal-4
**Frontier:** Open — no viable workaround found as of Toolkit-Version 0.1 for keeping a LIVE, writable,
externally-readable private store off Chromium. An encrypt-then-export-to-self portability pattern is
a candidate (snapshot transport, not a live store), unproven.
**Detectability:** feature-detect — page-side `'showDirectoryPicker' in window`. (Necessary but not
sufficient; see CST-PWA-STORAGE-EVICTABLE and the Android caveat in CST-PWA-NO-BACKGROUND for why a
positive check still doesn't guarantee a *durable* store.)

**Ceiling:** The File System Access API — the only browser API granting a web app a persistent
writable handle to a user-chosen, user-visible file — is Chromium-only. On Safari, Firefox, and all
iOS browsers the private store can live only in the opaque OPFS sandbox or escape as a frozen download
snapshot. The "private half" of the PNA — meant to be the user's sovereign, live, manipulable data —
degrades to read-only-snapshot-at-best.

**Recommended handling:** per-platform capability reduction. On FSA-capable platforms, offer folder
mode (a real file). On non-FSA platforms, do not promise a durable live private store; offer an
explicit manual backup/export path and SAY SO. The reduction MUST enforce at the data layer (refuse
durable private writes when no verified folder backs the store), not UI-only. Demonstrated by
`fellows_local_db` (reference_designs/fellows_local_db/).

### CST-PWA-SANDBOX-SEALED — OPFS store is invisible to the user and to their other tools

**Triggered-by:** storage:opfs-sqlite-wasm
**Bounds:** AC-1, Goal-4, AC-MCP-A
**Frontier:** Solved-on-chromium
**Workaround:** File System Access folder mode relocates the store to a real, user-visible file that
companion tools (MCP servers, backups, CLIs) can read directly; the sandbox boundary dissolves. Off
Chromium the boundary stands and only a snapshot export bridges it.
**Detectability:** feature-detect.

**Ceiling:** OPFS is an origin-scoped sandbox. The store is invisible in the user's file manager and
unreadable by any other program on the machine, and a PWA cannot host native integration (no stdio,
no sockets, no local server) to bridge it — so the app's own MCP servers must ship as separate native
processes that can only read an EXPORTED copy. A PNA is meant to be the hub the user's other tools act
on; a store those tools cannot read is half a PNA.

**Recommended handling:** folder mode where available (dissolves the boundary — the private MCP server
reads the live file); elsewhere, an explicit export/import bridge with honest messaging that companion
tools see a snapshot, not the live store. A read-only Shared-DB MCP surface (which reads the on-device
mirror, not the private store) is unaffected and stays useful off-folder. Demonstrated by
`fellows_local_db`.

### CST-PWA-STORAGE-EVICTABLE — Script-managed storage is evictable

**Triggered-by:** storage:opfs-sqlite-wasm
**Bounds:** Goal-4
**Frontier:** Mitigated
**Workaround:** `navigator.storage.persist()` is requested best-effort (once per install) and, where a
verified folder backs the canonical store, the durable copy lives on disk *outside* evictable browser
storage — turning "Mitigated" into "Avoided for the private store" on that platform. A small backup
ring + manual export remain the recoverability floor everywhere.
**Detectability:** empirical-probe — `persist()` is advisory: it can return `true` and the browser can
still evict (notably Safari). Probe actual durability; do not trust the boolean.

**Ceiling:** OPFS and IndexedDB are "best-effort" script-managed storage the browser MAY evict under
storage pressure. A canonical private store that lives only there can vanish without user action.

**Recommended handling:** never make evictable storage the *canonical* home of durable private data.
Where FSA exists, the canonical file is on disk (folder mode); off-folder, keep only localStorage-grade
preferences in browser storage and lean on explicit export for anything that must survive. Demonstrated
by `fellows_local_db`.

### CST-PWA-NO-SYNC — Origin/device-local silos, no built-in portability

**Triggered-by:** distribution:web-bundle, storage:opfs-sqlite-wasm
**Bounds:** Goal-4
**Frontier:** Open — the medium provides no cross-device sync; the handling disambiguates copies and
bridges them manually but does not synchronize them.
**Detectability:** feature-detect.

**Ceiling:** OPFS is per-origin, per-device. A web-bundle PNA has no built-in way to move the private
store between a user's devices or browsers, and no authority to reconcile divergent copies.

**Recommended handling:** stamp an in-db **workspace identity** (a stable UUID + a monotonic
write-generation + a human device label) so the user (and a re-pick chooser) can answer "which copy is
canonical?" by content; offer a manual `.db` export/import as the cross-device bridge. Declare sync
explicitly out of scope rather than implying it. Demonstrated by `fellows_local_db`.

### CST-PWA-SINGLE-OWNER — Multi-tab contention with no OS file lock

**Triggered-by:** storage:opfs-sqlite-wasm
**Bounds:** AC-11
**Frontier:** Solved-on-chromium
**Workaround:** a Web Lock (`navigator.locks`) over the canonical write path plus ownership-conflict
detection: a second tab/window refuses cleanly with a specific "another tab/window is already open"
message rather than corrupting the store. Realizes AC-11 for this substrate.
**Detectability:** empirical-probe — contention only manifests when two contexts actually race.

**Ceiling:** Two tabs of the same origin can open the storage layer concurrently, and OPFS offers no
OS-level advisory file lock to arbitrate them — concurrent writers can corrupt the store.

**Recommended handling:** serialize canonical writes under a Web Lock and detect the ownership
conflict, surfacing a specific message (not a generic "unsupported"). Demonstrated by `fellows_local_db`.

### CST-PWA-NO-BACKGROUND — No reliable scheduled background execution

**Triggered-by:** distribution:web-bundle
**Bounds:** Goal-4
**Frontier:** Mitigated
**Workaround:** make backups *opportunistic* — a per-boot debounced snapshot (AC-9's cadence), never a
promise of scheduled protection. The user is told backups happen on use, not on a timer.
**Detectability:** feature-detect — Periodic Background Sync is absent on iOS and unreliable elsewhere;
its presence does not imply it will actually run.

**Ceiling:** A web bundle has no reliable scheduled background execution (especially on iOS): you
cannot promise "your data is backed up every night."

**Recommended handling:** opportunistic, per-boot debounced backups; frame them honestly as
use-triggered, never scheduled. Demonstrated by `fellows_local_db`.

### CST-PWA-SERVER-FLOOR — Origin + TLS + secure context required

**Triggered-by:** distribution:web-bundle
**Bounds:** PNA-DEFINITION
**Frontier:** Inherent — a web-bundle PNA cannot reach true serverless-local; it needs an origin.
**Detectability:** feature-detect (`isSecureContext`).

**Ceiling:** A web-served PNA needs an HTTP origin, TLS, and a secure context to install and run.
"Pure local, no server at all" is unreachable for this distribution shape — there is always at least a
delivery origin.

**Recommended handling:** bound the server to **distribution and update only** (Never-SaaS, AC-2):
authenticate the download, hand over the bundle, and hold no per-user RW state. The server is a
delivery channel, not a service. Demonstrated by `fellows_local_db`.

## Implementation notes (non-normative)

These are navigable PWA footguns — recorded so builders don't re-derive them, but they are NOT
ceilings and carry no `CST-*` ID.

- **Service-worker staleness.** A cached app shell can pin users to old code; "what code is running"
  is ambiguous. Handle with source-tied build labels + an explicit update banner.
- **No atomic factory reset.** OPFS has no per-origin wipe API; an HttpOnly session cookie needs a
  server round-trip. A full reset must reach each layer deliberately.
- **PWA install + manifest gotchas.** WebAPK `related_applications` can trigger Play-Store
  verification failures; a `POST` `share_target` silently fails on some WebAPK servers; iOS hides
  install behind Share → Add to Home Screen. Keep the manifest minimal; document per-platform install
  flows.

## Origin

The Constraints concept was distilled from operating the `fellows_local_db` reference design: a
fellow's Private Data Ops MCP server stopped connecting to a cloud client, and chasing *why the handoff
was that fragile in the first place* surfaced a class-level ceiling the app had been routing around
without naming (the FSA-only durable private store; the sealed OPFS sandbox). Constraints are the dual
of [Exceptions](exceptions.md): where an Exception is a deviation the user raises, a Constraint is a
ceiling the platform imposes. Per PNT's reference-driven model, this concept ships alongside the working
design that demonstrates the handling (folder mode + per-platform capability reduction). See that
design's `docs/architectural_findings.md` (upstream) and `reference_designs/fellows_local_db/`.
