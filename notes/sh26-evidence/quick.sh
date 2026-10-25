#!/bin/bash
# sh26: build the head tree both tiers and run the areas and sessions
# this lane touches (a quick look before the gauntlet)
set -u
S=/home/mfwolffe/lanes/sh26
cd $S/head || exit 9
ulimit -c 0
tools/check-fmt 2>&1 | tail -3
tools/build --all 2>&1 | tail -3 || exit 2
for t in native release; do
  echo "== $t"
  tools/difftest --bin target/$t simple builtin option printf cd signal quote jobsctl jobs exec redir 2>&1 | grep -vE '^ok ' | tail -40
  tools/session --bin target/$t c_ignoreeof c_mail mail_path mail_interval jc_assign_text 2>&1 | tail -8
done
tools/clause-census 2>&1 | tail -3
