#!/usr/bin/env bash
# Only private temporary test locks; never acquire/modify real hasu locks here.
set -eu
scratch=$1
guard=$(cd "$(dirname "$0")" && pwd)/hasu-paired-lock.sh
tmp=$(mktemp -d "$scratch/lock-pair.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
touch "$tmp/outer" "$tmp/inner"
for held in inner outer; do
    set +e
    flock -w 21600 "$tmp/$held" bash "$guard" --verify "$tmp/outer" "$tmp/inner" -- touch "$tmp/work"
    code=$?
    set -e
    [ "$code" = 1 ]
    [ ! -e "$tmp/work" ]
    echo "LOCK_TEST only-$held-held exit=$code work=no"
done
flock -w 21600 "$tmp/outer" flock -w 21600 "$tmp/inner" \
    bash "$guard" --verify "$tmp/outer" "$tmp/inner" -- touch "$tmp/work"
[ -f "$tmp/work" ]
echo 'LOCK_TEST both-held exit=0 work=yes'
echo 'END paired-lock-selftest exit=0'
