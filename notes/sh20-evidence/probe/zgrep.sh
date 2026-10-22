#!/bin/bash
# sh20: kasumi's own xzgrep, zgrep and zdiff (run, never read) under SH
SH=$1; D=$(mktemp -d); cd $D
printf "alpha\nbeta\ngamma\nbeta two\n" > a; printf "alpha\nBETA\ngamma\n" > b
gzip -k a; gzip -k b; xz -k a
for c in "/usr/bin/zgrep beta a.gz" "/usr/bin/zgrep -c beta a.gz b.gz" "/usr/bin/xzgrep -n beta a.xz" "/usr/bin/zgrep -i beta a.gz b.gz" "/usr/bin/zdiff a.gz b.gz" "/usr/bin/xzgrep -l gamma a.xz a.gz"; do
  out=$($SH $c 2>&1); echo "$c -> st=$? $(printf %s "$out" | tr "\n" "|")"
done
cd /; rm -rf $D
