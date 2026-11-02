#!/usr/bin/env bash
# Future hasu dispatch: paired long locks, with a live-path check before work.
set -eu
if [ "${1:-}" = --verify ]; then
    outer=$2
    inner=$3
    shift 3
    [ "${1:-}" != -- ] || shift
    [ "$#" -gt 0 ] || { echo 'lock check needs a command' >&2; exit 2; }
    for lock in "$outer" "$inner"; do
        stat -c 'LOCK_INODE %D:%i %n' "$lock"
        set +e
        flock -n -E 75 "$lock" true
        code=$?
        set -e
        if [ "$code" != 75 ]; then
            echo "LOCK_VERIFY_FAIL path=$lock probe_exit=$code" >&2
            exit 1
        fi
        echo "LOCK_HELD $lock"
    done
    exec "$@"
fi
block=${1:-}
case "$block" in A|B) ;; *) echo 'usage: hasu-paired-lock.sh A|B command...' >&2; exit 2 ;; esac
shift
outer="/home/mfwolffe/lanes/hasu-block-$block.lock"
inner="/home/mfwolffe/lanes/hasu-$block.lock"
exec flock -w 21600 "$outer" flock -w 21600 "$inner" \
    bash "$0" --verify "$outer" "$inner" -- "$@"
