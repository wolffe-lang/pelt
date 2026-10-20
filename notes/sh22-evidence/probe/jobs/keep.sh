#!/bin/bash
# jobs/keep.sh — lane-local (sh22): how many of N unwaited jobs `jobs`
# lists after a loop (both shells keep them all), and whether the shell
# can still start a program when the container's pids limit (CTRPIDS)
# is below N: the count of "cannot" lines on standard error. Inside
# ctr.sh. usage: keep.sh N SHELL...
N=$1; shift
W=$TMPDIR/keep.$$; mkdir -p "$W"; cd "$W" || exit 9
echo "pids limit: $(cat /sys/fs/cgroup/pids.max 2>/dev/null)"
for sh in "$@"; do
  for body in 'env true &' 'true &'; do
    { echo 'i=0'; echo "while [ \$i -lt $N ]; do $body i=\$((i+1)); done"; echo 'sleep 0.5'
      echo 'jobs > j.txt'; echo 'echo "listed $(wc -l < j.txt)"'; } > s.sh
    out=$("$sh" s.sh 2> e.txt); rc=$?
    echo "keep: $(basename "$sh") [$body] x $N: $out, exit $rc, stderr lines $(wc -l < e.txt), first: $(head -1 e.txt)"
  done
done
cd / && rm -rf "$W"
