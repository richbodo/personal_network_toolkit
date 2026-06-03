# Private DB export

A human-readable snapshot of your Private DB, openable in any spreadsheet, text
editor, or JSON viewer — no PNA tooling required.

- `groups.csv`, `record_notes.csv` — one CSV per table.
- `private-export.json` — the same data as JSON, with the schema embedded.

This export is one-way: it is a portability and longevity escape hatch, not a
re-import surface. To restore, use the canonical SQLite backup.
