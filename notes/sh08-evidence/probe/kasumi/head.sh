#!/bin/bash
# sh08: the gauntlet at the branch head, in its own worktree (the checkout runs the baseline census)
set -u
W=$HOME/lanes/sh08/wt-$1
cd "$HOME/lanes/sh08/pelt" || exit 9
git fetch -q origin
if [ -d "$W" ]; then (cd "$W" && git checkout -q --detach origin/sh08); else git worktree add -q --detach "$W" origin/sh08; fi
"$HOME/lanes/sh08/gauntlet.sh" "$1" "$W"
echo finished > "$HOME/lanes/sh08/logs/$1.done"
