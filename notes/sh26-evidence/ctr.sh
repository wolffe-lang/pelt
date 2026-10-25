#!/bin/bash
# sh26: run a command in this lane's own throwaway container (its own
# pid namespace: whatever a case or a harness kills or times out is the
# container's, never kasumi's host process table, RULES §5). /usr is
# kasumi's own, read only, so dash 0.5.13.4, bash 5.3.20, strace and
# python3 are run as binaries, never read; the lane directory is
# mounted at the same path; no network; cores off; every process on
# CPUs 0-3 (taskset INSIDE: crun resets the affinity a container is
# started with, measured 2026-10-24). usage: ctr.sh CMD...
S=$HOME/lanes/sh26
exec podman run --rm --network none --userns=keep-id -u $(id -u):$(id -g) \
  --init --ulimit core=0:0 --pids-limit ${CTRPIDS:-4096} --cpuset-cpus ${CTRCPUS:-0-3} \
  -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro \
  -v $S:$S -w "${CTRDIR:-$S/pelt}" -e TMPDIR=$S/tmp -e HOME=$S/tmp \
  -e PELT_REAP_LOG -e KEEP_TRACES -e PELT_DIFF_DIR -e CTRCPUS -e TREE \
  docker.io/library/archlinux:base-devel bash -c 'ulimit -c 0; exec taskset -c ${CTRCPUS:-0-3} "$@"' ctr "$@"
