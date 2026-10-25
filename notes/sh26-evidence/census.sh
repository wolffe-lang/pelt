#!/bin/bash
# sh26 census: usage census.sh TAG PELTBIN [extra script-census args…]
# (the tool from the tree at $TREE, default the lane clone; every
# container on CPUs 0-3 through podman-03)
T=$1; P=$2; shift 2
S=$HOME/lanes/sh26
TREE=${TREE:-$S/pelt}
cd "$TREE" || exit 9
export TMPDIR=$S/tmp
L=$S/logs
SC=$S/sc
mkdir -p $SC
sha256sum "$P" > "$L/sc-$T.bin"
echo "tree $(git -C $TREE rev-parse HEAD) $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L/sc-$T.start"
tools/script-census --dir "$SC" --pelt "$P" --podman "$S/podman-03" \
  --tsv "$SC/$T.tsv" "$@" > "$L/sc-$T.log" 2>&1
echo "census=$? $(tail -n 1 $L/sc-$T.log) $(date -Is)" > "$L/sc-$T.status"
