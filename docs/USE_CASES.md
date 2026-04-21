# Use Cases

This document captures the human workflows the toolkit is meant to support. It
is intentionally broader than the first implementation so design decisions can
keep future uses in view without overbuilding them now.

## 1. Preserve And Distribute A Group Directory

An organization, fellowship, club, school, or community may already have rich
directory data in an old system. The toolkit should make it easy to massage that
data into a local-first offline-capable directory.

This is the `fellows_local_db` pattern:

- Import old directory data and images.
- Build a compact SQLite database.
- Serve a fast installable PWA.
- Let members browse, search, and use the directory offline.
- Preserve richer profile data that does not fit well in a spreadsheet.

This is useful when a group closes down, changes platforms, or wants a durable
member-owned copy of its directory.

## 2. Turn A Large Directory Into A Smaller Useful View

Users often need a small subset of a much larger network:

- People from work.
- People in a city.
- Family members for an upcoming visit.
- People connected to a topic, skill, community, or event.
- People tagged privately as relevant to a situation.

The text directory viewer should make narrowing the set fast. Search and filters
are both part of that workflow. A simple filter such as "has email address" can
be extremely useful when a directory contains many people who are not actually
reachable or active.

Over time, search should help with curation: hiding low-value records by
default, combining multiple criteria, using private tags, and eventually using
natural language to help turn a messy intent into a precise filtered set. The
filtered view can then be exported as a smaller directory bundle.

## 3. Make A Face-Friendly Directory

After filtering, users may want a visual artifact rather than a text-first app:

- A PDF on a phone before a family visit.
- A printable face/name sheet for an event.
- A static website directory for a group.
- A visual graph or grid that helps associate faces, names, and context.

The visual directory maker should consume the exported bundle and generate these
outputs without needing the original database.

## 4. Quickly Notify A Selected Group

Sometimes the user finds the right subset of people and wants to contact them:

- "I want to talk about pickleball. Here are some possible times."
- "I want to ask work friends about a project idea."
- "I want to check in with people tagged as close friends."
- "I want to reach people who care about mental health."

The key is speed. Most directories are noisy, and the value of this toolkit is
that a curated, targeted set can be created quickly and acted on immediately.

The first version may not need a full notifier. Generated HTML can start with
individual `mailto:` links and possibly a group email link. A later notifier can
send email to selected contacts, with responses coming back to the user. It does
not need to coordinate schedules or manage replies in the first version.

Later, the same notifier model should support additional channels through
plugins.

## 5. Manage Private Relationship Context

Centralized contact systems are good at storing basic contact facts, but not
always good at storing the private context that helps a person decide who to
reach out to. They are also the wrong place for sensitive relationship context:
not everyone wants large platforms, their administrators, or governments that can
compel those platforms to know who they might contact about mental health,
politics, immigration, family issues, or other private topics.

The relationship layer should let the user add:

- Tags such as `close friend`, `pickleball`, `mental health`, `family`,
  `former coworker`, or `Auckland`.
- Notes about context, history, interests, boundaries, and follow-up ideas.
- Searchable private metadata that stays local.

This layer should be writable even when imported contact facts remain read-only.
It should stay local by default and should not need to see the internet.

## 6. Avoid Social Network Overload

Many contact databases grow opportunistically. They contain hundreds or thousands
of people accepted through Google Contacts, LinkedIn, social networks, work
directories, or event lists. When the user is tired or distressed, searching
through those lists can consume all the energy they had for reaching out.

The toolkit should help the user get from "I need to talk to someone about this"
to a small, meaningful set of people quickly.

This is especially important for sensitive or emotionally difficult topics where
the cost of failed search is high.

## 7. Build Toward Peer-To-Peer Community Tools

The personal toolkit should leave room for future community tools without making
them part of the first product.

A future community relationship system might:

- Let toolkit instances communicate peer-to-peer.
- Use encrypted community message stores.
- Bootstrap through a shared community repository or decentralized protocol.
- Support rules about who can decrypt what.
- Produce community-health signals without exposing sensitive private messages.
- Trigger nudges or introductions when someone appears isolated or unsupported.

For example, a community may want a system that can notice that someone has
reached out about mental health and gone unanswered, while still protecting the
details of that person's communication. A future rule-based nudger could make
appropriate introductions without revealing more than the community rules allow.

This is future work. The current architecture should only preserve the necessary
seams: stable identities, relationship metadata, exportable filtered groups, and
pluggable notification channels.

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

Peer-to-peer communication, encrypted community sync, community rules, and
automated nudgers belong to a later layer.
