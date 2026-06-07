# Should the spec allow Exceptions at all? — an existential review

*Design note · 2026-06 · status: deliberation recorded, proposals open. Indexed from
[`../PriorArt.md` § Design notes](../PriorArt.md). Drove the honest-exit RFC
([PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32)).*

> **Home of this note.** The toolkit's design-note *log* lives in [`docs/PriorArt.md` § Design notes](../PriorArt.md)
> — dated, newest-first, one entry per decision. That log is the index; full-length deliberations
> (like this one) live as their own files under `docs/design-notes/` and are linked from a log entry.

## The question

The Exceptions mechanism ([`spec/exceptions.md`](../../spec/exceptions.md)) lets a PNA *deliberately*
depart from its defining guarantee — "runs local-only, never as SaaS" — by **raising an `EX-*`
exception**, while still being treated as "a conformant PNA operating in a declared non-PNA mode."
The first such exception, `EX-CLOUD-LLM`, was distilled from operating the `fellows_local_db`
reference design with ~500 users who wanted to connect **Claude Desktop** — a cloud model — to their
local relationship data.

That raises an existential question for the toolkit: **is admitting exceptions a corruption of the
spec?** Once any PNA can be in a "not a PNA" mode, does the word "PNA" still mean anything? Or is the
honest, consented, reversible exception actually the *right* way to serve users? Should we allow
exceptions at all — and if so, **where do we draw the line, and are we drawing it in the right
place?**

This note records how that was worked through and what it concluded.

## The flow: goals → architecture → environmental constraints

The toolkit reasons top-down: from the **Goals**, to the **architectural commitments** that make them
achievable, and then into the **environmental constraints** the real world imposes. The tension lives
at the third layer. Users demand less privacy when they make exceptions; we would like their data to
be *always* as protected as possible — but the surest way to fail at protecting data is to ship a tool
too pure to use. The fellows users demanded a cloud LLM. Connecting one hands some of the data that
forms the **root** of a personal network to an outside system. In return it provides real
productivity. **That is the equation.** The thing we care about most is that people are *aware* of
what is happening, are *explicit* about the exception, and that we are talking to the *actual user* and
that they *understand*. The exception, to be legitimate, has to come **from the individual user** — it
must be what they *need*, not merely what some vendor or proxy *wants* for them.

## The hard environmental constraint: an MCP server cannot identify the consuming LLM

