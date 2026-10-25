#!/bin/bash
# sh26: the gauntlet inside the container. usage: gauntlet.sh TAG [quick]
# Builds both tiers and the static one from the tree at $S/pelt, keeps
# the binaries under $S/bin/TAG, and runs what CI's linux leg runs; each
# step's log under $S/logs/TAG, the statuses in $S/logs/TAG.status.
set -u
T=$1; MODE=${2:-full}
S=/home/mfwolffe/lanes/sh26
cd "${TREE:-$S/pelt}" || exit 9
ulimit -c 0
L=$S/logs/$T; mkdir -p "$L"
ST=$S/logs/$T.status
printf 'tag=%s head=%s dirty=%s\ncpus=%s core=%s\n' "$T" "$(git rev-parse HEAD)" "$(git status --porcelain | wc -l)" "$(taskset -pc $$)" "$(ulimit -c)" > "$ST"
run() {
 local name=$1; shift
 echo "$(date -Is) start $name $(cut -d' ' -f1-3 /proc/loadavg)" | tee -a "$ST"
 "$@" > "$L/$name.log" 2>&1 &
 local pid=$! ticks=0
 while kill -0 "$pid" 2>/dev/null; do
  sleep 1; ticks=$((ticks+1))
  if (( ticks % 120 == 0 )); then echo "$(date -Is) running $name ${ticks}s"; fi
 done
 wait "$pid"; local rc=$?
 echo "$name=$rc $(tail -n 1 "$L/$name.log" | cut -c1-200)" | tee -a "$ST"
 return "$rc"
}
run fmt tools/check-fmt
run build tools/build --all || { echo "build failed" | tee -a "$ST"; exit 2; }
run build-static tools/build --static
mkdir -p "$S/bin/$T"
for t in native release static; do mkdir -p "$S/bin/$T/$t"; cp -f target/$t/pelt "$S/bin/$T/$t/pelt" 2>/dev/null; done
sha256sum "$S"/bin/$T/*/pelt | tee -a "$ST"
run test tools/check-test
run clause tools/clause-census
for t in native release; do
 run diff-$t tools/difftest --bin target/$t
 run sess-$t tools/session --bin target/$t
done
if [ "$MODE" = full ]; then
 run width tools/gen-width --check
 for t in native release; do
  run self-$t tools/self-check $t
  for gate in glob-rss loop-rss exec-witness edit-witness hist-witness signal-witness; do
   run $gate-$t tools/$gate target/$t/pelt
  done
  run reap-$t tools/reap-witness target/$t
  run shape-$t tools/shape-rss target/$t/pelt
 done
 run diff-selftest tools/difftest-selftest target/release
 run sess-selftest tools/session-selftest target/release
 run oracle-check tools/oracle-record --check
fi
echo "done $(date -Is)" | tee -a "$ST"
