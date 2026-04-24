# Use Cases

This document captures the human workflows the toolkit is meant to support. It
is intentionally broader than the first implementation so design decisions can
keep future uses in view without overbuilding them now.

## Use Cases

### Take control of your relationship data

Problem: Your SaaS contact dbs are a mess and you don't trust the vendors.

Export your contacts and add relationship data to a local db - your relationship database.

Stop telling centralized apps things they should not know.

Centralized contact systems are not even good at storing basic contact facts, 
because they run on the profit motive alone, with the goal of collecting data 
and creating system lockin, which leads to the largest amount of low-quality
data and an unusable system overall.

They are also the wrong place for sensitive relationship context:
not everyone wants large platforms, their administrators, or governments that can
compel those platforms to know who they might contact about mental health,
politics, immigration, family issues, or other private topics. They also shut down
apps, get cracked, and lose data from time to time.

Actual relationship data is more important and more sensitive than contact data:

- Notes about context, history, interests, boundaries, and follow-up ideas.
- Tags such as `close friend`, `pickleball`, `mental health discussion`, `family`,
  `work friend`, `sensitive about x`
- And other searchable private metadata that stays local, and helps the user find things quickly.

This data will never see the internet.  It is local-only, for the user only, 
and free forever.

### Build a distributable directory for your community or org

Problem: Your org wants to get away from some expensive SaaS directory for 
whatever reason.

Distribute a directory in an organized way that is fast and easy for members.
You don't need SaaS to own your groups data - and every member should be able
to add private notes and relationship data that are useful only to them.

This is particularly useful for porting out legacy directories from orgs that 
are closing down their SaaS.

The toolkit should make it easy to massage that data into a local-first 
offline-first directory that is installable on any device and supports rich data that would 
be horrible to work with in a shittier alternative to porting out, like a spreadsheet.

### Filter, discover and analyze your own contact data for high quality, rapid retrieval

Problem: You need a really fast way to find critical subsets of contacts based on 
your private tags, notes, and contact data.

A lot of folks will want to keep track of personal relationships they have with others, wihtout
giving all their personal relationship data to facebook, salesforce, or any other 
corporation.  

One problem with large directories that try to steal as much information from users as possible,
is that they are impossible to browse and discover data you need with.  In addition to stealing 
your personal data and selling it, contact managers and CRMs are a mess of 
centralized SaaS and do not serve this function well in any way.

KEY USE CASE: When the author of this toolkit wants to find someone to talk about mental health
with, browsing a SaaS directory like linkedin or google contacts turns into a very depressing
boondoggle very quickly, exacerbating the problem rather than solving it.  About 100 contacts 
into the A's in the alphabetical list, you wonder who these people are and why you don't 
know any of them, and give up.

When you take control, you have the local tools, and can build more, with this toolkit,
to analyze and discover data, and prepare personal networks and directories for the
future.

You can search and filter to create small, **Visual** subset of a much larger set of 
contacts in a portable or distributable way.  I can build a small visual directory with PNT
that I can access instantly when I want to find someone to talk to about mental health issues.

Exporting modalities include things like, a PDF on a phone before a family visit or party,
or a community directory for publishing on a website, or a json file for consumption by 
another app.

The toolkit should support deterministic filtering first:

- text search across contact facts, overlays, tags, and non-private notes
- simple filters such as `has_email:true`
- tag filters such as `#work` or `#pickleball`
- combinations that can be saved, shared, or represented as a small search DSL

That deterministic layer is the foundation for augmented natural-language
filtering later. An LLM should be able to help turn a user request like "people
from work who play pickleball and have an email address" into an inspectable
filter expression, then let the deterministic engine run it. The LLM helps with
discovery and curation, but the result set should still be explainable and
repeatable.

Later, local-LLM support will be added for natural language search and assisted discovery.

Also, OSS FTW, because people are definitely going to just rewrite the search layer 
with AI, and use their own local AIs to help with discovery using private context.

### Quickly notify a selected group

Problem: You need a fast way to send out a notification to a group that 
may not have a unified chat group or mailing list.

Sometimes the user finds the right subset of people and wants to contact them all:

- "I want to talk about pickleball. Here are some possible times."
- "I want to ask work friends about a project idea."
- "I want to check in with people tagged as close friends."
- "I want to reach people who care about mental health."

When the user needs the right people quickly, failed search is not just annoying; it
can consume the energy they had for reaching out.  So the key is speed. Most directories 
are noisy, and the value of this toolkit is that a curated, targeted set can be created 
quickly and acted on immediately.

The first version may not need a full notifier. Generated HTML can start with
individual `mailto:` links and possibly a group email link. A later notifier can
send email to selected contacts, with responses coming back to the user. It does
not need to coordinate schedules or manage replies in the first version.

Later, the same notifier model should support additional channels through
plugins.  If every person in a list responds differently on a different channel, 
then the appropriate default channel can be used for each, as long as the plugin
exists.

### Build Toward Peer-To-Peer Community Tools

Problem: You want to understand your personal network, or
Your whole community wants to understand how their community health is holding up -
this requires data be analyzed - and that data can reveal important insights.

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

Peer-to-peer and other communication channels, encrypted community sync (ZKPs), community rules, and
automated nudgers belong to a later layer.
