# Visual Validator — browser-render testing (Playwright)

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../VERSION).
>
> The *how/when* of adding real-browser render tests for the Visual Validator viewer
> ([`visual-validator-plan.md`](visual-validator-plan.md)). Mirrors how `fellows_local_db` runs
> Playwright, shrunk to a static-file viewer, and reconciled with this repo's stdlib-only rule.

## Why & the convention it touches

The viewer (`tools/report-viewer/index.html`) is browser JS. `just ci` is **stdlib-only `python3`** and
cannot render it — so Phase 2 shipped with its live render *unverified* (the gap this plan closes).
Browser rendering genuinely cannot be tested in stdlib; a browser-driver (Playwright) is required.

**The reconciliation** is the same one `fellows_local_db` already lives: *stdlib-only governs the
runtime and the `just ci` gate — not optional dev/test tooling.* fellows' app is stdlib-only too;
Playwright sits in `requirements-dev.txt`, and its e2e suite runs **outside** the pure-Python gate.

> **Scoped exception (decided 2026-06-08).** This is the toolkit's **only** sanctioned third-party /
> `pytest` dependency, **scoped to browser-UI rendering**. It uses **pytest + pytest-playwright**
> (the fellows stack) and runs in its **own dedicated CI job** — but is **never** part of `just ci`,
> which stays bare `python3` with zero deps. To be recorded as an explicit carve-out in `CLAUDE.md`.

(Context: the toolkit is *not* pytest-naive — `.gitignore` already lists `.pytest_cache/`, and
`tools/attestation-evidence-lint.py` already parses reference designs' pytest files. What's new is
the toolkit running pytest on *its own* code, for this one suite.)

## Decisions (locked)
- **Runner:** `pytest` + `pytest-playwright` (the fellows idiom: `page.goto` → `locator` → `expect`).
- **CI:** a **separate** GitHub Actions job (installs Playwright + Chromium, caches browsers); isolated
  from the stdlib-only `lint-spec-ids` / `lint-selftest` jobs, which keep running bare `python3`.
- **Browser:** Chromium only (matches fellows; the viewer is engine-agnostic so one engine suffices
  for render coverage — Firefox/WebKit are an additive later option).
- **Server:** stdlib `http.server.ThreadingHTTPServer` rooted at `tools/report-viewer/` — no app
  server needed (the viewer is static + `fetch`es sibling JSON).
- **Port:** a dedicated **8791** (distinct from fellows `8765` / PRM `8770`, so all three can run on one
  host); same serialize-server-runs-across-worktrees discipline.

## Phases

### Phase 1 — Harness & opt-in deps
- `requirements-dev.txt` (new — the toolkit has had **zero** deps): `pytest>=7`, `playwright>=1.40`,
  `pytest-playwright>=0.4`. **Dev/test only**, never runtime.
- `.gitignore`: add `.venv/` (`.pytest_cache/` and `__pycache__/` are already there).
- `tools/report-viewer/tests/conftest.py`:
  - a session-scoped **`static_server`** fixture — `functools.partial(SimpleHTTPRequestHandler,
    directory=<report-viewer>)` on `ThreadingHTTPServer(("127.0.0.1", 8791))`, daemon thread, poll
    `GET /` until `200`, `yield`, `shutdown()` (the fellows pattern, minus the app server);
  - a **`base_url`** fixture → `http://127.0.0.1:8791` (with a `VIEWER_BASE_URL` env override to point
    at a deployed copy, optional);
  - a free-the-port pre-step (`lsof -ti:8791 | xargs kill`) for clean re-runs.
- **Done-when:** `pytest tools/report-viewer/tests/` boots the server and a trivial `page.goto(base_url)`
  test passes locally after `playwright install chromium`.

