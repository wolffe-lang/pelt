#!/bin/bash
# sh08: tools/bench, trunk (base) against the head, release and native tiers; then user instructions per script.
set -u
S=$HOME/lanes/sh08
export TMPDIR=$S/tmp
B=$S/bench
H=${1:-$S/head}
mkdir -p "$B/bin"; : > "$B/status"
cp "$S/bin/base-release" "$B/bin/base-release"; cp "$S/bin/base-native" "$B/bin/base-native"
cp "$S/bin/trunk2-release" "$B/bin/trunk-release"; cp "$S/bin/trunk2-native" "$B/bin/trunk-native"
cp "$H/target/release/pelt" "$B/bin/head-release"; cp "$H/target/native/pelt" "$B/bin/head-native"
{ echo "head $(git -C "$H" rev-parse HEAD)"; sha256sum "$B"/bin/*; } > "$B/heads"
rm -rf "$B/tool"; cp -r "$H/tools/bench" "$B/tool"
python3 "$B/tool/gen-configure-shaped" 1200 > "$B/tool/configure-shaped.sh"
ARGS="dash=/usr/bin/dash base=$B/bin/base-release trunk=$B/bin/trunk-release head=$B/bin/head-release base-native=$B/bin/base-native trunk-native=$B/bin/trunk-native head-native=$B/bin/head-native"
uptime > "$B/load-pinned.txt"
python3 "$B/tool/run" --dir "$B/scratch" --runs 9 --pin 0-3 $ARGS > "$B/speed-pinned.txt" 2>&1
echo "pinned=$?" >> "$B/status"; uptime >> "$B/load-pinned.txt"
uptime > "$B/load-unpinned.txt"
python3 "$B/tool/run" --dir "$B/scratch" --runs 9 $ARGS > "$B/speed-unpinned.txt" 2>&1
echo "unpinned=$?" >> "$B/status"; uptime >> "$B/load-unpinned.txt"
: > "$B/instructions.txt"
mkdir -p "$B/iscratch"; cd "$B/iscratch" || exit 9
for bin in base-release trunk-release head-release base-native trunk-native head-native; do
  for sc in fork pipeline param configure-shaped; do
    for k in 1 2 3; do
      n=$(env -i PATH=/usr/bin:/bin HOME=/home/pelt LC_ALL=C perf stat -x, -e instructions:u "$B/bin/$bin" "$B/tool/$sc.sh" 2>&1 >/dev/null | grep instructions | cut -d, -f1)
      echo "$bin $sc $k $n" >> "$B/instructions.txt"
    done
  done
done
echo "instructions=done" >> "$B/status"
echo done >> "$B/status"
