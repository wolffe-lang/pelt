#!/bin/bash
# sh23: start a job detached, signals at their defaults, pid recorded.
# usage: launch.sh NAME CMD...   (stop it by the pid in $S/NAME.pid only)
N=$1; shift
S=$HOME/lanes/sh23
cd "$S" || exit 9
setsid -f env --default-signal bash -c 'echo $$ > "$0"; exec "$@"' "$S/$N.pid" "$@" > "$S/logs/$N.launch.log" 2>&1 < /dev/null
sleep 1
echo "pid $(cat $S/$N.pid): $(grep -E 'SigBlk|SigIgn' /proc/$(cat $S/$N.pid)/status 2>/dev/null | tr '\n\t' '  ')"
