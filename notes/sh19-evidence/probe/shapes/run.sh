#!/bin/bash
# sh19 #34: shapes.sh under a pelt ($1) and, on linux in the container,
# dash and bash --posix; the endless producer under a 3-second limit.
D=$(cd "$(dirname "$0")" && pwd); P=$1; O=$2; mkdir -p "$O"
# a 3-second limit: timeout(1) where there is one, else perl's alarm
# (macOS has no timeout); either ends the run by SIGALRM or SIGTERM
limit() { if command -v timeout >/dev/null 2>&1; then timeout 3 "$@"; else perl -e 'alarm 3; exec @ARGV' "$@"; fi; }
one() { name=$1; shift
  "$@" "$D/shapes.sh" > "$O/shapes.$name.txt" 2>&1; echo "exit=$?" >> "$O/shapes.$name.txt"
  limit "$@" -c 'while :; do echo y; done | head -n 1' > "$O/endless.$name.txt" 2>&1; echo "exit=$?" >> "$O/endless.$name.txt"
}
one pelt "$P"
if [ -x "$HOME/lanes/sh19/refrun.sh" ]; then
  one dash "$HOME/lanes/sh19/refrun.sh" dash
  one bash "$HOME/lanes/sh19/refrun.sh" bash --posix
fi
