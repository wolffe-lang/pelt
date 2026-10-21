#!/bin/bash
# sh23: the fast loop: fmt, both builds, then the new cases on both tiers
# inside the container. usage: quick.sh TAG
T=$1
S=$HOME/lanes/sh23
cd $S/pelt || exit 9
export TMPDIR=$S/tmp
L=$S/logs/$T; mkdir -p $L
echo "head=$(git rev-parse --short HEAD) dirty=$(git status --porcelain | wc -l)" > $L/status
tools/check-fmt > $L/fmt.log 2>&1; echo "fmt=$?" >> $L/status
tools/build --all > $L/build.log 2>&1; echo "build=$?" >> $L/status
sha256sum target/native/pelt target/release/pelt >> $L/status
$S/ctr.sh bash -c 'for t in native release; do taskset -c 0-3 tools/difftest --bin target/$t simple > '$L'/diff-simple-$t.log 2>&1; echo "diff-simple-$t=$?"; taskset -c 0-3 tools/session --bin target/$t autocd_off autocd_list autocd_slash autocd_bare autocd_not_dir autocd_wins autocd_words autocd_hook autocd_status autocd_invoked cnf_cd cnf_skipped cnf_127 > '$L'/sess-new-$t.log 2>&1; echo "sess-new-$t=$?"; done' >> $L/status
echo done >> $L/status
