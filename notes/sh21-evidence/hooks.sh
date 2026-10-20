#!/bin/bash
# sh21: lope's own tools/hook-sessions (lope 5ac37df, its tree at
# ~/lanes/sh21/lope, lope built there at its pin) on PTYs it starts, each
# shell with a scratch HOME and XDG_*: pelt TAG's two tiers against
# hooks/expected-sh21.tsv (the oracle: 0 rows) and against lope's own
# tests/hooks/expected.tsv (pelt cc2fdc9's rows: the four jump rows
# differ). usage: hooks.sh TAG [--refs]   (--refs: bash, zsh, fish and
# fortsh too, the reference rows on this host)
set -u
T=$1
S=$HOME/lanes/sh21
L=$S/hooks/$T
mkdir -p "$L"
export TMPDIR=$S/tmp
cd "$S/lope" || exit 9
echo "lope $(git rev-parse HEAD) $(sha256sum target/release/lope | cut -c1-16)" > "$L/status"
for t in release native; do
  p=$S/pelt/target/$t/pelt
  echo "pelt $t $(sha256sum "$p" | cut -c1-16)" >> "$L/status"
  python3 tools/hook-sessions --tool lope=target/release/lope --shells pelt --pelt "$p" \
    --report "$L/pelt-$t.tsv" --expect "$S/pelt/notes/sh21-evidence/hooks/expected-sh21.tsv" \
    --logs "$L/logs-$t" > "$L/pelt-$t-sh21.log" 2>&1
  echo "expect-sh21-$t=$?" >> "$L/status"
  python3 tools/hook-sessions --tool lope=target/release/lope --shells pelt --pelt "$p" \
    --expect tests/hooks/expected.tsv --logs "$L/logs-$t-lope" > "$L/pelt-$t-lope.log" 2>&1
  echo "expect-lope-$t=$?" >> "$L/status"
done
if [ "${2:-}" = --refs ]; then
  python3 tools/hook-sessions --tool lope=target/release/lope --shells bash,zsh,fish,fortsh \
    --report "$L/refs.tsv" --expect tests/hooks/expected.tsv --logs "$L/logs-refs" > "$L/refs.log" 2>&1
  echo "refs=$?" >> "$L/status"
  bash --version | head -1 >> "$L/status"; zsh --version >> "$L/status"; fish --version >> "$L/status"
fi
echo done >> "$L/status"
