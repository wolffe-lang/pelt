#!/bin/bash
# reap/leak.sh — lane-local (sh22): pelt#27 seen black-box at trunk, inside
# ctr.sh (its own pid namespace). A one-case corpus whose case times out
# (pelt blocks opening a FIFO nobody writes, with a child of its own
# asleep), run by tools/syscall-census and by tools/difftest alone; after
# each, every process left in the container is listed. Then this script
# ends what it listed, by pid (they are the container's).
# usage: leak.sh PELT_TREE BIN_DIR OUT
T=$1; B=$2; O=$3; mkdir -p "$O"
C=$O/corpus; rm -rf "$C"; mkdir -p "$C/hang"
printf 'probe: sh22 leak\n' > "$C/ORACLE"
printf 'none\n' > "$C/PENDING.md"
cat > "$C/hang/c_fifo.sh" <<'S'
sleep 300 &
mkfifo f
: < f
S
printf 'exit=0\nstderr=no\n' > "$C/hang/c_fifo.meta"
: > "$C/hang/c_fifo.out"
left() {
  echo "-- processes left after $1 (but this script's own):"
  ps -eo pid=,ppid=,pgid=,stat=,args= | awk -v me=$$ '$1 != me && $2 != me && $1 != 1'
}
echo "== tools/syscall-census, the one case"
PELT_DIFF_DIR=$C "$T/tools/syscall-census" "$B" "$O/sysc" --no-session
echo "exit $?"
grep -E 'FAIL|total' "$O/sysc/difftest-under-strace.log"
left syscall-census | tee "$O/left-census.txt"
for p in $(awk '{print $1}' "$O/left-census.txt" | grep -E '^[0-9]+$'); do kill -9 "$p" 2>/dev/null && echo "ended $p"; done
sleep 1
echo "== tools/difftest alone, the one case"
PELT_DIFF_DIR=$C "$T/tools/difftest" --bin "$B"
echo "exit $?"
left difftest | tee "$O/left-difftest.txt"
for p in $(awk '{print $1}' "$O/left-difftest.txt" | grep -E '^[0-9]+$'); do kill -9 "$p" 2>/dev/null && echo "ended $p"; done
