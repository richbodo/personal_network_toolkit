# Research Plan: Contact Data Format Atlas

**A PNA Toolkit documentation contribution tracking vendor contact data formats, quirks, community knowledge, and interop initiatives.**

- **Status:** Draft
- **Parent project:** PNA Toolkit
- **Consumer:** PRM reference implementation (AC-PRM-B use case) and the PRT conformance suite
- **Author:** Rich Bodo
- **License:** Same as the toolkit repo

---

## 1. Problem Statement

Every Personal Network Application must ingest contact data from SaaS silos, yet no canonical, maintained reference exists that documents what those silos actually emit. The vCard RFCs describe an ideal; vendors ship deviations. Knowledge of those deviations is scattered across parser test suites, blog posts, converter-tool changelogs, and GitHub issues — and it rots quickly as vendors change export behavior without notice.

The toolkit's ingestion architecture (multi-source-merge-with-dedup, file import baseline, vdirsyncer for CardDAV, py-vobject parsing) depends on accurate knowledge of these formats. This project creates a living document — the **Contact Data Format Atlas** — that consolidates that knowledge as a citable, versioned doc in the toolkit repo, backed by a synthetic test corpus.

## 2. Goals

1. **Document the export formats** of the major contact-data custodians: what formats they offer, what schema they map to internally, and what is lost in export.
2. **Catalog the quirks** per vendor per format, with reproducible evidence.
3. **Index community documentation** — interop studies, parser wikis, library test suites — so future contributors don't re-discover them.
4. **Track relevant initiatives** (standards bodies, portability consortia) and assess their usefulness to PNAs.
5. **Produce a golden test corpus** of synthetic vendor-realistic export files for the PRT conformance suite.

### Non-Goals

- Documenting CRM/B2B SaaS exports (Salesforce, HubSpot) in v1 — out of scope until a PNA use case demands it.
- Writing converters. The Atlas informs the toolkit's ingestion code; it is not itself code.
- Tracking social-graph data beyond contact-equivalent records (e.g., full Facebook activity exports).

## 3. Scope: Vendors and Formats (v1)

| Vendor | Export surface | Formats | Canonical internal schema |
|---|---|---|---|
| Google | Takeout, Contacts UI export, CardDAV | vCard 3.0, Google CSV, Outlook CSV | People API `Person` resource |
| Apple | iCloud.com export, Contacts.app, CardDAV | vCard 3.0 (Apple-grouped `item1.X-AB*` style) | CNContact (Contacts framework) |
| Microsoft | Outlook classic, New Outlook / Outlook.com, Graph API | vCard 2.1 (classic, quoted-printable), CSV (documented column set), PST | Graph `contact` resource |
| Meta/Facebook | Download Your Information | JSON (`friends_and_followers/friends.json`), HTML | none public (no Graph API friends access) |
| LinkedIn | Data export | `Connections.csv` | none public |
| Android (AOSP/Samsung) | Contacts app share/export | vCard 2.1 (quoted-printable, Samsung variants) | ContactsContract |
| CardDAV servers (Nextcloud, Radicale, FastMail) | CardDAV/vdirsyncer | vCard 3.0/4.0 | RFC-conformant baseline for comparison |

Candidate v2 additions: WhatsApp, Signal, Proton, Thunderbird, SIM/PBAP exports.

## 4. Research Questions

Per vendor/format:

