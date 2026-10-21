#!/bin/bash
# sh20: the probes of a built tree, inside ctr.sh: sh19's shapes probe and
# the child-state probe under pelt (both tiers) beside dash; the five
# shapes on the checked machine (`conform-run --checked`) and lupin's
# answer; the threads of the shell and of a forked child.
# usage: head-probes.sh TREE OUT (both absolute)
TREE=$1; OUT=$2
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
ulimit -c 0
cd "$TMPDIR" || exit 9
P=( "dash=/usr/bin/dash" "pelt-native=$TREE/target/native/pelt" "pelt-release=$TREE/target/release/pelt" )
for e in "${P[@]}"; do
  n=${e%%=*}; s=${e#*=}
  { "$s" "$D/shapes.sh"; echo "exit=$?"; } > "$OUT/shapes.$n.txt" 2>&1
  { "$s" "$D/checked.sh"; echo "exit=$?"; } > "$OUT/checked.$n.txt" 2>&1
  bash "$D/childstate-run.sh" "$s" "$OUT/childstate.$n.txt"
done
W=$TREE/.wolf-bin
{
  echo "# $W/wolf conform-run --json --checked src/pelt.lu < checked.sh ($($W/wolf --version | head -1))"
  (cd "$TREE" && "$W/wolf" conform-run --json --checked src/pelt.lu < "$D/checked.sh")
  echo "exit $?"
  echo "# $W/lupin run --json --std-root .wolf-bin/std src/pelt.lu ($($W/lupin --version | head -1)) < /dev/null"
  (cd "$TREE" && "$W/lupin" run --json --std-root .wolf-bin/std src/pelt.lu < /dev/null)
  echo "exit $?"
} > "$OUT/machines.txt" 2>&1
cat > threads.sh <<'T'
echo "shell threads: $(ls /proc/$$/task | wc -l)"
( p=$(sh -c 'echo $PPID'); echo "forked child threads: $(ls /proc/$p/task | wc -l)"; : )
trap 'echo usr1' USR1
( p=$(sh -c 'echo $PPID'); echo "forked child threads with a trap set: $(ls /proc/$p/task | wc -l)"; : )
T
for e in "${P[@]}"; do
  n=${e%%=*}; s=${e#*=}
  { echo "## $n"; "$s" ./threads.sh; } >> "$OUT/threads.txt" 2>&1
done
echo probes-done
