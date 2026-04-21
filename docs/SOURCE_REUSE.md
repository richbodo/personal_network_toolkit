# Source Reuse Plan

This document records what should be lifted from `fellows_local_db` and `prt`,
what should be rewritten, and what should be deferred. The goal is to move fast
without inheriting avoidable complexity.

## Summary Recommendation

Start this repository as a fresh codebase, not as a direct fork or copy of
either prior repo.

Use `fellows_local_db` as the reference implementation for the PWA directory
mode and local/offline distribution model. Port the useful pieces intentionally:
server shape, importer shape, SQLite/FTS5 schema pattern, two-phase frontend
loading, PWA caching, tests, and possibly the magic-link distribution mode.

Use `prt` as a source of domain components and contracts: Google Takeout import,
relationship metadata concepts, directory export JSON shape, and the directory
maker tool. Avoid carrying forward the current all-in-one SQLAlchemy/TUI/LLM
architecture as the base.

## Why Not Start By Copying `fellows_local_db` Wholesale?

`fellows_local_db` is the closest working product. It has a successful PWA, a
small runtime, useful tests, a proven SQLite/FTS5 flow, and a real deployment
mode. That makes it tempting to copy and strip.

The risk is that it is also specific in ways this toolkit should not be:

- EHF/fellows naming and data assumptions are deeply present.
- The production auth/deploy system is useful but not always core.
- The schema is a fellowship-directory schema, not a general personal-network
  schema.
- The frontend includes production PWA/auth/update logic that should be
  preserved carefully, not casually generalized in one pass.

The better path is a fresh repo with staged ports. This keeps the generic toolkit
clean while preserving the ability to copy known-good code when it is time.

## What To Lift From `fellows_local_db`

### Lift Early

- **Tiny server pattern**: Python stdlib HTTP server, simple JSON routes, static
  file serving, SQLite per request.
- **SQLite + FTS5 importer pattern**: fixed display/search columns plus
  `extra_json` overflow, rebuildable database, FTS rebuild after import.
- **Two-phase load**: list/minimal records first, full records in the background.
- **Fast text/image directory UX**: the core browse/search/detail behavior.
- **Image lookup conventions**: image paths by slug/name with fallback matching.
- **Basic API and database tests**: adapt the test shape to contacts.
- **PWA/offline behavior**: service worker, manifest, offline database/static
  cache, update checks, and "install once, works locally" posture.

### Lift Later As Optional Distribution Mode

- **Magic-link PWA distribution**: useful when a group wants to distribute a
  directory privately to members.
- **Email allowlist hashing**: useful for group-directory distribution.
- **Install landing / email gate behavior**: proven UX for private PWA installs.
- **Production deployment docs/scripts**: useful for a hosted directory mode,
  but not the core personal-local flow.

This should become an optional "hosted private directory" mode, not the default
architecture.

### Leave Behind Or Rewrite

- Fellowship-specific fields, stats, copy, routes, and naming.
- Production-only Caddy/Ansible flow in the first local toolkit build.
- Any sensitive data, generated DBs, or project-specific image/data artifacts.

## What To Lift From `prt`

### Lift Early

- **Google Takeout import logic**: especially vCard parsing and profile image
  extraction. Rewrite the output path so it produces a normalized contact bundle
  rather than writing directly into the old app model.
- **Directory maker concept**: a small standalone tool that consumes an export
  bundle and generates static HTML. Keep this spirit.
- **JSON export schema ideas**: timestamped export directory, JSON results,
  image directory, README, image path references.
- **Relationship metadata concepts**: tags and notes as private writable context
  associated with contacts.

### Lift As Design Reference, Not Code

- **API-first rule**: useful principle. Interfaces should not bypass core data
  contracts casually.
- **Search experiments**: FTS, caches, autocomplete, and unified search ideas
  are valuable, but v1 should use a much smaller search implementation.
- **LLM/natural-language search**: keep as a future translator into structured
  filters, not a first dependency.

### Avoid Carrying Forward

- The TUI-first application shape.
- The full SQLAlchemy model/API stack as the foundation.
- The LLM toolchain as part of the first runtime.
- Broad backup/migration/debug layers before the small tools exist.

## Proposed Build Strategy

The build should combine "fresh repo" cleanliness with "known-good reference"
speed.

1. Define the v0 data contracts:
   - normalized contact bundle
   - SQLite directory schema
   - export bundle schema
2. Implement a tiny fixture importer into SQLite, borrowing the shape of
   `fellows_local_db/build/import_json_to_sqlite.py`.
3. Port the `fellows_local_db` local viewer/server pattern to generic contacts.
4. Port the minimal useful PWA behavior after the generic viewer works.
5. Add filtered export from the current viewer result set.
6. Adapt the PRT directory maker into `pnt export html`.
7. Add PDF output.
8. Add private relationship tags/notes.
9. Revisit magic-link distribution as an optional mode.
10. Revisit a real notifier after `mailto:` links have been tested.

## Decision Frame For Future Reuse

When deciding whether to copy, port, or rewrite a prior component, use this
checklist:

- Does it already express a stable behavior we want?
- Is it small enough to understand in one sitting?
- Can it be tested in isolation?
- Does it depend on project-specific assumptions?
- Does it preserve the core contracts, or does it create hidden coupling?
- Would decentralized-web developers be able to replace it with their own script
  without replacing the whole toolkit?

If the answer is "small, tested, contract-shaped, low coupling," port it. If it
is useful but tangled with old app assumptions, rewrite the idea. If it is useful
only for one deployment mode, defer it.

