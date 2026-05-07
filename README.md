# Personal Network Toolkit

Personal Network Toolkit is a local-first set of small tools for managing personal connections and relationships privately.  

- **Import your contacts** from one or more centralized databases (Google, Apple, Facebook, Linkedin, bespoke directories).
- **Add relationship data** on top of your contact data, without giving that information back up to centralized vendors.
- Use a super fast local viewer to view, filter, discover and **organize them into personal networks**.
- **Export networks** as web apps, pdfs, emails and lists for use elsewhere.
- **Plug into communications** channels and use them in the viewer - email, p2p chat, AT protocol, etc.
- **Build** your own personal network tools, or tools for relationship or directory management, or plugins for those apps.

Private, local-only apps need to be the place we keep private data.  To build killer apps for ourselves, those apps need to be able to source data from the legacy centralized internet.  To communicate with the natural tools of a community, we need to be able to plug in those communications tools - only with sufficient privacy can we begin to gather data for personal and community insights to social network health.

## Status

PNT is in the design stages. No code exists yet.

## Goals

- Build tools in the tradition of UNIX software tools, and killer apps on top - follow a compositional, privilege-separated architecture in the qmail tradition. 
- Don't be the contact manager - be the relationship documentor and discoverer - the launching pad for actions that begin with personal relationshiop data -keep imported contact data read-only and rebuildable from source exports from contact managers.
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
- Understand what data is needed to support personal network health and social network health in communities.  Build tools that will support the analysis of that data, while keeping private data private.
- Interface well with other tools that are adjacent - contact managers - directories - communications tools.

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

This was developed from [PRT](https://github.com/richbodo/prt) which was used to develop [Fellows_Local_Db](https://github.com/richbodo/fellows_local_db), and borrows from both codebases.  The social network health guidance is coming from [the social network health project](https://toolkit.socialnetwork.health/wiki/Main_Page)

## License

GPL-3.0. Copyright (C) 2026 Rich Bodo.
