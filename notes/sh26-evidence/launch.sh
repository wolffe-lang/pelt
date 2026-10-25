#!/bin/bash
# sh26: start a job detached (setsid -f), signals at their defaults, its
# pid recorded; an exit marker when it ends. usage: launch.sh NAME CMD...
# (stopped by the pid in $S/NAME.pid only, never by name, pattern or group)
N=$1; shift
S=$HOME/lanes/sh26
cd "$S" || exit 9
rm -f "$S/$N.pid" "$S/$N.exit"
setsid -f bash -c 'p=$0; l=$1; x=$2; shift 2; echo $$ > "$p"; env --default-signal "$@" > "$l" 2>&1 < /dev/null; echo $? > "$x"' \
  "$S/$N.pid" "$S/logs/$N.log" "$S/$N.exit" "$@" < /dev/null > /dev/null 2>&1
sleep 1
P=$(cat "$S/$N.pid" 2>/dev/null)
echo "pid $P: $(grep -E 'SigBlk|SigIgn' /proc/$P/status 2>/dev/null | tr '\n\t' '  ')"
