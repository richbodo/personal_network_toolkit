# Memorize — Plan v0

A first-draft, deliberately-verbose plan for a face/name/role memorization feature, designed for the **personal_network_toolkit** (pnt) ecosystem. Built as a combination of (a) a small set of Unix-tradition tools that augment a directory bundle, and (b) a feature pattern in pnt's static-directory-PWA application pattern. **fellows_local_db** is the first proof-of-concept rebuild target.

This document carries the research from the prior ideation doc forward and translates it to pnt's actual architecture as described in the project README: a local-first toolkit "in the tradition of UNIX software tools, and killer apps on top," following "a compositional, privilege-separated architecture in the qmail tradition," with imported contact data kept read-only and rebuildable, and private relationship data in a separate writable layer.

> **Status:** idea-stage, first-draft, intentionally verbose. Some sections are notes-to-self. Where this plan touches pnt's own architecture (especially §4), it should be read as *proposal* / *pressure-test*, not commitment — pnt itself is at the architecture-and-planning stage. Trim aggressively before this becomes a build doc.

> **What I know about pnt as of this draft, and what I don't:**
>
> *Known (from the pnt README):*
> 1. Local-first toolkit; small Unix-style tools that compose; "qmail-tradition" privilege-separated architecture; killer apps built on top.
> 2. Imported contact data is read-only and rebuildable from source exports. Private relationship data (tags, notes) lives in a separate writable layer. This is the same two-layer split as fellows_local_db.
> 3. The canonical interchange format is portable JSON bundles with referenced images, exported from filtered directory views.
> 4. Apps are *exports* / *artifacts*: web apps, PDFs, emails, and lists are all things you generate from a bundle. fellows_local_db is one instance of the static-PWA application pattern.
> 5. Search must be fast on large personal networks and must work without an LLM.
> 6. PNT explicitly leaves "clean seams" for future community/P2P/comms-channel pluggability without committing to those in the first build.
>
> *Unknown (the docs I haven't seen yet — `ARCHITECTURE.md`, `APPLICATION_PATTERNS.md`, `CONTRACTS.md`, `USE_CASES.md`, `SOURCE_REUSE.md`):*
> - The exact bundle schema (the M0 data contract).
> - The set of recognized application patterns and what each commits to.
> - How the writable layer is scoped — per-app (per-origin OPFS, like fellows_local_db) or shared across pnt-built apps the user has installed.
> - The intended invocation model for tools (CLI? library? both?) and how privilege separation is enforced in practice.
> - What's already-decided from prt vs. what's open.
>
> When those docs are visible, the parts of this plan that would change first are §4 (the architectural decomposition) and §10 (the spike's exact entry point).

---

## 0 · TL;DR

Decompose Memorize across pnt's two architectural layers:

- **Toolkit layer (build-time, Unix-style tools, compose via the bundle contract):**
  small programs that take a directory bundle as input, augment it with study-relevant data (visual-similarity neighbors, tag clusters), and emit an enriched bundle. These can run independently in a pipeline. Initially: `pnt-bundle-similarity`, possibly `pnt-bundle-clusters`. They write only to the read-only/rebuildable side of the bundle; they never touch user-private state.
- **App-runtime layer (the generated PWA, runs in the user's browser, writes to the writable layer):**
  the actual study experience — Cram mode (in-session Leitner), Library mode (FSRS-scheduled), mnemonic creation, briefing card, and the writable-layer schema additions (FSRS state, mnemonics, sessions, review events, briefings). All of this is per-user, all of it stays in the writable layer, none of it leaves the user's device.

Spike: face→name multiple-choice quiz over an existing group, in the app-runtime layer, in a fellows_local_db-style PWA. Ship in a day. Then layer in cram-mode Leitner, similar-distractor selection (which is when the toolkit-side tool first lands), FSRS, mnemonic prompts, and the briefing card. Use the spike to stress-test what the bundle contract has to provide for an app-runtime feature like this to work.

---

## 1 · Why this plan exists and what it is for

This is a *first-draft, verbose* plan, by request. It's structured to be cut down later, not to be the build doc. It carries the research grounding from the prior face-name ideation doc forward, and reshapes it onto pnt's actual architecture: a toolkit of small Unix-tradition tools, a set of recognized application patterns built on top, and a hard local-only stance with a read-only/writable-layer split.

The plan is therefore not a "design doc for a plugin to one app." It's two things at once:
- A **feature spec** for what the user-facing memorization experience should be.
- An **architectural decomposition** of that experience across pnt's toolkit + app layers, designed to expose the data contracts and application-pattern requirements that the feature implies.

The latter is at least as valuable as the former at this stage, because pnt is itself in the architecture-and-planning stage. The Memorize feature is a non-trivial second use case (the directory display being the first); using it to pressure-test the architecture is exactly the kind of "build a real thing to validate the design" move that catches problems the abstract design doc misses.

Two readers in mind:
- Future-Rich, deciding how to build it.
- Whatever agent or co-developer ends up implementing it. The level of specificity reflects this — implementation-ready in places, ideation-loose in others. Both modes are intentional in a v0.

---

## 2 · Constraints inherited from pnt and from fellows_local_db

These are non-negotiable; they come from pnt's stated goals and from fellows_local_db's design stance, which is the closest existing instance of the static-PWA application pattern.

### 2.1 The bundle is the contract

Per pnt's stated goals: "Export filtered directory views as portable JSON bundles with referenced images" and "Generate visual directories, static websites, and PDFs from those bundles." The bundle is the canonical hand-off between the toolkit layer and the app layer.

For Memorize this means:
- Anything Memorize needs at *build time* — a per-fellow table of visually-similar neighbors, pre-computed tag clusters, anything else — is computed by a toolkit tool that takes a bundle in and emits an enriched bundle out.
- The schema additions to the bundle (e.g. a `visual_similarity` table or JSON file) must be backwards-compatible: a Memorize-aware app reads them; a non-Memorize-aware app ignores them. The toolkit tool augments, never replaces.
- Anything Memorize needs at *runtime* — FSRS state, mnemonics, sessions, briefings — is *not* in the bundle. It's in the user's writable layer. Bundle = directory data; writable layer = personal data.

This is a much cleaner architectural line than the "plugin manifest with mount points" model I proposed in the previous draft. It's also the one pnt's README commits to.

### 2.2 Read-only / writable-layer split

Per pnt: "Keep imported contact data read-only and rebuildable from source exports... Store private relationship data, such as tags and notes, in a separate writable layer." For fellows_local_db this is `fellows.db` (read-only, in OPFS, re-imported on every boot from the shipped bundle) and `relationships.db` (writable, in OPFS, durable across app updates).

For Memorize, all writes are to the writable layer. The full list of tables added to it is in §8. Every one of them is namespaced `memorize_`. None of them is ever sent to a server.

### 2.3 Local-only, not SaaS

The fellows_local_db design stance applies and is reinforced by pnt's purpose: every FSRS card record, mnemonic, session, review event, and briefing card stays on the user's device. The server-side surface (where one exists, as in fellows_local_db's prod deployment) gains no per-user routes for any Memorize data. There is no cross-device sync, no leaderboard, no "see what other fellows are studying," no aggregated anonymized telemetry. Computations that need per-user data run on the user's device. Computations that need only directory data (e.g. visual-similarity neighbors) run at bundle-build time and ship as part of the read-only side.

### 2.4 Compositional, privilege-separated tools (qmail tradition)

Per pnt: "Build tools in the tradition of UNIX software tools... follow a compositional, privilege-separated architecture in the qmail tradition." That implies:
- Each toolkit tool does one thing and reads/writes a contracted format.
- Tools compose via filesystem and pipes; no shared state machine.
- Tools that need different privileges run in separate processes. For Memorize specifically, the embedding-computation tool (which loads and runs an ML model and is the heavyweight dependency) runs separately from the bundle-augmentation tool (which only needs read access to the bundle and write access to the augmented output). Isolating the model behind its own tool means the model choice is swappable, the heavy ML dependency stays out of the rest of the toolkit, and a future "users compute their own embeddings on first install" flow can reuse the same tool unchanged.

The Memorize toolkit tools must respect this even when it's tempting to fold them together for convenience.

### 2.5 Search must be fast and LLM-optional

Per pnt: "Make search fast enough for large personal networks and simple enough to work without an LLM." Memorize benefits from this in two places:
- The "find the X" guided mode uses host search, which therefore must work without an LLM.
- Distractor selection is fast index lookups against a pre-computed similarity table — never a runtime LLM call.

This rules out a tempting design move: "use an LLM to generate plausible distractors for each face at runtime." That would (a) require network, (b) leak directory data to the LLM provider, and (c) be slow. Pre-compute, ship in the bundle, look up locally.

### 2.6 The static-PWA application pattern (as exemplified by fellows_local_db)

For the first runtime target, the relevant application pattern is the static directory PWA: vanilla JS frontend with a service worker, Python stdlib HTTP server, two-DB split in OPFS, magic-link delivery as the distribution channel. Memorize's runtime layer is a feature pattern within *this* application pattern.

If pnt later adds a TUI/CLI application pattern (a natural fit, given prt's lineage), Memorize might also live there as a parallel feature pattern. That's a future iteration — the plan here targets the static-PWA pattern only.

Specifics carried from fellows_local_db:

- **Vanilla JS, no framework.** Plain HTML/CSS/JS with a service worker. FSRS runs in the browser as a plain ES module (vendored or implemented from scratch in <300 lines).
- **Python stdlib only at runtime.** Any pip deps live in `requirements-dev.txt` and run only at build time.
- **Service-worker caching with build-label cache busting.** Memorize's static assets join the SW cache list and version with the rest of the bundle.
- **Two-phase load.** The directory list endpoint is fast, full payload fetches in the background. Memorize must not call into a study session before the full payload arrives, and must degrade gracefully if it hasn't.
- **Magic-link auth on prod, none on dev.** The feature doesn't think about this; the application pattern enforces it.

---

## 3 · Research foundations (carried forward, abridged)

These were in the previous ideation doc; restating tersely so this plan stands on its own.

- **Face-name binding is uniquely hard** — anterior hippocampal task, used as an early-AD marker (FNAME-12). Don't assume vocab-flashcard intuitions transfer.
- **Baker/baker paradox** — role/occupation is much easier to remember than surname. Treat face→name and face→role as separate cards with separate state.
- **Distinctive feature + transformed name + visual link** is the validated mnemonic recipe (Lorayne; replicated). Build encoding prompts around this, not just retrieval prompts.
- **Pattern separation matters when the population is similar.** Distractors must be visually-similar fellows, not random ones. This is the single highest-leverage UX choice the feature will make.
- **FSRS** beats SM-2 by 20–30% in benchmark; default in Anki since 2023. Three Component Model (Retrievability, Stability, Difficulty) per card.
- **Production effect doesn't help face-name pairs.** Don't bake "say the name out loud" features in expecting memory benefits — only ergonomic / engagement benefits.
- **Encoding > scheduling for the hard cases.** When a card lapses, don't just reschedule; force a brief re-encoding step.

If we're going to put research breadcrumbs in the codebase, the right place is `docs/Memorize.md` in the host app, with citations and short rationales next to the design choices that depend on them. Future contributors deserve to know *why* distractors are similar-not-random, etc.

---

## 4 · How Memorize decomposes onto pnt

This is the part that moved most between the previous draft and this one. Once the pnt README is on the table, "what is a plugin" stops being the right question. The right question is: **for each capability Memorize needs, which pnt layer does it belong in, and what data contract does it cross?**

I'll lay out the decomposition, then say what pnt would need to provide for it to work cleanly.

### 4.1 The two layers Memorize touches

**Toolkit layer** — small, composable, Unix-tradition tools. Each takes a bundle on input and emits a (possibly augmented) bundle on output. They run at build time, on the operator's machine or in CI. They never see per-user state.

**App layer** — code that runs *inside* a generated app. For the static-PWA application pattern, that means JS in the browser, Python stdlib in the dev/prod server, and the writable layer in OPFS. The app layer reads the (Memorize-augmented) bundle and reads/writes the user's writable layer.

The bundle contract is the only thing the two layers share. That's the architecture's whole point.

### 4.2 Toolkit-layer tools (proposed)

Initial set, all standalone executables that read/write bundles or bundle-adjacent files:

- **`pnt-bundle-similarity`** — reads a bundle and a sibling vectors file, computes per-fellow k-nearest-neighbors, emits an augmented bundle with a `visual_similarity` table (or sibling JSON file — depends on the bundle schema in `CONTRACTS.md`). Pure data manipulation; no ML dependency; trivially auditable. This is the highest-value toolkit piece for Memorize: it's what makes confusion-grid mode and similar-distractor selection possible.
- **`pnt-embed-faces`** *(separate tool, separate process, isolated dependency)* — loads a vendored ONNX face-embedding model and runs it locally over a bundle's image directory, emitting a vector file. **No network calls. No remote service. No third-party API.** `pnt-bundle-similarity` shells out to this, but the two tools share no code beyond the vector-file format. The split exists so that (a) the heavy ML dependency stays confined to one tool, (b) the model choice is swappable without touching the similarity tool, and (c) the same tool can later run on a user's device for the "users compute their own embeddings on install" flow (see §4.6) — same code, same model file, different invocation context.
- **`pnt-bundle-clusters`** *(later)* — pre-computes tag/role co-occurrence clusters. Used by cluster mode (§6/§7) and by the briefing card's "unexpected overlap" section. Cheap; pure data; could in principle be folded into `pnt-bundle-similarity`, but separate is cleaner per the Unix-tradition stance.

**The vendored model.** Default ships with **MobileFaceNet** in ONNX format — a 4MB model that achieves ~99.5% accuracy on standard face-verification benchmarks and runs in ~18–25ms per face on a mobile phone, well under 5ms on a modern laptop. MobileFaceNet was specifically designed for mobile/embedded inference and is mature: published 2018, widely deployed, well-documented ONNX conversions exist, no training required for our use case (we only need its embeddings, not classification).

The model file lives in the source tree, vendored alongside the tool, with a recorded SHA-256. It does **not** ship inside generated bundles by default — only the *vectors* it produces ship. (Reasoning: the bundle is what users download; bloating it with a 4MB model file every user already has, or could re-download, is wasteful. The model lives with `pnt-embed-faces`.) Users who want to recompute embeddings on their own device get the model alongside the tool; the PWA flow that wants the model in-browser ships it as part of the PWA's static assets, not the bundle's content.

Why MobileFaceNet specifically over alternatives: it's the smallest mature option that hits production accuracy, the conversion path to ONNX is well-trodden, and Hugging Face's ONNX-community ecosystem has compatible quantizations. Alternatives worth keeping on the radar: EdgeFace (smaller, newer), ArcFace at the larger end if accuracy ever turns out to matter more than size. The vendoring discipline (§4.2.1 below) makes swapping models cheap.

**Privacy posture as a result of this decision:**
- No headshot ever leaves the operator's machine during bundle build.
- No external service is in the trust path.
- No per-image API cost or rate limit.
- No "did you read the embedding service's privacy policy" friction at install time.
- The embedding step is fully reproducible: same model + same images = same vectors (modulo float-precision noise from quantization, which we pin).

#### 4.2.1 Model vendoring discipline

Because the model file is the heaviest single artifact in the pipeline and the one most likely to evolve, treat it carefully:

- The model lives at `tools/pnt-embed-faces/model/mobilefacenet.onnx` (or the equivalent path in pnt's actual layout). Vendored, committed, not fetched at runtime.
- A `MODEL_CARD.md` next to it records: source, version, conversion notes, SHA-256 of the file, license, accuracy benchmarks reproduced locally, and the date this combination was validated end-to-end with `pnt-bundle-similarity`.
- Bundle-augmentation reproducibility metadata (per §4.3) records *which* model produced the vectors. So a bundle augmented in 2026 with MobileFaceNet v1 is distinguishable from one augmented in 2027 with EdgeFace v3, and downstream code can decide how to handle that.
- Updating the vendored model is a deliberate PR with a changelog entry and a re-run of `pnt-bundle-similarity` against the project's reference fixture bundles. Not a casual upgrade.
- Same vendoring rule applies in the PWA context: when the model ships as a static asset for in-browser inference (§4.6 path), it's vendored into the PWA's static directory with the same SHA-256 verification at load time.

Likely composition:

```
pnt-bundle-export --filter ehf-2026 --output bundles/ehf-2026.bundle
pnt-embed-faces bundles/ehf-2026.bundle --vectors bundles/ehf-2026.vectors
pnt-bundle-similarity bundles/ehf-2026.bundle bundles/ehf-2026.vectors \
    --output bundles/ehf-2026.augmented.bundle
pnt-bundle-clusters bundles/ehf-2026.augmented.bundle \
    --output bundles/ehf-2026.studyready.bundle
pnt-app-build-pwa --pattern static-directory --features memorize \
    bundles/ehf-2026.studyready.bundle --output dist/
```

That last line invokes the app-build step, which is where the app layer is materialized.

### 4.3 The bundle augmentation contract (proposal back to pnt)

For Memorize's toolkit tools to work cleanly, the bundle schema needs to support:

- **A namespace for feature-specific augmentations.** Concretely: a recognized way for a tool to add a `visual_similarity` table (or JSON sibling file, or whatever the canonical extension mechanism is in `CONTRACTS.md`) without colliding with other tools. Suggest: `extensions/<feature_name>/...` inside the bundle, or a top-level `extensions: { feature_name: ... }` object in the bundle manifest.
- **Backwards compatibility.** A bundle augmented by `pnt-bundle-similarity` must still be valid input to a tool that doesn't know about Memorize. Augmentation, never replacement.
- **Reproducibility metadata.** Each augmentation step records (in the bundle manifest) what tool ran, with what args, against what bundle hash, when. So three months later you can tell whether your similarity vectors are stale.

These are properties of the bundle contract itself, not Memorize-specific. Presumably they're in (or will be in) `CONTRACTS.md`. If they're not, this is the prompt.

### 4.4 App-layer feature within the static-PWA pattern

The runtime experience — the actual study sessions, FSRS scheduler, mnemonic prompts, briefing cards — lives in the app layer of a static-PWA-pattern app. From the application-pattern perspective, it's a *feature* the pattern supports, not a separate "plugin" in the host-plus-loader sense.

What the static-PWA application pattern needs to provide for Memorize to slot in cleanly:

1. **A migration story for the writable layer.** A way to apply the SQL in §8 to the user's writable layer (`relationships.db` in fellows_local_db terms) on first run and on app upgrade. fellows_local_db today has a hand-rolled approach that's about 80% of what's needed; pnt can formalize it. Memorize tables are namespaced `memorize_*` so multiple features can coexist without collision.
2. **Read access to bundle extensions from the runtime.** Memorize needs to read the `visual_similarity` extension (and later `clusters`) from the bundle at runtime. Whatever API the static-PWA pattern exposes for "read bundle contents" should support extension namespaces. The simplest version: just SQL `SELECT` against attached tables that the bundle ETL produced.
3. **Server-side route extension within local-only invariants.** Memorize adds a small set of `/api/memorize/*` endpoints (§9). Those endpoints touch only the user's writable layer + the bundle, and they live behind whatever auth the application pattern provides (magic-link in fellows_local_db). The application pattern should formalize how features add routes — convention over configuration is fine — and should statically prevent any of those routes from leaking writable-layer rows back through the magic-link channel as if they were directory data.
4. **UI integration points.** A "Study this group" affordance on the group detail view, a "Memorize" entry in the main nav, and an aside on the fellow detail view for memory hints / mnemonics. In a vanilla-JS world this is just "the application pattern's templates have well-known IDs that features can target." Not a heavy framework.
5. **Service-worker manifest contribution.** Feature static assets join the SW cache list and version with the build label. Same as fellows_local_db today.

Notice that none of this requires a "plugin loader" abstraction. It requires:
- A bundle contract that supports namespaced augmentations.
- An application pattern that has well-known seams (writable-layer migrations, route additions, template targets, SW manifest contribution).
- A convention for where feature code lives in the source tree.

This is genuinely lighter weight than the manifest-and-mount-points plugin model from the previous draft, and is much more in keeping with pnt's stated direction.

### 4.5 Source tree shape (proposal)

For pnt itself:

```
pnt/
  tools/                              # the Unix-tradition tools
    pnt-bundle-export/
    pnt-bundle-similarity/
    pnt-embed-faces/
    pnt-bundle-clusters/              # later
    pnt-app-build-pwa/
    ...
  patterns/
    static-directory-pwa/             # the application pattern fellows_local_db is an instance of
      template/                       # source for the generated app
      features/
        memorize/
          migrations/                 # SQL applied to writable layer
          server/                     # Python route handlers
          static/                     # JS / CSS / templates
          docs/Memorize.md
          tests/
  contracts/                          # bundle schema, etc.
  docs/
    ARCHITECTURE.md
    APPLICATION_PATTERNS.md
    CONTRACTS.md
    USE_CASES.md
    SOURCE_REUSE.md
```

The features under `patterns/static-directory-pwa/features/` are not "plugins" in the Wordpress sense. They're optional source modules that the build step composes in based on flags (`--features memorize`). Composition happens at app-build time, not runtime.

### 4.6 What this leaves open

- **Whether features can ship in third-party repos.** The above puts features in pnt's own tree. That's right for `memorize` if it's a canonical feature; it's wrong if pnt wants a thriving external-feature ecosystem. The pnt README's "build your own personal network tools, or tools for relationship or directory management, or plugins for those apps" suggests external is on the table. The decision point is whether external features are *tools* (toolkit-layer, naturally external — anyone can write a tool that consumes the bundle) or *features* (app-layer, harder to externalize because they extend an application pattern's runtime).
- **The cross-pattern story.** If Memorize ever gets a TUI/CLI implementation (which prt's lineage suggests is plausible), there'd be a TUI-pattern variant of `features/memorize/`. The two share the writable-layer schema and the FSRS implementation; they don't share UI. There's a real architectural question about whether shared logic (FSRS, distractor selection, briefing-card generation) lives in `tools/` or in some `lib/` shared by both patterns. Out of scope for v0; flag for `ARCHITECTURE.md`.
- **The writable-layer scope.** Per-app-origin (each generated app has its own OPFS) or shared across pnt-built apps? Per-app is what fellows_local_db does today and is simpler; shared is what users probably want eventually ("my notes about Anna show up in *both* my EHF directory and my dweb directory"). This decision is upstream of Memorize and should be made for pnt as a whole, not for one feature.
- **User-side embedding as a future option.** The default path is operator pre-computes vectors via `pnt-embed-faces`, ships them in the bundle. The `pnt-embed-faces`-as-its-own-tool architecture preserves the option for a "user computes their own vectors on first install" flow — same model file, same tool, but invoked in the browser via the WASM/WebGPU runtime against the bundle's images. This is valuable for high-trust contexts where users want to verify the similarity table themselves, or where the bundle ships without pre-computed vectors at all. Not a v0 path; explicitly preserved as a v2 option.

### 4.7 What the spike will reveal that this proposal misses

I expect at least:
- The bundle-extension namespace shape: tables in the same SQLite file vs sibling files vs JSON-in-manifest. Whatever's chosen affects every subsequent toolkit tool.
- The migration runner's story for *feature uninstall / data wipe*. Important given the local-only stance — users must be able to reclaim space.
- How application-pattern templates target seams in vanilla JS without becoming a faux-React component model.
- Service-worker version-bumping when *only* feature assets change (probably solved by treating feature assets as part of the host bundle for cache-busting purposes — same approach fellows_local_db uses today).

The plan is to build the spike (§10) with these gaps acknowledged, then feed the findings back into `ARCHITECTURE.md` / `CONTRACTS.md` / `APPLICATION_PATTERNS.md` before iteration 2.

---

## 5 · The two modes

This is the central design move. Same data, two algorithms, two UIs, *one* underlying card-state table.

### 5.1 Mode A — Cram

**User goal:** "I'm walking into a room of N people tomorrow morning. Help me recognize as many as possible by then."

**Wrong tool:** classic spaced repetition. Spacing intervals don't fit a single-night session.

**Right tool:** in-session Leitner with coverage and lag constraints.

**Flow:**

1. **Trigger.** User picks a group (existing first-class object), taps "Study" / "Cram for this group" on the group detail view.
2. **Encoding pass.** Slow swipe through every fellow once, ~5 seconds each. Face + name + role + one tag. No quiz. Optional inline prompt "notice one thing about this face" (the Lorayne distinguishing-feature step). User can pin a mnemonic mid-pass; saved to `memorize_mnemonic`.
3. **Quiz rounds.** Faces enter box 1. Each correct answer promotes a face one box (up to ~4). Each wrong answer drops back to box 1. The session ends when every fellow has been promoted out of box 1 *and* hit at least one correct answer with intervening cards between presentations. Sampling rule: pick the highest-priority face under the constraint "not seen in the last K cards" where K starts at ~3 and grows as box level grows.
4. **Coverage guarantee.** Track `seen_count` per face within the session. The sampler is biased to under-seen faces until every face has been quizzed at least once. Without this, the easy half of the room gets re-drilled and the hard half stays untouched.
5. **End-of-session diagnostic.** A final cold-pass: every face shown exactly once, no feedback during, score reported at the end. Tell the user upfront: *this* is the score that matters. The during-practice score is for navigation, not assessment. (This is consciously using the testing effect for one last consolidation pass and calibrating the user's confidence.)
6. **Briefing card.** Generated from the cram session + group data. (See §6.)

**What we are *not* doing in Cram:** writing FSRS state. Cram sessions are short-horizon-only by design and shouldn't pollute long-term scheduling. They write to `memorize_session` and `memorize_review_event`, but `memorize_card_state` is not touched. *Optionally* the user can choose at session end "remember what I struggled with for next time" — that one button promotes the worst-performing N cards into Library mode with appropriate initial FSRS state.

### 5.2 Mode B — Library

**User goal:** "I want to actually know the people in this fellowship over time."

**Right tool:** FSRS, per-card-type, with a few customizations for face-name's quirks.

**Card types** (separate FSRS state per type per fellow):
- `face_to_name`
- `face_to_role`
- `name_to_face`
- `role_to_faces` (group of N fellows who do something — different mechanic, see §6.4)

**Customizations vs vanilla FSRS:**
- **Lapse → re-encode.** When a card hits "Again," the next review forces an encoding-prompt step before scheduling. The encoding event itself logs to `memorize_review_event` so we can later analyze whether the re-encode is helping.
- **Difficulty floor for face_to_name.** This card type is uniformly harder than face_to_role (Baker paradox). Initialize with a higher difficulty than FSRS's default to avoid early over-confidence.
- **Confusion-aware scheduling boost.** When a face is correctly identified but the user briefly hovered over a similar fellow's name (we track last-considered choice in MCQ format), schedule the *similar* fellow's card slightly sooner. Borrowed conceptually from the LECTOR (2025) approach to semantic similarity in SRS, simplified.

**FSRS implementation:** vendor `ts-fsrs` if its license is compatible, or implement FSRS-5 from scratch in vanilla JS — it's roughly 200–300 lines of arithmetic (the algorithm is well-documented in fsrs4anki's tutorial.md). Implementing from scratch may actually be preferable here given the no-framework / vendored-only-after-review house style.

---

## 6 · Quiz / game modes (concrete, with bindings to the host UI)

Each mode targets a different cognitive operation. They mix freely in Library mode (interleaving improves retention); in Cram mode the user can opt for one or two and stay in them.

### 6.1 Face → Name (4-way MCQ)
The default. Face shown big, four name buttons below. Distractors selected with similarity logic (§6.6) — *not* random.
- **Cram:** swipe / tap, no FSRS rating.
- **Library:** the four buttons translate to FSRS ratings — correct on first try = Good, correct after a hesitation = Hard, wrong then corrected = Again-then-Good treated as Again.

### 6.2 Face → Role (4-way MCQ)
Easier baseline; useful as warm-up, especially for new users. Role-cluster distractors (other fellows in adjacent roles) keep this from being trivial.

### 6.3 Name + Role → Face (3×3 grid pick)
Reverse direction. Show "Anna Chen — climate finance researcher," 3×3 grid of faces. Trains the room-scanning retrieval pathway.

### 6.4 Role → Faces (multi-select)
"Tap all the fellows working on community health." Five-second pause before submission. Trains the *cluster* retrieval that matters most for "who should I introduce to whom." Closer to a real-world task than any other format.

### 6.5 Free recall + self-grade
Show face. User types or speaks name/role. Self-grade. Highest-yield format for Library mode but most effortful — opt-in. Voice optional and non-required.

### 6.6 Confusion grid (pattern separation drill)
2×2 of the most-confusable faces — computed from this user's `memorize_review_event` history (which distractors did they hover or click incorrectly?), or from pre-computed visual similarity in the read-only DB if no user history exists yet. The single highest-ROI drill for the failure mode where you confidently call someone the wrong name.

### 6.7 Mnemonic creation step (encoding mode, not testing)
Triggered on (a) first exposure to a face, (b) second consecutive lapse on a card. Three lightweight prompts: "Notice one feature of this face." → "What does the name remind you of?" → "Type a phrase linking them." Saves to `memorize_mnemonic`. Replays on next review if available.

### 6.8 Speed round
60 seconds, one-tap correct/skip, no distractors, name-or-role-shown-with-face. Less rigorous; high engagement. Useful in Cram and as ADHD-friendly variety. Don't let it dominate — trains shallow recognition.

### 6.9 Distractor selection logic — the make-or-break detail

This is where most flashcard apps fail at face-name learning specifically and where we have an unfair advantage: the directory has structured tag/role data and we can pre-compute visual similarity. Tiered fallback:

1. If the user has accumulated ≥ ~25 `memorize_review_event` rows for this group, use their personal confusion matrix: "fellow X is, for this user specifically, most often confused with fellow Y."
2. Otherwise, use the pre-computed visual-similarity neighbors from the content DB.
3. Fall back to "shares a role/tag cluster with the target."
4. Fall back to random (only as last resort).

The toolkit step (`pnt-embed-faces` + `pnt-bundle-similarity`, see §4.2) computes embeddings for each headshot using a locally-vendored MobileFaceNet ONNX model, then stores k-NN per face as a `visual_similarity` extension in the augmented bundle. No external service; no headshot ever leaves the operator's machine; reproducible. The data is per-fellow not per-user, so every installer of the bundle gets the same similarity table — no per-user computation at install time, no per-user data leaking out.

---

## 7 · The connection-spark layer (the differentiator)

This is where the feature earns its keep relative to a generic flashcard app. The directory has structured tag, role, and (in some pnt apps) relationship data. Use it.

### 7.1 Pre-event briefing card

Generated at the end of (or on demand for) a group. One screen, four sections:

- **People you should seek out** — top-N fellows whose tags overlap with the user's stated interests (a settings entry asking the user to list their interests; if absent, fall back to the tags they've previously starred / noted).
- **Unexpected overlap** — pairs of fellows whose work has non-obvious adjacency. Computed as: tag co-occurrence that is rare *across the directory* but present *within this group*. This surfaces "the longevity researcher and the smart-contract person both work on funding mechanisms" — the kind of thing the user wouldn't notice on their own.
- **Bridge opportunities** — pairs of fellows where the user is the only path between them in the relationship graph (where one exists; depends on the host app's notion of "relationship"). The user is positioned as connector, not seeker.
- **Names you struggled with** — distilled from the cram session. The five hardest faces, with their mnemonics if the user wrote any.

The briefing card is itself a saved record (`memorize_briefing`) so the user can pull it up tomorrow morning on the ferry without re-running the computation. It is local-only.

### 7.2 "Find the X" guided mode

Instead of (or alongside) random quizzes, frame the session: "Tonight, find the 3 fellows working on community health you haven't met yet" or "Find 5 fellows whose work intersects with rainwater systems." Memorization-via-search-task. Engagement is much higher when there's a narrative goal. Implementation-wise this is just a query against the content DB with a quiz wrapper.

### 7.3 Cluster mode (build schemas first)

Group fellows by tag cluster on first-pass learning. Memory research suggests learning items within a coherent category is more efficient than random for *schema-building*; once the schema exists, interleaving wins. So: cluster on first pass, interleave on subsequent passes. The default Library mode session structure should reflect this.

### 7.4 Notes pinned to faces

Let the user attach a private note to any fellow ("met at 2025 retreat, talks fast, also into FSRS coincidentally"). These notes become powerful retrieval cues *and* future event prep. They're long-tail value. fellows_local_db already supports per-group notes; consider whether per-fellow notes also fit, or whether adding a fellow to a group is the canonical way to attach context.

### 7.5 Group as event context (already mostly there)

`group` is already a first-class object in fellows_local_db. The cram-mode flow just adds a "Study" affordance to the existing group detail view. No new entity needed for the v0. Later iterations might add `group.event_date` and `group.event_location` (already optional fields on the group table per the existing schema) and use them for briefing copy.

---

## 8 · Schema additions (concrete)

All additions to `relationships.db`, all namespaced `memorize_`. No additions to the read-only `fellows.db` *except* via the build-time hook that adds `fellows_visual_similarity`.

```sql
-- Per-card FSRS state. One row per (fellow, card_type).
-- Cram mode does NOT write here. Library mode does.
CREATE TABLE memorize_card_state (
  id              INTEGER PRIMARY KEY,
  fellow_id       INTEGER NOT NULL,    -- references fellows.record_id (in attached fellows.db)
  card_type       TEXT NOT NULL CHECK (card_type IN
                    ('face_to_name','face_to_role','name_to_face','role_to_face')),
  -- FSRS state
  due             TEXT,                -- ISO-8601
  stability       REAL,
  difficulty      REAL,
  elapsed_days    INTEGER,
  scheduled_days  INTEGER,
  reps            INTEGER NOT NULL DEFAULT 0,
  lapses          INTEGER NOT NULL DEFAULT 0,
  state           INTEGER NOT NULL DEFAULT 0,
                    -- 0=new, 1=learning, 2=review, 3=relearning
  last_review     TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (fellow_id, card_type)
);

-- Encoding aids the user has authored. May exist independently of card_state.
CREATE TABLE memorize_mnemonic (
  id            INTEGER PRIMARY KEY,
  fellow_id     INTEGER NOT NULL,
  feature_note  TEXT,         -- "wide mouth", "always wears red"
  name_hook     TEXT,         -- "Whealen → whale"
  link          TEXT,         -- "whale wedged in their wide mouth"
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (fellow_id)
);

-- One row per study session (cram or library).
CREATE TABLE memorize_session (
  id              INTEGER PRIMARY KEY,
  group_id        INTEGER,                 -- nullable: library sessions may be ungrouped
  mode            TEXT NOT NULL CHECK (mode IN ('cram','library','cluster','find_the_x')),
  started_at      TEXT NOT NULL,
  ended_at        TEXT,
  cards_seen      INTEGER NOT NULL DEFAULT 0,
  correct         INTEGER NOT NULL DEFAULT 0,
  diagnostic_score        INTEGER,         -- final cold-pass score in cram
  diagnostic_total        INTEGER
);

-- One row per shown card / answer. The high-volume table.
-- The shown_distractors column is the magic dataset for personal
-- confusion-matrix learning — see §6.6 / §6.9.
CREATE TABLE memorize_review_event (
  id                 INTEGER PRIMARY KEY,
  session_id         INTEGER NOT NULL,
  fellow_id          INTEGER NOT NULL,
  card_type          TEXT NOT NULL,
  rating             INTEGER,          -- 1=Again, 2=Hard, 3=Good, 4=Easy
                                       --   (in cram, derived from correct/incorrect)
  response_ms        INTEGER,
  shown_distractors  TEXT,             -- JSON array of fellow_ids shown as choices
  picked_distractor  INTEGER,          -- which distractor was wrongly picked, if any
  created_at         TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Cached briefing cards. Local-only.
CREATE TABLE memorize_briefing (
  id              INTEGER PRIMARY KEY,
  group_id        INTEGER NOT NULL,
  generated_at    TEXT NOT NULL,
  payload_json    TEXT NOT NULL    -- the structured briefing
);
```

**Build-time addition to the bundle's read-only side** (shipped to all users, identical content for everyone). In fellows_local_db terms this is a table added to `fellows.db`; in pnt-bundle-contract terms it's a `visual_similarity` extension namespaced under whatever the contract specifies for feature augmentations. The schema is the same regardless:

```sql
CREATE TABLE fellows_visual_similarity (
  fellow_id        INTEGER NOT NULL,
  similar_fellow_id INTEGER NOT NULL,
  rank             INTEGER NOT NULL,    -- 1 = most similar
  score            REAL NOT NULL,
  PRIMARY KEY (fellow_id, similar_fellow_id)
);
CREATE INDEX idx_fellows_vis_sim_lookup ON fellows_visual_similarity(fellow_id, rank);
```

This table is produced by `pnt-bundle-similarity` (§4.2). It's per-fellow data, not per-user, so it ships in the bundle and every installer gets the same thing.

---

## 9 · API surface (server, all under `/api/memorize/*`)

All handlers run against `relationships.db` (for user state) with `fellows.db` ATTACHed read-only — same pattern as the existing groups endpoints.

```
GET    /api/memorize/cards/<fellow_id>          # all card_state for a fellow
GET    /api/memorize/cards/due                  # cards due now (Library mode)
PATCH  /api/memorize/cards/<id>                 # FSRS state update after a review
POST   /api/memorize/sessions                   # start a session
PATCH  /api/memorize/sessions/<id>              # end / update session
POST   /api/memorize/sessions/<id>/events       # batch-append review events
GET    /api/memorize/mnemonics/<fellow_id>      # read mnemonic
PUT    /api/memorize/mnemonics/<fellow_id>      # upsert mnemonic
GET    /api/memorize/briefing/<group_id>        # cached briefing
POST   /api/memorize/briefing/<group_id>        # regenerate briefing
GET    /api/memorize/distractors                # distractor candidates for a fellow
                                                # (reads similarity from fellows.db
                                                #  + confusion from review_event)
```

These are all single-user-scoped (the server has no per-user state beyond the magic-link session cookie that already exists), and all of them write to or read from tables namespaced `memorize_*`. The local-only invariant from §2.3 holds.

Note: `GET /api/memorize/distractors` is interesting because it joins read-only similarity data with read-write user confusion data. The implementation lives in the feature's `server/routes.py`; nothing about the join shape needs to be visible to other features.

---

## 10 · Spike — the v0 build

**Goal:** in one focused day, ship a face → name multiple-choice quiz playable from any existing group, with simple-then-similarity-tiered distractors, scoring at the end. No FSRS yet, no mnemonics, no briefing.

This is shippable, useful by itself for cramming, and is the smallest concrete app-layer feature we can build to pressure-test what the static-PWA application pattern needs to provide.

The spike is **app-layer only**. It does not exercise the toolkit-layer tools (`pnt-bundle-similarity` etc.) — those land in iteration 3, when visual-similarity distractors arrive. The spike uses tag-overlap fallback for distractors, which is good enough to validate the experience without committing to the bundle-augmentation contract before it's worth committing.

### 10.1 What ships in the spike

- Migrations applied to the writable layer: `001_create_card_state.sql`, `002_create_session.sql`, `003_create_review_event.sql`. (The card-state table is added now even though Library mode doesn't use it yet — keeps the migration sequence stable.)
- Server route: `GET /api/memorize/quiz/<group_id>` — returns the next card (face URL, name, role, 4 name choices) given a session ID. Server-side picks the next fellow + 3 distractors using simple "share at least one tag, else random" logic. (Visual similarity lands in iteration 3.)
- Server routes: `POST /api/memorize/sessions` and `POST /api/memorize/sessions/<id>/events`.
- Front end: a "Study this group" button on the group detail view. Tapping it opens a full-screen quiz view. Big face, four buttons. Progress bar. Score at the end. Hard reload returns to the directory.
- Service worker entry for the new static assets.
- Three tests:
  - `tests/test_memorize_routes.py` — quiz endpoint returns a well-formed card.
  - `tests/test_memorize_migrations.py` — migrations are idempotent and reversible.
  - `tests/e2e/memorize.spec.js` — Playwright: open a group, hit "Study," answer 5 questions, see a final score.

### 10.2 What the spike *does not* ship

- FSRS scheduling (Library mode). Quiz is purely random-from-the-group.
- Cram-mode in-session Leitner. (Order is random, no box state.)
- Mnemonic creation prompts.
- Briefing card.
- Visual-similarity distractors. (Random + tag-overlap only.)
- Confusion-grid mode.
- Speed round.
- Free-recall input.
- Any toolkit-layer tooling. (`pnt-bundle-similarity` is iteration 3.)

These all land in numbered iterations after.

### 10.3 What the spike must reveal about pnt's architecture

- **Where in the source tree feature code actually goes.** §4.5 proposes `patterns/static-directory-pwa/features/memorize/`; the spike is the test of whether that decomposition feels right when you're holding a working feature.
- **How a feature targets template seams in vanilla JS.** "Study this group" needs to appear on the group detail view. The cleanest version is "the group-detail template has well-known IDs/slots that features can target." The dirtiest version is "hand-edit the host template." The spike will hand-wire it the dirty way and surface the seam shape we want.
- **How writable-layer migrations get sequenced** when multiple features want to add tables. Even with one feature in the spike, the question of "what does the migration runner look like" needs an answer.
- **Whether the bundle's runtime SQL access pattern handles feature-added tables** when those tables eventually arrive (iteration 3). Spike validates the access pattern even before the table exists, by reading existing tables (tags, roles) for distractor selection.
- **Service-worker version-bumping** when feature assets change. Probably solved by treating feature assets as part of the host bundle for cache-busting purposes — same approach fellows_local_db uses today.

### 10.4 What the spike does *not* try to validate

- The toolkit-layer / bundle-augmentation contract (§4.3). Iteration 3.
- The tool boundary between `pnt-embed-faces` and `pnt-bundle-similarity` (§4.2). Iteration 3.
- The application-pattern abstraction itself. The spike builds *one* feature against *one* pattern; whether the pattern abstraction is right requires a second feature, which is out of scope for this plan.
- Backwards compatibility with the existing fellows_local_db. This is for the rebuild-on-pnt version, not retrofit. If we want a feature-comparable experiment in the *current* app to validate user demand before the toolkit work, that's a separate, narrower task.

---

## 11 · Iteration plan (numbered, post-spike)

Each iteration is shaped to be a meaningful 1–3 day Claude Code worktree. Order optimizes for (a) earliest user value and (b) earliest stress on the architecture.

1. **Spike** (§10). App-layer only.
2. **In-session Leitner cram mode.** Box state derived from `memorize_session` + `memorize_review_event`, sampler with min-lag and coverage constraints, end-of-session diagnostic pass with separate score. Big UX jump for the room-tomorrow use case. *Architectural pressure:* session lifecycle + stateful UI flow within the static-PWA pattern.
3. **`pnt-bundle-similarity` and visual-similarity distractors.** First toolkit-layer tool ships. Splits into `pnt-embed-faces` (vendored MobileFaceNet ONNX, runs locally — no network, no service contracts, no per-image API costs, no consent friction) and `pnt-bundle-similarity` (the augmentation tool). Bundle gains a `visual_similarity` extension. App layer reads it and replaces tag-overlap distractor logic. *Architectural pressure:* this is the first iteration that exercises the bundle-augmentation contract — namespace, backwards compatibility, reproducibility metadata. Likely surfaces real questions for `CONTRACTS.md`. *Lower-risk than earlier drafts framed it:* the local-only embedding decision means there's no service contract to negotiate, no privacy-policy review to gate the iteration on, and no "what if the API changes" maintenance overhead.
4. **FSRS Library mode.** Implement FSRS-5 scheduler in vanilla JS (vendored or written from scratch). Per-card-type state. Daily "review queue." Lapse → re-encode prompt. *Architectural pressure:* longer-running per-user state, larger writable-layer footprint, query patterns at scale.
5. **Mnemonic creation prompts.** Encoding step on first exposure / lapse. Saved to `memorize_mnemonic`. Surfaced on review. *Architectural pressure:* template-seam targeting on the *fellow detail* view, not just group detail.
6. **Confusion-grid mode + personal confusion matrix.** Use accumulated `memorize_review_event` data to surface drill targets. *Architectural pressure:* read patterns over many sessions in the writable layer; no architectural change but exercises the writable-layer schema for queries we haven't done yet.
7. **Briefing card / connection-spark.** Tag overlap, unexpected adjacency, bridge opportunities, struggle list. Saved to `memorize_briefing`. *Architectural pressure:* feature-layer code reading directory-shape data (tags / roles / relationships) — formalizes whatever query API the static-PWA application pattern exposes for "give me the directory's structured data."
8. **Find-the-X mode + cluster mode.** Different session shapes, share infrastructure. Mostly UX + sampler variants on top of (4)–(7). May spawn a `pnt-bundle-clusters` toolkit tool if cluster pre-computation pays off; could also be done at runtime.
9. **Polish.** Voice input on free-recall, haptics, offline robustness audit, accessibility pass.

Iteration 7 is the moment Memorize proves it can do something a generic flashcard app cannot, and is therefore the highest-leverage point to evaluate whether the whole project has earned its name. If it doesn't feel meaningfully better than Anki at iteration 7, something's wrong upstream.

Iteration 3 is the architectural fork-in-the-road: it's the first time the bundle-augmentation contract is real, and decisions made there shape every subsequent toolkit-layer feature. Worth slowing down for and feeding learnings back into `CONTRACTS.md` before iteration 4.

---

## 12 · Privacy / security boundary

The data this feature collects is more sensitive than it might seem.

- **Mnemonics often involve personal/embarrassing imagery.** "He looks like my uncle Larry" is not what you'd want to leak. Local-only is the right default; never sync to server, never include in any export that doesn't ask explicitly.
- **Confusion data is socially fraught.** "I always confuse Person A with Person B" being attributed to a specific user could be uncomfortable or insulting. Stays in OPFS, never aggregated, never sent.
- **Mnemonic export should be opt-in and explicit.** A future "export my study data" feature should default-exclude mnemonics and require a confirm.
- **The briefing card is a magnet for data leakage.** "Here's who you should seek out tomorrow" being shared accidentally (screenshot, "look what my app suggested") is fine for the user — but the feature should never cause it to be shared automatically. No "share briefing" button in v0. If it appears later, it should require explicit confirm and strip mnemonic content.
- **Service-worker cache should not store briefings or mnemonic content beyond what's needed for offline.** The OPFS DB is the source of truth; treat the SW cache as ephemeral.
- **Toolkit-layer tools that handle images need privacy boundaries too — but the default architecture eliminates the biggest risk.** Because `pnt-embed-faces` (§4.2) runs a locally-vendored ONNX model and never makes a network call, headshots never leave the operator's machine during bundle build. This was the single most concerning data-flow in earlier drafts of this plan; commit to the local-vendored-model architecture and most of the privacy concern in the build pipeline goes away. Residual concerns: keeping the model file integrity-checked (SHA-256 in `MODEL_CARD.md`, verified at load time), keeping the choice of model auditable, and not letting future "convenience" PRs reintroduce a remote-API path without explicit review. The `MODEL_CARD.md` discipline from §4.2.1 is the durable defense.

A test that should exist: "no `memorize_*` table content appears in any HTTP response body of any feature endpoint that accepts an unauthenticated request." Run as part of the test suite.

---

## 13 · UX details worth getting right early

Things that are easy to get wrong and hard to fix later.

- **Tap targets are huge.** This is a phone-in-bed feature. Big buttons.
- **No reading. Show, don't tell.** A quiz UI with a paragraph of explanation is a quiz UI no one uses. The first session should require literally one tap to start.
- **Honest self-assessment.** Don't gamify accuracy — gamify *consistency* and *coverage*. People should not feel punished for pressing "Again."
- **A "they're new to me" toggle on each face.** Library mode shouldn't penalize "I genuinely don't know this person yet" the same way as "I forgot."
- **Image preloading.** Preload the next 5 faces in the queue. Nothing kills flow like a half-second face load.
- **Haptic on right/wrong.** Quiet — others may be in the room. Do NOT play audio.
- **One-handed friendly.** Test on phone with one thumb, holding tea in the other hand.
- **Dark mode by default for evening cram sessions.** This is when most people will use it.
- **An ADHD-friendly "I'm done for now" exit.** End-session anywhere; partial sessions are saved with what was learned. No guilt UI.

---

## 14 · Open questions (need Rich's input)

Resolved by getting the pnt README:
- ~~"Is pnt's plugin contract being designed in parallel?"~~ — yes, `ARCHITECTURE.md` etc. exist. The questions below replace this.
- ~~"What's the canonical pnt repo layout?"~~ — proposed in §4.5; pending review against the actual docs.

Still open, and most are upstream of Memorize:

1. **What's actually in `CONTRACTS.md` (the M0 data contracts)?** Specifically the bundle schema and its extension mechanism. Iteration 3 of this plan commits to a particular augmentation shape; before it ships, we need that shape to be the one the contract uses, not the one I sketched in §4.3.
2. **What's actually in `APPLICATION_PATTERNS.md`?** Especially: is the static-PWA pattern explicitly named and described? Are there other patterns relevant to Memorize (TUI? PDF directory)? Memorize might want a parallel feature in a TUI pattern eventually, and that's much easier to plan for if the patterns are pre-named.
3. **What's actually in `SOURCE_REUSE.md`?** prt has tools (`make_directory.py`), models, and a TUI codebase. fellows_local_db has a working PWA. How much of Memorize's app-layer code can be lifted from existing prt/fellows_local_db code, and how much is new? Probably the migration runner approach, the SW cache list approach, the two-DB ATTACHed-read pattern, and possibly groups CRUD all carry forward; FSRS, Leitner, mnemonic capture, briefing generation are net new.
4. **Writable-layer scope.** Per-app-origin (each generated app has its own OPFS, like fellows_local_db today) or shared across pnt-built apps the user has installed? The latter is what users probably want eventually but is much harder; the former is simpler and matches today's behavior. Memorize works fine either way, but the briefing card's "people you should seek out" feature is much more valuable if user interests/notes are shared across apps. Worth knowing the direction before iteration 7.
5. **Image quality and uniformity.** The prior research point about "mixed lighting / framing trains you on photo properties not face properties" — is the EHF data uniform enough? Worth eyeballing before iteration 3 (visual similarity). If the photos are very heterogeneous, the embedding-based similarity is less useful and we lean harder on tag-cluster fallback.
6. **Headshot rights.** Mostly resolved by the §4.2 commitment: `pnt-embed-faces` runs locally with a vendored MobileFaceNet model, no headshot ever leaves the operator's machine, no third-party service is in the trust path. Residual question is narrower: are there contexts where the *bundle itself* containing headshots is a privacy concern (e.g. the dweb personal-network app's second target where users may want to share a directory with peers)? That's a bundle-distribution question, not a Memorize question, and lives upstream in pnt's privacy model. Memorize itself doesn't make this any worse than the directory display already does.
7. **Group sizes and session lengths.** The example was 100 people. What's the actual distribution? If most groups are 15–25 people, the cram-mode UX is different than for 100–200, and pre-event briefing logic (top-N picks) tunes differently.
8. **Relationship graph in the bundle.** Bridge-opportunity logic in the briefing assumes the bundle has *some* notion of fellow-to-fellow relationships. fellows_local_db's bundle today has none — only user-to-fellow (groups, notes). For the dweb personal-network app (the second pnt target), there will presumably be fellow-to-fellow ties in the bundle. The briefing should degrade gracefully when those don't exist; ideally the bundle contract has an optional "relationships" extension that other features can produce and Memorize can consume.
9. **License / dependency posture for FSRS.** Vendor `ts-fsrs` (license check needed: MIT, but verify) or implement FSRS-5 from scratch. Strong lean toward implement-from-scratch given the no-pip / vendor-only-after-review house style and the algorithm's compact size. Decision blocks iteration 4.
10. **Are toolkit tools written in Python, JS/Node, or polyglot?** prt is Python; fellows_local_db is Python+JS. The qmail tradition doesn't care, as long as the data contract is clean. But picking a default for `pnt-bundle-similarity` etc. matters for `SOURCE_REUSE.md` reasons. Best guess: Python for toolkit tools (prt lineage, easier image processing, `pip install` of vision-model SDK is dev-only so doesn't violate fellows_local_db's stdlib-runtime stance), JS for app-layer feature code.
11. **Auth in the spike.** fellows_local_db has magic-link auth on prod and none on dev. The spike presumably runs on dev. The contract should be "the application pattern enforces auth, the feature doesn't think about it." Confirm that's right before iteration 1.

---

## 15 · References

Memory & face-name research (carried from prior doc, lightly curated):
- Sperling et al., "Putting names to faces" (PMC3230827). Anterior-hippocampal localization.
- James et al. (2008), Amariglio et al. (2012). Baker/baker paradox.
- Werheid & Clare (2007) on differential difficulty of face-name vs face-occupation.
- Biss et al. (2018) on implicit re-exposure benefits.
- Frontiers in Psychology (2018) review of FNAME for early AD diagnosis.
- ScienceDirect (2023) novel face-name mnemonic-discrimination task.

Spaced repetition:
- Anki FAQ on FSRS (faqs.ankiweb.net).
- `open-spaced-repetition/fsrs4anki` GitHub — see `docs/tutorial.md` for the algorithm spec.
- LECTOR (arxiv 2508.03275, 2025) — LLM-augmented semantic SRS. Inspiration for confusion-aware scheduling boost.

Mnemonics:
- Lorayne, *Ageless Memory*. Substitute Word system; distinguishing-feature method.
- Dominic O'Brien, *Quantum Memory Power*.
- Art of Memory wiki — Memorizing Names and Faces.

General learning science:
- Bjork, "Desirable difficulties."
- Roediger & Karpicke, testing effect.
- Dunlosky et al. (2013), "Improving Students' Learning With Effective Learning Techniques."

Host architecture (for plan context):
- `richbodo/fellows_local_db` README — the local-only stance, two-DB split, two-phase load.
- `richbodo/prt` README — the lineage, especially `tools/make_directory.py`'s precedent of generating standalone artifacts from directory data.

---

## 16 · What this doc is *not*

- Not a finished build doc. The §4 architectural decomposition is a *proposal*; iterations 1–3 will revise it based on what the spike teaches us and what the pnt design docs (`ARCHITECTURE.md`, `CONTRACTS.md`, `APPLICATION_PATTERNS.md`, `SOURCE_REUSE.md`) commit to.
- Not a UX spec. UX detail in §13 is checklist-grade, not flow-grade. The cram-mode flow alone deserves a separate document with screen-by-screen spec before iteration 2 ships.
- Not a privacy audit. §12 is the right shape but a serious audit happens before this is enabled in any production app handling real fellow data.
- Not a contract pnt has signed up to. §4 should be reviewed against pnt's actual architecture docs before the spike is built; the spike commits us to a particular shape and changing it later is much harder.
- Not a TUI plan. The application pattern this targets is the static-PWA pattern (fellows_local_db's shape). A TUI variant is plausible later given prt's lineage; out of scope here.

---

## 17 · Closing thought

The most interesting move in this design isn't the FSRS scheduling or even the similar-distractor logic — it's that the briefing card / connection-spark layer reframes the whole thing from "yet another flashcard app" into a **pre-event social cognition tool**. That framing only works because the bundle has structured tag/role data that a generic SRS doesn't have. The pnt architecture should let apps lean into their domain knowledge, not abstract over it. If the bundle contract or the application pattern ends up looking too much like "Anki for X," we've lost the thing that makes pnt's apps special.

The deeper architectural payoff of this plan, if it survives contact with pnt's actual design, is that Memorize ends up being a *clean test case* for the toolkit/app-pattern split. The toolkit-layer tools (`pnt-embed-faces`, `pnt-bundle-similarity`) are reusable across any pnt-built app that wants visual-similarity behavior — a memorial / family-album app might want the same thing for entirely different reasons. The app-layer feature is specific to the static-PWA pattern. The split between them is exactly the thing pnt's qmail-tradition stance is supposed to enable. If iteration 3 feels natural, the architecture's working.
