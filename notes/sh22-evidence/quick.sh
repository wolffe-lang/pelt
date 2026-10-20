#!/bin/bash
# sh22 quick check (inside ctr.sh): the corpus and the sessions on both
# tiers of the tree's build, totals only. usage: quick.sh TAG TREE
T=$1; TREE=$2
S=$(cd "$(dirname "$0")" && pwd)
cd "$TREE" || exit 9
mkdir -p "$S/logs/quick"
for t in native release; do
  tools/difftest --bin target/$t > "$S/logs/quick/$T-diff-$t.log" 2>&1; echo "diff-$t=$? $(tail -1 "$S/logs/quick/$T-diff-$t.log")"
  grep -E '^(FAIL|UNLISTED)' "$S/logs/quick/$T-diff-$t.log" | head -20
  tools/session --bin target/$t > "$S/logs/quick/$T-sess-$t.log" 2>&1; echo "sess-$t=$? $(tail -1 "$S/logs/quick/$T-sess-$t.log")"
  grep -E '^(FAIL|UNLISTED)' "$S/logs/quick/$T-sess-$t.log" | head -20
done
