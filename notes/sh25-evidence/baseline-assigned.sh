#!/bin/bash
# Repeat trunk's instrument and binaries with every leg confined to12–15.
set -u
S=/home/mfwolffe/lanes/sh25
cd "$S/pelt" || exit 9
ulimit -c 0
ST=$S/logs/baseline-assigned.status
printf 'cpus=%s core=%s\n' "$(taskset -pc $$)" "$(ulimit -c)" > "$ST"
for tier in native release; do
 for p in 1 2 3; do
  for mode in bare taskset; do
   echo "$(date -Is) $tier/$p/$mode $(uptime)" | tee -a "$ST"
   cmd=(tools/shape-rss-base --only fork-background-subshell "$S/base-bin/$tier/pelt")
   if [ "$mode" = taskset ]; then cmd=(taskset -c 12-15 "${cmd[@]}"); fi
   "${cmd[@]}" > "$S/logs/base-assigned-$tier-$p-$mode.log" 2>&1
   echo "$tier-$p-$mode=$?" | tee -a "$ST"
  done
 done
done
echo done | tee -a "$ST"
