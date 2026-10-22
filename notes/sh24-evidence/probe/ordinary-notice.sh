#!/bin/bash
S=$(cd "$(dirname "$0")/.." && pwd)
D=$TMPDIR/sh24-ordinary.$$
mkdir -p "$D"
trap 'rm -rf "$D"' EXIT
cd "$D" || exit 9
ulimit -c 0
for shell in /usr/bin/dash "$S/base/target/native/pelt" "$S/head/target/native/pelt" "$S/base/target/release/pelt" "$S/head/target/release/pelt"; do
  "$shell" -c 'command sh -c '\''kill -TERM $$'\'' 2>f; st=$?; if [ -s f ]; then echo "ordinary in f: $st"; else echo "ordinary outside: $st"; fi' >out 2>err
  echo "shell=$shell exit=$? stdout=$(cat out) stderr_bytes=$(wc -c <err)"
done
