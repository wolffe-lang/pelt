#!/bin/bash
set -eu
S=$HOME/lanes/sh29
exec flock "$HOME/lanes/kasumi-cores-4-7.lock" taskset -c 4-7 \
  podman run --rm --network none --userns=keep-id -u "$(id -u):$(id -g)" \
  --init --pids-limit 4096 -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v "$S:$S" -w "$S/pelt" -e "TMPDIR=$S/tmp" -e "HOME=$S/tmp" \
  3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f \
  bash -c 'ulimit -c 0; exec "$@"' ctr "$@"
