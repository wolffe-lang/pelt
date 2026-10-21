#!/bin/bash
# sh23: run a command in this lane's own throwaway container (sh22's):
# its own pid namespace, so whatever a case or a harness kills or times
# out is the container's, never kasumi's host process table (RULES §5).
# /usr is kasumi's own, read only, so dash 0.5.13.4, bash 5.3.20 and
# zsh 5.9 run as binaries, never read; the lane directory is mounted at
# the same path; no network; no core files (ulimit -c 0).
# usage: ctr.sh CMD...
S=$HOME/lanes/sh23
exec podman run --rm --network none --userns=keep-id -u $(id -u):$(id -g) \
  --init --pids-limit ${CTRPIDS:-4096} --ulimit core=0 \
  -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v $S:$S -w "${CTRDIR:-$S/pelt}" -e TMPDIR=$S/tmp -e HOME=$S/tmp \
  docker.io/library/archlinux:base-devel bash -c 'ulimit -c 0; exec "$@"' ctr "$@"
