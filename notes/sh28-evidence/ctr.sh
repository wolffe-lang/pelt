#!/bin/bash
set -eu
S=$HOME/lanes/sh28
exec flock "$HOME/lanes/kasumi-cores-12-15.lock" taskset -c 12-15 \
  podman run --rm --network none --userns=keep-id -u "$(id -u):$(id -g)" \
  --init --pids-limit 4096 -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v "$S:$S" -w "$S/pelt" -e "TMPDIR=$S/tmp" -e "HOME=$S/tmp" \
  docker.io/library/archlinux:base-devel bash -c 'ulimit -c 0; exec "$@"' ctr "$@"
