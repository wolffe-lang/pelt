#!/bin/bash
# sh26: after the head gauntlet, in order on CPUs 0-3: the census at the
# head (the head's tool), the coins 300 runs a shell at the pin and the
# head, the bench at the pin (inside the container), and the new cases
# against the pin's binaries (red at trunk)
set -u
S=$HOME/lanes/sh26
echo "after: start $(date -Is)"
TREE=$S/head $S/census.sh head-unaided $S/bin/head2/static/pelt
cat $S/logs/sc-head-unaided.status
TREE=$S/head $S/census.sh coins-base $S/bin/base/static/pelt --coins 300
cp $S/sc/coins.tsv $S/sc/coins-base.tsv; cat $S/logs/sc-coins-base.log | grep '^coin'
TREE=$S/head $S/census.sh coins-head $S/bin/head2/static/pelt --coins 300
cp $S/sc/coins.tsv $S/sc/coins-head.tsv; cat $S/logs/sc-coins-head.log | grep '^coin'
mkdir -p $S/pelt-bench && cp $S/head/notes/sh26-evidence/bench/* $S/pelt-bench/
$S/ctr.sh bash $S/head/notes/sh26-evidence/bench/bench.sh > $S/logs/bench-pin.txt 2>&1; tail -20 $S/logs/bench-pin.txt
CTRDIR=$S/head $S/ctr.sh bash -c 'tools/difftest --bin /home/mfwolffe/lanes/sh26/bin/base/native simple builtin option signal quote jobsctl cd printf > /home/mfwolffe/lanes/sh26/logs/red-at-pin-diff.log 2>&1; tools/session --bin /home/mfwolffe/lanes/sh26/bin/base/native c_ignoreeof c_mail mail_path mail_interval jc_assign_text > /home/mfwolffe/lanes/sh26/logs/red-at-pin-sess.log 2>&1; tools/script-census --selftest > /home/mfwolffe/lanes/sh26/logs/census-selftest-head.log 2>&1; echo "selftest=$?" >> /home/mfwolffe/lanes/sh26/logs/census-selftest-head.log'
grep -E '^FAIL|total' $S/logs/red-at-pin-diff.log; grep -E '^FAIL|^ok|session:' $S/logs/red-at-pin-sess.log; tail -2 $S/logs/census-selftest-head.log
echo "after: done $(date -Is)"
# every probe's answers under dash, bash and the pin's and the head's pelt
mkdir -p $S/logs/probe-base $S/logs/probe-head
for f in $S/probe/p[0-9]*.sh; do
  n=$(basename $f .sh)
  case $n in p16-*|p17-*|p18-*|p19-*|p23-*) continue;; esac
  $S/ctr.sh env PELT=$S/bin/base/release/pelt bash $S/probe/run.sh $f > $S/logs/probe-base/$n.txt 2>&1
  $S/ctr.sh env PELT=$S/bin/head2/release/pelt bash $S/probe/run.sh -s "pelt=$S/bin/head2/release/pelt" $f > $S/logs/probe-head/$n.txt 2>&1
done
for n in p16-ignoreeof p17-mail p18-mail-timing p19-mail-mtime p23-jobs-typed; do
  $S/ctr.sh env PELT=$S/bin/head2/release/pelt bash $S/probe/$n.sh > $S/logs/probe-head/$n.txt 2>&1
done
echo "after: probes $(date -Is)"
