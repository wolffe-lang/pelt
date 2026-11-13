#!/usr/bin/env bash
# Recorded steps run only from a committed checkout, in a bounded container.
set -eu
image=$1; shift
root=$(git rev-parse --show-toplevel)
work=$(dirname "$root")
: "${PELT_ENGINE:?set the approved container engine}"
exec "$PELT_ENGINE" run --rm --init --userns keep-id --user "$(id -u):$(id -g)" --memory 12g --pids-limit 16384 \
  --ulimit nproc=32768:32768 -v "$work:$work" -v "$work/container-temp:/tmp" -w "$root" \
  --tmpfs "$work/noexec:rw,noexec,mode=1777,size=1m" \
  -e HOME="$work/home" -e TMPDIR="$work/temp" -e CARGO_BUILD_JOBS=2 \
  -e WOLF_BIN="$root/.wolf-bin/wolf" -e LUPIN_BIN="$root/.wolf-bin/lupin" \
  -e WOLF_STD="$root/.wolf-bin/std" -e PELT_NOEXEC_DIR="$work/noexec" \
  "$image" sh -c 'cpus=$1; shift
    if [ -x /usr/bin/taskset.real ]; then exec /usr/bin/taskset.real -c "$cpus" "$@"; fi
    exec taskset -c "$cpus" "$@"' sh "${PELT_CPUS:-0-3,8-11}" "$@"
