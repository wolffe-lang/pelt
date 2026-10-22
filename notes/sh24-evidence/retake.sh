#!/bin/bash
# sh24: coordinator's load ruling; no timeout or assertion changes.
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/head" || exit 9
ulimit -c 0
for t in native release; do
  for mode in bare four; do
    while ! awk '{exit !($1 < 16)}' /proc/loadavg; do
      echo "$(date -Is) waiting for load below16: $(uptime)"
      sleep 60
    done
    echo "$(date -Is) retake tier=$t mode=$mode $(uptime)"
    log="$S/logs/retake-times-$t-$mode.log"
    uptime > "$log"
    if [ "$mode" = four ]; then
      taskset -c 8-11 tools/difftest --bin target/$t builtin/c_times_real >> "$log" 2>&1
    else
      tools/difftest --bin target/$t builtin/c_times_real >> "$log" 2>&1
    fi
    rc=$?
    cat "$log"
    echo "retake tier=$t mode=$mode exit=$rc"
  done
done
