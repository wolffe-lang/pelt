#!/bin/bash
# the sh22 shape-rss rows on trunk (red) and the head (green), both tiers
S=/home/mfwolffe/lanes/sh22
R=builtin-read-redir,builtin-eval,builtin-cd,builtin-command,builtin-umask,background-nowait,background-program-nowait
cd $S/snaps/rows
for b in $S/base/target/native/pelt $S/base/target/release/pelt $S/snaps/rows/target/native/pelt $S/snaps/rows/target/release/pelt; do
  echo == $b
  tools/shape-rss --only $R $b; echo "exit $?"
done
