# Contact Data Format Atlas

> **Toolkit-Version:** 0.2 — versioned as a unit with the toolkit; see [VERSION](../VERSION).
>
> A survey of the contact-export / contact-sync formats a Personal Network Application
> ingests, **ranked by commonality (account base that produces the format)** and answering,
> per vendor, the research questions from
> [`plans/contact-data-formats-research-plan.md`](../plans/contact-data-formats-research-plan.md)
> (deliverable **D1**). Compiled from **public sources** (vendor docs, RFCs, parser-library
> test suites/wikis, interop studies). **No golden corpus was generated** — that needs real
> vendor accounts + byte-exact exports, flagged in § Gaps as a manual step (D3). This document
> is AI-research-assisted and dated; re-verify per the plan's maintenance model.

## The one architectural takeaway

**Stable IDs live in the vendors' *APIs*, not in the flat-file *exports* a PRM actually
ingests.** Takeout/CSV/.vcf/DYI-JSON mostly strip the vendor's real identifier. So cross-source
dedup **must be content-fingerprint-based by default** (normalized name + any email + any E.164
phone), treating an embedded `UID`/`resourceName`/`etag` as an *opportunistic fast-path* — and
treating **Apple `UID`s as non-authoritative** (Apple's CardDAV overwrites them; `CNContact`
identifiers are device-local).

## 1. Commonality-ranked vendor table

Ranked by order-of-magnitude reach of the account base that produces the format.

| Rank | Vendor / format | Formats produced | Est. reach (source) | Primary stable ID | Tier |
|---|---|---|---|---|---|
| 1 | **Google** (Contacts / Takeout / People API) | vCard 3.0, Google CSV, Outlook CSV; JSON (People API) | Gmail ≈ 1.8 B; Workspace ≈ 3 B MAU | API `resourceName` + `etag`; **no UID/id in vCard/CSV** | Billions |
| 2 | **Apple** (iCloud / Contacts.app / CardDAV) | vCard 3.0 (`itemN.X-AB*` grouping); CardDAV | 2 B+ active devices; iCloud ~768 M | vCard `UID` / `getetag`; `CNContact.identifier` (device-local) — **all weak** | Billions |
| 3 | **Microsoft** (Outlook / Exchange / Graph) | vCard **2.1 (quoted-printable)** default, CSV, Graph JSON | Hundreds of M (consumer figure murky) | Graph `id` (**mutable** unless `Prefer: IdType="ImmutableId"`), `changeKey` | Hundreds of M |
| 4 | **Facebook / Meta** (Download Your Information) | `friends.json` / HTML | FB ≈ 3.07 B MAU — but contact export is name+timestamp only | **None** | Billions of accounts / ~zero fidelity |
| 5 | **LinkedIn** (Connections export) | `Connections.csv` | 1.3 B registered, ~310 M MAU | **None** in export; email blank ~80–90% | Billions of accounts / thin fidelity |
| 6 | **Android / Samsung** (on-device Contacts) | vCard **2.1 + per-prop `CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE`** (Samsung); vCard 3.0 (Pixel/AOSP) | Android 3 B+ devices | vCard `UID` if present (often absent on 2.1) | Billions (subset of Google) |
| 7 | **CardDAV servers** (Nextcloud, Radicale, Baïkal, Fastmail, SabreDAV) | RFC vCard 3.0 / 4.0 | Self-host + niche (millions) | vCard `UID` + DAV `getetag` (**cleanest of the set**) | Millions |
| — | **Loose vCard / CSV files** (cross-cutting) | vCard 2.1/3.0/4.0, ad-hoc CSV | The lowest-common-denominator a PRM actually receives | Whatever was embedded (often nothing) | Cross-cutting |
| — | **JSContact (RFC 9553) / jCard (RFC 7095)** | JSON | Emerging; ~zero production exports today | JSContact `uid` | Future-facing |

**The PRM-critical set** (extra care below): Google, Apple, LinkedIn, Facebook, loose vCard/CSV.

### What kinds of data the list holds, and how common each is

