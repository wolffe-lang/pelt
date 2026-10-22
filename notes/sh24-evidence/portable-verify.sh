#!/bin/bash
set -u
S=$(cd "$(dirname "$0")" && pwd)
ulimit -c 0
St=$S/logs/portable.status
: > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$S/logs/portable-$n.log" 2>&1 &
  local p=$! tick=0
  while kill -0 "$p" 2>/dev/null; do
    sleep 1; tick=$((tick+1))
    if ((tick %60==0)); then echo "running $n $(uptime)"; fi
  done
  wait "$p"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
cd "$S/portable" || exit 9
run head-build tools/build --all || exit 2
cd "$S/portable-base" || exit 9
run base-build tools/build --all || exit 2
cd "$S/portable" || exit 9
run oracle-record tools/oracle-record builtin/write_full jobs/write_failure
for t in native release; do
  run base-red-$t tools/difftest --bin "$S/portable-base/target/$t" builtin/write_full jobs/write_failure
  run head-targeted-$t tools/difftest --bin target/$t builtin/write_full jobs/write_failure
  run diff-$t tools/difftest --bin target/$t
  run diff-$t-taskset taskset -c 8-11 tools/difftest --bin target/$t
done
run oracle-check tools/oracle-record --check
sha256sum target/{native,release}/pelt >> "$St"
echo done >> "$St"
