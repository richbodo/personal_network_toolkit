# export-readable-lint fixtures

Synthetic exports for the PR-6 checker's CI self-test (mirrors the
`egress-lint-fixtures/` pattern). Not a real PNA — just enough to exercise the
two outcomes:

- **`clean/`** — a tool-free human-readable export: CSV per table, a
  schema-embedded JSON, and a Markdown vault. `export-readable-lint.py clean/`
  exits 0.
- **`dirty/`** — an export that is *not* readable without PNA tooling: the
  canonical `private.sqlite` binary (the exact form PR-6 complements), a JSON
  that doesn't parse, and an empty file. `export-readable-lint.py dirty/` exits 1.
