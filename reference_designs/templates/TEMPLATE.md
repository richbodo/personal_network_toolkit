# <design-name>

> **Toolkit-Version:** 0.2 — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](../../VERSION).

**Maintainer:** <name> (<canonical-repo-url>)
**License:** <OSI-approved license SPDX identifier>
**First accepted:** Toolkit-Version <X.Y>, <YYYY-MM-DD>
**Status:** active | archived | superseded

## Summary

One paragraph describing what this design is and what it demonstrates.

## Axis picks at first acceptance

| Axis | Pick | Axis version |
|---|---|---|
| distribution | <pick> | v<n> |
| storage substrate | <pick> | v<n> |
| ingestion shape | <pick> | v<n> |
| workspace shell | <pick> | v<n> |
| comms transport set | <pick> | v<n> |
| MCP-exposure | <pick> | v<n> |

## Contributions to the spec

### Toolkit-Version <X.Y> — <short title> (PR #<n>)

- Reference design version: commit `<sha>`
- Software Heritage: `swh:1:dir:<id>`
- Optional archive: `archive/<design-name>` at commit `<sha>` (if the toolkit forked for high-signal archival)
- Summary: <2–4 sentences>

### Toolkit-Version <X.Y+n> — <short title> (PR #<m>)

(Add a section per accepted contribution from this design over time.)

## Architectural learnings

Notes that emerged from building or operating this design — constraints first-principles
reasoning would have missed, design-tradeoff stories, things that surprised the
maintainer. These accumulate as the design evolves, and are what makes a reference
design genuinely valuable to future builders.

## Reproducibility notes

Build/run instructions sufficient for someone to make a fighting attempt from the
archived source. List dependencies, build commands, external services required,
and any known dependency-rot risks.

## Architecture document

See [Architecture.md](./Architecture.md), the design's Security Target, copied at first acceptance.
