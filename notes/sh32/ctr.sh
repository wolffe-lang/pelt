#!/usr/bin/env bash
set -eu
S=$HOME/lanes/sh32
export PATH="$HOME/lanes/hasu-env/bin:$HOME/lanes/hasu-env/profile/bin:$PATH"
exec flock "$HOME/lanes/hasu-A.lock" podman run --rm --network none \
 --userns=keep-id -u "$(id -u):$(id -g)" --memory 12g --pids-limit 4096 \
 -v "$S:$S" -w "$S/pelt" -e "TMPDIR=$S/tmp" -e "HOME=$S/tmp" \
 localhost/sh32-oracle taskset -c 0-5 bash -c 'ulimit -c 0; exec "$@"' ctr "$@"