| Data kind | Commonality | Note for the ingester |
|---|---|---|
| Name (display + structured N) | Universal | Often the *only* thing Facebook/LinkedIn give |
| Email | Common but **adversarially sparse** on social exports | LinkedIn blank ~80–90%; Facebook opt-in/absent |
| Phone | Common (Google/Apple/MS/Android) | Carries labels that survive unevenly |
| **Labels** on multi-value fields | Common but **fragile — #1 fidelity loss** | Apple `itemN.X-ABLabel`; Google CSV "Type" cols |
| Photo (base64) | Google/Apple/MS vCard; absent in CSV & social | Dropped on CSV conversion; size-capped |
| Org / title | Common (incl. LinkedIn Company/Position) | LinkedIn's one rich field |
| Postal address | vCard common; CSV-lossy | Apple tags locale via `X-ABADR` |
| Dates (birthday/anniversary) | Moderate; **year often omitted** | `BDAY:--MMDD`; many sinks can't store yearless |
| Groups / memberships | Moderate; **export-fragile** | Google CSV keeps; Google **vCard drops** |
| Social/IM handles | Apple-rich (`X-SOCIALPROFILE`…), else ad-hoc | All non-standard X-props |
| Related names | Apple-only (`X-ABRELATEDNAMES`) | Pure Apple extension |
| Notes | Most; **Apple historically drops in vCard** | Google exempts Notes from 1024-char truncation |
| **Stable identity** | Rare-to-weak in exports | The central dedup problem (§3) |
| Relationship/edge metadata | Facebook only (friend-since timestamp) | Connection log, not a contact record |

## 2. Per-vendor notes (RQ1 fidelity · RQ2 encoding · RQ3 extensions · RQ4 round-trip · RQ5 identity · RQ6 limits · RQ7 drift)

### 2.1 Google (rank 1)
- **Fidelity/round-trip:** three exports (Google CSV, Outlook CSV, vCard 3.0). **Photos** embed only in Google CSV or vCard, **silently dropped** on vCard→CSV. **Groups** are **dropped from the vCard export** but **preserved in Google CSV** as a `Group Membership` column using the `* myContacts ::: * label` convention. **Per-field truncation at 1,024 chars except Notes.**
- **Encoding:** vCard 3.0 UTF-8; known quirk of **over-escaping colons in URLs** (`item1.URL:https\://…`).
- **Extensions:** Apple-style `itemN.URL` + `itemN.X-ABLabel`; `X-SOCIALPROFILE`/`X-SKYPE`.
- **Identity:** **export files carry no Google ID.** Stable identity is API-only: `resourceName` (`people/c…`) + per-source `etag`; `resourceName` **can change** on profile-link changes.
- **Drift:** still vCard 3.0 as of 2026; groups-dropped-from-vCard is long-standing.

### 2.2 Apple (rank 2)
- **Fidelity:** vCard 3.0 (`PRODID:-//Apple Inc.//iOS…`). Distinguishing trait: **`itemN.` grouped properties** (a value line + its `itemN.X-ABLabel`). **Notes historically not exported** in Apple's vCard (verify on current OS). Group membership often lost on import.
- **Extensions (load-bearing):** `X-ABLabel, X-ABADR, X-ABDATE, X-ABRELATEDNAMES, X-PHONETIC-*, X-SOCIALPROFILE, X-SERVICE-TYPE, X-MSN, X-AIM, …`. The **`X-ABLabel` special-value vocabulary** `_$!<HomePage>!$_`, `_$!<Anniversary>!$_`, `_$!<Mother>!$_`, … is a fixed enumeration Apple localizes at display time; **custom labels bypass the `_$!<>!$_` wrapper** as bare text. An ingester must (a) reassemble `itemN` groups and (b) translate `_$!<X>!$_` → "X" or users see garbage.
- **Identity:** vCard `UID` + CardDAV `getetag`, **but Apple's CardDAV overwrites `UID` with the resource URL on upload** (spec-violating; breaks downstream references). `CNContact.identifier` is **device-local**, changes on re-import. **Treat Apple UIDs as advisory, not authoritative.**
- **Limits:** **iCloud rejects photos > 224 KB; whole-vCard cap ~256 KB**; oversized photos **silently trimmed**.
- **Drift:** `PRODID` stamps the iOS version — the most reliable drift marker in the atlas; capture it.

