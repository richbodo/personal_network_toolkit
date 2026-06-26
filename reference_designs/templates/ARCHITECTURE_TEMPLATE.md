# <design-name> — Architecture

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../../VERSION).

> The Architecture document is this design's Security Target: a declaration of its conformance against the PNA Spec (which plays the Protection Profile role). The PNA Toolkit requires every accepted reference design to ship one. A row missing the Verification field in the AC attestation table below is grounds for PR rejection.

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

For every AC in `spec/PNA_Spec.md § Universal architectural commitments` and every conditional AC in `spec/axes.md` triggered by this design's picks, a row stating Realization, Verification, and Status. ACs the design declares not applicable are listed with a brief reason.

The Verification field is load-bearing — a row missing this field is grounds for PR rejection. Three kinds of verification are acceptable:

1. **Deterministic test** — a test file or script that decides conformance mechanically. Example: a script that scans the codebase for any `fetch(...)` call to a non-localhost URL on the Private DB code path.
2. **LLM evaluation rubric** — a prompt or rubric describing what an LLM should look for when evaluating this AC against the source. Useful for posture/intent ACs that mechanical tests can't reach. Example: "Read every code path that reads from Private DB and decide whether any of them sends data off-device. Cite specific call sites supporting the decision."
3. **Human-review note** — a short note explaining why no automated test is feasible, with the review record itself archived in the design's repo (e.g., `docs/conformance-review-2026-05.md`).

Mixed verification is fine — for example, "deterministic test (file-presence lint) plus LLM rubric (read transport handlers and confirm no SaaS broker is reachable)". Whichever combination, the Verification cell names them concretely.

**A `conformant` row needs executable evidence — a doc pointer is not evidence.** A doc that *asserts* a property does not *prove* it. If the only Verification you can name for a `conformant` row is a `*.md` file, either add a test, declare one of the three verification kinds above explicitly, or downgrade the row to `partial`/`Open`.

**Negative invariants need negative tests.** A row whose realization *forbids* something — "off-folder there is no durable private store", "no transport reads message contents", "the gated capability's write does not happen" — must cite a test that asserts the thing does **NOT** happen. The happy-path test ("X happens when enabled") does not cover the negative; over-claiming a negative is a silent conformance failure, the most dangerous kind because the suite stays green.

**Cite code pointers deterministically — `path:symbol`, not a bare `symbol()`; full `path/to/test.py::name`, never a bare `::name` continuation.** The Realization and Verification cells are not just for human readers: the toolkit harvests them into a cross-design [realization index](../../docs/realization-index.md) so a builder can find proven code for an AC by reading one table instead of every design's source. That harvest only works when every pointer resolves on its own. So in the **Realization** cell, write each code reference as `path/to/file.ext:symbol` (e.g. `core/snapshots.py:rotate`), never a bare `symbol()` whose file the reader must infer from prose. In the **Verification** cell, write each test as the full `path/to/test.py::name`; if several tests share a file, repeat the path rather than abbreviating later ones to `::name`. A symbol named without its file, or an HTTP route / `*.md` doc link offered where a code path belongs, is invisible to the index — and the per-design pointer-coverage number it reports (the standing goal is **100%**) is exactly the count of rows that got this right.

**Deferrals are strict-xfail tests anchored to an issue, never code comments.** When an invariant is designed but not yet enforced, encode it as `@pytest.mark.xfail(strict=True, reason="…tracking: #NNN…")` carrying a machine-readable **issue** anchor — an issue, not a PR: issues close when the *work* is done; a PR closes when *something* merges, so a PR ref goes stale while the invariant stays unmet. A deferral parked in a `// TODO` or an `INERT` comment is unowned and evaporates — the only other home for one is an honest `partial`/`Open` status in this table.