### Phase 2 — Render tests (`tools/report-viewer/tests/test_viewer.py`)
Drive the viewer with `?report=sample-reports/NN.json` and assert it **actually renders** — the exact
Phase-2 gap. Parametrize over the three samples and assert per sample:
- candidate name text is present;
- the **posture badge** text matches (`conformant` / `non-conformant` / `mixed`);
- the **finding-card count** equals the sample's finding count;
- a known `ac_id` is visible (e.g. `AC-MCP-A` in sample 03, `AC-1` in 02);
- at least one evidence-source badge (`.ev-src`) renders where the sample has evidence;
- the page **title** updates to the candidate name;
- **no console errors / no `pageerror`** (collect via `page.on("console")` / `page.on("pageerror")`).

Plus two edge cases:
- **empty state:** `goto /index.html` (no `?report`) → the `.empty` drop-prompt is visible;
- **error path:** load a deliberately-malformed report (a small `tests/fixtures/broken.json`, kept
  *under the tests dir* so it doesn't trip `report-fixtures-lint` on `sample-reports/`) → the `.error`
  panel renders.

A `just test-viewer` recipe runs the suite (with the free-port pre-step). **Excluded from `just ci`.**
- **Done-when:** the suite renders all three samples + both edge cases green; a deliberately-broken
  viewer change (e.g. a renamed selector) turns it red.

### Phase 3 — Dedicated CI job
- A job in `.github/workflows/` (extend `spec-lint.yml` or a new `viewer-e2e.yml`): `setup-python`,
  `pip install -r requirements-dev.txt`, `playwright install --with-deps chromium`, **cache**
  `~/.cache/ms-playwright`, then `pytest tools/report-viewer/tests/`. Optional `paths:` filter to the
  viewer so it only runs on viewer-touching PRs.
- It is the **documented non-stdlib job**, sitting beside (never inside) the bare-`python3` lint jobs.
- **Done-when:** the job runs green on a PR and red when a render assertion is broken; the existing
  `lint-spec-ids` / `lint-selftest` jobs are untouched and still dependency-free.

### Phase 4 — Docs & the convention carve-out
- **`CLAUDE.md`** — a short, explicit exception under *Conventions*: stdlib-only governs runtime + the
  `just ci` gate; the viewer's opt-in `pytest`+Playwright suite (`just test-viewer`,
  `requirements-dev.txt`) is the **sole** sanctioned dep/pytest exception, scoped to browser-UI
  rendering, running in its own CI job and **never** in `just ci`.
- **`CLAUDE.md` Worktrees** — update: the viewer test binds **port 8791**, the one shared resource;
  serialize `just test-viewer` (and the Phase-5 `just view-reports`) across worktrees. Everything else
  in this repo stays parallel-safe.
- **`docs/users-guide.md`** — add `just setup-test` (one-time: venv + `playwright install chromium`)
  and `just test-viewer` to the *Working in this repo* command table, flagged **opt-in / not in
  `just ci`**.
- **`CHANGELOG.md`** — record the suite + the convention exception.

## Open / deferred
- **Multi-engine** (Firefox/WebKit) — additive `pytest-playwright --browser` matrix; defer until the
  viewer is feature-complete (Phase 3/5 of the VV plan).
- **Responsive/mobile matrix** — fellows has one; the viewer doesn't need it yet.
- **Drag-drop / file-picker paths** — harder to drive headlessly; `?report=` exercises the same
  `loadText` → `renderReport` path, so cover those two input modes only if a regression motivates it.
- **Reuse for other toolkit UI** — if the toolkit grows more browser surfaces, this harness
  (server fixture + base_url + the CI job) is the template; keep it generic.

## Fit with the roadmap
This is a **Wave-3 / Tier-2** hardening step on the Visual Validator ([`docs/roadmap.md`](../docs/roadmap.md)),
independent of the Wave-1/Wave-2 keystone. It closes the "viewer render unverified" gap from VV Phase 2
and gives Phases 3 (registers / side-by-side) and 5 (directory flip-through) a regression net to build on.
