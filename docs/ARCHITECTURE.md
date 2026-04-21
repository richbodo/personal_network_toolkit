# Architecture

Personal Network Toolkit is a modular local-first application suite. The modules
share stable data contracts instead of one large runtime. Each tool should be
usable from a CLI, callable as a small Python library, and able to exchange data
through documented SQLite and JSON formats.

## Design Principles

- **Local first**: the user's directory, notes, tags, exports, and generated
  directories live on their machine by default.
- **Imported facts are read-only**: contacts imported from Google Contacts,
  Google Takeout, old directories, spreadsheets, or other systems are not edited
  in place. The source system remains canonical.
- **Private relationship data is first class**: tags and notes are stored in a
  separate writable layer anchored to stable contact IDs.
- **Small tools over one big app**: import, view, search, export, visualize, and
  notify should remain separable.
- **Offline capable by default**: the primary viewer should work as a PWA and
  continue to be useful without network access.
- **Plain contracts**: SQLite, JSON, static files, and documented CLI commands
  are preferred over hidden framework coupling.
- **LLM optional**: natural-language search and assistants are valuable future
  layers, but basic search, filtering, export, and directory generation must work
  without them.

## v1 Proof-Of-Principle Component Map

```text
source exports
  |
  v
pnt-import adapters
  |
  v
normalized contact bundle
  |
  v
pnt-db SQLite directory database
  |
  +--> pnt-viewer text/image PWA directory
  |       |
  |       v
  |     pnt-search filters and FTS queries
  |       |
  |       v
  |     filtered result set
  |       |
  |       +--> pnt-export portable directory bundle
  |       |       |
  |       |       +--> static HTML visual directory
  |       |       |
  |       |       +--> PDF directory
  |       |
  |       +--> mailto links for quick individual/group email
```

In v1, export is usually triggered from the filtered result set currently shown
in the text/image PWA directory viewer. The user searches and filters the
directory, sees the useful subset, then exports that exact subset.

The first proof of principle does not need a full notifier service. Generated
HTML can include `mailto:` links for individual contacts and, if practical,
group email links. That may be enough to prove the workflow before building a
real multi-channel notifier.

## Extended Component Map

```text
filtered result set from any viewer
  |
  +--> pnt-export
  |       |
  |       +--> JSON bundle
  |       +--> static HTML directory
  |       +--> PDF directory
  |       +--> future layout/export application
  |
  +--> pnt-notifier
          |
          +--> email
          +--> Slack / WhatsApp / Matrix / other channel plugins
          +--> future community or peer-to-peer transports
```

In the extended architecture, any contact set can become an action target: a
single contact, a filtered text-directory view, a generated visual directory, or
another exported bundle. A viewer may call export, notify, or both.

## Modules

### pnt-import

Adapters convert source-specific data into a normalized contact bundle. Initial
adapter candidates:

- Google Takeout contacts, including profile images.
- Google Contacts API export.
- CSV or spreadsheet import.
- Existing group-directory JSON exports.
- Custom fellowship/community directory exports.

Adapters should not write relationship tags or notes. They produce imported
contact facts plus source aliases.

### pnt-db

Owns SQLite schema, rebuild/import behavior, FTS indexes, stable contact IDs,
and relationship metadata tables.

The database should distinguish:

- **Contact facts**: imported, read-only, rebuildable.
- **Contact aliases**: source and external ID mappings used to preserve stable
  identity across imports.
- **Relationship metadata**: private tags and notes written by this toolkit.

The first schema should stay close to the compact `fellows_local_db` model:
fixed display/search columns plus `extra_json` overflow for source-specific
fields.

### pnt-viewer

The high-speed text/image directory viewer. It should inherit the successful
shape of `fellows_local_db`:

- Python standard-library HTTP server or similarly small runtime.
- SQLite per-request access.
- Vanilla JavaScript SPA.
- Two-phase load: minimal directory list first, full records in the background.
- Local PWA install and offline cache support.
- Image display when contact images exist.

The viewer reads contact facts and relationship metadata, but it should remain
small. Relationship editing can be a separate panel or companion tool.

### pnt-search

Search starts with SQLite FTS5, field filters, and relationship metadata filters.

Initial search should support:

- Name, email, phone, location, organization, notes/public bio fields.
- Tags and private notes from the relationship layer.
- Structured filters that can be represented as JSON.
- Simple toggles for common high-value filters, such as "has email address."

Natural-language search can be added later as a translator from user language to
structured filters. It should not replace the deterministic search API.

### pnt-export

Exports a filtered result set as a portable directory bundle. In the normal v1
flow, this happens from the current filtered view in the PWA directory viewer.

Candidate bundle layout:

```text
directory.json
manifest.json
images/
README.md
```

The JSON should contain enough contact and relationship data for downstream
tools while keeping image files separate and referenced by relative path.

For v1, this module may also generate static HTML and PDF directly. A separate
visual-directory application is not required until layout selection, website
publishing, or more interactive generation workflows justify it.

### Static HTML And PDF Outputs

Generates visual outputs from exported directory bundles:

- Static interactive HTML directory.
- Phone/laptop friendly PDF.
- Later, multiple layouts such as face grid, graph, family tree, event roster,
  or organization chart.

These outputs should be viewable in ordinary browsers or PDF readers. The HTML
can include contact-detail panels, individual `mailto:` links, and possibly a
group `mailto:` link when browser and operating-system limits make that useful.

### pnt-notifier

The notifier is an extended component, not required for the first proof of
principle. It consumes a filtered result set or exported directory bundle and
sends a message to that group.

The first real notifier should support email:

```text
recipients + topic + proposed times + message template -> delivery report
```

The notifier should be designed around channel plugins. Future channels might
include Slack, WhatsApp, Matrix, ActivityPub, Nostr, or custom peer-to-peer
protocols.

### Future Community Layer

The toolkit should leave room for a future Community Relationship Tool style
system, but not implement it initially.

Future community tools may include:

- Peer-to-peer app-to-app communication.
- Encrypted community message stores.
- Rule-based access to sensitive relationship or community-health signals.
- Nudger processes that can detect unmet needs without exposing private
  communication to everyone.
- Community statistics and introductions governed by community-defined rules.

The current toolkit should only preserve clean data and notifier seams so those
systems can be built later.

## Data Contracts

Three contracts should be treated as central:

1. **Normalized contact bundle**: importer output.
2. **Directory SQLite schema**: viewer/search/runtime storage.
3. **Directory export bundle**: visual directory and notifier input.

Keeping these stable lets each component evolve independently.

## Suggested CLI Shape

```bash
pnt import google-takeout takeout.zip --db contacts.db
pnt serve --db contacts.db
pnt search --db contacts.db --query "work pickleball" --export exports/work-pickleball
pnt export html exports/work-pickleball --output directories/work-pickleball
pnt export pdf exports/work-pickleball --output directories/work-pickleball.pdf
pnt notify email exports/work-pickleball --topic "Pickleball meetup"  # later
```

Exact command names can change, but this captures the desired composition.

## Initial Build Order

1. Define v0 normalized contact JSON.
2. Define v0 SQLite schema.
3. Create a tiny importer for fixture JSON into SQLite.
4. Port the fast directory viewer from the `fellows_local_db` pattern.
5. Add basic FTS search and filtered export.
6. Generate static HTML and PDF directories from the export bundle.
7. Add relationship tags/notes.
8. Add mail links in generated HTML where useful.
9. Add a real email notifier later if mail links are not enough.
