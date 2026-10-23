#!/bin/bash
set -u
S=/home/mfwolffe/lanes/sh25
cd "$S/pelt" || exit 9
ulimit -c 0
run() { local n=$1; shift; echo "$(date -Is) $n $(uptime)"; "$@" > "$S/logs/$n.log" 2>&1; local rc=$?; echo "$n=$rc" | tee -a "$S/logs/baseline.status"; return "$rc"; }
: > "$S/logs/baseline.status"
run base-build taskset -c 12-15 tools/build --all || exit 2
mkdir -p "$S/base-bin/native" "$S/base-bin/release"
cp target/native/pelt "$S/base-bin/native/"
cp target/release/pelt "$S/base-bin/release/"
sha256sum "$S"/base-bin/{native,release}/pelt
for t in native release; do
 run base-cases-$t taskset -c 12-15 tools/difftest --bin target/$t pwd cd printf
 for pass in 1 2 3; do
  run base-shape-$t-$pass taskset -c 12-15 tools/shape-rss --only fork-background-subshell target/$t/pelt
  run base-shape-$t-$pass-bare tools/shape-rss --only fork-background-subshell target/$t/pelt
 done
done
run base-notice5 taskset -c 12-15 bash notes/sh20-evidence/probe/notice5.sh /usr/bin/dash
run oracles taskset -c 12-15 bash notes/sh25-evidence/oracles.sh
echo done | tee -a "$S/logs/baseline.status"