- **RQ1 — Fidelity:** Which fields survive export? What is silently dropped, truncated, or mangled (photos, labels, custom fields, groups, notes, dates without years)?
- **RQ2 — Encoding:** Character encoding, line endings, folding, quoted-printable usage, escaping behavior.
- **RQ3 — Extensions:** Which X-properties and grouped-property conventions does the vendor emit, and what do they mean?
- **RQ4 — Round-trip behavior:** What happens on re-import to the same vendor? To each other vendor?
- **RQ5 — Identity:** What stable identifiers (UID, etag, resourceName) exist, and do they survive export? (Directly feeds the toolkit's dedup design.)
- **RQ6 — Limits:** File size caps, batching behavior, contact-count limits.
- **RQ7 — Drift:** When did the export behavior last observably change, and how would we detect future change?

## 5. Method

### 5.1 Primary evidence: golden corpus generation

1. Define a **synthetic "maximal contact"**: one fictional person exercising every field type — multiple names, phonetics, 3+ phones with mixed labels, emails, postal addresses, IM handles, social URLs, photo, birthday (with and without year), anniversary, org/title, related names, custom labels, groups, notes with newlines and non-ASCII (macrons, CJK, emoji).
2. Enter the maximal contact into each vendor's system; export through every export surface; capture the raw files **byte-exact** (no editor round-trip).
3. Round-trip: import each vendor's export into every other vendor; re-export; diff against original.
4. Supplement with anonymized structural observations from real SaaS data already feeding the test suite (structure only — no real PII enters the repo; corpus files are 100% synthetic).
5. Vendor the corpus into the toolkit repo under `tests/corpus/<vendor>/<surface>/`, each file with a metadata sidecar: capture date, account region, client version, capture procedure.

### 5.2 Secondary evidence: literature and code survey

- Interop studies (e.g., Rossini's vCard interoperability study and its comment thread's "maximally compatible vCard").
- Parser libraries whose tests encode vendor reality: **ez-vcard** (and its vendor-compatibility wiki), **py-vobject**, **cozy-vcard** (explicitly targets vendor behavior over RFC), vdirsyncer's compatibility notes, DAVx5/Nextcloud issue trackers.
- Converter-tool vendors that publish benchmark findings across real exports.
- Each source gets an annotated bibliography entry: what it documents, how current, how trustworthy.

### 5.3 Initiatives survey

- **IETF**: vCard 4.0 (RFC 6350), jCard (RFC 7095), JSContact (RFC 9553) and the calext WG — assess JSContact as a possible toolkit-internal interchange representation.
- **Data Transfer Initiative / Data Transfer Project** (Google/Meta/Apple/Microsoft): per-vendor adapter code is effectively executable schema documentation; assess reusability.
- **CardDAV ecosystem**: vdirsyncer, Radicale, DAVx5 as RFC-baseline implementations.
- DMA/portability regulatory developments insofar as they change export surfaces.
- For each: relevance to PNAs, maturity, and whether the toolkit should reference, adopt, or merely watch.

## 6. Deliverables

| # | Deliverable | Location | Definition of done |
|---|---|---|---|
| D1 | Atlas main doc | `docs/contact-data-format-atlas.md` | One section per vendor answering RQ1–RQ7, with corpus citations |
| D2 | Quirk registry | `docs/atlas/quirks.md` (or YAML for machine-readability) | Each quirk: ID, vendor, format, description, evidence file, workaround, status (active/fixed/unverified) |
| D3 | Golden corpus | `tests/corpus/` | Synthetic exports + sidecars for all v1 vendors |
| D4 | Annotated bibliography | `docs/atlas/sources.md` | All secondary sources with currency assessment |
| D5 | Initiatives brief | `docs/atlas/initiatives.md` | Recommendations: adopt / reference / watch |
| D6 | Maintenance protocol | section in D1 | Re-verification cadence + drift-detection procedure |

D2's machine-readable form is the bridge to PRM: ingestion code can reference quirk IDs in comments and tests, and the conformance suite can assert handling of each registered quirk.

## 7. Phases and Sequencing

**Phase 0 — Scaffold (small):** Repo structure, doc templates, quirk-entry schema, maximal-contact field list. Open a tracking issue in the toolkit.

**Phase 1 — Big Two (Google + Apple):** Highest-value, most-divergent pair; exercises Takeout, iCloud export, and CardDAV via vdirsyncer. Produces first corpus entries and validates the method. PRM ingestion work can consume results immediately.

**Phase 2 — Microsoft + Android:** Adds the vCard 2.1 / quoted-printable / CSV-column world. Likely the richest quirk harvest.

**Phase 3 — Graph silos (Meta, LinkedIn):** JSON/CSV exports without vCard semantics; documents the mapping decisions the toolkit must make to normalize them.

**Phase 4 — Synthesis:** Cross-vendor round-trip matrix, initiatives brief, "maximally compatible export profile" recommendation for the toolkit's own export path (connects to PR-6 human-readable export work), maintenance protocol.

Each phase ends with a PR to the toolkit; the doc is useful after Phase 1, not only at the end. Phases are sized for daily-ship: a single vendor surface capture is a shippable unit.

## 8. Maintenance Model

- Every corpus file and Atlas section carries a **verified-as-of date**; anything older than 12 months is flagged stale.
- Lightweight drift check: re-export the maximal contact from each vendor annually (or when a vendor announces export changes) and byte-diff against the corpus.
- Quirk registry entries are never deleted — quirks get status transitions, preserving history for parsers handling old files.
- Invite community contributions via a `QUIRK_REPORT` issue template requiring an evidence file.

## 9. Risks

- **Vendor ToS / capture friction:** Some exports require account setup overhead (e.g., a clean test account per vendor avoids polluting personal data and keeps corpus synthetic). Mitigation: dedicated test accounts.
- **Drift outpaces maintenance:** Mitigated by sidecar dating and the stale flag — an honest, dated Atlas beats an undated one.
- **Scope creep into CRM-land:** Held off by the non-goals; v2 list exists as a pressure valve.
- **Single-maintainer risk:** Mitigated by making the corpus + quirk schema the contribution interface, so others can add evidence without context.

## 10. Success Criteria

1. PRM's ingestion pipeline cites quirk IDs from D2 in its tests.
2. The PRT conformance suite consumes D3 corpus files directly.
3. At least one external project or contributor references or extends the Atlas within 6 months of publication.
4. A newcomer can answer "what does an iCloud export actually look like and what will break?" from the repo alone, without external searching.
