#!/bin/bash
# sh18: start a job detached, signals at their defaults, pid recorded. usage: launch.sh NAME CMD…
N=$1; shift
S=$HOME/lanes/sh18
cd "$S" || exit 9
setsid env --default-signal "$@" > "$S/logs/$N.launch.log" 2>&1 < /dev/null &
echo $! > "$S/$N.pid"
sleep 1
echo "pid $(cat $S/$N.pid): $(grep -E 'SigBlk|SigIgn' /proc/$(cat $S/$N.pid)/status | tr '\n\t' '  ')"