The whole debate is shaped by a fact that turned out to be structural, not a gap to patch (see the
sibling design note in the PRM reference design,
[`mcp-cannot-identify-the-consuming-llm`](https://github.com/richbodo/prm/blob/main/docs/design-notes/mcp-cannot-identify-the-consuming-llm.md)):

- The MCP **server is the data source**; the **host** (Claude Desktop) is the sink. Once the server
  returns a tool result, what the host does with it — feed a cloud model, a local model, log it,
  forward it — is outside the server's view and control. You cannot govern data after handing it over.
- `clientInfo` in the MCP `initialize` handshake is **self-reported** and identifies the *app*, not
  the model; it is trivially spoofable.
- MCP's OAuth (2025-06-18 spec) authenticates the **client → server** — the wrong direction. There is
  no mechanism by which "the LLM" proves it is local or discloses its owner.

So "detect and block cloud LLMs" is a dead end. The distinction the spec cares about — *does this data
leave the device?* — is **invisible at the protocol boundary.** That means a prohibition on cloud
egress at the MCP surface is **architecturally unenforceable**: the egress happens regardless, and the
spec's only real choice is **governed** egress (consent gate, signal, reversal, honest disclosure)
versus **ungoverned** egress (a fork, a lie, or a silent deviation). That reframing is what makes the
exception mechanism a serious candidate rather than a capitulation.

## Method: two adversarial analyses, then synthesis

To avoid talking ourselves into a comfortable answer, the question was put to **two independent
analyses with opposed briefs** — one building the strongest honest case *for* the spec admitting
exceptions, one *against* — each required to steelman and rebut the other, then a third synthesis pass.
What follows distills both.

### The case FOR (keep and bless the mechanism)

1. **The prohibition doesn't prevent egress; it un-governs it.** Given the constraint above, banning
   the cloud connection yields a fork, a lie, or a silent deviation — and `exceptions.md` names the
   silent deviation as the actual failure mode. The handler contract converts an unenforceable
   *prohibition* into an enforceable *handler*: consent-before-raise (EX-H2), a persistent "not a PNA"
   signal (EX-H3), a runtime explainer (EX-H4), a reversal path (EX-H5). That is strictly more
   protection than a ban that gets routed around.
2. **It maximizes the top-stated value — awareness — exactly when it matters.** A ban produces zero
   awareness infrastructure. Exceptions make disclosure a *conformance requirement*. The shipped
   fellows consent flow ("you are leaving the local-only model… this sends your data to a SaaS
   vendor… no one can guarantee what they do with it") is more honest than most *compliant* software.
3. **The strength profile (EX-H8) refuses to launder the bad news.** It grades per dimension and says
   the quiet part out loud — "provider won't train/retain → `provider-asserted`," "data already sent →
   `none`." A corrupt mechanism hides the cost of deviating; this one itemizes it.
4. **"Want vs. need" is satisfied by goal-anchoring + individual origin.** Every exception must name
   the AC it relaxes; consent must come from the human (EX-H2) and must not be manufactured by a proxy
   (EX-H7). An informed adult trading disclosure of *their own* data for a real payoff is exercising
   autonomy, not failing to be protected.
5. **"Conformant in non-PNA mode" is coherent as conformance-to-process.** A program that throws and
   *catches* an exception isn't broken; an *uncaught* one is the bug.

The FOR side's honest concession: **EX-H7's "best-effort" is a real hole at the exact seam the
mechanism is named for** — in an agent-mediated future the immediate caller is often not the human, and
a non-cooperating client cannot be compelled to relay the notice. The strongest claim (informed
*individual* consent) is weakest in the orchestrated case the toolkit is being built to enable.

### The case AGAINST (the blessing corrupts the guarantee)

1. **"Conformant PNA in non-PNA mode" is an oxymoron that redefines the term out of existence.** The
   property that distinguishes a PNA — local-only — is suspended, yet the label survives. "PNA" stops
   meaning "privacy guaranteed by the architecture" and starts meaning "an intention to disclose
   nicely." A relying party can no longer trust the word without auditing.
2. **The central safeguard is structurally unenforceable** where it matters (EX-H7 `best-effort`; the
   consumer is invisible). If you cannot verify a comprehending human consented, you cannot claim the
   exception is what they *need*.
3. **Ceremony vs. protection.** Once data crosses, the spec guarantees `none` about the data and the
   reversal "cannot recall data already sent." A promise that degrades to "we told you loudly before
   we couldn't protect you" is a different, weaker kind of spec.
4. **The slippery slope is structural.** "Name the AC you relax" is trivially satisfiable; the
   user-demand gradient runs one way (toward more disclosure). `EX-CLOUD-LLM` is the sympathetic first
   case that sets the template.
5. **The bright line derives its power from refusing exceptions** — cf. E2E encryption, copyleft.
   Detect-and-report the deviation, but don't *bless* it; call it **"not a PNA right now."**

The AGAINST side's honest concession: on the **UX merits the FOR side is largely right** — a pure ban
would likely produce *worse* real-world privacy. Its case narrows to: keep the disclosure machinery,
but **don't attach the word "conformant" to the deviating state**, because the spec plans for
conformance to gate runtime interop — at which point the label is load-bearing, not bookkeeping.

## The convergence

Stripped to recommendations, the two analyses **agreed on almost everything** — the disagreement
reduced to a single word:

| | FOR | AGAINST |
|---|---|---|
| Keep the consent gate / banner / honest strength profile? | Yes — the spine | Yes — "the best part of the spec" |
| Is a pure prohibition the answer? | No (un-governs egress) | No (conceded: worse outcomes) |
| Fix EX-H7's best-effort consent? | Yes — **fail closed** | Yes — **fail closed**, at the app's own surface |
| Hold a hard floor of un-relaxable guarantees? | Yes — AC-MCP-B / human-review-before-send | Yes (implied by detect-only + tiering) |
| The word **"conformant PNA in non-PNA mode"** | Coherent (process) | **Laundering** — relabel "not a PNA right now" |

Two independent adversarial passes converging on *fail-closed consent* and *keep-the-disclosure* is the
signal those are right. The existential worry is real but **mislocated**: the mechanism isn't the
problem — **one overloaded word is.**

## Synthesis

**Allow exceptions.** The decisive reason is the environmental constraint: local-only at the MCP
boundary is unenforceable, so the choice is governed vs. ungoverned egress, and a ban buys a
cleaner-sounding "never" at the cost of every actual protection. A spec earns authority by being
*trustworthy* — every claim verifiable — not by being *pure*. "Local-only, no exceptions ever" is an
*unverifiable* claim here, and an unverifiable guarantee is worth less than an honest, bounded one.
**Honesty scales; purity doesn't.**

**"Want vs. need" dissolves into provenance + comprehension.** The legitimacy of an exception has
nothing to do with the *content* of the choice and everything to do with *where it came from*. The
toolkit's north star is **informed autonomy over your own personal network**, not maximal data
confinement. Confinement is the *default* expression of that autonomy; the exception is *another*
expression of the same autonomy — provided the choice provably came from the comprehending individual.
That single "iff" is where the whole weight rests — and it is exactly where EX-H7's `best-effort`
fails. When you cannot establish that a comprehending human chose it, you cannot tell *want* from
*need*, and you must **fail closed**.

**"Where is the line?" is three different lines, currently conflated:**

1. **What may never be relaxed (the floor).** Some guarantees are absolute even with consent: the
   human-in-the-loop on **action taken on the user's behalf** (AC-19 user-sees-payload-before-send,
   AC-MCP-B not-bypassable-by-AI, AC-18 no-content-reading transports). The principle: *you may consent
   to disclose data you read; you may never consent away the human-in-the-loop on action taken on your
   behalf* — because that action reaches **other people**, the contacts in your graph, who consented to
   nothing. Disclosure is a bounded harm to your own data; unreviewed delegated action is an
   open-ended harm to third parties.
2. **Handled vs. merely detected (the bar to be blessed).** An exception is "handled" only if consent
   is **enforced** at a surface the app controls, comprehension is checked, and it **fails closed**
   when a comprehending human can't be confirmed. Best-effort relayed consent is *below* the line —
   detected and reported, not blessed.
3. **The label (the one real disagreement).** Resolve it by **decomposition**, which keeps both sides'
   truths. The word "conformant" was carrying two predicates:
   - *Is this a PNA right now?* → `pna-active` — `false` while an exception is active. A relying party
     (a user; an interop gate) keys on this, and only this.
   - *Does it handle its declared exceptions correctly?* → `exception-handling` conformant.

   Report them **separately**. The handler genuinely *is* conformant (FOR keeps its point); the
   deviation genuinely *is* "not a PNA right now" and *fails the interop gate* (AGAINST keeps its
   point). **The error was one word carrying two meanings.** Notably, the fellows banner already says
   *"Going rogue — not a PNA"* — the spec's prose was *less honest than the reference design's own UI.*

## Verdict and the three corrections

The mechanism belongs in the spec; the line is drawn in the right *neighborhood*; three corrections
make the FOR case sound rather than a rationalization. They are proposed in
[PR #32](https://github.com/richbodo/personal_network_toolkit/pull/32):

1. **Split the overloaded predicate** — `pna-active` (mode bit; gates interop) vs. `exception-handling`
   conformant (process). Retire "a conformant PNA operating in a declared non-PNA mode."
2. **Harden EX-H7 to fail-closed** — consent on a PNA-controlled surface (`enforced`), best-effort
   relay up to cooperating clients, hard refuse down when a human can't be confirmed.
3. **Add an un-relaxable floor** — AC-18 / AC-19 / AC-MCP-B; charter member is human-review-before-send.

In one line: **we protect your autonomy over your own network — by default that means your data stays
home, and the one door out is named, individual, comprehended, revocable in posture, honest about what
it can't take back, and it is never the door for acting on your behalf without you.**

## Future-defense directions (raised, not yet specced)

The deepest unfixable bit — telling a human from a machine — invites layered defense rather than a
single gate. Three directions worth a future write-up:

- **Friendly-machine consent relay.** Even though we can't *compel* it, we can *ask*: via the MCP
  `instructions` handshake (and tool-result messages), a PNA tells a cooperating client *"have the user
  open the app and press confirm before I return private data — then come back."* Best-effort up, while
  the PNA fails closed down. This is the constructive half of EX-H7's hardening (PR #32).
- **Runtime egress detection as a toolkit metric.** The toolkit already ships a *static* egress scanner
  ([`tools/egress-lint.py`](../../tools/egress-lint.py), AC-1). A *dynamic* complement — observe a
  candidate PNA's actual network traffic during an evaluate run and flag off-device vectors — is how
  egress is detected in practice, and would feed the evaluate flow as runtime evidence alongside the
  static scan. Worth adding as an evaluate-flow probe.
- **Opt-in OS-level alerts.** For users who want a louder signal, a PNA could (opt-in) raise an
  operating-system notification when an exception goes active or when private data is about to cross the
  boundary — an out-of-band channel that doesn't depend on the cloud client cooperating.

None of these defeat the constraint; together they raise the cost of an un-noticed deviation, which is
the realistic goal once a hard guarantee is off the table.

## The deepest principle: design from behind the veil

This toolkit will have many future users (the maintainer expects to be only one of them). That is a
Rawlsian design position: choose the rule without knowing *which* user you'll be. From there, the right
design protects the **worst-off** user — the least technical, most likely to be steamrolled by a
manufactured-consent flow or a proxy that "accepts" on their behalf. That user is protected by the
**floor** (line 1) and **fail-closed consent** (line 2), which apply to *everyone*. The sophisticated
user who knowingly wants the cloud trade is served by the exception path *above* the floor. **A hard
floor for everyone plus an honest, enforced, individual opt-out above it** is the only design that's
fair across the whole future population — not just the experts.

## Provenance

Worked through in a Claude Code session (June 2026) while drafting the PRM reference design's
guidance, using the `fellows_local_db` precedent (`EX-CLOUD-LLM`, shipped consent flow, the
`never-saas` and `local_vs_saas_risk` notes) and the MCP-protocol research recorded in PRM's
`mcp-cannot-identify-the-consuming-llm` design note. Prior art for the exception *mechanism* itself
(macaroons → EX-H7, graded assurance, consent-receipt frameworks) is surveyed in
[`../PriorArt.md` § 9](../PriorArt.md).
