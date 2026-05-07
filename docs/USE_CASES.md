# Use Cases

> **Status: conflicting and uninformed ideas: this document is a mess. It was
> originally created before the project was fully explained and a rewrite in
> progress was made in stream of consciousness style. It needs to be completely
> rewritten but it should be read first.**

This document captures the human workflows the toolkit is meant to support. It
is intentionally broader than the first implementation so design decisions can
keep future uses in view without overbuilding them now.

## 1. Preserve And Distribute A Group Directory

Problem: an org wants to get away from an expensive or unreliable SaaS
directory — the vendor is shutting down, raising prices, locking data in, or
just doing a bad job — and members still need a fast, durable, member-owned
copy.

An organization, fellowship, club, school, or community may already have rich
directory data in an old system. The toolkit should make it easy to massage
that data into a local-first, offline-first directory that is installable on
any device and supports rich data that would be miserable to work with in a
spreadsheet.

This is the `fellows_local_db` pattern:

- Import old directory data and images.
- Build a compact SQLite database.
- Serve a fast installable PWA.
- Let members browse, search, and use the directory offline.
- Preserve richer profile data that does not fit well in a spreadsheet.
- Allow each member to add their own private notes and tags on top of the
  shared directory, visible only to them.

This is useful when a group closes down, changes platforms, or wants a durable
member-owned copy of its directory. You don't need SaaS to own your group's
data.

## 2. Turn A Large Directory Into A Smaller Useful View

Users often need a small subset of a much larger network:

- People from work.
- People in a city.
- Family members for an upcoming visit.
- People connected to a topic, skill, community, or event.
- People tagged privately as relevant to a situation.

The text directory viewer should make narrowing the set fast. Search and
filters are both part of that workflow. A simple filter such as "has email
address" can be extremely useful when a directory contains many people who are
not actually reachable or active.

Over time, search should help with curation: hiding low-value records by
default, combining multiple criteria, using private tags, and eventually using
natural language to help turn a messy intent into a precise filtered set. The
filtered view can then be exported as a smaller directory bundle.

## 3. Make A Face-Friendly Directory

After filtering, users may want a visual artifact rather than a text-first app.
Export modalities include:

- A PDF on a phone before a family visit or party.
- A printable face/name sheet for an event.
- A static website directory for a group.
- A visual graph or grid that helps associate faces, names, and context.
- A JSON export for consumption by another app.

The visual directory maker should consume the exported bundle and generate
these outputs without needing the original database.

## 4. Quickly Notify A Selected Group

Problem: the user needs a fast way to send a notification to a group that may
not have a unified chat group or mailing list.

Sometimes the user finds the right subset of people and wants to contact them
all:

- "I want to talk about pickleball. Here are some possible times."
- "I want to ask work friends about a project idea."
- "I want to check in with people tagged as close friends."
- "I want to reach people who care about mental health."

The key is speed. Most directories are noisy, and the value of this toolkit is
that a curated, targeted set can be created quickly and acted on immediately.
When the user needs the right people quickly, failed search is not just
annoying; it can consume the energy they had for reaching out.

The first version may not need a full notifier. Generated HTML can start with
individual `mailto:` links and possibly a group email link. A later notifier
can send email to selected contacts, with responses coming back to the user.
It does not need to coordinate schedules or manage replies in the first
version.

Later, the same notifier model should support additional channels through
plugins. If every person in a list responds differently on a different
channel, the appropriate default channel can be used for each, as long as the
plugin exists.

## 5. Manage Private Relationship Context

Problem: SaaS contact databases are a mess and the user does not trust the
vendors.

Centralized contact systems are not even good at storing basic contact facts,
because they run on the profit motive, with the goal of collecting data and
creating system lock-in. That incentive produces large amounts of low-quality
data and an unusable system overall.

They are also the wrong place for sensitive relationship context: not everyone
wants large platforms, their administrators, or governments that can compel
those platforms, to know who they might contact about mental health, politics,
immigration, family issues, or other private topics. Those platforms also shut
down apps, get cracked, and lose data from time to time.

