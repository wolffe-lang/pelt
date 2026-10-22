#!/bin/bash
# sh23: where an interactive shell is inside a pipeline stage, a { } group
# in a pipe, eval and a function body, with autocd on (each row prints the
# directory from inside the context)
P=$1
d=$(mktemp -d); cd "$d"; mkdir sub
printf '%s\n' 'W=$PWD' 'set -o autocd 2>/dev/null; shopt -s autocd 2>/dev/null' \
  '{ sub 2>/dev/null; echo "group-in-pipe [${PWD#$W}]"; } | cat' 'cd "$W"' \
  'sub 2>/dev/null | cat; echo "simple-stage-after [${PWD#$W}]"' 'cd "$W"' \
  'echo x | { sub 2>/dev/null; echo "last-stage [${PWD#$W}]"; }' 'cd "$W"' \
  'eval sub 2>/dev/null; echo "eval [${PWD#$W}]"' 'cd "$W"' \
  'f() { sub 2>/dev/null; echo "fn [${PWD#$W}]"; }; f' 'cd "$W"' \
  '(cd .; sub 2>/dev/null; echo "paren-two [${PWD#$W}]")' 'cd "$W"' \
  'exit' | taskset -c 8-11 "$P" -i 2>/dev/null | grep -E '^[a-z-]+ \['
cd /; rm -rf "$d"