### 2.3 LinkedIn (rank 5; thin fidelity)
- **Fidelity:** `Connections.csv` columns: First/Last Name, Email (only if shared), Company, Position, Connected On. No phone/photo/address. **Email blank ~80–90%** (requires the *other* party's opt-in).
- **Encoding/structure:** UTF-8 CSV with a **3–4-line "Notes" preamble before the real header** — must be skipped or every column misaligns.
- **Identity:** **no stable ID** (not even profile URL in the standard export). Dedup on (name + company) or sparse email — one of the hardest sources.
- **Drift:** preamble persists into 2026; column set has drifted (`Position`/`Connected On` added) → **parse by header name, not position.**

### 2.4 Facebook / Meta (rank 4; near-zero contact fidelity)
- **Fidelity:** friends export is **name + Unix timestamp only** — no email/phone/ID. HTML or JSON ZIP (`{"friends":[{"name":…,"timestamp":…}]}`).
- **Encoding:** JSON is UTF-8 but Facebook **double-encodes (mojibake)** — non-ASCII arrives as literal `Ã©` sequences needing re-decode.
- **Identity:** **none.** Treat as **edge/timeline metadata (a relationship timeline), not contact records.**
- **Drift:** Meta has progressively *removed* contact data from DYI post-Cambridge-Analytica.

### 2.5 Loose vCard / CSV (cross-cutting — what the PRM actually receives)
- Version fragmentation is real; **branch on version**:
  - **2.1:** nameless params, multi-WSP folding, **quoted-printable values**, newlines via QP soft breaks.
  - **3.0/4.0:** `TYPE=` params, exactly-one-WSP folding, `\n` allowed, **QP forbidden**.
  - **4.0:** mandatory UTF-8, `MEDIATYPE=`, adds `KIND`/`GENDER`/`ANNIVERSARY`.
- **The CSV trap: there is no standard contact-CSV schema** (Google CSV vs Outlook CSV vs ad-hoc differ; multi-value fields spread across numbered columns). **Header-driven mapping is mandatory.**

### 2.6 Microsoft (rank 3)
- **Fidelity/encoding:** default desktop-Outlook export is **vCard 2.1 + quoted-printable** (`N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:M=C3=BCller`) — the headline interop hazard; one .vcf per contact (classic Outlook). Graph `contact` JSON is rich.
- **Identity:** Graph `id` is **mutable by default** (changes on move/archive/export-reimport); an **immutable id exists only via the `Prefer: IdType="ImmutableId"` header**. vCard/CSV carry no Graph id.
- **Drift:** immutable-id opt-in since ~2019, still opt-in; default vCard 2.1 export decades-stable.

### 2.7 Android / Samsung (rank 6)
- **Encoding (defining quirk):** Samsung writes per-property `;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE` and QP-encodes the value; modern platforms frequently **fail to decode it**, garbling non-Latin names. Samsung 2.1 also drops group/category labels.
- **Identity:** `UID` if present on 3.0 (Pixel/AOSP); **often absent on Samsung 2.1**.

### 2.8 CardDAV servers (rank 7; cleanest identity)
- RFC vCard 3.0/4.0 baseline; mostly faithful passthroughs that **inherit the client's quirks** (Apple `itemN` grouping leaks through).
- **Identity (strong point):** RFC 6352 **requires** a collection-unique `UID` and a strong `getetag` per resource — the one tier where UID+etag are dependable (except where an Apple client overwrote the UID).

### 2.9 JSContact / jCard / RFC family (future-facing)
- **RFC 6350** (vCard 4.0), **7095** (jCard), **9553** (JSContact — *not* a 1:1 vCard map), **9554** (vCard extensions for JSContact), **9555** (JSContact↔vCard conversion + `JCardProp` escape hatch for un-mappable props). First-class `uid`. **~nil production exports today** — but the JSON-native, explicit-uid, lossless-extension shape a forward-looking PRM's internal schema should resemble. Watch adoption as the drift signal.

## 3. Cross-vendor stable-identity & dedup synthesis

Identity reliability ladder (best → useless):

1. **CardDAV `UID` + `getetag`** — spec-mandated; dependable unless an Apple client overwrote the UID.
2. **Google People API `resourceName` + `etag`** — stable but can shift on profile-link changes; **absent from Takeout/CSV**.
3. **Graph immutable `id` + `changeKey`** — stable only if the immutable-id header was used; **absent from .vcf/CSV**.
4. **vCard `UID` in a 3.0/4.0 file** — Apple's may be a non-portable URL; `CNContact` ids are device-local.
5. **Samsung/Outlook vCard 2.1** — frequently **no UID**.
6. **LinkedIn CSV / Facebook JSON** — **no ID, ever**; email rare/never.

**Consequences for the PRM:** build a **content fingerprint** (normalized name + any email + any E.164 phone) as the universal merge key; **never trust an Apple UID** as a cross-source primary key; **persist provenance + the source's native id/etag when present** so future *re-mirrors from the same source* stay incremental even though *cross-source* merge is content-based; expect **one human = many partial records** (a Facebook timestamp-only friend + a LinkedIn name+company row + a Google full contact) that must fuse — exactly the meta-view dedup the PNA spec's PRM vision describes (`AC-PRM-B`).

## 4. The load-bearing quirks an ingester MUST handle (ranked)

1. **Quoted-printable in vCard 2.1 (Outlook + Samsung)** — decode `=XX`; handle the `=`-at-EOL soft break (classic "lost first char of continuation line"); never emit QP into 3.0/4.0.
2. **Apple `itemN.` group reassembly + `_$!<…>!$_` label translation** — or labels render as `_$!<HomePage>!$_`.
3. **Photo size ceilings + silent drop** (iCloud 224 KB photo / 256 KB card; base64 +33%).
4. **Dates without years** (`BDAY:--MMDD`, `--MM-DD`) — schema must store a yearless date.
5. **CSV has no standard schema — map by header, not position** (Google numbered multi-value columns + `* group` membership; LinkedIn 3–4-line preamble).
6. **Charset** — 2.1 per-property `CHARSET=`; 3.0 assumed UTF-8; 4.0 mandatory UTF-8.
7. **Facebook double-encoded (mojibake) JSON** — re-decode `Ã©`; convert Unix-epoch timestamps.
8. **Line folding differs by version** (multi-WSP 2.1 vs one-WSP 3.0/4.0) — unfold before parsing.
9. **Over-/under-escaping** (Google's redundant `\:`; vendor-specific `,;\`) — be liberal in what you accept.
10. **Groups survive in some exports, vanish in others** — don't assume membership is preserved.

## 5. Gaps — flag for manual golden-corpus capture (D3, Rich's step)

These need a real account + a captured byte-exact export to resolve:

- Exact, current **header column lists** for Google CSV and Outlook CSV (templates drift).
- **Whether Apple still omits Notes in vCard export** on current macOS/iOS (well-attested historically; the public test file is iOS 8).
- **Microsoft consumer-Outlook user counts** (no clean public 2025 figure — tier-3 placement is inference).
- **Google Takeout vs in-app Contacts export** edge cases ("Other contacts" / auto-collected addresses).
- **LinkedIn export field drift** + whether a profile-URL column ever appears.
- **Facebook `friends.json` exact current schema/filename** under the latest DYI UI.
- **Real photo-survival matrix** (which source→sink pairs keep/strip/transcode photos) — needs binary diffs.
- **JSContact production adoption** — currently ~nil; the drift signal for the JSON-native era.

## Key sources

vCard/CardDAV/JSContact RFCs: [6350](https://www.rfc-editor.org/rfc/rfc6350.html) · [6352](https://www.rfc-editor.org/rfc/rfc6352) · [9553](https://datatracker.ietf.org/doc/html/rfc9553) · [9555](https://www.rfc-editor.org/rfc/rfc9555.html). Real Apple corpus + interop survey: [cozy-vcard iOS test](https://github.com/cozy/cozy-vcard/blob/master/test/ios-full.vcf) · ["the sad story of vCard"](https://alessandrorossini.org/the-sad-story-of-the-vcard-format-and-its-lack-of-interoperability/). Parser-maintainer knowledge: [ez-vcard version differences](https://github.com/mangstadt/ez-vcard/wiki/Version-differences) · [Fossify `itemN.X-ABLabel` #187](https://github.com/FossifyOrg/Contacts/issues/187). Identity: [Google People API](https://developers.google.com/people/v1/contacts) · [Graph immutable-id](https://learn.microsoft.com/en-us/graph/outlook-immutable-id) · [Apple CardDAV UID overwrite](https://gist.github.com/evert/b1cef035890701973fd9). Limits/quirks: [iCloud photo/vCard caps](https://discussions.apple.com/thread/253220487) · [Samsung 2.1+QP](https://univik.com/blog/export-contacts-from-samsung-to-vcf/) · [Google truncation](https://univik.com/blog/missing-fields-after-vcf-import/) · [LinkedIn CSV preamble + blank email](https://www.networkcleaner.com/blog/export-linkedin-connections-csv/) · [Facebook DYI](https://blog.coupler.io/how-to-export-facebook-data/). Prevalence: [Google Workspace](https://electroiq.com/stats/google-workspace-statistics/) · [Apple](https://www.businessofapps.com/data/apple-statistics/) · [LinkedIn](https://www.demandsage.com/linkedin-statistics/) · [Facebook](https://www.demandsage.com/facebook-statistics/).
