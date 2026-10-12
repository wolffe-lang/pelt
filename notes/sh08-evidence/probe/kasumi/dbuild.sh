#!/bin/bash
# lane-local: format check and build of the dev worktree; usage: dbuild.sh [--native|--release|--all]
cd "$HOME/lanes/sh08/dev" || exit 9
export TMPDIR=$HOME/lanes/sh08/tmp
tools/check-fmt > "$HOME/lanes/sh08/logs/dev-fmt.log" 2>&1
echo "fmt=$?"
tools/build "${1:---all}" > "$HOME/lanes/sh08/logs/dev-build.log" 2>&1
b=$?
echo "build=$b"
if [ "$b" != 0 ]; then head -60 "$HOME/lanes/sh08/logs/dev-build.log"; fi
if grep -q . "$HOME/lanes/sh08/logs/dev-fmt.log"; then head -20 "$HOME/lanes/sh08/logs/dev-fmt.log"; fi
