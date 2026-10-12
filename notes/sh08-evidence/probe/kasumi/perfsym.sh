#!/bin/bash
# lane-local: where user instructions go in a 100,000-turn loop of BODY (perf record, by symbol). usage: perfsym.sh BODY BIN
cd "$HOME/lanes/sh08/tmp" || exit 9
{ echo 'f() { :; }'; echo 'i=0'; echo 'while [ $i -lt 100000 ]; do'; echo "$1"; echo 'i=$((i+1)); done'; } > ps.$$.sh
env -i PATH=/usr/bin:/bin HOME=/ LC_ALL=C perf record -q -e instructions:u -o ps.$$.data "$2" ps.$$.sh > /dev/null 2>&1
perf report -i ps.$$.data --stdio --sort symbol 2>/dev/null | grep -v "^#" | grep -v "^$" | head -${3:-25}
rm -f ps.$$.data
