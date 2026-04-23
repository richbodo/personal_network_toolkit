# Personal Network Toolkit

Personal Network Toolkit is a local-first set of small tools for managing personal connections and relationships privately.

- **Import your contacts** from one or more centralized databases (Google, Apple, Facebook, Linkedin, bespoke directories).
- **Add relationship data** on top of your contact data, without giving that information back up to centralized vendors.
- Use a super fast local viewer to view, filter, discover and **organize them into personal networks**.
- **Export networks** as web apps, pdfs, emails and lists for use elsewhere.
- **Plug into communications** channels and use them in the viewer - email, p2p chat, AT protocol, etc.

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

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Application Patterns](docs/APPLICATION_PATTERNS.md)
- [M0 Data Contracts](docs/CONTRACTS.md)
- [Use Cases](docs/USE_CASES.md)
- [Source Reuse Plan](docs/SOURCE_REUSE.md)

## Status

This repository is at the architecture and planning stage. No implementation is
committed yet.

## History

This was developed from [PRT](https://github.com/richbodo/prt) which was used to develop [Fellows_Local_Db](https://github.com/richbodo/fellows_local_db), and borrows from both codebases.

## License

GPL-3.0. Copyright (C) 2026 Rich Bodo.
