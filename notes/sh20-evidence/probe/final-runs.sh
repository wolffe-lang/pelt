#!/bin/bash
# sh20: the measurements left after the final gauntlet (logs/final.status,
# b05b0cf): the RSS split at the final head beside the pin (rss-split.sh,
# taskset -c 8-11), then the cost bench (bench/run, taskset -c 0-3, alone
# on cpus 0-3), each in the lane's container with ulimit -c 0. Started by
# launch.sh; each step's status in logs/finalruns.status.
S=$HOME/lanes/sh20
L=$S/logs
St=$L/finalruns.status
mkdir -p "$L/bench" "$L/rssgap" "$S/tmp/sh20-bench"
: > "$St"
in_ctr() { CTRDIR=$S "$S/ctr.sh" bash -c 'ulimit -c 0; exec "$@"' _ "$@"; }
echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$St"
{
  echo "# sh20: rss-split.sh at the final head b05b0cf beside the pin 0eabfaf, each binary from its build tree; the container, taskset -c 8-11, $(date -Is)"
  in_ctr taskset -c 8-11 bash "$S/probe/rss-split.sh" \
    "$S/pin/target/native/pelt" "$S/pelt/target/native/pelt" \
    "$S/pin/target/release/pelt" "$S/pelt/target/release/pelt"
} > "$L/rssgap/split-final.txt" 2>&1
echo "split=$?" >> "$St"
echo "bench-start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$St"
in_ctr python3 "$S/probe/bench/run" --dir "$S/tmp/sh20-bench" --pin 0-3 \
  dash=/usr/bin/dash pin="$S/pin/target/release/pelt" \
  pelt="$S/pelt/target/release/pelt" native="$S/pelt/target/native/pelt" \
  > "$L/bench/bench-pin0-3.txt" 2>&1
echo "bench=$?" >> "$St"
echo "end $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$St"
rm -rf "$S/tmp/sh20-bench"
echo done >> "$St"
