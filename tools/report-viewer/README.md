# Visual Validator — report viewer

A static, zero-dependency, engine-agnostic vanilla-JS viewer for the toolkit's
**evaluate** flow output. It renders one instance of
[`../evaluate-report.schema.json`](../evaluate-report.schema.json) — see
[`plans/visual-validator-plan.md`](../../plans/visual-validator-plan.md).

- **`index.html`** — the viewer. No build, no framework, no network, no Chromium-only APIs.
  DOM is built with `textContent`, so report strings can't inject HTML.
  - **Phase 2 (this):** single-report renderer, **developer register** — candidate header,
    summary posture + counts, and a card per finding (status, goals, requirement, rationale,
    citations, evidence tagged `deterministic`/`llm`/`human`, `needs_human_review`).
  - **Phase 3 (next):** the end-user register + the toggle / finding-aligned side-by-side view.
- **`sample-reports/`** — the render fixtures + render contract (see its README), guarded by
  [`../report-fixtures-lint.py`](../report-fixtures-lint.py).

## Open it

- **Drag a report onto the page**, or use **open file…** — both work when you open `index.html`
  directly (`file://`), no server needed.
- **`?report=<path>` and the sample buttons** use `fetch()`, which browsers block on `file://`.
  Serve the folder first:

  ```
  python3 -m http.server --directory tools/report-viewer 8009
  # then open http://localhost:8009/index.html
  #   or    http://localhost:8009/index.html?report=sample-reports/03-mixed-exceptions-and-constraints.json
  ```

(A `just view-reports` recipe + the ←/→ directory flip-through land in Phase 5.)