Actual relationship data is more important and more sensitive than contact
data. The relationship layer should let the user add:

- Tags such as `close friend`, `pickleball`, `mental health`, `family`,
  `former coworker`, `work friend`, `sensitive about x`, or `Auckland`.
- Notes about context, history, interests, boundaries, and follow-up ideas.
- Searchable private metadata that stays local.

This layer should be writable even when imported contact facts remain
read-only. It should stay local by default and should not need to see the
internet. This data is local-only, for the user only, and free forever.

## 6. Filter And Discover Contacts Quickly

Problem: the user needs a really fast way to find critical subsets of contacts
based on private tags, notes, and contact data.

Many contact databases grow opportunistically. They contain hundreds or
thousands of people accepted through Google Contacts, LinkedIn, social
networks, work directories, or event lists. The practical task is to quickly
discover the people who are relevant to a situation without manually paging
through a noisy address book.

One problem with large directories that try to absorb as much information from
users as possible is that they become impossible to browse and discover with.
In addition to selling personal data, contact managers and CRMs are a mess of
centralized SaaS and do not serve discovery well.

**KEY USE CASE:** when the author of this toolkit wants to find someone to
talk about mental health with, browsing a SaaS directory like LinkedIn or
Google Contacts turns into a depressing boondoggle very quickly, exacerbating
the problem rather than solving it. About 100 contacts into the A's of an
alphabetical list, you wonder who these people are and why you don't know any
of them, and give up. The toolkit should make this kind of targeted discovery
fast, private, and useful — and let the user export the result as a small
visual directory they can pull up instantly.

The toolkit should support deterministic filtering first:

- text search across contact facts, overlays, tags, and non-private notes
- simple filters such as `has_email:true`
- tag filters such as `#work` or `#pickleball`
- combinations that can be saved, shared, or represented as a small search DSL

That deterministic layer is the foundation for augmented natural-language
filtering later. An LLM should be able to help turn a user request like
"people from work who play pickleball and have an email address" into an
inspectable filter expression, then let the deterministic engine run it. The
LLM helps with discovery and curation, but the result set should still be
explainable and repeatable.

This is especially important for sensitive or emotionally difficult topics.
When the user needs the right people quickly, failed search can consume the
energy they had for reaching out.

Later, local-LLM support will be added for natural language search and
assisted discovery. Because this is OSS, people are likely to rewrite the
search layer with their own local AIs anyway, using private context the user
would never want to send to a hosted model.

## 7. Build Toward Peer-To-Peer Community Tools

Problem: the user wants to understand their personal network, or a whole
community wants to understand how its health is holding up. That requires
analyzing data, and that data can reveal important insights — but the
sensitive parts of it should never leak.

The personal toolkit should leave room for future community tools without
making them part of the first product.

A future community relationship system might:

- Let toolkit instances communicate peer-to-peer.
- Use encrypted community message stores.
- Bootstrap through a shared community repository or decentralized protocol.
- Support rules about who can decrypt what.
- Produce community-health signals without exposing sensitive private
  messages.
- Trigger nudges or introductions when someone appears isolated or
  unsupported.

For example, a community may want a system that can notice that someone has
reached out about mental health and gone unanswered, while still protecting
the details of that person's communication. A future rule-based nudger could
make appropriate introductions without revealing more than the community
rules allow.

This is future work. The current architecture should only preserve the
necessary seams: stable identities, relationship metadata, exportable
filtered groups, and pluggable notification channels.

## Near-Term Boundary

The first product is a Personal Network Toolkit, not a full Community
Relationship Tool.

Near-term work should focus on:

- Importing contacts.
- Viewing and searching directories.
- Adding private tags and notes.
- Exporting filtered directory bundles.
- Making visual directories and PDFs.
- Sending simple notifications.

Peer-to-peer and other communication channels, encrypted community sync
(ZKPs), community rules, and automated nudgers belong to a later layer.
