#!/bin/bash
# sh22: start a job detached (setsid -f), signals at their defaults, its
# pid recorded. usage: launch.sh NAME CMD...  (stopped by the pid in
# $S/NAME.pid only, never by name, pattern or group)
N=$1; shift
S=$HOME/lanes/sh22
cd "$S" || exit 9
rm -f "$S/$N.pid"
setsid -f bash -c 'p=$0; l=$1; shift; echo $$ > "$p"; exec env --default-signal "$@" > "$l" 2>&1 < /dev/null' \
  "$S/$N.pid" "$S/logs/$N.launch.log" "$@"
sleep 1
P=$(cat "$S/$N.pid" 2>/dev/null)
echo "pid $P: $(grep -E 'SigBlk|SigIgn' /proc/$P/status 2>/dev/null | tr '\n\t' '  ')"
