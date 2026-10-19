#!/bin/bash
# sh19 probe: each script under dash, bash --posix (in the container,
# by refrun.sh) and a pelt binary given as $1 (on the host).
D=$(cd "$(dirname "$0")" && pwd)
P=$1; O=$2; mkdir -p "$O"
for s in "$D"/w*.sh; do
  b=$(basename "$s" .sh)
  "$HOME/lanes/sh19/refrun.sh" dash "$s" > "$O/$b.dash.txt" 2>&1; echo "exit=$?" >> "$O/$b.dash.txt"
  "$HOME/lanes/sh19/refrun.sh" bash --posix "$s" > "$O/$b.bash.txt" 2>&1; echo "exit=$?" >> "$O/$b.bash.txt"
  "$P" "$s" > "$O/$b.pelt.txt" 2>&1; echo "exit=$?" >> "$O/$b.pelt.txt"
done