Mind the asymmetry: `strict=True` trips the day the fix *lands* (it XPASSes, prompting promotion to a hard guard), but stays a contented green xfail *forever* if the fix is **abandoned** — so the marker catches accidental success, never silent abandonment (PRs closed, the invariant quietly dropped from scope). Two cheap reinforcements close that blind spot: **(a)** require the `tracking: #NNN` anchor above, and if your tracker can report issue state, flag any strict-xfail whose issue is **closed while the test still xfails** — that deferral was dropped, not done; **(b)** cap the deferral count low (a handful) so the honest-frontiers list (`grep "xfail(strict"`) stays glanceable and debt can't normalize. The fellows_local_db design ships both — an anchor lint and a report that probes issue state — in `tests/test_xfail_discipline.py`.

**Mechanical check (recommended).** Ship a checker that parses this table and fails CI when a `conformant` row's evidence isn't real — so the table can't drift back into asserting properties the code never proved. The toolkit ships a portable, stdlib-only reference implementation: [`tools/attestation-evidence-lint.py`](../../tools/attestation-evidence-lint.py) (with clean/dirty fixtures and a self-test). Copy it into your design and run it against your Architecture document + test tree. For each row whose Status contains `conformant` and not `partial`, it requires a resolvable `path/to/test.py[::name]` ref (file exists; if `::name`, a `def`/`class name` exists) **that is not decorated `xfail` or unconditional `skip`**, or one of the declared review-kind keywords. A doc-only cell fails; **a cited `xfail` test fails** — a declared-false invariant is not evidence (this is the exact seam where a row cited `xfail(strict=True)` as proof and the suite stayed green); a conditional `skipif` is exempt, as a real environment guard. The first toolkit reference design (fellows_local_db) ships this lint alongside a Stop-hook that blocks a commit touching the attestation without touching tests, and a CLAUDE.md "Conformance discipline" stanza.

**Validation timing — non-conforming code must not reach users.** The lint above is the *deterministic* half of "exists **and passes**": a static check proves the cited test is a live, non-deferred assertion, but it cannot prove the test *passes* — that's the runtime layer. So run the suite (lint + tests) at the boundary where code becomes user-available, and require it finding-free there. Name your boundary: a project with a ship/deploy step gates there (fellows_local_db gates `deploy-preflight`); a continuously-deployed or merge-to-main-is-prod project gates per-PR; a library gates at release/tag. The cue to re-run is a **behavior change** — adding or removing a feature. The deferral cap is *secondary* hygiene between those runs, not the safety mechanism; the gate is.

### Universal architectural commitments

| AC | Realization | Verification | Status |
|---|---|---|---|
| AC-1 (sovereign, sealed private layer) | <how the design realizes it — the canonical two-store split, or a single-store data-layer-enforced classification; file/code references> | <test file(s), LLM evaluation rubric, or human-review note> | conformant / partial-conformance / not-applicable |
| AC-4 (versioned cross-boundary handshake) | | | |
| AC-6 (always-reachable diagnostic escape) | | | |
| AC-7 (self-service field-debug substrate) | | | |
| AC-9 (auto-backup of private data) | | | |
| AC-10 (opt-in non-destructive re-imports) | | | |
| AC-11 (concurrent-access detection) | | | |
| AC-15 (build label tied to source revision) | | | |
| AC-16 (user-driven transport selection) | | | |
| AC-17 (sourced provenance) | | | |
| AC-18 (transports cannot read message contents) | | | |
| AC-19 (user-visible payload before send) | | | |
| AC-20 (LLM calls over user data are transports) | | | |
| AC-21 (re-ingestion is user-initiated) | | | |
| AC-MCP-A (cloud AI clients require per-call consent for Private DB) | | | |
| AC-MCP-B (MCP Communications stages; workspace launches) | | | |
| AC-22 (honest capability assessment) | | | |
| AC-23 (source available for verification) | | | |

### Conditional architectural commitments

List the conditional ACs triggered by this design's axis picks. Look these up in `spec/axes.md` based on the picks declared above. Add a row per triggered AC.

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
