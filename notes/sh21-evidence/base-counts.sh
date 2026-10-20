#!/bin/bash
# sh21: trunk be1a75d (no hook): the corpus and the sessions on both tiers, the counts before
set -u
S=$HOME/lanes/sh21
export TMPDIR=$S/tmp
cd $S/pelt
for t in native release; do
  tools/difftest --bin target/$t > $S/logs/base-diff-$t.log 2>&1; echo diff-$t=$?
  tools/session --bin target/$t > $S/logs/base-sess-$t.log 2>&1; echo sess-$t=$?
done
tools/clause-census > $S/logs/base-census.log 2>&1; echo census=$?
echo done
