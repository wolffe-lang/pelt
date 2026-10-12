#!/bin/bash
# lane-local: instructions a turn of BODY at each commit (release). usage: icommits.sh BODY SHA…
B=$1; shift
cd "$HOME/lanes/sh08/pelt" || exit 9
git fetch -q origin
export TMPDIR=$HOME/lanes/sh08/tmp
bins=""
for c in "$@"; do
  W=$HOME/lanes/sh08/wt-$c
  [ -d "$W" ] || git worktree add -q --detach "$W" "$c"
  [ -x "$W/target/release/pelt" ] || (cd "$W" && tools/fetch-toolchain > /dev/null 2>&1 && tools/build --release > /dev/null 2>&1)
  bins="$bins $W/target/release/pelt"
done
"$HOME/lanes/sh08/icount.sh" "$B" $bins
