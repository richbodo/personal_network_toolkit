#!/usr/bin/env bash
# Toolkit-Version: 0.1
#
# swh-save.sh — request Software Heritage archival of a reference design's
# source and print the git-compatible SWHIDs to record in its design entry.
#
# Why: PNT records a Software Heritage Persistent IDentifier (SWHID) for each
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
set -euo pipefail

URL="${1:?usage: swh-save.sh <repo-url> [git-ref] [local-clone-path]}"
REF="${2:-HEAD}"
CLONE="${3:-}"
URL="${URL%/}"
SAVE_API="https://archive.softwareheritage.org/api/1/origin/save/git/url/${URL}/"

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

echo
# Compute the git-compatible SWHIDs from a local clone if one is available.
GITDIR=""
if [ -n "$CLONE" ]; then
  GITDIR="$CLONE"
elif git rev-parse --git-dir >/dev/null 2>&1; then
  GITDIR="."
fi

if [ -n "$GITDIR" ] && git -C "$GITDIR" rev-parse "$REF" >/dev/null 2>&1; then
  fmt=$(git -C "$GITDIR" rev-parse --show-object-format 2>/dev/null || echo sha1)
  commit=$(git -C "$GITDIR" rev-parse "$REF")
  tree=$(git -C "$GITDIR" rev-parse "${REF}^{tree}")
  echo "SWHIDs for ${URL} @ ${REF} (${commit:0:12}):"
  echo "  swh:1:rev:${commit}"
  echo "  swh:1:dir:${tree}   <- record this in reference_designs/<name>/README.md"
  if [ "$fmt" != "sha1" ]; then
    echo "  ⚠ repo object-format is ${fmt}, not sha1 — these are NOT git-compatible;"
    echo "    take the canonical swh:1:dir from the SH archive after ingest instead."
  fi
else
  echo "No local clone provided — re-run with a clone path to compute the SWHID locally:"
  echo "    tools/swh-save.sh ${URL} ${REF} <clone-path>"
  echo "or read swh:1:dir from the SH archive UI once ingest completes."
fi
