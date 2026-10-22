#!/bin/bash
# sh23: the status of a command substitution whose command names a
# directory, with autocd on, in an interactive shell
P=$1
d=$(mktemp -d); cd "$d"; mkdir sub
printf '%s\n' 'W=$PWD' 'set -o autocd 2>/dev/null; shopt -s autocd 2>/dev/null' \
  'x=$(sub 2>/dev/null); echo "cs-bare st=$? [$x] [${PWD#$W}]"' \
  'x=$(./sub 2>/dev/null); echo "cs-slash st=$? [$x] [${PWD#$W}]"' \
  'exit' | taskset -c 8-11 "$P" -i 2>/dev/null | grep -E '^cs-'
cd /; rm -rf "$d"
