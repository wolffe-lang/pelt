#!/bin/bash
# shapes — lane-local (sh08): peak RSS (KB) of a shell over loops whose body is one construct,
# at N and 4N turns, and over long scripts of N and 4N lines. usage: shapes.sh SHELL [N]
P=$1; N=${2:-5000}
D=$HOME/lanes/sh08/tmp/shapes.$$; mkdir -p "$D"; cd "$D" || exit 1
rss() { /usr/bin/time -f '%M' -o t.out "$@" > o.out 2> e.out; echo "$(tail -1 t.out) out=$(tail -c 20 o.out | tr '\n' ' ') err=$(wc -c < e.out)"; }
for body in 'true' 'true | true' 'echo x | cat >/dev/null' 'x=$(true)' 'x=$(echo y)' 'x=`true`' 'f' 'g a b' '( true )' '{ true; }' 'true && true' 'if true; then :; fi' 'case a in a) :;; esac' 'x=$(echo a | cat)' 'for j in 1; do :; done' 'true &'; do
  for n in $N $((4*N)); do
    { echo 'f() { :; }'; echo 'g() { local v; v=$1; return 0; }'; echo 'i=0'
      echo "while [ \$i -lt $n ]; do $body; i=\$((i+1)); done"; echo 'wait; echo $i'; } > l.sh
    echo "loop $n [$body]: kb $(rss "$P" l.sh)"
  done
done
for line in 'true' 'true | true' 'x=$(true)' 'f' ': $((i=i+1))'; do
  for n in $N $((4*N)); do
    { echo 'f() { :; }'; k=0; while [ $k -lt $n ]; do echo "$line"; k=$((k+1)); done; echo 'echo done'; } > s.sh
    echo "script $n [$line]: kb $(rss "$P" s.sh)"
  done
done
cd / && rm -rf "$D"
