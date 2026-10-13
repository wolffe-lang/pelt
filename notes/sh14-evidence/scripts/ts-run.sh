#!/bin/bash
# sh14: ts.sh 300 times under each shell; how often the first look already sees the second file newer.
S=$HOME/lanes/sh14
cd "$S/probe" || exit 9
mkdir -p ts-w && cd ts-w || exit 9
for pair in dash=/usr/bin/dash base=$S/sc/pelt-base pin=$S/sc/pelt-pin head=$S/sc/pelt-head dash-again=/usr/bin/dash head-again=$S/sc/pelt-head base-again=$S/sc/pelt-base; do
  n=${pair%%=*}; sh=${pair#*=}
  one=0; two=0; more=0
  for i in $(seq 300); do
    r=$(env -i PATH=/usr/bin:/bin "$sh" ../ts.sh)
    case $r in 1) one=$((one+1));; 2) two=$((two+1));; *) more=$((more+1));; esac
  done
  echo "$n: first look newer (0.1) $one, second (0.2) $two, later $more of 300; load $(cut -d' ' -f1 /proc/loadavg)"
done
