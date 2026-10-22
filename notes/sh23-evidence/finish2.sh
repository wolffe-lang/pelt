#!/bin/bash
# sh23: after autocd_wins gained the ordinary path's rows (93561ad): plants
# B5 and B6 again at that head (plant.sh, quick), then gauntlet g2 there.
# Progress in logs/finish2.status. usage: finish2.sh
S=$HOME/lanes/sh23
L=$S/logs; St=$L/finish2.status
export TMPDIR=$S/tmp
: > "$St"
for n in b5-found b6-first; do
  HEAD=93561ad69b41aec9735cd272984b7615c79b1ad2 bash "$S/plant.sh" $n-rows "$S/plants/$n.patch" quick
  echo "plant-$n-rows=$(tr '\n' ' ' < $L/plant-$n-rows/status)" >> "$St"
done
git -C "$S/pelt" worktree remove --force "$S/plant-wt"; echo "wt-removed=$?" >> "$St"
bash "$S/gauntlet.sh" g2; echo "g2=$(tr '\n' ' ' < $L/g2.status)" >> "$St"
echo done >> "$St"
