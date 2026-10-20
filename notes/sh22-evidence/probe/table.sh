#!/bin/bash
# table.sh — lane-local (sh22): the before/after table. Three passes of
# tools/shape-rss's own rows (sh22's seven and the controls, each at the
# gate's N) and of shapes22.py's neighbours, over trunk's and the head's
# binaries on both tiers and dash. Inside ctr.sh.
# usage: table.sh OUT HEAD_TREE BASE_TREE
O=$1; H=$2; B=$3; mkdir -p "$O"
P=$(cd "$(dirname "$0")" && pwd)
ROWS=baseline,builtin-wait,builtin-read-redir,builtin-eval,builtin-cd,builtin-command,builtin-umask,background-nowait,background-program-nowait,background-wait
NB=bi-read-here,bi-eval-arg,bi-cd-dir,bi-command-v,bi-umask-print,bi-jobs,bi-redir
for pass in 1 2 3; do
  for bin in "$B/target/native/pelt:trunk-native" "$B/target/release/pelt:trunk-release" \
             "$H/target/native/pelt:head-native" "$H/target/release/pelt:head-release" "/usr/bin/dash:dash"; do
    path=${bin%%:*}; tag=${bin##*:}
    "$H/tools/shape-rss" --only "$ROWS" "$path" > "$O/gate-$tag-$pass.log" 2>&1
    PELT_TOOLS=$H/tools python3 "$P/shapes22.py" --only "$NB" "$path" > "$O/nb-$tag-$pass.log" 2>&1
  done
done
echo done > "$O/DONE"
