# PNA Toolkit Next Steps — High-Level Plan

Ordered as requested: **1 → 4 → 5 → 3 → 6 → 2**. High-level only; work the details with Claude Code. Each item notes how it rides the existing reorg phases and `tools/` conventions rather than starting a parallel track.

Sequencing logic: a cheap README win first; then formalize the evaluate *output* (4) so later checks have a place to land; then a real design to test against (5); then the deterministic check (3) whose findings flow into that output; then a reading-gated architecture decision (6); then the skill split (2) last, once Evaluate has earned its place as the front door.

---

## 1. Install signpost + promote Evaluate (quick win) — ✅ DONE (2026-05-29)

**Goal.** Close the two remaining README gaps now that the skill is already surfaced and linked.

> **Status:** Done. README now leads the three modes with Evaluate ("audit any contact app for safety before you install it") and carries a concrete symlink install snippet pointing to `docs/users-guide.md § Install the skill`; `llms.txt` opens with a "Start with the skill" line routing a cold agent to `SKILL.md` as the entry point.

- Add a concrete **install/activation** snippet: how an agent picks up the skill (copy `pna-build-eval-contrib/` into `.claude/skills/`, or the equivalent one-liner), so it auto-discovers rather than relying on a human pasting the path.
- Reorder the "three modes" so **Evaluate leads** for the average reader — frame it as "audit any contact app for safety before you install it," with Build/Contribute following. Evaluate is the lowest-friction front door and the one a non-builder actually wants.
- Make `llms.txt` route a cold agent to the SKILL.md as the build/eval entry point.

**Done when.** A new person can read the README and get an agent running Evaluate without asking how.

---

## 4. Typed evaluate-report artifact — ✅ DONE (2026-05-29)

**Goal.** Turn the evaluate flow's existing structured report into a typed artifact so results are machine-comparable and drift becomes a diff.

> **Status:** Done. JSON Schema at `tools/evaluate-report.schema.json` (Draft 2020-12, validated): AC-keyed `findings` with per-AC `status` (`conformant`/`non-conformant`/`not-applicable`/`unable-to-determine`), code-location citations, a `summary` posture, and an `evidence` array tagged by `source` (`deterministic`/`llm`/`human`) — the seam item 3's egress lint feeds into. Conditional rules enforce citations-on-(non)conformant and rationale-on-(n/a, undetermined). Lives in `tools/`, not `contracts/`, because it realizes no AC (would fail `lint-spec-ids.py`). `SKILL.md` § Evaluate flow now emits the artifact as source of truth with the prose report as a view; `docs/users-guide.md` Goal 2 and the skill's Key resources updated.

- Define a JSON Schema for the AC-keyed report (per-AC status: `conformant` / `non-conformant` / `not-applicable` / `unable-to-determine`, plus cited code locations and the summary posture).
- Have the evaluate flow emit to this schema; keep the human-readable rendering as a view over it.
- Reinforces README Goal 6 (AC as unit of identity) and gives the "occasionally re-check we didn't drift" workflow a concrete regression signal.

**Done when.** Two eval runs on the same design can be diffed to show exactly which ACs changed status.

---

## 5. Attest the mutual-aid / community-care use case

**Goal.** Add the use case closest to your social-network-health origin — surface who in a personal network needs help and who can offer it, then communicate — alongside the existing Directory Archive / PRM / Multi-PNA entries in `use_cases.md`.

- You're already building a reference design for this; let the design drive the use-case attestation rather than writing it speculatively.
- Treat it as the hardest privacy stress test: a "needs help" field is health/vulnerability-adjacent, so it should exercise your sovereignty and consent ACs harder than any prior design. Note any new flavor-derived ACs it surfaces (candidate Contribute-flow spec diff).

**Done when.** The use case is attested in `use_cases.md` and backed by a working reference design with a filled AC attestation table.

---

## 3. Egress lint (deterministic sovereignty check) — ✅ DONE (2026-05-29)

**Goal.** One deterministic check guarding Goal 1 (private-data sovereignty): does any code path send private data off-device?

> **Status:** Done. `tools/egress-lint.py` statically scans a PNA source tree for egress vectors (`fetch`/XHR/`sendBeacon`/`WebSocket`/`EventSource`/`import()`/`importScripts`/axios/jQuery and HTML `src`/`action`/`object data`/`<link href>`/`<use href>`), flagging any remote origin not on the design's `egress-allow.json` allow-list (localhost, root-relative, `data:`/`mailto:`, and `<a href>` navigation are correctly ignored). Exit 0/1 like `lint-spec-ids.py`; `--json` emits a `source: deterministic`, `tool: egress-lint` evidence object that validates against `#/$defs/evidence` in the item-4 schema and drops into an AC-1 finding (verified). Self-test fixtures in `tools/egress-lint-fixtures/{clean,dirty}` are CI-enforced via a new `egress-lint-selftest` job in `.github/workflows/spec-lint.yml`. Referenced from `SKILL.md` Key resources and `docs/users-guide.md` Goal 6.

- Static scan for egress vectors (fetch / XHR / `sendBeacon` / form actions / `img`/script `src` to remote origins, etc.), allow-listing the legitimately remote picks per axis flavor.
- Lives in `tools/` next to `lint-spec-ids.py`, CI-enforced, same pattern. Not a general test runner — just the one violation that most destroys trust and that an LLM scanning a large tree might miss.
- Wire its output into the item-4 report schema as evidence on the relevant AC, so deterministic + LLM layers land in one place.

**Done when.** A reference design's CI fails if an unsanctioned egress path is introduced.

---

## 6. Tonsky file-sync as a candidate axis pick (reading-gated)

**Goal.** After reading "Local, First, Forever," evaluate commodity file-sync (per-client append-only op logs over Dropbox/iCloud/Syncthing, CRDT merge underneath) as a new pick on the comms/distribution axes.

- This is the local-first-pure path to multi-device / household-shared PNAs without reintroducing a SaaS root — relevant when a use case (e.g. a shared PRM or the item-5 community-care design) needs more than `mailto-only` + static mirror.
- Add as an axis pick with its flavor-derived ACs only if a real design needs it; don't add the option in the abstract.

**Done when.** Either a documented axis pick backed by a design that uses it, or a recorded decision that it's deferred and why.

---

## 2. Split out `pna-evaluate` as its own skill (last)

**Goal.** Once Evaluate has proven itself as the front door (items 1, 4), give it its own skill for sharper auto-activation and standalone discoverability ("is this app safe to install?").

- Separate entry point + tight, trigger-phrase-rich description; **share a reference file** with the build/contribute skill so the "Principles to honor" and "Key resources" sections aren't duplicated.
- Keep Build (+ Contribute) together. Optionally publish Evaluate as a standalone surface (e.g. a Claude Project) so non-builders can use it without the rest of the toolkit.

**Done when.** Evaluate triggers reliably on audit-intent requests on its own, with no duplicated spec body across skills.

---

### Fit with the existing roadmap
- Items 1, 4, 3 are small and CI/README-local — landable independently of Phase 5.
- Item 5 is gated on your in-progress reference design and is the natural thing to validate Phase 5's end-to-end build/attestation against.
- Item 6 is gated on reading + a design that needs sync.
- Item 2 is deliberately last; it's an optimization, not a prerequisite.
- The meta-methodology extraction stays out of scope until a second non-trivial reference design ships.
