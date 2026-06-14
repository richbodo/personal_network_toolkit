# PNA Toolkit

> **Toolkit-Version:** 0.1 (draft) — the toolkit (spec, contracts, skill, lint, templates) is versioned as a unit; see [VERSION](VERSION).

The PNA Toolkit is a [generative application-class blueprint](docs/PriorArt.md) for building and validating **[personal network applications (PNAs)](spec/PNA_Spec.md#goals)** — local-only apps that take local ownership of your contact data and let you build **private relationship memory** over it behind a firewalled private data layer. PNAs run on the user's device, never as SaaS, and bridge SaaS-held contact data into a private workspace. The spec is organized around **four goals** — *take ownership of the root · protect its integrity by validation · protect it from egress · protect it from entropy & accidents*. **[Why do this?](spec/PNA_Spec.md#preamble)**

When building a PNA, specs are foundational because users will increasingly compose software by prompting AI agents, and success is measured by adherence to them.

Three deliverables, in dependency order:

1. **Foundational specs.** Universal vocabulary, goals, axes, architectural commitments, and typed contracts for a PNA. — **shipping in v0.1 (draft)**.
2. **Production-ready reference applications.** Working PNAs you can install, study, and adapt. — the first two reference designs are a distributed directory archive ([richbodo/fellows_local_db](https://github.com/richbodo/fellows_local_db)) and a Personal Relationship Manager ([richbodo/prm](https://github.com/richbodo/prm)).
3. **AI tooling — skill + MCP (Model Context Protocol) servers.** How AI agents work with the toolkit. The skill at [`pna-build-eval-contrib/SKILL.md`](pna-build-eval-contrib/SKILL.md) is what an agent reads to consume the spec at design time. The MCP servers (typed contracts in [`contracts/`](contracts/); three v1 stdio implementations in `fellows_local_db/mcp_servers/`) expose an already-built PNA's capabilities at runtime so AI clients (Claude Desktop, Cursor, local Ollama agents) can drive a PNA on the user's behalf.

The PNA Toolkit supports four modes of use, all packaged in the [skill](pna-build-eval-contrib/SKILL.md). **Install it once** so your agent auto-discovers it — symlink the skill into your skills directory (run from your toolkit working directory):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/pna-build-eval-contrib" ~/.claude/skills/pna-build-eval-contrib
```

A `git pull` here then updates the skill everywhere it's used. See [`docs/users-guide.md` § Install the skill](docs/users-guide.md#install-the-skill) for copy-instead-of-symlink, project-scoped, and no-install alternatives. With the skill installed, drive any mode in natural language:

- **Evaluate.** *Audit any contact app for safety before you install it.* An AI agent reads the candidate's source, checks it against every applicable AC (Architectural Commitment), and returns a structured report flagging anything that would put your data at risk. The lowest-friction way in — and it doubles as a self-check on your own in-progress design.
- **Build.** An AI agent reads the spec and helps you compose a conformant PNA against the typed contracts, adapting from a reference design that shares your axis picks.
- **Contribute.** When you find a spec gap or have a design that adds ecosystem value, the skill walks you through preflight validation (Architecture document + AC attestation table) and then opens the PR back to the toolkit.
- **Harden.** *Secure the environment your PNA runs in, not just the app.* The first three modes check the app; Harden is **advisory** — when an OS-level AI agent or another local process could reach your data out-of-band, an agent walks you through which environmental countermeasures fit your hazard (sandbox the agent, a separate OS user, an MCP access broker with just-in-time grants, a honeytoken + watchdog), which are already in place, and what is still exposed. It recommends; it does not mandate. (App security is build / evaluate / contribute; environment security is harden / advise.)

See [`docs/users-guide.md`](docs/users-guide.md) for step-by-step instructions for each.

The toolkit augments human-AI builder teams; it doesn't auto-build applications itself. It's a blueprint for AI agents to implement and humans to customize and verify. Conformance verification works at three layers: mechanical lints in `tools/` (CI-enforced), LLM (Large Language Model) architectural review via the skill above, and human PR review.

## Status

**v0.1 (draft).** The spec is feature-complete for v0.1 — universal ACs, axes, use cases, slot map with sub-contracts, and typed contracts are all in place. The "draft" label reflects that the contribution workflow described in [`plans/reorganization-plan.md`](plans/reorganization-plan.md) hasn't yet been validated against `fellows_local_db` as the first reference design.

*Most recent landing: the June 2026 direction work — `prm` accepted and archived as the second reference design, the spec restructured to four goals, the countermeasure library + the advisory Harden flow, the Contact Data Format Atlas, and a rewritten roadmap. See [`CHANGELOG.md`](CHANGELOG.md).*

What we're working toward — success looks like:

1. A new builder can read `README.md` + `CONTRIBUTING.md` and build a conformant PNA using the skill. *— Materials in place; the build flow is still being dogfooded against the reference designs.*
2. A new user can ask an LLM (via the skill) to audit a candidate PNA's source and get an actionable AC-keyed report. *— Skill flow documented; validation against a candidate pending.*
3. A new contributor can submit a reference design end-to-end without maintainer hand-holding beyond review. *— Exercised: `prm` was authored through the contribute flow and accepted as the second reference design; awaits a first **external** (non-maintainer) contribution.*
4. Every accepted design has a permanent Software Heritage identifier that survives upstream repo deletion. *— Met: `tools/swh-save.sh` ships, and both `fellows_local_db` and `prm` are archived with recorded SWHIDs.*
5. The PNA Spec evolves at least one minor version based on a contributed reference design's findings. *— In progress: `prm` promoted `AC-PRM-B` / `AC-PRM-C` from draft to attested flavor-derived ACs; the v0.2 cut that formalizes the toolkit version is the next roadmap step (see [`docs/roadmap.md`](docs/roadmap.md)).*
6. Every AC in the spec carries a stable ID; every typed contract names the AC(s) it realizes; every Architecture document maps each applicable AC to a verification mechanism. *— First two CI-enforced via [`tools/lint-spec-ids.py`](tools/lint-spec-ids.py); both reference designs carry Architecture docs with AC attestation tables.*

Step-by-step instructions for each of those goals live in [`docs/users-guide.md`](docs/users-guide.md).
How they're **sequenced** — the dependency-ordered priority tiers and the registry of inbound findings
from reference designs — lives in [`docs/roadmap.md`](docs/roadmap.md).

Substantive changes from v0.1 bump the toolkit version per [`CHANGELOG.md`](CHANGELOG.md).

## Entry points

Read in this first if you are new:

- [`docs/users-guide.md`](docs/users-guide.md) — step-by-step instructions for each of the success criteria in § Status (building a PNA, auditing one, submitting a reference design).
- [`spec/PNA_Spec.md`](spec/PNA_Spec.md) — universal PNA specification. Vocabulary, goals, use cases, axes, composition, universal architectural commitments, slot map with 57 sub-contracts, scope/versioning.

To contribute to the spec with a new reference design or architectural finding:

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how reference designs (and any spec changes they motivate) get accepted into the toolkit.

To dig into the spec more deeply:

- **[`pna-build-eval-contrib/SKILL.md`](pna-build-eval-contrib/SKILL.md)** — the skill packaging the four flows (build, evaluate, contribute, harden) for AI agents. The agent-consumption view of the toolkit.
- **[`spec/axes.md`](spec/axes.md)** — the Axes a PNA varies along, attested picks per Axis, and the flavor-derived ACs each pick triggers.
- **[`spec/use_cases.md`](spec/use_cases.md)** — attested classes of PNA (Minimum Viable PNA; Directory Archive realized; Personal Relationship Manager realized; Multi-PNA ecosystem target).
- **[`contracts/`](contracts/)** — typed contracts for the load-bearing interfaces: JSON Schema for the worker init handshake + RPC (Remote Procedure Call) protocol, OpenAPI for distribution auth, SQL DDL (Data Definition Language) for the two database schemas, TypeScript for the Communications transport interface, JSON Schema for the five canonical MCP server tool surfaces.
- **[`CHANGELOG.md`](CHANGELOG.md)** — toolkit version history.
- **[`llms.txt`](llms.txt)** — discovery file for the spec (humans + AI agents land here cold).

## Reference designs

A reference design is a working, deployed PNA that demonstrates one valid combination of axis picks against the spec. Each lives in its own repository so it can ship under its own release cadence.

- **[fellows_local_db](https://github.com/richbodo/fellows_local_db)** — first reference design. Directory Archive use case. Its [`docs/Architecture.md`](https://github.com/richbodo/fellows_local_db/blob/main/docs/Architecture.md) declares Toolkit-Version conformance and the per-slot specializations. Flavor:

  | Axis                | Pick                          |
  | ------------------- | ----------------------------- |
  | distribution        | `web-bundle-with-magic-link`  |
  | storage substrate   | `opfs-sqlite-wasm`            |
  | ingestion shape     | `single-source-static-mirror` |
  | workspace shell     | `vanilla-js-spa`              |
  | comms transport set | `mailto-only`                 |
  | MCP-exposure        | `shared+private+comms`        |


- **[prm](https://github.com/richbodo/prm)** — second reference design (accepted 2026-06-10). Personal Relationship Manager use case. Mirrors contacts scattered across Google / Apple / LinkedIn / Facebook / loose vCard / CSV into one user-owned store, deduplicates them, and lets an AI *propose* merges the user applies. First design to exercise multi-source dedup (`AC-PRM-B`) and the `native-sqlite-via-filesystem` substrate (`AC-PRM-C`), and the first build-from-verifiable-source distribution demonstrator. Its [`docs/Architecture.md`](https://github.com/richbodo/prm/blob/main/docs/Architecture.md) carries the AC attestation. Flavor:

  | Axis                | Pick                            |
  | ------------------- | ------------------------------- |
  | distribution        | `never-distributed-single-user` |
  | storage substrate   | `native-sqlite-via-filesystem`  |
  | ingestion shape     | `multi-source-merge-with-dedup` |
  | workspace shell     | `vanilla-js-spa`                |
  | comms transport set | `none`                          |
  | MCP-exposure        | `shared-only`                   |

When a further reference design lands, it'll be linked from here.

## Prior Art

The PNA Toolkit is a *generative application-class blueprint*: a machine-readable spec, written for AI agents, that defines what makes an instance of a whole *class* of apps correct and lets many implementations attest conformance. [`docs/PriorArt.md`](docs/PriorArt.md) surveys the landscape — spec-driven-development tooling, agent-interface standards, conformance test suites, Common Criteria Protection Profiles, and local-first infrastructure — and finds no published artifact occupies the same quadrant: *generative + class-scoped + multi-flavor + machine-checkable*. The full annotated source list is in [`docs/PriorArtReferences.md`](docs/PriorArtReferences.md).

## License

[LICENSE](LICENSE).