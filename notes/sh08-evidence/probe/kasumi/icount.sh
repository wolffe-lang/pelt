#!/bin/bash
# lane-local: user instructions per turn of a 100,000-turn loop of one body, for each binary. usage: icount.sh BODY BIN…
B=$1; shift
cd "$HOME/lanes/sh08/tmp" || exit 9
{ echo 'f() { :; }'; echo 'i=0'; echo 'while [ $i -lt 100000 ]; do'; echo "$B"; echo 'i=$((i+1)); done'; } > ic.sh
{ echo 'f() { :; }'; echo 'i=0'; echo 'while [ $i -lt 100000 ]; do'; echo 'i=$((i+1)); done'; } > ic0.sh
for b in "$@"; do
  n=$(env -i PATH=/usr/bin:/bin HOME=/ LC_ALL=C perf stat -x, -e instructions:u "$b" ic.sh 2>&1 >/dev/null | grep instructions | cut -d, -f1)
  z=$(env -i PATH=/usr/bin:/bin HOME=/ LC_ALL=C perf stat -x, -e instructions:u "$b" ic0.sh 2>&1 >/dev/null | grep instructions | cut -d, -f1)
  echo "$b [$B]: $(( (n - z) / 100000 )) instructions a turn (the bare loop $(( z / 100000 )))"
done
