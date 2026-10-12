#!/bin/bash
# lane-local: build pelt at each named commit (release) and run loop-rss -n 20000 on it. usage: bisect.sh SHA…
cd "$HOME/lanes/sh08/pelt" || exit 9
git fetch -q origin
export TMPDIR=$HOME/lanes/sh08/tmp
for c in "$@"; do
  W=$HOME/lanes/sh08/wt-$c
  [ -d "$W" ] || git worktree add -q --detach "$W" "$c"
  (cd "$W" && tools/fetch-toolchain > /dev/null 2>&1 && tools/build --release > /dev/null 2>&1) || { echo "$c build failed"; continue; }
  echo "== $c $(git log --format=%s -1 $c)"
  "$W/tools/loop-rss" -n 20000 "$W/target/release/pelt" | tail -1
done
