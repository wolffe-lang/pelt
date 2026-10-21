#!/bin/bash
# sh20: the before/after table of the shapes that fork. Three passes of
# tools/shape-rss's rows (sh20's seven, the rows that fork since sh20,
# and the loop's own floor), over the pin's binaries (the shapes in
# process) and the head's (forked), both tiers, and dash. Inside ctr.sh.
# usage: table.sh OUT HEAD_TREE PIN_TREE
O=$1; H=$2; B=$3; mkdir -p "$O"
ulimit -c 0
ROWS=baseline,subshell,substitution,substitution-pipeline,background-builtin-wait,background-nowait,script-background-wait,typed-background-wait,fork-substitution,fork-subshell,fork-background-group,fork-background-subshell,fork-stage,script-fork-substitution,typed-fork-subshell
for pass in 1 2 3; do
  for bin in "$B/target/native/pelt:pin-native" "$B/target/release/pelt:pin-release" \
             "$H/target/native/pelt:head-native" "$H/target/release/pelt:head-release" "/usr/bin/dash:dash"; do
    path=${bin%%:*}; tag=${bin##*:}
    "$H/tools/shape-rss" --only "$ROWS" "$path" > "$O/rows-$tag-$pass.log" 2>&1
    echo "$tag pass $pass: $?" >> "$O/status"
  done
done
echo done > "$O/DONE"
