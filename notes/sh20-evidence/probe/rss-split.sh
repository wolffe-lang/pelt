#!/bin/bash
# sh20: what a pelt's peak is made of after a 10,000-turn `:` loop: its
# own /proc status (VmHWM, RssAnon, RssFile), read from inside the
# shell, twice per binary (inside ctr.sh). usage: rss-split.sh BIN...
T=${TMPDIR:-/tmp}/sh20-split.$$.sh
cat > "$T" <<'S'
i=0
while [ $i -lt 10000 ]; do :; i=$((i+1)); done
grep -E 'VmHWM|RssAnon|RssFile' /proc/$$/status | tr -s ' \t' ' ' | tr '\n' ' '; echo
S
for b in "$@"; do
  echo "$b ($(sha256sum "$b" | cut -c1-12))"
  for i in 1 2; do "$b" "$T"; done
done
rm -f "$T"
