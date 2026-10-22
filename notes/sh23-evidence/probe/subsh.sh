#!/bin/bash
# sh23: where an interactive shell is inside ( ), $( ) and a pipeline stage with autocd on
P=$1
d=$(mktemp -d); cd "$d"; mkdir sub
printf '%s\n' 'W=$PWD' 'set -o autocd 2>/dev/null; shopt -s autocd 2>/dev/null' '(sub 2>/dev/null; echo "in-sub [${PWD#$W}]"); echo "after [${PWD#$W}]"' 'echo "cs [$(sub 2>/dev/null; echo "${PWD#$W}")]"' 'sub 2>/dev/null | cat; echo "pipe-after [${PWD#$W}]"' 'exit' | taskset -c 8-11 "$P" -i 2>/dev/null | grep -E '^(in-sub|after|cs|pipe)'
cd /; rm -rf "$d"
