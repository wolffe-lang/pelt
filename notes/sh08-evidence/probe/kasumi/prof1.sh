#!/bin/bash
# lane-local: heapprof of the dev native build over a 3000-turn loop of one body. usage: prof1.sh BODY
cd "$HOME/lanes/sh08/tmp" || exit 9
{ echo 'f() { :; }'; echo 'g() { local v; v=$1; return 0; }'; echo 'i=0'; echo 'while [ $i -lt ${2:-3000} ]; do'; echo "$1"; echo 'i=$((i+1)); done'; } > p1.sh
TMPDIR=$PWD timeout 900 python3 ../probe/heapprof.py ../dev/target/native/pelt p1.sh 3 | sed -n '1p;/innermost four/,/on the stack/p' | head -16
