#!/bin/bash
# sh22: a frozen copy of the dev tree (its sources, harness and built
# binaries), so a run in the container reads one build however the dev
# tree moves on. usage: snap.sh TAG  -> prints the snapshot's path
S=$HOME/lanes/sh22
mkdir -p "$S/snaps"
rm -rf "$S/snaps/$1"
rsync -a --exclude .git --exclude .wolf-bin "$S/pelt/" "$S/snaps/$1/"
echo "$S/snaps/$1"
