#!/bin/bash
# census.sh — lane-local (sh22): tools/syscall-census over the whole
# corpus, trunk's tree (its harness and its pelt) and then the head's,
# inside ctr.sh; after each, every process left in the container is
# listed and then ended by its pid (they are the container's). The head
# is taken again with the sessions.
# usage: census.sh OUT TRUNK_TREE HEAD_TREE
O=$1; B=$2; H=$3; mkdir -p "$O"
left() {
  ps -eo pid=,ppid=,stat=,args= | awk -v me=$$ '$1 != 1 && $1 != me && $2 != me' | grep -v -E ' (ps|awk|grep) ' > "$O/left-$1.txt"
  echo "census.sh: left after $1: $(wc -l < "$O/left-$1.txt")"
  cat "$O/left-$1.txt"
  for p in $(awk '{print $1}' "$O/left-$1.txt"); do kill -9 "$p" 2>/dev/null; done
}
for tag in trunk head; do
  T=$B; [ $tag = head ] && T=$H
  echo "== $tag ($T), the corpus under strace"
  "$T/tools/syscall-census" "$T/target/release" "$O/$tag" --no-session
  echo "exit $?"
  left "$tag"
done
echo "== head, the corpus and the sessions under strace"
"$H/tools/syscall-census" "$H/target/release" "$O/head-all"
echo "exit $?"
left head-all
