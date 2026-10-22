#!/bin/bash
S=$(cd "$(dirname "$0")/.." && pwd)
D=$TMPDIR/sh24-leftovers.$$
mkdir -p "$D"
trap 'rm -rf "$D"' EXIT
ulimit -c 0
text=$'set -v\necho a\n'
printf '%s' "$text" > "$D/s.sh"
for shell in /usr/bin/dash "$S/head/target/native/pelt" "$S/head/target/release/pelt"; do
  "$shell" "$D/s.sh" > "$D/out" 2> "$D/err"
  echo "verbose script shell=$shell exit=$? stdout=$(cat "$D/out") stderr_bytes=$(wc -c < "$D/err")"
  "$shell" -c "$text" > "$D/out" 2> "$D/err"
  echo "verbose command shell=$shell exit=$? stdout=$(cat "$D/out") stderr_bytes=$(wc -c < "$D/err")"
done
cd "$S/head" || exit 9
for tier in native release; do
  tools/difftest --bin target/$tier quote/c_s_high_bytes
done
