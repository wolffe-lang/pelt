#!/bin/bash
# sh20: the final head\x27s table, syscall census and probes, on cpus 8-15 (inside ctr.sh)
S=/home/mfwolffe/lanes/sh20
ulimit -c 0
taskset -c 8-15 bash $S/probe/table.sh $S/logs/table-head $S/pelt $S/pin
echo table-done >> $S/logs/after.status
cd $S/pelt
for t in pin head; do b=$S/pin/target/release; [ $t = head ] && b=$S/pelt/target/release; taskset -c 8-15 tools/syscall-census $b $S/logs/census/$t --no-session > $S/logs/census/$t.log 2>&1; echo "census-$t=$?" >> $S/logs/after.status; done
taskset -c 8-15 bash $S/probe/head-probes.sh $S/pelt $S/logs/probe/final > $S/logs/probe/final/run.log 2>&1
echo "probes=$?" >> $S/logs/after.status
echo done >> $S/logs/after.status
