#!/bin/bash
# sh08 census: usage census.sh TAG PELTBIN [extra script-census args…]
T=$1; P=$2; shift 2
cd "$HOME/lanes/sh08/pelt" || exit 9
export TMPDIR=$HOME/lanes/sh08/tmp
L=$HOME/lanes/sh08/logs
SC=$HOME/lanes/sh08/sc
mkdir -p "$SC"
sha256sum "$P" > "$L/sc-$T.bin"
tools/script-census --dir "$SC" --pelt "$P" \
  --podman "podman --root $SC/store --runroot $SC/run-podman" \
  --tsv "$SC/$T.tsv" "$@" > "$L/sc-$T.log" 2>&1
echo "census=$? $(tail -1 $L/sc-$T.log)" > "$L/sc-$T.status"
