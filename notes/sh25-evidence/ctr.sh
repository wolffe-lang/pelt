#!/bin/bash
# sh25: run a command in this lane's own throwaway container (its own
# pid namespace: whatever a case or a harness kills or times out is the
# container's, never kasumi's host process table, RULES §5). /usr is
# kasumi's own, read only, so dash 0.5.13.4, bash 5.3.20, strace 7.2,
# gdb and python3 are run as binaries, never read; the lane directory is
# mounted at the same path; no network. usage: ctr.sh CMD...
S=$HOME/lanes/sh25
exec podman run --rm --network none --userns=keep-id -u $(id -u):$(id -g) \
  --init --pids-limit ${CTRPIDS:-4096} \
  -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v $S:$S -w "${CTRDIR:-$S/pelt}" -e TMPDIR=$S/tmp -e HOME=$S/tmp \
  -e PELT_REAP_LOG -e KEEP_TRACES -e PELT_DIFF_DIR \
  docker.io/library/archlinux:base-devel "$@"
