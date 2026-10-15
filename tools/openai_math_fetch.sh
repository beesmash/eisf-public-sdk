#!/usr/bin/env bash
# Read-only acquisition of upstream research files. No upstream code is run.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.research/openai-math"
REMOTE="https://github.com/openai/math.git"
command -v git >/dev/null || { echo "git required" >&2; exit 2; }
mkdir -p "$ROOT/.research"
if [[ -d "$DEST/.git" ]]; then
  ACTUAL="$(git -C "$DEST" remote get-url origin)"
  [[ "$ACTUAL" == "$REMOTE" ]] || { echo "Untrusted source remote: $ACTUAL" >&2; exit 3; }
  git -C "$DEST" diff --quiet || { echo "Uncommitted research files changed; aborting" >&2; exit 4; }
  git -C "$DEST" fetch --depth=1 origin main
  git -C "$DEST" checkout --detach FETCH_HEAD
elif [[ ! -e "$DEST" ]]; then
  echo "Cloning full OpenAI mathematics research release (large download)."
  git clone --depth=1 --filter=blob:none "$REMOTE" "$DEST"
else
  echo "Destination exists and is not a clone; aborting" >&2
  exit 5
fi
SHA="$(git -C "$DEST" rev-parse HEAD)"
test -f "$DEST/CONTENTS.md" && test -f "$DEST/LICENSE" || { echo "Incomplete repository" >&2; exit 6; }
printf "Source checkout: %s\nCommit: %s\n" "$DEST" "$SHA"
