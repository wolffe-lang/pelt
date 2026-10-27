#!/bin/bash
set -eu
S=/home/mfwolffe/lanes/sh33
exec flock /home/mfwolffe/lanes/kasumi-cores-8-11.lock \
  taskset -c 8-11 podman run --rm --network none --userns=keep-id \
  -u "$(id -u):$(id -g)" --init --pids-limit 4096 \
  -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v "$S:$S" -w "$S/pelt" -e "HOME=$S/tmp" -e "TMPDIR=$S/tmp" \
  docker.io/library/archlinux@sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785 \
  bash -c 'ulimit -c 0; exec "$@"' ctr "$@"
