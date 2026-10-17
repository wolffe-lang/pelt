#!/bin/bash
# sh17 census: usage census.sh TAG PELTBIN [extra script-census args…]
T=$1; P=$2; shift 2
S=$HOME/lanes/sh17
TREE=${TREE:-$S/pelt}
cd "$TREE" || exit 9
export TMPDIR=$S/tmp
L=$S/logs
SC=$S/sc
sha256sum "$P" > "$L/sc-$T.bin"
tools/script-census --dir "$SC" --pelt "$P" \
  --podman "podman --root $SC/store --runroot $SC/run-podman" \
  --tsv "$SC/$T.tsv" "$@" > "$L/sc-$T.log" 2>&1
echo "census=$? $(tail -n 1 $L/sc-$T.log)" > "$L/sc-$T.status"
