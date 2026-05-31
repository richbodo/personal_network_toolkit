# <design-name> — Architecture

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../../VERSION).

> The Architecture document is this design's Security Target: a declaration of its conformance against the PNA Spec (which plays the Protection Profile role). PNT requires every accepted reference design to ship one. A row missing the Verification field in the AC attestation table below is grounds for PR rejection.

## Toolkit-Version

This design was built and validated against Toolkit-Version <X.Y> (the `/VERSION` minor, e.g. `0.1`), which fixes the version of the whole toolkit — spec, contracts, skill, lint, and templates — that this design conforms to.

## Axis picks

| Axis | Pick | Axis version | Notes |
|---|---|---|---|
| distribution | <pick> | v<n> | (optional brief note) |
| storage substrate | <pick> | v<n> | |
| ingestion shape | <pick> | v<n> | |
| workspace shell | <pick> | v<n> | |
| comms transport set | <pick> | v<n> | |
| MCP-exposure | <pick> | v<n> | |

## Per-axis implementation notes

### distribution

(Short paragraph describing how this design realizes the chosen pick. Reference code locations where relevant.)

### storage substrate

(...)

### ingestion shape

(...)

### workspace shell

(...)

### comms transport set

(...)

### MCP-exposure

(...)

## AC attestation table

For every AC in `spec/PNA_Spec.md § Universal architectural commitments` and every flavor-derived AC in `spec/axes.md` triggered by this design's picks, a row stating Realization, Verification, and Status. ACs the design declares not applicable are listed with a brief reason.

The Verification field is load-bearing — a row missing this field is grounds for PR rejection. Three kinds of verification are acceptable:

1. **Deterministic test** — a test file or script that decides conformance mechanically. Example: a script that scans the codebase for any `fetch(...)` call to a non-localhost URL on the Private DB code path.
2. **LLM evaluation rubric** — a prompt or rubric describing what an LLM should look for when evaluating this AC against the source. Useful for posture/intent ACs that mechanical tests can't reach. Example: "Read every code path that reads from Private DB and decide whether any of them sends data off-device. Cite specific call sites supporting the decision."
3. **Human-review note** — a short note explaining why no automated test is feasible, with the review record itself archived in the design's repo (e.g., `docs/conformance-review-2026-05.md`).

Mixed verification is fine — for example, "deterministic test (file-presence lint) plus LLM rubric (read transport handlers and confirm no SaaS broker is reachable)". Whichever combination, the Verification cell names them concretely.

### Universal architectural commitments

| AC | Realization | Verification | Status |
|---|---|---|---|
| AC-1 (two-store ownership split) | <how the design realizes it; file/code references> | <test file(s), LLM evaluation rubric, or human-review note> | conformant / partial-conformance / not-applicable |
| AC-4 (versioned cross-boundary handshake) | | | |
| AC-6 (always-reachable diagnostic escape) | | | |
| AC-7 (self-service field-debug substrate) | | | |
| AC-9 (auto-backup of private data) | | | |
| AC-10 (opt-in non-destructive re-imports) | | | |
| AC-11 (concurrent-access detection) | | | |
| AC-15 (build label tied to source revision) | | | |
| AC-16 (user-driven transport selection) | | | |
| AC-17 (mirrored data is sourced) | | | |
| AC-18 (transports cannot read message contents) | | | |
| AC-19 (user-visible payload before send) | | | |
| AC-PRM-A (LLM calls over user data are transports) | | | |
| AC-PRM-D (re-ingestion is user-initiated) | | | |
| AC-MCP-A (cloud AI clients require per-call consent for Private DB) | | | |
| AC-MCP-B (MCP Communications stages; workspace launches) | | | |

### Flavor-derived architectural commitments

List the flavor-derived ACs triggered by this design's axis picks. Look these up in `spec/axes.md` based on the picks declared above. Add a row per triggered AC.

| AC | Triggered by | Realization | Verification | Status |
|---|---|---|---|---|
| <AC-N> | <axis-pick> | | | |

## Contributions to the spec

What spec changes (if any) this submission proposes, and what working code in the design demonstrates each:

- **<change 1>**: ... — demonstrated by `<file:line>` in the canonical repo.
- **<change 2>**: ... — demonstrated by `<file:line>` in the canonical repo.

If this is an additive submission (no spec changes proposed; the design simply attests against the current Toolkit-Version), say so: "No spec changes proposed; this submission attests conformance to Toolkit-Version <X.Y>."

## Reproducibility notes

Build/run instructions sufficient for someone to make a fighting attempt from the archived source.

- **Dependencies:** <list>
- **Build commands:** <list>
- **External services required (if any):** <list>
- **Known dependency-rot risks:** <if relevant, note packages or APIs that may be deprecated by the time this is read>

The goal is not "the design will always build" — it's that a future reader has enough information to recover the intent even when the environment has rotted.
