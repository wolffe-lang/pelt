#!/bin/bash
# sh20: the before/after table of the shapes that fork. Three passes of
# tools/shape-rss's rows (sh20's seven, the rows that fork since sh20,
# and the loop's own floor), over the pin's binaries (the shapes in
# process) and the head's (forked), both tiers, and dash. Inside ctr.sh.
# usage: table.sh OUT HEAD_TREE PIN_TREE [FIRST_PASS]
# Each binary is first copied the same way into OUT/bin (`cp`, then read
# once): a file's page-cache state decides how much of its mapping a
# run's peak counts (RssFile, `logs/rssgap/`), so the pin's and the
# head's peaks are only comparable from copies made alike.
O=$1; H=$2; B=$3; P0=${4:-1}; mkdir -p "$O/bin"
ulimit -c 0
ROWS=baseline,subshell,substitution,substitution-pipeline,background-builtin-wait,background-nowait,script-background-wait,typed-background-wait,fork-substitution,fork-subshell,fork-background-group,fork-background-subshell,fork-stage,script-fork-substitution,typed-fork-subshell,fork-redirected-subshell
for src in "$B/target/native/pelt:pin-native" "$B/target/release/pelt:pin-release" \
           "$H/target/native/pelt:head-native" "$H/target/release/pelt:head-release" "/usr/bin/dash:dash"; do
  cp "${src%%:*}" "$O/bin/${src##*:}"
  cat "$O/bin/${src##*:}" > /dev/null
  echo "${src##*:} $(sha256sum "$O/bin/${src##*:}" | cut -c1-12) from ${src%%:*}" >> "$O/bins"
done
for pass in $(seq "$P0" 3); do
  for bin in "$O/bin/pin-native:pin-native" "$O/bin/pin-release:pin-release" \
             "$O/bin/head-native:head-native" "$O/bin/head-release:head-release" "$O/bin/dash:dash"; do
    path=${bin%%:*}; tag=${bin##*:}
    "$H/tools/shape-rss" --only "$ROWS" "$path" > "$O/rows-$tag-$pass.log" 2>&1
    echo "$tag pass $pass: $?" >> "$O/status"
  done
done
echo done > "$O/DONE"
