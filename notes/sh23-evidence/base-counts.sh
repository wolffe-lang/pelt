#!/bin/bash
# sh23: trunk 3b0bab9: the corpus and the sessions on both tiers inside
# the container, under taskset -c 0-3; the counts before.
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd $S/pelt
for t in native release; do mkdir -p $S/base/$t; cp $S/base/pelt-$t $S/base/$t/pelt; done
for t in native release; do
  taskset -c 0-3 tools/difftest --bin $S/base/$t > $S/logs/base-diff-$t.log 2>&1; echo diff-$t=$?
  taskset -c 0-3 tools/session --bin $S/base/$t > $S/logs/base-sess-$t.log 2>&1; echo sess-$t=$?
done
tools/clause-census > $S/logs/base-census.log 2>&1; echo census=$?
echo done
