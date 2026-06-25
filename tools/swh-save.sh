#!/usr/bin/env bash
# Toolkit-Version: 0.2
#
# swh-save.sh — request Software Heritage archival of a reference design's
# source and print the git-compatible SWHIDs to record in its design entry.
#
# Why: the toolkit records a Software Heritage Persistent IDentifier (SWHID) for each
# accepted reference design so the source survives even if the upstream repo
# is deleted (spec/PNA_Spec.md § Vocabulary "reference design"; CONTRIBUTING
# § Archival). SH's content/dir/rev identifiers are git-compatible, so
# swh:1:dir / swh:1:rev can be computed locally from a clone the moment it's
# tagged — Save Code Now then makes them resolvable and permanent.
#
# Usage:
#   tools/swh-save.sh <repo-url> [<git-ref>] [<local-clone-path>]
#
# Examples:
#   tools/swh-save.sh https://github.com/richbodo/fellows_local_db v0.1.0 ~/src/fellows_local_db
#   tools/swh-save.sh https://github.com/you/your-pna     # save default branch; no local SWHID computed
#
# Env:
#   SWH_SAVE_NO_REQUEST=1   skip the Save Code Now POST and only compute/print the
#                           local SWHIDs (offline use; exercised by the self-test).
set -euo pipefail

URL="${1:?usage: swh-save.sh <repo-url> [git-ref] [local-clone-path]}"
REF="${2:-HEAD}"
CLONE="${3:-}"
URL="${URL%/}"
SAVE_API="https://archive.softwareheritage.org/api/1/origin/save/git/url/${URL}/"

if [ -n "${SWH_SAVE_NO_REQUEST:-}" ]; then
  echo "→ SWH_SAVE_NO_REQUEST set — skipping the Save Code Now request; computing SWHIDs only."
else
  echo "→ Requesting Software Heritage archival (Save Code Now) for:"
  echo "    ${URL}"
  if curl -fsS -X POST -H 'Accept: application/json' "$SAVE_API"; then
    echo
    echo "  queued — track at https://archive.softwareheritage.org/save/ (ingest can take minutes to hours)"
  else
    echo
    echo "  ⚠ Save request failed (network or rate-limit). Submit manually:"
    echo "    https://archive.softwareheritage.org/save/  → paste ${URL}"
  fi
fi

echo
# Compute the git-compatible SWHIDs from a local clone if one is available.
GITDIR=""
if [ -n "$CLONE" ]; then
  GITDIR="$CLONE"
elif git rev-parse --git-dir >/dev/null 2>&1; then
  GITDIR="."
fi

if [ -z "$GITDIR" ]; then
  # No clone at all (none passed, cwd isn't a git repo).
  echo "No local clone provided — re-run with a clone path to compute the SWHID locally:"
  echo "    tools/swh-save.sh ${URL} ${REF} <clone-path>"
  echo "or read swh:1:dir from the SH archive UI once ingest completes."
elif ! git -C "$GITDIR" rev-parse "${REF}^{commit}" >/dev/null 2>&1; then
  # The clone IS here, but the ref doesn't resolve in it — the common typo/un-fetched
  # case (e.g. asking for 'pnt-ref-0.2.0' when the tag is 'pnt-ref-0.2'). Say so
  # specifically rather than the misleading "No local clone provided".
  echo "Clone ${GITDIR} has no ref '${REF}' — the clone is there, but that ref isn't."
  echo "Check the exact name (e.g. 'pnt-ref-0.2', not 'pnt-ref-0.2.0'), then re-run:"
  echo "    git -C ${GITDIR} tag -l                  # list local tags to confirm the name"
  echo "    git -C ${GITDIR} fetch --tags origin     # if the ref is only on the remote"
  echo "or read swh:1:dir from the SH archive UI once ingest completes."
else
  fmt=$(git -C "$GITDIR" rev-parse --show-object-format 2>/dev/null || echo sha1)
  # Peel to the commit: `git rev-parse <annotated-tag>` yields the tag *object*
  # hash, but a swh:1:rev names a revision (a git commit). `^{commit}` is a no-op
  # for branches / lightweight tags / raw SHAs and unwraps an annotated tag.
  commit=$(git -C "$GITDIR" rev-parse "${REF}^{commit}")
  tree=$(git -C "$GITDIR" rev-parse "${REF}^{tree}")
  echo "SWHIDs for ${URL} @ ${REF} (${commit:0:12}):"
  echo "  swh:1:rev:${commit}"
  echo "  swh:1:dir:${tree}"
  if [ "$fmt" != "sha1" ]; then
    echo "  ⚠ repo object-format is ${fmt}, not sha1 — these are NOT git-compatible;"
    echo "    take the canonical swh:1:dir from the SH archive after ingest instead."
  fi
  echo
  echo "Paste into reference_designs/<name>/design.toml (and record in the README),"
  echo "then set archival = \"archived\" — the lint requires and cross-checks these:"
  echo "  commit    = \"${commit}\""
  echo "  swhid_rev = \"swh:1:rev:${commit}\""
  echo "  swhid_dir = \"swh:1:dir:${tree}\""
fi
