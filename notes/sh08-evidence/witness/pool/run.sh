#!/bin/bash
cd "$HOME/lanes/sh08/probe/pool" || exit 9
W=$HOME/lanes/sh08/dev/.wolf-bin/wolf
"$W" build --release main.lu -o p-release > build.log 2>&1 || { echo build-release failed; cat build.log; exit 1; }
"$W" build main.lu -o p-native >> build.log 2>&1 || { echo build-native failed; cat build.log; exit 1; }
for t in native release; do for s in pool fresh; do for n in 1000000 2000000; do
  /usr/bin/time -f %M -o t.out ./p-$t $s $n > o.out; echo "$t $s $n peak_kb $(cat t.out) out $(cat o.out)"
done; done; done
