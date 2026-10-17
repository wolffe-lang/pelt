#!/bin/bash
# sh17: run a command in a throwaway, network-less container whose /usr is
# kasumi own (read only), so dash 0.5.13.4 and bash 5.3.20 are the oracles
# of record, run as binaries; the lane tree mounted at the same path.
S=$HOME/lanes/sh17
exec podman run --rm --network none --userns=keep-id -u $(id -u):$(id -g)   -v /usr:/usr:ro -v /var/lib/pacman:/var/lib/pacman:ro   -v $S:$S -w "${REFDIR:-$S}" -e TMPDIR=$S/tmp -e HOME=$S/tmp   docker.io/library/archlinux:base-devel "$@"
