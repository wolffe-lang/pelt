#!/usr/bin/env bash
# Recorded steps run only from a committed checkout, in a bounded container.
set -eu
image=$1; shift
root=$(git rev-parse --show-toplevel)
work=$(dirname "$root")
: "${PELT_ENGINE:?set the approved container engine}"
exec "$PELT_ENGINE" run --rm --init --memory 12g --pids-limit 16384 \
  --ulimit nproc=32768:32768 -v "$work:$work" -w "$root" \
  --tmpfs "$work/noexec:rw,noexec,size=1m" \
  -e HOME="$work/home" -e TMPDIR="$work/temp" -e CARGO_BUILD_JOBS=2 \
  -e WOLF_BIN="$root/.wolf-bin/wolf" -e LUPIN_BIN="$root/.wolf-bin/lupin" \
  -e WOLF_STD="$root/.wolf-bin/std" -e PELT_NOEXEC_DIR="$work/noexec" \
  "$image" /usr/bin/taskset.real -c "${PELT_CPUS:-0-3,8-11}" "$@"
