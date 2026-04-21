# Personal Network Toolkit

Personal Network Toolkit is a local-first set of small tools for importing,
viewing, searching, exporting, visualizing, and selectively contacting people in
a personal or group directory.

The project starts from two working lessons:

- `fellows_local_db` proved that a small offline-capable PWA can make a rich
  directory fast, useful, and easy to distribute.
- `prt` explored richer contact import, relationship metadata, JSON export, and
  visual directory generation, but should be rebuilt as smaller composable tools
  instead of one large TUI-first application.

## Goals

- Keep imported contact data read-only and rebuildable from source exports.
- Store private relationship data, such as tags and notes, in a separate
  writable layer.
- Make search fast enough for large personal networks and simple enough to work
  without an LLM.
- Export filtered directory views as portable JSON bundles with referenced
  images.
- Generate visual directories, static websites, and PDFs from those bundles.
- Notify selected groups of contacts through pluggable channels, starting with
  email.
- Leave clean seams for future community and peer-to-peer tools without making
  those systems part of the first build.

## First Components

The first implementation track is the directory flow:

```text
importers -> directory database -> text directory viewer/search
          -> filtered directory export -> visual directory/PDF/notifier
```

The first viewer should follow the `fellows_local_db` model: a small Python
server, SQLite with FTS5, vanilla JavaScript, local-first PWA behavior, and no
heavy frontend build system.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Use Cases](docs/USE_CASES.md)
- [Source Reuse Plan](docs/SOURCE_REUSE.md)

## Status

This repository is at the architecture and planning stage. No implementation is
committed yet.
