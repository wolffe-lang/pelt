#!/bin/bash
S=/home/mfwolffe/lanes/sh22
echo "== trunk harness, trunk pelt (release)"
$S/snaps/reap-oldharness/tools/reap-witness $S/snaps/reap-oldharness/target/release; echo exit $?
echo "== head harness, head pelt (native)"
$S/snaps/reap-head/tools/reap-witness $S/snaps/reap-head/target/native; echo exit $?
echo "== head harness, head pelt (release)"
$S/snaps/reap-head/tools/reap-witness $S/snaps/reap-head/target/release; echo exit $?
echo "== processes in the container now:"; ps -eo pid=,ppid=,stat=,args= | grep -v -E "ps -eo|grep"
