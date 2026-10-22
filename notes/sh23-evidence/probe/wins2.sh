#!/bin/bash
# sh23: a directory named like a function, a built-in and a PATH program,
# with the option on, in the shapes that take pelt's ordinary path: the
# command with an assignment, with a redirection, and under set -x
P=$1
d=$(mktemp -d); cd "$d"; mkdir basename echo fn
printf '%s\n' 'W=$PWD' 'set -o autocd 2>/dev/null; shopt -s autocd 2>/dev/null' \
  'fn() { echo "fn ran $#"; }' \
  'cd "$W"; X=1 fn a; echo "function-assign st=$? ${PWD#"$W"}"' \
  'cd "$W"; fn a >/dev/null; echo "function-redir st=$? ${PWD#"$W"}"' \
  'cd "$W"; X=1 echo builtin; echo "builtin-assign st=$? ${PWD#"$W"}"' \
  'cd "$W"; { set -x; basename /a/b; set +x; } 2>/dev/null; echo "path-traced st=$? ${PWD#"$W"}"' \
  'exit' | taskset -c 8-11 "$P" -i 2>/dev/null | grep -vE '^\s*$|^\$ |^% '
cd /; rm -rf "$d"
