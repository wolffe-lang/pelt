#!/bin/bash
# sh18: pelt's own system calls over the corpus and the sessions, the
# bare pin's static build against the head's (tools/syscall-census)
set -u
S=$HOME/lanes/sh18
L=$S/logs
H=${1:-head4}
until grep -q ^done $L/$H.status 2>/dev/null; do sleep 30; done
export TMPDIR=$S/tmp
cd $S/pin && tools/syscall-census target/static $S/sysc/pin > $L/sysc-pin.log 2>&1; echo "pin=$?" > $L/sysc.status
cd $S/head && tools/syscall-census target/static $S/sysc/head > $L/sysc-head.log 2>&1; echo "head=$?" >> $L/sysc.status
echo done >> $L/sysc.status
