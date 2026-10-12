#!/bin/bash
cd "$HOME/lanes/sh08/probe/emptystr" || exit 9
W=$HOME/lanes/sh08/dev/.wolf-bin/wolf
"$W" build --release main.lu -o es-release > build.log 2>&1 || { echo build-release failed; cat build.log; exit 1; }
"$W" build main.lu -o es-native >> build.log 2>&1 || { echo build-native failed; cat build.log; exit 1; }
for t in native release; do for s in none via infn infnshort short; do for n in 1000000 2000000; do
  /usr/bin/time -f %M -o t.out ./es-$t $s $n > o.out; echo "$t $s $n peak_kb $(cat t.out) out $(cat o.out)"
done; done; done
