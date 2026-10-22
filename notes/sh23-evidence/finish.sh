#!/bin/bash
# sh23: what remained at the pause, in one detached job (launch.sh): the
# cost (cost.sh) and lope's session with the hook (autocd-jump.py) on a
# quiet kasumi with the head's binaries (copied aside from g1's build, the
# shas checked against logs/g1.status), then the plants (plant.sh).
# Progress in logs/finish.status. usage: finish.sh
S=$HOME/lanes/sh23
L=$S/logs; St=$L/finish.status
export TMPDIR=$S/tmp
: > "$St"
mkdir -p "$S/bins/head/native" "$S/bins/head/release"
for t in native release; do cp "$S/pelt/target/$t/pelt" "$S/bins/head/$t/pelt"; done
for t in native release; do
  h=$(sha256sum "$S/bins/head/$t/pelt" | cut -d' ' -f1)
  grep -q "^$h  target/$t/pelt" "$L/g1.status" && echo "head-$t=$h g1" >> "$St" || { echo "head-$t=$h NOT g1's" >> "$St"; exit 3; }
done
echo "uptime before cost: $(uptime)" >> "$St"
"$S/ctr.sh" bash "$S/cost.sh" "$S/bins/head" "$S/cost/head" > "$L/cost-head.log" 2>&1; echo "cost-head=$?" >> "$St"
"$S/ctr.sh" bash "$S/cost.sh" "$S/base" "$S/cost/trunk" > "$L/cost-trunk.log" 2>&1; echo "cost-trunk=$?" >> "$St"
for set in head trunk; do
  d=$S/bins/$set; [ $set = trunk ] && d=$S/base
  mkdir -p "$L/jump/$set"
  for m in on off; do
    "$S/ctr.sh" env JUMP_LOGS="$L/jump/$set" python3 -I "$S/autocd-jump.py" "$S/lope" "$S/lope/target/release/lope" $m "$d/native/pelt" "$d/release/pelt" > "$L/jump/$set/rows-$m.txt" 2>&1
    echo "jump-$set-$m=$?" >> "$St"
  done
done
P=$S/plants
bash "$S/plant.sh" a "$P/a-trunk-src.patch" full; echo "plant-a=$(tr '\n' ' ' < $L/plant-a/status)" >> "$St"
bash "$S/plant.sh" b "$P/b.patch" full; echo "plant-b=$(tr '\n' ' ' < $L/plant-b/status)" >> "$St"
for n in b1-option b2-interactive b3-isdir b4-hook b5-found b6-first; do
  bash "$S/plant.sh" $n "$P/$n.patch" quick; echo "plant-$n=$(tr '\n' ' ' < $L/plant-$n/status)" >> "$St"
done
git -C "$S/pelt" worktree remove --force "$S/plant-wt"; echo "wt-removed=$?" >> "$St"
echo done >> "$St"
