#!/bin/bash
# sh20: peak RSS at 10,000 and 20,000 turns of a compound command with a
# redirection, each shape a loop body (inside ctr.sh). The shapes that
# run in the shell keep ~690 B a turn at trunk and at the head; a
# redirected subshell forks since sh20 and keeps what a fork does.
# usage: compound-redir-rss.sh SH
SH=$1
T=${TMPDIR:-/tmp}/sh20-crr.$$
mkdir -p "$T"
for shape in "( true ) >/dev/null" "{ true; } >/dev/null" "( true; true ) >/dev/null" \
             "if true; then :; fi >/dev/null" "while false; do :; done >/dev/null" "true >/dev/null"; do
  for n in 10000 20000; do
    printf 'i=0\nwhile [ $i -lt %s ]; do %s; i=$((i+1)); done\n' "$n" "$shape" > "$T/l$n.sh"
    eval "kb$n=\$( { /usr/bin/time -f %M \"\$SH\" \"\$T/l$n.sh\"; } 2>&1 >/dev/null | tail -1)"
  done
  echo "$shape: $kb10000 -> $kb20000 KB, $(( (kb20000 - kb10000) * 1024 / 10000 )) B a turn"
done
rm -rf "$T"
