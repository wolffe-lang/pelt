#!/bin/bash
# All children inherit CPUs12-15 and the container's private pid namespace.
set -u
S=/home/mfwolffe/lanes/sh25
cd "$S/pelt" || exit 9
ulimit -c 0
L=$S/logs/final; mkdir -p "$L"
ST=$S/logs/final.status
printf 'code_head=%s\ncpus=%s core=%s\n' "$(cat "$S/CODE_HEAD")" "$(taskset -pc $$)" "$(ulimit -c)" > "$ST"
run() {
 local name=$1; shift
 echo "$(date -Is) start $name $(uptime)" | tee -a "$ST"
 "$@" > "$L/$name.log" 2>&1 &
 local pid=$! ticks=0
 while kill -0 "$pid" 2>/dev/null; do
  sleep 1; ticks=$((ticks+1))
  if (( ticks % 60 == 0 )); then echo "$(date -Is) running $name $(uptime)"; fi
 done
 wait "$pid"; local rc=$?
 echo "$name=$rc" | tee -a "$ST"
 return "$rc"
}
run fmt tools/check-fmt
run build tools/build --all || exit 2
run test tools/check-test
run clause tools/clause-census
run width tools/gen-width --check
sha256sum target/{native,release}/pelt | tee -a "$ST"
for t in native release; do
 run diff-$t tools/difftest --bin target/$t
 run diff-$t-taskset taskset -c 12-15 tools/difftest --bin target/$t
 run sess-$t tools/session --bin target/$t
 run sess-$t-taskset taskset -c 12-15 tools/session --bin target/$t
 run self-$t tools/self-check $t
 for gate in glob-rss loop-rss exec-witness edit-witness hist-witness signal-witness; do
  run $gate-$t tools/$gate target/$t/pelt
 done
 run reap-$t tools/reap-witness target/$t
done
shape_tier() {
 local t=$1
 for pass in 1 2 3; do
  run shape-$t-$pass tools/shape-rss target/$t/pelt
  run shape-$t-$pass-taskset taskset -c 12-15 tools/shape-rss target/$t/pelt
 done
}
shape_tier native & pn=$!
shape_tier release & pr=$!
wait "$pn"; echo "shape-native-worker=$?" | tee -a "$ST"
wait "$pr"; echo "shape-release-worker=$?" | tee -a "$ST"
run diff-selftest tools/difftest-selftest target/release
run sess-selftest tools/session-selftest target/release
run oracle-check tools/oracle-record --check
for t in native release; do
 run notice-before-$t bash notes/sh25-evidence/notice5-before.sh "$S/base-bin/$t/pelt"
 run notice-$t bash notes/sh20-evidence/probe/notice5.sh "$S/pelt/target/$t/pelt"
 run notice-check-$t python3 -I notes/sh25-evidence/check-notice5.py "$L/notice-before-$t.log" "$L/notice-$t.log"
done
echo done | tee -a "$ST"
